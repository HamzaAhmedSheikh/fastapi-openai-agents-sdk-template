# 🚀 Quick Start Guide

Get your AI-powered todo app running in 5 minutes!

---

## Step 1: Install uv (30 seconds)

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

---

## Step 2: Get Gemini API Key (2 minutes)

1. Visit: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"**
3. Copy your API key (starts with `AIza...`)

---

## Step 3: Setup Project (1 minute)

```bash
# Navigate to project
cd crud-template

# Install dependencies
uv sync

# Create .env file
echo "GEMINI_API_KEY=your_actual_key_here" > .env
```

**⚠️ Important:** Replace `your_actual_key_here` with your real API key!

---

## Step 4: Run the Server (10 seconds)

```bash
# Start the app
uv run python main.py

# You should see:
# 🚀 AI-Powered Todo App
# 📍 Server: http://localhost:8000
# 📖 Docs:   http://localhost:8000/docs
```

---

## Step 5: Test It!

### Option A: Browser (Recommended for Beginners)

1. Open: http://localhost:8000/docs
2. Find **POST /chat** endpoint
3. Click **"Try it out"**
4. Enter message: `Create a todo: Buy groceries`
5. Click **"Execute"**
6. See AI response! ✨

### Option B: Command Line

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a todo: Learn AI agents"}'
```

---

## 🎯 Try These Commands

```
✅ Create todos:
  - "Add a todo: Buy groceries with description: milk, eggs, bread"
  - "Create task: Finish homework"
  - "Remember to call mom"

📋 View todos:
  - "Show all my todos"
  - "Show completed todos"
  - "Show incomplete todos"
  - "Get details of todo #1"

✓ Complete todos:
  - "Mark todo #1 as complete"
  - "Mark todo #2 as done"

🗑️ Delete todos:
  - "Delete todo #3"
  - "Remove todo #1"
```

---

## 🐛 Troubleshooting

### Problem: "GEMINI_API_KEY not found"

```bash
# Check .env file exists
ls -la .env

# Check contents
cat .env

# Should show: GEMINI_API_KEY=AIza...
```

### Problem: "Port 8000 already in use"

```bash
# Option 1: Kill existing process
lsof -ti:8000 | xargs kill -9

# Option 2: Use different port
uv run uvicorn main:app --port 8080
```

### Problem: "uv: command not found"

```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal
source ~/.bashrc  # or source ~/.zshrc
```

---

## 📚 Next Steps

1. **Read TEMPLATE_DOCS.md** - Complete learning guide
2. **Explore /docs** - Interactive API documentation
3. **Modify main.py** - Change agent personality
4. **Add features** - Try the learning challenges

---

## 💡 Pro Tips

- **Use /docs endpoint** - Best way to test without curl
- **Check server logs** - See which tools AI calls
- **Experiment freely** - In-memory storage, nothing breaks permanently
- **Read comments** - Every section of main.py is documented

---

## 🎉 You're Ready!

Your AI-powered todo app is running. Start chatting with your AI assistant!

**Questions?** Read TEMPLATE_DOCS.md for detailed explanations.
