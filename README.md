# AI Education Copilot

A comprehensive AI-powered educational content generation system capable of producing complete learning modules from instructor-provided prompts. It features a modern React frontend, a robust Flask backend, and supports multiple LLM providers.

![AI Education Copilot](https://img.shields.io/badge/AI-Education-blue?style=for-the-badge&logo=ai)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=flat-square&logo=flask)
![React](https://img.shields.io/badge/React-Frontend-blue?style=flat-square&logo=react)
![OpenAI](https://img.shields.io/badge/OpenAI-Supported-orange?style=flat-square&logo=openai)
![Google Gemini](https://img.shields.io/badge/Gemini-Supported-blue?style=flat-square&logo=google)

## ✨ Features

- 🎓 **Complete Module Generation:** Produces full learning modules including lesson plans, slides, exercises, assessments, and micro-learning content.  
- 📚 **Structured Curriculum:** Creates day-by-day learning content aligned with Bloom’s Taxonomy.  
- 📁 **File Management:** Automatically organizes generated files with clean naming and structured folders.  
- 📦 **ZIP Export:** Supports exporting the entire module as a downloadable ZIP.  
- 🤖 **Multi-LLM Support:** Works with OpenAI GPT, Google Gemini, and Groq.  
- 🎨 **Modern UI:** Built using React with a VS Code-style file explorer.  
- ⚡ **Optimized Generation:** Fast and efficient content creation pipeline.  
- 🔄 **Real-time File Tree Updates:** Instantly displays newly generated files.  

---

## 🏗️ Architecture

### **Backend (Flask)**  
- Flask with CORS  
- Modular LLM integration  
- Automated file creation & ZIP archiving  
- RESTful API endpoints  

### **Frontend (React)**  
- Vite-powered React application  
- Tailwind CSS styling  
- Markdown preview  
- VS Code-style file explorer  
- Axios API communication  

---

## 📁 Project Structure

```
ai-education-copilot/
├── flask-ai-copilot/
│   ├── app.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── generator.py
│   │   ├── file_builder.py
│   │   └── zipper.py
│   ├── prompts/
│   │   ├── curriculum.md
│   │   └── pedagogy.md
│   ├── output/
│   ├── test_system.py
│   ├── verify_setup.py
│   └── check_env.py
│
├── react-ai-copilot/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── run.bat
├── run.sh
├── render.yaml
├── QUICK_START.md
├── DEPLOYMENT_README.md
├── END_TO_END_TEST_SUMMARY.md
└── README.md
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+  
- Node.js 16+  
- API Key from Groq / OpenAI / Google Gemini  

---

### **One-Click Start**

#### **Windows**
```bash
run.bat
```

#### **Linux / Mac**
```bash
chmod +x run.sh
./run.sh
```

The script will automatically:
- Start Flask backend (`http://localhost:5000`)  
- Start React frontend (`http://localhost:3000`)  
- Verify API keys  
- Open the application in your browser  

---

## 🔧 Manual Setup

### **Backend Setup**
```bash
cd flask-ai-copilot
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python app.py
```

### **Frontend Setup**
```bash
cd react-ai-copilot
npm install
npm run dev
```

---

## ⚙️ Configuration

Create `.env` inside `flask-ai-copilot/`:

```env
# Primary Provider
GROQ_API_KEY=your_groq_key_here

# Optional Providers
# OPENAI_API_KEY=your_openai_key
# GEMINI_API_KEY=your_google_key

# Optional Model Selection
# GROQ_MODEL=llama-3.1-8b-instant
# OPENAI_MODEL=gpt-4
# GEMINI_MODEL=gemini-1.5-pro
```

---

## 📘 Usage

### **Generating a Module**
Enter prompts such as:

- "RAG module, intermediate, 5 days"  
- "Python basics, beginner, 3 days"  
- "Machine learning fundamentals, advanced, 7 days"  

Then click **Generate** to create the module.

### **Generated Output Structure**

```
Module_Name/
├── summary.md
├── Day1/
│   ├── lesson.md
│   ├── slides.md
│   ├── exercises.md
│   ├── video_script.md
│   └── micro_learning.md
├── Day2/...
├── final_project.md
├── rubric.md
└── FILE_TREE.md
```

---

## 🔌 API Documentation

### **GET /**
Health check:
```json
{
  "status": "success",
  "message": "AI Education Copilot API is running"
}
```

### **POST /generate-module**
Body:
```json
{
  "instructor_prompt": "RAG module, intermediate, 5 days"
}
```

### **GET /download-module?module=<name>**
Download ZIP.

### **GET /list-modules**
List generated modules.

### **GET /check-keys**
Check API key availability.

---

## 🧪 Testing

### End-to-End Test
```bash
cd flask-ai-copilot
python test_system.py
```

### Setup Verification
```bash
python verify_setup.py
```

### Environment Check
```bash
python check_env.py
```

---

## 🚀 Deployment

### **Render Deployment (Recommended)**

1. Connect your GitHub repo  
2. Deploy backend using `render.yaml`  
3. Deploy frontend as a static site  
4. Set `VITE_API_URL` to the backend URL  

### **Manual Deployment**
Backend:
```bash
python app.py
```
Frontend:
```bash
npm run build
```

---

## 🔧 Troubleshooting

### Backend Issues
```bash
python --version
pip install -r requirements.txt
python check_env.py
```

### Frontend Issues
```bash
rm -rf node_modules package-lock.json
npm install
```

### Module Generation Problems
```bash
curl http://localhost:5000/test-llm
```

