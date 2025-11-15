# AI Education Copilot

A comprehensive AI-powered educational content generation system that creates complete learning modules from instructor prompts. Features a modern React frontend and robust Flask backend with support for multiple LLM providers.

![AI Education Copilot](https://img.shields.io/badge/AI-Education-blue?style=for-the-badge&logo=ai)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=flat-square&logo=flask)
![React](https://img.shields.io/badge/React-Frontend-blue?style=flat-square&logo=react)
![OpenAI](https://img.shields.io/badge/OpenAI-Supported-orange?style=flat-square&logo=openai)
![Google Gemini](https://img.shields.io/badge/Gemini-Supported-blue?style=flat-square&logo=google)

## ✨ Features

- 🎓 **Complete Module Generation**: Automatically creates comprehensive learning modules including lesson plans, slides, video scripts, exercises, and assessments
- 📚 **Structured Content**: Generates day-by-day curriculum with Bloom's Taxonomy integration
- 📁 **File Management**: Organizes content into structured folders with proper naming conventions
- 📦 **ZIP Export**: Creates downloadable archives of generated modules
- 🤖 **Multi-LLM Support**: Works with OpenAI GPT-4, Google Gemini, or Groq
- 🎯 **Bloom's Taxonomy**: All content tagged with appropriate cognitive levels
- 🎨 **Modern UI**: Clean, professional React interface with VS Code-style file explorer
- ⚡ **Fast Generation**: Optimized for quick content creation
- 🔄 **Real-time Updates**: Live file tree updates as modules are generated

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with CORS support
- **AI Integration**: Modular LLM service supporting multiple providers
- **File Management**: Automated file creation and ZIP archiving
- **API**: RESTful endpoints for module generation and downloads

### Frontend (React)
- **Framework**: React 18 with Vite
- **UI**: Tailwind CSS with custom components
- **File Explorer**: VS Code-style tree navigation
- **Markdown Preview**: Syntax-highlighted content rendering
- **API Client**: Axios-based communication with backend

## 📁 Project Structure

```
ai-education-copilot/
├── flask-ai-copilot/          # Backend (Flask)
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── services/              # Business logic services
│   │   ├── generator.py       # LLM integration
│   │   ├── file_builder.py    # File creation
│   │   └── zipper.py          # ZIP archiving
│   ├── prompts/               # AI prompt templates
│   │   ├── curriculum.md      # Curriculum guidelines
│   │   └── pedagogy.md        # Teaching guidelines
│   ├── output/                # Generated modules (auto-created)
│   ├── test_system.py         # End-to-end testing
│   ├── verify_setup.py        # Setup verification
│   └── check_env.py           # Environment checker
│
├── react-ai-copilot/          # Frontend (React)
│   ├── src/
│   │   ├── api/               # API client
│   │   ├── components/        # React components
│   │   ├── utils/             # Utility functions
│   │   └── App.jsx            # Main app component
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
│
├── run.bat                    # Windows startup script
├── run.sh                     # Linux/Mac startup script
├── render.yaml                # Render deployment config
├── QUICK_START.md             # Quick start guide
├── DEPLOYMENT_README.md       # Deployment guide
├── END_TO_END_TEST_SUMMARY.md # Testing documentation
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** and **pip**
- **Node.js 16+** and **npm**
- **API Key**: OpenAI, Google Gemini, or Groq API key

### One-Click Start

#### Windows
```bash
run.bat
```

#### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

That's it! The script will:
- ✅ Start the Flask backend on `http://localhost:5000`
- ✅ Start the React frontend on `http://localhost:3000`
- ✅ Open your browser automatically
- ✅ Verify API key configuration

### Manual Setup

If the automated scripts don't work:

#### 1. Backend Setup
```bash
cd flask-ai-copilot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env

# Start backend
python app.py
```

#### 2. Frontend Setup
```bash
cd react-ai-copilot

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## ⚙️ Configuration

### API Keys

Create a `.env` file in the `flask-ai-copilot/` directory:

```env
# Choose your AI provider (required)
GROQ_API_KEY=gsk_your_groq_key_here

# Optional: Other providers
# OPENAI_API_KEY=sk-your-openai-key-here
# GOOGLE_API_KEY=your-google-api-key-here
# GEMINI_API_KEY=your-gemini-api-key-here

# Optional: Model selection
# GROQ_MODEL=llama-3.1-8b-instant
# OPENAI_MODEL=gpt-4
# GEMINI_MODEL=gemini-1.5-pro

# Optional: Flask settings
# PORT=5000
# FLASK_DEBUG=True
```

### Getting API Keys

#### Groq (Recommended - Fast & Free)
1. Visit [Groq Console](https://console.groq.com/)
2. Create account and generate API key
3. Add to `.env` as `GROQ_API_KEY`

#### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create API key
3. Add to `.env` as `OPENAI_API_KEY`

#### Google Gemini
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Generate API key
3. Add to `.env` as `GEMINI_API_KEY`

## 📖 Usage

### Generating a Module

1. **Enter Prompt**: In the sidebar, enter an instructor prompt like:
   - `"RAG module, intermediate, 5 days"`
   - `"Python basics, beginner, 3 days"`
   - `"Machine learning fundamentals, advanced, 7 days"`

2. **Click Generate**: The system will create a complete learning module

3. **Explore Files**: Use the file explorer to navigate generated content

4. **Download**: Click "Download ZIP" to save the entire module

### Generated Content Structure

Each module includes:

```
Module_Name/
├── summary.md              # Module overview & objectives
├── Day1/
│   ├── lesson.md          # Detailed lesson plan
│   ├── slides.md          # Presentation slides
│   ├── exercises.md       # Interactive exercises
│   ├── video_script.md    # Micro-video script (<10 min)
│   └── micro_learning.md  # Micro-learning chunks
├── Day2/
│   └── ... (same structure)
├── final_project.md        # Capstone project
├── rubric.md              # Assessment criteria
└── FILE_TREE.md           # Complete file structure
```

## 🔌 API Documentation

### Backend Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "success",
  "message": "AI Education Copilot API is running"
}
```

#### `POST /generate-module`
Generate a learning module.

**Request:**
```json
{
  "instructor_prompt": "RAG module, intermediate, 5 days"
}
```

**Response:**
```json
{
  "status": "success",
  "module_name": "RAG_Module_Intermediate",
  "files": {
    "summary.md": "# Module Summary...",
    "Day1/lesson.md": "# Day 1: Introduction..."
  },
  "file_tree": [...],
  "zip_path": "output/RAG_Module_Intermediate.zip",
  "message": "Module generated successfully"
}
```

#### `GET /download-module?module=<name>`
Download module as ZIP file.

#### `GET /list-modules`
List all generated modules.

#### `GET /check-keys`
Check API key configuration.

#### `GET /test-llm`
Test LLM connectivity.

## 🧪 Testing

### End-to-End Testing
```bash
cd flask-ai-copilot
python test_system.py
```

This will test:
- ✅ Backend endpoints
- ✅ Module generation
- ✅ File creation
- ✅ ZIP archiving
- ✅ Download functionality

### Setup Verification
```bash
cd flask-ai-copilot
python verify_setup.py
```

### Environment Check
```bash
cd flask-ai-copilot
python check_env.py
```

## 🚀 Deployment

### Render (Recommended)

1. **Create Render Account**: [render.com](https://render.com)

2. **Deploy Backend**:
   - Connect GitHub repository
   - Use `flask-ai-copilot/render.yaml` configuration
   - Set environment variables for API keys

3. **Deploy Frontend**:
   - Create Static Site service
   - Build command: `cd react-ai-copilot && npm install && npm run build`
   - Publish directory: `./react-ai-copilot/dist`

4. **Update Frontend**: Set `VITE_API_URL` to backend URL

### Manual Deployment

#### Backend
```bash
cd flask-ai-copilot
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd react-ai-copilot
npm install
npm run build
# Serve dist/ directory with any static server
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Check .env file
python check_env.py
```

#### Frontend Won't Start
```bash
# Check Node version
node --version  # Should be 16+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -i :3000  # Kill if needed
```

#### Module Generation Fails
```bash
# Check API key
python check_env.py

# Test LLM connection
curl http://localhost:5000/test-llm

# Check backend logs
tail -f flask-ai-copilot/backend.log
```

#### CORS Issues
- Backend automatically handles CORS
- Ensure frontend is accessing correct backend URL
- Check browser console for CORS errors

### Performance Tips
- Use Groq for fastest generation
- Close unused browser tabs
- Ensure stable internet connection
- Module generation can take 1-5 minutes

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** changes: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Submit** a pull request

### Development Setup
```bash
# Clone repository
git clone https://github.com/your-username/ai-education-copilot.git
cd ai-education-copilot

# Setup backend
cd flask-ai-copilot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../react-ai-copilot
npm install

# Start both (in separate terminals)
python app.py              # Backend
npm run dev               # Frontend
```

## 📄 License

This project is provided as-is for educational purposes. See individual component licenses for details.

## 🙏 Acknowledgments

- **Flask**: Web framework
- **React**: Frontend library
- **Tailwind CSS**: Styling framework
- **Vite**: Build tool
- **OpenAI/Groq/Google**: AI providers
- **Axios**: HTTP client

## 📞 Support

### Getting Help
1. Check this README
2. Review `QUICK_START.md`
3. Check `END_TO_END_TEST_SUMMARY.md`
4. Run diagnostic scripts

### Common Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Render Deployment](https://docs.render.com/)

---

**Happy Teaching! 🎓**

The AI Education Copilot makes creating comprehensive, structured learning content faster and more effective than ever before.
