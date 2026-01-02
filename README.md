# 🤖 AI-Powered Todo App Template

A production-ready template for building AI-native applications with **FastAPI** and **Google Gemini** using the **OpenAI Agents SDK**.

Perfect for students learning modern web development, AI integration, and clean code architecture.

---

## ✨ Features

- 🎯 **FastAPI** - Modern Python web framework with auto-generated docs
- 🤖 **Google Gemini AI** - Intelligent todo management assistant
- 🛠️ **Tool Functions** - AI agent can create, read, update, delete todos
- 📝 **Clean Code** - Well-commented, production-ready structure
- 🚀 **Zero Config** - In-memory storage, no database required
- 📚 **Educational** - Complete documentation and learning resources

---

## 🎓 What You'll Learn

This template teaches you:

1. **Building REST APIs** with FastAPI
2. **AI Agent Integration** with OpenAI Agents SDK
3. **Async Python** for concurrent request handling
4. **Tool Functions** - Giving AI real-world capabilities
5. **Clean Architecture** - Separating concerns in code
6. **API Design** - Request/response patterns

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Get Gemini API key from:
https://aistudio.google.com/api-keys
```

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/HamzaAhmedSheikh/fastapi-openai-agents-sdk-template.git
cd fastapi-openai-agents-sdk-template

# Install dependencies
uv sync

# Configure API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Run

```bash
# Start server
 uv run uvicorn main:app --port 8000

# Open browser: http://localhost:8000/docs
```


---

## 📁 Project Structure

```
fastapi-openai-agents-sdk-template/
├── main.py              # 🎯 Complete application (300 lines)
│   ├── Configuration    # Gemini AI setup with OpenAI SDK
│   ├── Data Layer       # Todo storage (in-memory)
│   ├── AI Tools         # Functions AI can call
│   ├── AI Agent         # Gemini assistant via OpenAI SDK
│   └── API Endpoints    # FastAPI routes
│
├── .env                 # 🔐 API keys (create this)
├── .env.example         # 🔐 Environment variables template
├── .gitignore           # 🚫 Files to exclude from git
├── pyproject.toml       # 📦 Dependencies
├── README.md            # 📖 This file
└── TEMPLATE_DOCS.md     # 📚 Complete learning guide
```

**Every section of `main.py` is clearly documented with comments!**

---

## 🧩 Code Architecture

### 1. Configuration Layer
```python
# Setup Gemini AI client
set_tracing_disabled(True)
gemini_client = AsyncOpenAI(...)
set_default_openai_client(gemini_client)
```

### 2. Data Layer
```python
# Simple in-memory storage
todos_db: dict[int, Todo] = {}

class Todo:
    id, title, description, created_at, completed
```

### 3. Tool Functions
```python
@function_tool
def create_todo(title: str, description: str = "") -> str:
    # AI calls this to create todos
    todo = Todo(...)
    todos_db[id] = todo
    return "✅ Created todo #1"
```

### 4. AI Agent
```python
assistant_agent = Agent(
    name="TodoAssistant",
    instructions="You are a helpful todo assistant...",
    model="gemini-2.5-flash",
    tools=[create_todo, get_todos, ...]
)
```

### 5. API Endpoints
```python
@app.post("/chat")
async def chat(request: ChatRequest):
    result = await Runner.run(assistant_agent, input=request.message)
    return ChatResponse(response=result.final_output)
```

---

## 🎯 API Endpoints

### POST /chat
Send message to AI assistant

**Request:**
```json
{
  "message": "Create a todo: Buy groceries"
}
```

**Response:**
```json
{
  "response": "✅ Created todo #1: Buy groceries"
}
```

### GET /health
Health check

**Response:**
```json
{
  "status": "ok",
  "model": "gemini-2.5-flash",
  "total_todos": 5
}
```

### GET /docs
Interactive API documentation (Swagger UI)

---

## 💬 Example Commands

Try these with your AI assistant:

```
✅ Create todos:
  "Add a todo: Buy groceries"
  "Create task: Finish homework by Friday"
  "Remember to call mom"

📋 View todos:
  "Show all my todos"
  "Show completed todos"
  "Get details of todo #1"

✓ Complete todos:
  "Mark todo #1 as complete"
  "Mark todo #2 as done"

🗑️ Delete todos:
  "Delete todo #3"
  "Remove todo #1"
```

---

## 🎓 Learning Resources

### Documentation Files

1. **TEMPLATE_DOCS.md** - Complete learning guide with:
   - Step-by-step code explanations
   - How AI agents work with OpenAI SDK
   - Customization guide
   - Common issues & solutions
   - Learning challenges (beginner → advanced)

### Code Comments

Every section of `main.py` has:
- 🎯 Section headers with clear boundaries
- 💡 Short, powerful comments explaining **why**
- 📚 Function docstrings with examples

### External Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/
- **Gemini API**: https://ai.google.dev/gemini-api/docs
- **uv Package Manager**: https://docs.astral.sh/uv/

---

## 🔧 Customization

### Change Agent Personality

```python
instructions="Hey! I'm your chill todo buddy 🎉"  # Casual
instructions="I am a professional productivity assistant."  # Formal
```

### Add New Tools

```python
@function_tool
def prioritize_todo(todo_id: int, priority: str) -> str:
    """Set todo priority: low, medium, high."""
    # Your implementation
    return f"🎯 Priority set to {priority}"
```

### Switch AI Model

```python
model="gemini-2.0-flash-exp"  # Faster
model="gpt-4o"                 # Use OpenAI instead
```

### Add Database

See TEMPLATE_DOCS.md → "Add Persistence" section

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "API key not found" | Check `.env` file exists with `GEMINI_API_KEY=...` |
| "Port 8000 in use" | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| "uv: command not found" | Reinstall: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| "Runner.run() error" | Use: `Runner.run(agent, input=msg)` (agent first!) |

**Detailed troubleshooting:** See TEMPLATE_DOCS.md

---

## 🎯 Learning Challenges

### Beginner
1. Add a `get_stats()` tool (count total/completed/incomplete)
2. Change agent personality to pirate speak
3. Add logging for every tool call

### Intermediate
4. Add todo categories (work, personal, shopping)
5. Add due dates and overdue detection
6. Implement search by keyword

### Advanced
7. Multi-user support with authentication
8. Replace in-memory storage with SQLite
9. Add webhooks for external integrations
10. Multi-agent system (separate agents for different tasks)

**Detailed challenges:** See TEMPLATE_DOCS.md → "Learning Challenges"

---

## 📊 Technical Stack

- **Python** 3.13+ - Modern Python with type hints
- **FastAPI** 0.128+ - High-performance async web framework
- **OpenAI Agents SDK** 0.6+ - AI agent orchestration
- **Google Gemini** 2.5 Flash - Cost-effective AI model
- **uv** - Fast Python package manager
- **Pydantic** - Data validation with type safety

---

## 🚀 Deployment

### Local Development
```bash
uv run python main.py
```

### Production (Coming Soon)
- Add PostgreSQL database
- Add JWT authentication
- Deploy to Railway/Fly.io/Render
- Add rate limiting
- Add HTTPS

See TEMPLATE_DOCS.md → "Next Steps" for deployment guides

---

## 🤝 Contributing

This is an educational template. Feel free to:

- ⭐ Star the repo if it helped you
- 🐛 Report issues or unclear docs
- 💡 Suggest improvements
- 🎓 Share projects built with this template

---

## 📜 License

MIT License - Free for learning, personal, and commercial use.

---

## 🎉 Ready to Build?

1. **Complete setup** → Read QUICKSTART.md
2. **Understand the code** → Read TEMPLATE_DOCS.md
3. **Start experimenting** → Modify main.py
4. **Build your own** → Apply what you learned

**Have questions?** All documentation is in TEMPLATE_DOCS.md

---

## 📞 Support

- 📖 **Documentation**: TEMPLATE_DOCS.md has everything
- 🐛 **Issues**: Check troubleshooting section first
- 💡 **Ideas**: See learning challenges for inspiration
- 🎓 **Learning**: Code comments explain every section

---

## 📝 Acknowledgments

- **FastAPI**: High-performance async web framework
- **OpenAI Agents SDK**: AI agent orchestration
- **Google Gemini**: Cost-effective AI model
- **uv**: Fast Python package manager
- **Pydantic**: Data validation with type safety

---

**Template Version:** 1.0.0
**Last Updated:** January 2026
