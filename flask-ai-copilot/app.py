"""
Flask AI Education Copilot Backend
Main application file with API endpoints
"""

import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from services.generator import ModuleGenerator
from services.file_builder import FileBuilder
from services.zipper import ModuleZipper

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable full CORS support for React frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Check API keys for test endpoint
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize services (will raise exception if no API key)
try:
    generator = ModuleGenerator()
    file_builder = FileBuilder()
    zipper = ModuleZipper()
    print("Generator initialized successfully:", generator is not None)
except Exception as e:
    print(f"Warning: Failed to initialize services: {e}")
    generator = None
    file_builder = FileBuilder()
    zipper = ModuleZipper()

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "AI Education Copilot API is running"
    })


@app.route("/check-keys", methods=["GET"])
def check_keys():
    """Return diagnostic info about API keys and generator state"""
    return jsonify({
        "openai_key_present": OPENAI_API_KEY is not None,
        "google_key_present": GOOGLE_API_KEY is not None,
        "gemini_key_present": GOOGLE_API_KEY is not None,
        "groq_key_present": GROQ_API_KEY is not None,
        "generator_initialized": generator is not None
    })


@app.route("/test-llm", methods=["GET"])
def test_llm():
    """Test endpoint to check LLM API key configuration"""
    api_key_loaded = (OPENAI_API_KEY is not None) or (GOOGLE_API_KEY is not None) or (GROQ_API_KEY is not None)

    return jsonify({
        "status": "ok",
        "api_key_loaded": api_key_loaded,
        "openai_key_present": OPENAI_API_KEY is not None,
        "google_key_present": GOOGLE_API_KEY is not None,
        "groq_key_present": GROQ_API_KEY is not None,
        "generator_initialized": generator is not None
    })


@app.route("/test-llm-call", methods=["GET"])
def test_llm_call_route():
    """Perform a lightweight test call to the configured LLM"""
    if generator is None:
        return jsonify({
            "status": "error",
            "message": "Generator not initialized. Check API keys."
        }), 500

    result = generator.test_llm_call()
    return jsonify(result)


@app.route("/generate-module", methods=["POST"])
def generate_module():
    """
    Generate a complete learning module from instructor prompt
    
    Expected JSON:
    {
        "instructor_prompt": "RAG module, intermediate, 5 days"
    }
    
    Returns:
    {
        "status": "success",
        "module_name": "...",
        "file_tree": [...],
        "zip_path": "..."
    }
    """
    try:
        # Check if generator is initialized
        if generator is None:
            return jsonify({
                "status": "error",
                "message": "LLM generator not initialized. Check API keys in .env file."
            }), 500
        
        # Validate request
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        
        if not data or "instructor_prompt" not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'instructor_prompt' in request body"
            }), 400
        
        instructor_prompt = data["instructor_prompt"].strip()
        
        if not instructor_prompt:
            return jsonify({
                "status": "error",
                "message": "instructor_prompt cannot be empty"
            }), 400
        
        # Generate module using LLM
        print(f"Generating module for prompt: {instructor_prompt}")
        module_data = generator.generate_module(instructor_prompt)
        
        if not module_data or "module_name" not in module_data:
            return jsonify({
                "status": "error",
                "message": "Failed to generate module structure"
            }), 500
        
        module_name = module_data["module_name"]
        files = module_data.get("files", {})
        
        # Write files to disk
        print(f"Writing files for module: {module_name}")
        file_tree = file_builder.build_module(module_name, files)
        
        # Create ZIP file
        print(f"Creating ZIP for module: {module_name}")
        zip_path = zipper.create_zip(module_name)
        
        # Ensure files are included in response
        return jsonify({
            "status": "success",
            "module_name": module_name,
            "files": files,  # Include files in response for frontend
            "file_tree": file_tree,
            "zip_path": zip_path,
            "message": f"Module '{module_name}' generated successfully"
        })
    
    except Exception as e:
        print(f"Error generating module: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route("/download-module", methods=["GET"])
def download_module():
    """
    Download the generated module as ZIP file
    
    Query parameters:
    - module: module name (required)
    
    Returns: ZIP file download
    """
    try:
        module_name = request.args.get("module")
        
        if not module_name:
            return jsonify({
                "status": "error",
                "message": "Missing 'module' query parameter"
            }), 400
        
        # Sanitize module name to prevent path traversal
        module_name = os.path.basename(module_name)
        zip_path = os.path.join(OUTPUT_DIR, f"{module_name}.zip")
        
        if not os.path.exists(zip_path):
            return jsonify({
                "error": f"ZIP not found for module {module_name}"
            }), 404
        
        response = send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{module_name}.zip",
            mimetype="application/zip"
        )
        # Add CORS headers for file download
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    except Exception as e:
        print(f"Error downloading module: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route("/list-modules", methods=["GET"])
def list_modules():
    """
    List all generated modules
    
    Returns:
    {
        "status": "success",
        "modules": [...]
    }
    """
    try:
        modules = []
        
        if os.path.exists(OUTPUT_DIR):
            for item in os.listdir(OUTPUT_DIR):
                item_path = os.path.join(OUTPUT_DIR, item)
                if os.path.isdir(item_path) and not item.endswith(".zip"):
                    modules.append({
                        "name": item,
                        "path": item_path,
                        "zip_available": os.path.exists(f"{item_path}.zip")
                    })
        
        return jsonify({
            "status": "success",
            "modules": modules
        })
    
    except Exception as e:
        print(f"Error listing modules: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


if __name__ == "__main__":
    # Get port from environment or default to 5000
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    print(f"Starting Flask AI Education Copilot on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

