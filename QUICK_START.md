# Quick Start Guide

## 🚀 Fastest Way to Start

### Windows
```bash
run.bat
```

### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

That's it! The script will:
- ✅ Start Flask backend
- ✅ Start React frontend  
- ✅ Open your browser automatically

## 📋 What You Need First

1. **Install Python 3.8+** and **Node.js 16+**
2. **Add API keys** to `flask-ai-copilot/.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. **Install dependencies** (first time only):
   ```bash
   # Backend
   cd flask-ai-copilot
   pip install -r requirements.txt
   
   # Frontend
   cd react-ai-copilot
   npm install
   ```

## 🌐 Access the App

After running the script, open:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000

## 🛠️ Manual Start (Alternative)

If scripts don't work, start manually:

**Terminal 1:**
```bash
cd flask-ai-copilot
python app.py
```

**Terminal 2:**
```bash
cd react-ai-copilot
npm run dev
```

Then open http://localhost:3000 in your browser.

## ❓ Need Help?

See [RUNNING_THE_PROJECT.md](RUNNING_THE_PROJECT.md) for detailed instructions and troubleshooting.

