# Flask AI Education Copilot Backend

A complete Flask backend for generating AI-powered educational modules including lesson plans, slides, video scripts, exercises, and more.

## Features

- 🎓 **Complete Module Generation**: Automatically creates comprehensive learning modules from instructor prompts
- 📚 **Structured Content**: Generates lesson plans, slides, video scripts, exercises, diagrams, and rubrics
- 📁 **File Management**: Organizes content into day-by-day folders with proper structure
- 📦 **ZIP Export**: Creates downloadable ZIP archives of generated modules
- 🤖 **Multi-LLM Support**: Works with OpenAI GPT-4 or Google Gemini
- 🎯 **Bloom's Taxonomy**: All content tagged with appropriate learning levels

## Project Structure

```
flask-ai-copilot/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
│
├── prompts/
│     ├── curriculum.md   # Curriculum design guidelines
│     └── pedagogy.md     # Pedagogy design guidelines
│
├── services/
│     ├── generator.py    # LLM integration and module generation
│     ├── file_builder.py # File creation and organization
│     └── zipper.py       # ZIP archive creation
│
├── output/               # Generated modules (created automatically)
│
└── README.md            # This file
```

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd flask-ai-copilot
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Choose AI provider: "openai" or "gemini"
AI_PROVIDER=openai

# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# For Gemini (alternative)
# GEMINI_API_KEY=your_gemini_api_key_here
# GEMINI_MODEL=gemini-1.5-pro

# Flask Configuration
PORT=5000
FLASK_DEBUG=False
```

### 5. Get API Keys

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

### Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` (or the port specified in `.env`).

### API Endpoints

#### 1. Generate Module

**POST** `/generate-module`

Generate a complete learning module from an instructor prompt.

**Request Body:**
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
  "file_tree": [
    {
      "path": "summary.md",
      "full_path": "output/RAG_Module_Intermediate/summary.md",
      "size": 1234
    },
    ...
  ],
  "zip_path": "output/RAG_Module_Intermediate.zip",
  "message": "Module 'RAG_Module_Intermediate' generated successfully"
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/generate-module \
  -H "Content-Type: application/json" \
  -d '{"instructor_prompt": "RAG module, intermediate, 5 days"}'
```

#### 2. Download Module

**GET** `/download-module?module=<module_name>`

Download the generated module as a ZIP file.

**Example:**
```bash
curl -O http://localhost:5000/download-module?module=RAG_Module_Intermediate
```

#### 3. List Modules

**GET** `/list-modules`

List all generated modules.

**Response:**
```json
{
  "status": "success",
  "modules": [
    {
      "name": "RAG_Module_Intermediate",
      "path": "output/RAG_Module_Intermediate",
      "zip_available": true
    }
  ]
}
```

#### 4. Health Check

**GET** `/`

Check if the API is running.

## Generated Module Structure

Each generated module includes:

- `summary.md` - Module overview and learning objectives
- `Day1/`, `Day2/`, etc. - Day-by-day content folders
  - `lesson.md` - Detailed lesson plan with Bloom's tags
  - `slides.md` - Presentation slides in markdown
  - `exercises.md` - Interactive exercises and coding challenges
  - `video_script.md` - Micro-video script (≤10 min)
  - `micro_learning.md` - Micro-learning chunks
- `final_project.md` - Final project description
- `rubric.md` - Assessment rubric
- `FILE_TREE.md` - Complete file structure documentation

## Configuration

### AI Provider Selection

Edit `.env` to switch between providers:

```env
# Use OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4

# Or use Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-pro
```

### Model Selection

- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Gemini**: `gemini-1.5-pro`, `gemini-1.5-flash`

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `404` - Not Found (module doesn't exist)
- `500` - Internal Server Error

Error responses include:
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Security Considerations

- File paths are sanitized to prevent directory traversal attacks
- Module names are validated before use
- API keys are stored in environment variables (never commit `.env`)

## Troubleshooting

### Module Generation Fails

1. Check API key is set correctly in `.env`
2. Verify API key has sufficient credits/quota
3. Check console logs for detailed error messages
4. Ensure `prompts/curriculum.md` and `prompts/pedagogy.md` exist

### ZIP Download Fails

1. Verify module was generated successfully
2. Check `output/` directory permissions
3. Ensure module name matches exactly (case-sensitive)

### Import Errors

1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check Python version (3.8+ required)

## Development

### Running in Debug Mode

Set in `.env`:
```env
FLASK_DEBUG=True
```

### Adding Custom Prompts

Edit `prompts/curriculum.md` and `prompts/pedagogy.md` to customize the generation guidelines.

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, check the console logs for detailed error messages.

