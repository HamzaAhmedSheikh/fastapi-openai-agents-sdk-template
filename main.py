"""
AI-Powered Todo App with FastAPI + Google Gemini
=================================================
A complete example of building AI-native applications.

Learn: FastAPI, AI Agents, Async Python, Tool Functions
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import (
    Agent,
    AsyncOpenAI,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

# ============================================================================
# CONFIGURATION - Setup Gemini AI
# ============================================================================

load_dotenv()  # Load .env file with API keys

# Configure SDK to use Gemini instead of OpenAI
set_tracing_disabled(True)  # Faster execution (no debug logs)
set_default_openai_api("chat_completions")  # Use chat API

# Connect to Gemini endpoint
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(gemini_client)

# ============================================================================
# DATA LAYER - Simple in-memory storage (no database required)
# ============================================================================

todos_db: dict[int, "Todo"] = {}  # Store all todos (id -> Todo object)
todo_counter: int = 0  # Auto-increment ID for new todos


class Todo:
    """Simple data structure for a todo item."""

    def __init__(self, id: int, title: str, description: str = ""):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.completed = False


# ============================================================================
# AI TOOLS - Functions the agent can call to interact with todos
# ============================================================================


@function_tool
def create_todo(title: str, description: str = "") -> str:
    """
    Create a new todo item.

    AI calls this when user says:
    - "Add a todo: buy milk"
    - "Create task: finish homework"
    - "Remember to call mom"
    """
    global todo_counter
    todo_counter += 1
    todo = Todo(todo_counter, title, description)
    todos_db[todo_counter] = todo
    return f"✅ Created todo #{todo.id}: {todo.title}"


@function_tool
def get_todos(completed: Optional[bool] = None) -> str:
    """
    Get all todos, optionally filtered by completion status.

    Args:
        completed: None = all, True = completed only, False = incomplete only
    """
    if not todos_db:
        return "📝 No todos found. Create your first todo!"

    # Filter by completion status
    filtered = [
        todo
        for todo in todos_db.values()
        if completed is None or todo.completed == completed
    ]

    if not filtered:
        status = "completed" if completed else "incomplete"
        return f"📝 No {status} todos found."

    # Format each todo with status symbol
    result = []
    for todo in filtered:
        status_icon = "✓" if todo.completed else "○"
        desc = f" - {todo.description}" if todo.description else ""
        result.append(f"{status_icon} #{todo.id}: {todo.title}{desc}")

    return "\n".join(result)


@function_tool
def get_todo(todo_id: int) -> str:
    """Get detailed information about a specific todo."""
    todo = todos_db.get(todo_id)
    if not todo:
        return f"❌ Todo #{todo_id} not found."

    status = "Completed ✓" if todo.completed else "Incomplete ○"
    return (
        f"📋 Todo #{todo.id}\n"
        f"Title: {todo.title}\n"
        f"Description: {todo.description or 'No description'}\n"
        f"Status: {status}\n"
        f"Created: {todo.created_at}"
    )


@function_tool
def delete_todo(todo_id: int) -> str:
    """Delete a todo permanently."""
    todo = todos_db.pop(todo_id, None)
    if not todo:
        return f"❌ Todo #{todo_id} not found."
    return f"🗑️ Deleted todo #{todo_id}: {todo.title}"


@function_tool
def mark_complete(todo_id: int) -> str:
    """Mark a todo as completed."""
    todo = todos_db.get(todo_id)
    if not todo:
        return f"❌ Todo #{todo_id} not found."
    todo.completed = True
    return f"✓ Marked todo #{todo_id} as completed: {todo.title}"


@function_tool
def mark_incomplete(todo_id: int) -> str:
    """Mark a todo as incomplete."""
    todo = todos_db.get(todo_id)
    if not todo:
        return f"❌ Todo #{todo_id} not found."
    todo.completed = False
    return f"○ Marked todo #{todo_id} as incomplete: {todo.title}"


# ============================================================================
# AI AGENT - The brain that decides which tools to use
# ============================================================================

assistant_agent = Agent(
    name="TodoAssistant",
    instructions="""You are a helpful todo list assistant powered by Google Gemini.

    Your capabilities:
    - Create new todos with titles and optional descriptions
    - View all todos or filter by completion status
    - Get details of specific todos
    - Delete todos
    - Mark todos as complete or incomplete

    Personality: Be friendly, concise, and helpful. Present information clearly.""",
    model="gemini-2.5-flash",  # Fast, cost-effective model
    tools=[
        create_todo,
        get_todos,
        get_todo,
        delete_todo,
        mark_complete,
        mark_incomplete,
    ],
)

# ============================================================================
# API LAYER - FastAPI endpoints
# ============================================================================


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str  # User's message to the AI
    stream: bool = False  # Future: streaming responses


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    response: str  # AI's response text


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager - runs on startup/shutdown."""
    print("🚀 Starting Todo App with AI agent...")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="AI-Powered Todo App",
    description="Todo list with Google Gemini AI assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow requests from any origin (remove in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API information and usage examples."""
    return {
        "name": "AI-Powered Todo App",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "POST /chat": "Send message to AI assistant",
            "GET /health": "Health check",
        },
        "examples": [
            "Create a todo: buy groceries",
            "Show all my todos",
            "Mark todo #1 as complete",
            "Delete todo #2",
        ],
    }


@app.get("/health")
async def health():
    """Health check - returns system status."""
    return {
        "status": "ok",
        "model": "gemini-2.5-flash",
        "total_todos": len(todos_db),
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Main endpoint: Send message to AI, get response.

    The AI agent will:
    1. Read the user's message
    2. Decide which tools to call
    3. Execute the tools
    4. Return a natural language response
    """
    try:
        # Run agent with user message (agent as first positional arg)
        result = await Runner.run(assistant_agent, input=request.message)
        return ChatResponse(response=result.final_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MAIN - Run the server
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AI-Powered Todo App")
    print("=" * 60)
    print(f"📍 Server: http://localhost:8000")
    print(f"📖 Docs:   http://localhost:8000/docs")
    print(f"💚 Health: http://localhost:8000/health")
    print("=" * 60)
    print("\n💡 Example queries:")
    print("  - Create a todo: finish project documentation")
    print("  - Show my todos")
    print("  - Mark todo #1 as done")
    print("  - Delete todo #2")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
