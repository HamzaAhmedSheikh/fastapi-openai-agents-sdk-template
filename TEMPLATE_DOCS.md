# AI-Powered Todo App Template 📝

A complete student-friendly template for building AI-native applications with FastAPI and Google Gemini.

---

## 📚 What You'll Learn

- **FastAPI** - Build modern REST APIs with automatic docs
- **AI Agents** - Integrate Google Gemini using OpenAI Agents SDK
- **Async Python** - Handle concurrent requests efficiently
- **Tool Functions** - Give AI agents real-world capabilities
- **Clean Architecture** - Write maintainable, production-ready code

---

## 🚀 Quick Start (5 minutes)

### Prerequisites

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Get your Gemini API key
# Visit: https://makersuite.google.com/app/apikey
```

### Setup

```bash
# Clone or download this template
cd fastapi-openai-agents-sdk-template

# Install all dependencies
uv sync

# Create .env file with your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the server
uv run uvicorn main:app --port 8000
```

### Test It

```bash
# Open in browser: http://localhost:8000/docs

# Or use curl:
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a todo: Learn AI agents"}'
```

---

## 📁 Project Structure

```
fastapi-openai-agents-sdk-template/
├── main.py              # 🎯 FastAPI app + AI agent setup
├── .env                 # 🔐 Your API keys (never commit!)
├── pyproject.toml       # 📦 Dependencies (managed by uv)
├── README.md            # 📖 Original project readme
└── TEMPLATE_DOCS.md     # 📚 This file - your learning guide
```

---

## 🧩 Understanding main.py (Step by Step)

### Part 1: Imports & Setup

```python
# Standard Python libraries
import os                          # Access environment variables
from datetime import datetime      # Timestamp todos

# AI Agent SDK
from agents import (
    Agent,                         # Create AI agents
    AsyncOpenAI,                   # Connect to Gemini
    Runner,                        # Execute agent tasks
    function_tool,                 # Decorator for AI-callable functions
    set_default_openai_client,     # Configure Gemini as default
    set_tracing_disabled,          # Turn off debug tracing
)

# FastAPI - Web framework
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel    # Data validation
```

**💡 Key Concept**: We use `agents` library to connect FastAPI with Google Gemini AI.

---

### Part 2: Gemini Configuration

```python
# Load API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY", "")

# Configure OpenAI Agents SDK to use Gemini
set_tracing_disabled(True)  # Faster execution
set_default_openai_api("chat_completions")

# Create Gemini client with custom endpoint
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini endpoint
)
set_default_openai_client(external_client)  # Use Gemini everywhere
```

**💡 Key Concept**: OpenAI Agents SDK works with multiple AI providers (OpenAI, Gemini, etc). We configure it to use Gemini's API.

---

### Part 3: In-Memory Storage (Simple Database)

```python
# Dictionary stores all todos (id -> Todo object)
todos_db = {}
todo_counter = 0  # Auto-increment ID

class Todo:
    """Simple data structure for a todo item."""
    def __init__(self, id, title, description=""):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.completed = False
```

**💡 Key Concept**: In-memory storage is perfect for learning. In production, use a real database (PostgreSQL, MongoDB, etc).

---

### Part 4: Tool Functions (AI Agent's Hands)

```python
@function_tool
def create_todo(title: str, description: str = "") -> str:
    """
    Create a new todo item.

    The AI agent calls this function when users say:
    - "Add a todo: buy milk"
    - "Create task: finish homework"
    - "Remember to call mom"
    """
    global todo_counter
    todo_counter += 1
    todo = Todo(todo_counter, title, description)
    todos_db[todo_counter] = todo
    return f"✅ Created todo #{todo.id}: {todo.title}"
```

**💡 Key Concept**: `@function_tool` decorator makes functions callable by AI. The AI reads the docstring to understand when to use each tool.

---

### Part 5: The AI Agent

```python
assistant_agent = Agent(
    name="TodoAssistant",

    # Instructions define agent's personality and capabilities
    instructions="""You are a helpful todo list assistant powered by Google Gemini.

    You can:
    - Create new todos with titles and descriptions
    - View all todos or filter by completion status
    - Get details of a specific todo
    - Delete todos
    - Mark todos as complete or incomplete

    Be friendly, concise, and helpful.""",

    model="gemini-2.5-flash",  # Fast, cost-effective model

    # Give agent access to these functions
    tools=[
        create_todo,
        get_todos,
        get_todo,
        delete_todo,
        mark_complete,
        mark_incomplete,
    ],
)
```

**💡 Key Concept**: The agent is like hiring an employee. You:
1. Give them a job description (instructions)
2. Provide tools to do the job (functions)
3. Let them decide when to use each tool

---

### Part 6: FastAPI Endpoints

```python
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Main endpoint: Send message, get AI response.

    The AI agent:
    1. Reads the user's message
    2. Decides which tools to call
    3. Calls the functions
    4. Returns a natural language response
    """
    result = await Runner.run(assistant_agent, input=request.message)
    return ChatResponse(response=result.final_output)
```

**💡 Key Concept**: `Runner.run()` is the magic function that:
- Takes your agent and user message
- Lets the agent think and use tools
- Returns the final response

---

## 🎓 How AI Agents Work

### The Agent Reasoning Loop

```
User: "Create a todo: Buy groceries and mark todo #1 as done"
   ↓
1. AI reads message
   ↓
2. AI decides: "I need to create a todo AND mark another complete"
   ↓
3. AI calls: create_todo("Buy groceries")
   Result: "✅ Created todo #5: Buy groceries"
   ↓
4. AI calls: mark_complete(1)
   Result: "✓ Marked todo #1 as completed"
   ↓
5. AI generates response:
   "I've created a new todo for buying groceries and marked todo #1 as complete!"
```

**💡 Key Concept**: The AI agent can call multiple tools in sequence and combine results into a natural response.

---

## 🔧 Customization Guide

### 1. Change the Agent's Personality

```python
# Make it more casual
instructions="Hey! I'm your chill todo buddy. Let's organize your life! 🎉"

# Make it professional
instructions="I am a productivity assistant specializing in task management."

# Make it funny
instructions="I'm a todo list that refuses to let you procrastinate! 😤"
```

### 2. Add New Tools

```python
@function_tool
def prioritize_todo(todo_id: int, priority: str) -> str:
    """Set todo priority: low, medium, high."""
    todo = todos_db.get(todo_id)
    if not todo:
        return f"❌ Todo #{todo_id} not found."
    todo.priority = priority  # Add priority field to Todo class
    return f"🎯 Set priority of todo #{todo_id} to {priority}"

# Add to agent's tools list
tools=[..., prioritize_todo]
```

### 3. Change the AI Model

```python
# Faster, cheaper
model="gemini-2.0-flash-exp"

# More capable (if available)
model="gemini-2.0-pro"

# Use OpenAI instead
model="gpt-4o"  # Change base_url to OpenAI endpoint
```

### 4. Add Persistence (Real Database)

```python
# Install: uv add sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace todos_db with SQLAlchemy models
# See: https://docs.sqlalchemy.org/en/20/tutorial/
```

---

## 🐛 Common Issues & Solutions

### Issue: "API key not found"

```bash
# Solution: Check .env file exists and has correct key
cat .env
# Should show: GEMINI_API_KEY=AIza...

# If missing:
echo "GEMINI_API_KEY=your_actual_key" > .env
```

### Issue: "Runner.run() got unexpected keyword argument"

```python
# ❌ Wrong:
result = await Runner.run(agent=assistant_agent, input=msg)

# ✅ Correct:
result = await Runner.run(assistant_agent, input=msg)
```

### Issue: "Port 8000 already in use"

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8080
```

---

## 📊 API Endpoints Reference

### POST /chat

**Request:**
```json
{
  "message": "Create a todo: Learn FastAPI"
}
```

**Response:**
```json
{
  "response": "✅ Created todo #1: Learn FastAPI"
}
```

### GET /health

**Response:**
```json
{
  "status": "ok",
  "model": "gemini-2.5-flash",
  "total_todos": 5
}
```

### GET /docs

Opens interactive API documentation (Swagger UI).

---

## 🎯 Learning Challenges

### Beginner

1. ✅ **Add a new tool**: Create `get_stats()` that returns total/completed/incomplete counts
2. ✅ **Modify personality**: Make the agent respond in pirate speak
3. ✅ **Add logging**: Print every tool call to console

### Intermediate

4. ✅ **Add categories**: Let todos have categories (work, personal, shopping)
5. ✅ **Add due dates**: Store and check if todos are overdue
6. ✅ **Implement search**: Tool to search todos by keyword

### Advanced

7. ✅ **Add user authentication**: Multiple users with separate todo lists
8. ✅ **Add database**: Replace in-memory storage with SQLite
9. ✅ **Add webhooks**: Notify external services when todos change
10. ✅ **Multi-agent**: Create separate agents for different tasks

---

## 🔗 Resources

### Official Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/
- **Gemini API**: https://ai.google.dev/gemini-api/docs
- **uv Package Manager**: https://docs.astral.sh/uv/

### Tutorials

- **FastAPI Crash Course**: https://fastapi.tiangolo.com/tutorial/
- **Async Python**: https://realpython.com/async-io-python/
- **AI Agent Patterns**: https://www.anthropic.com/research/building-effective-agents

### Community

- **FastAPI Discord**: https://discord.gg/fastapi
- **r/FastAPI**: https://reddit.com/r/FastAPI
- **AI Agents Forum**: https://community.openai.com/

---

## 💡 Pro Tips

1. **Read Error Messages**: They tell you exactly what's wrong
2. **Use /docs endpoint**: Interactive API testing without curl
3. **Check agent logs**: See which tools the AI decides to call
4. **Start simple**: Get one feature working before adding more
5. **Ask the AI**: The agent can explain its own code!

---

## 🎓 Next Steps

### After Mastering This Template

1. **Deploy to production**
   - Add database (PostgreSQL)
   - Add authentication (JWT tokens)
   - Deploy to cloud (Railway, Fly.io, Render)

2. **Build your own AI app**
   - Customer support bot
   - Recipe recommendation agent
   - Code review assistant
   - Data analysis chatbot

3. **Explore advanced features**
   - Multi-agent systems (agents talking to agents)
   - Streaming responses (real-time updates)
   - Function calling chains (complex workflows)
   - Custom context injection (RAG patterns)

---

## 📝 Code Comments Philosophy

This template uses **short, powerful comments** that explain **why**, not **what**:

```python
# ❌ Bad comment (obvious):
# Loop through todos
for todo in todos:

# ✅ Good comment (explains purpose):
# Filter completed items for daily report
for todo in [t for t in todos if t.completed]:

# ❌ Bad comment (redundant):
# Set completed to True
todo.completed = True

# ✅ Good comment (explains reasoning):
# Mark complete without AI validation (instant action)
todo.completed = True
```

---

## 🤝 Contributing

This template is open-source and educational. Feel free to:

- ⭐ Star the repo if it helped you learn
- 🐛 Report bugs or unclear documentation
- 💡 Suggest improvements or new features
- 🎓 Share your projects built with this template

---

## 📜 License

MIT License - Use this template for learning, personal projects, or commercial applications.

---

## 🎉 You're Ready!

You now have:
- ✅ A working AI-powered app
- ✅ Understanding of FastAPI + AI agents
- ✅ Tools to build your own projects

**Start experimenting, break things, and learn by doing!** 🚀

---

*Last Updated: January 2026*
*Template Version: 1.0.0*
