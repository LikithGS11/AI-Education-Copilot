"""
Module Generator Service
Handles LLM integration and module generation
"""

import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables BEFORE reading any keys
load_dotenv()

# Read API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Console diagnostics
print("Loaded OPENAI_API_KEY:", OPENAI_API_KEY is not None)
print("Loaded GOOGLE/GEMINI_API_KEY:", GOOGLE_API_KEY is not None)
print("Loaded GROQ_API_KEY:", GROQ_API_KEY is not None)

# Validate that at least one API key is present
if not OPENAI_API_KEY and not GOOGLE_API_KEY and not GROQ_API_KEY:
    raise Exception("Missing API key. Add your key to .env file. Required: OPENAI_API_KEY, GOOGLE_API_KEY (or GEMINI_API_KEY), or GROQ_API_KEY")

# Try to import Gemini (optional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    try:
        from google import genai
        GEMINI_AVAILABLE = True
    except ImportError:
        GEMINI_AVAILABLE = False

# Try to import Groq (optional)
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class ModuleGenerator:
    """Generates learning modules using LLM"""
    
    def __init__(self):
        # Get the project root directory (parent of services/)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.curriculum_path = os.path.join(project_root, "prompts", "curriculum.md")
        self.pedagogy_path = os.path.join(project_root, "prompts", "pedagogy.md")
        
        # Initialize AI client (OpenAI by default, can switch to Gemini or Groq)
        self.ai_provider = os.getenv("AI_PROVIDER", "openai").lower()

        # Auto-detect provider if not specified
        if self.ai_provider == "openai" or (not self.ai_provider and OPENAI_API_KEY):
            if not OPENAI_API_KEY:
                raise Exception("OPENAI_API_KEY not found in environment variables")
            print("Initializing OpenAI client...")
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
            self.ai_provider = "openai"
            print(f"Using OpenAI model: {self.model}")
        elif self.ai_provider == "gemini" or (not OPENAI_API_KEY and GOOGLE_API_KEY and not GROQ_API_KEY):
            if not GEMINI_AVAILABLE:
                raise ImportError("Google Gemini package not installed. Install with: pip install google-generativeai")
            if not GOOGLE_API_KEY:
                raise Exception("GOOGLE_API_KEY not found in environment variables")
            print("Initializing Google Gemini client...")
            # Configure Gemini
            genai.configure(api_key=GOOGLE_API_KEY)
            self.client = genai
            self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro") or os.getenv("GOOGLE_MODEL", "gemini-pro")
            self.ai_provider = "gemini"
            print(f"Using Gemini model: {self.model}")
        elif self.ai_provider == "groq" or (not OPENAI_API_KEY and not GOOGLE_API_KEY and GROQ_API_KEY):
            if not GROQ_AVAILABLE:
                raise ImportError("Groq package not installed. Install with: pip install groq")
            if not GROQ_API_KEY:
                raise Exception("GROQ_API_KEY not found in environment variables")
            print("Initializing Groq client...")
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            self.ai_provider = "groq"
            print(f"Using Groq model: {self.model}")
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}. Available: openai, gemini, groq")
    
    def _load_prompt_files(self):
        """Load curriculum.md and pedagogy.md"""
        print("Loading curriculum.md...")
        try:
            with open(self.curriculum_path, "r", encoding="utf-8") as f:
                curriculum = f.read()
            print(f"Loaded curriculum.md: {len(curriculum)} characters")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Prompt file not found: {e}")
        except Exception as e:
            raise Exception(f"Error loading curriculum.md: {e}")
        
        print("Loading pedagogy.md...")
        try:
            with open(self.pedagogy_path, "r", encoding="utf-8") as f:
                pedagogy = f.read()
            print(f"Loaded pedagogy.md: {len(pedagogy)} characters")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Prompt file not found: {e}")
        except Exception as e:
            raise Exception(f"Error loading pedagogy.md: {e}")
        
        return curriculum, pedagogy
    
    def _build_master_prompt(self, instructor_prompt, curriculum, pedagogy):
        """Build the master prompt for LLM"""
        system_prompt = """You are an AI Course-Builder Copilot designed for instructors. 
Using three inputs:

1. Instructor Prompt
2. curriculum.md
3. pedagogy.md

Generate a complete learning module including:

- Module overview
- Bloom-tagged learning outcomes
- Day-by-day lesson plans
- Slides (markdown)
- Micro-video scripts
- Coding & interactive exercises
- Diagrams (ASCII/text)
- Micro-learning chunks (≤10 min)
- Final project + rubric
- A complete file tree
- Each file should be returned in JSON as:
  { "filepath": "content" }

Output format (MANDATORY):

{
  "module_name": "<Folder_Name>",
  "files": {
      "summary.md": "...",
      "Day1/lesson.md": "...",
      "Day1/slides.md": "...",
      "Day1/exercises.md": "...",
      "Day1/video_script.md": "...",
      "Day1/micro_learning.md": "...",
      "Day2/lesson.md": "...",
      ...
  }
}

Do NOT return anything except JSON."""
        
        user_prompt = f"""Instructor Prompt:
{instructor_prompt}

---

Curriculum Guidelines:
{curriculum}

---

Pedagogy Guidelines:
{pedagogy}

---

Now generate the complete module following the format specified above. Return ONLY valid JSON."""
        
        print(f"Final LLM prompt length: {len(system_prompt) + len(user_prompt)} characters")
        print(f"System prompt: {len(system_prompt)} characters")
        print(f"User prompt: {len(user_prompt)} characters")
        
        return system_prompt, user_prompt
    
    def _extract_json(self, text):
        """Extract JSON from text using regex to find first { and last }"""
        try:
            # Try to find JSON object boundaries
            first_brace = text.find('{')
            last_brace = text.rfind('}')
            
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                json_text = text[first_brace:last_brace + 1]
                # Remove markdown code blocks if present
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0].strip()
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_text)
            else:
                raise ValueError("No JSON object found in response")
        except Exception as e:
            raise Exception(f"Failed to extract JSON: {e}")
    
    def _call_openai(self, system_prompt, user_prompt):
        """Call OpenAI API"""
        print("Calling OpenAI API...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            print("LLM responded successfully")
            print(f"Response length: {len(content)} characters")
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print("Warning: Direct JSON parse failed, attempting extraction...")
                return self._extract_json(content)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise Exception(f"OpenAI API error: {e}")
    
    def _call_gemini(self, system_prompt, user_prompt):
        """Call Google Gemini API"""
        print("Calling Google Gemini API...")
        try:
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            # Use GenerativeModel for Gemini
            model = self.client.GenerativeModel(self.model)

            # Generate content with JSON response format
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7
                }
            )

            content = response.text
            print("LLM responded successfully")
            print(f"Response length: {len(content)} characters")

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print("Warning: Direct JSON parse failed, attempting extraction...")
                return self._extract_json(content)
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise Exception(f"Gemini API error: {e}")

    def _call_groq(self, system_prompt, user_prompt):
        """Call Groq API"""
        print("Calling Groq API...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            print("LLM responded successfully")
            print(f"Response length: {len(content)} characters")

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print("Warning: Direct JSON parse failed, attempting extraction...")
                return self._extract_json(content)
        except Exception as e:
            print(f"Groq API error: {e}")
            raise Exception(f"Groq API error: {e}")
    
    def generate_module(self, instructor_prompt):
        """
        Generate a complete learning module
        
        Args:
            instructor_prompt: The instructor's prompt (e.g., "RAG module, intermediate, 5 days")
        
        Returns:
            dict: Module data with module_name and files
        """
        print(f"\n{'='*60}")
        print("Starting module generation...")
        print(f"Instructor prompt: {instructor_prompt[:100]}...")
        print(f"{'='*60}\n")
        
        # Load prompt files
        curriculum, pedagogy = self._load_prompt_files()
        
        # Build master prompt
        system_prompt, user_prompt = self._build_master_prompt(
            instructor_prompt, curriculum, pedagogy
        )
        
        # Call appropriate AI provider
        if self.ai_provider == "openai":
            module_data = self._call_openai(system_prompt, user_prompt)
        elif self.ai_provider == "gemini":
            module_data = self._call_gemini(system_prompt, user_prompt)
        elif self.ai_provider == "groq":
            module_data = self._call_groq(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
        
        print("Validating LLM response...")
        
        # Validate response structure
        if not isinstance(module_data, dict):
            raise ValueError("LLM response is not a dictionary")
        
        if "module_name" not in module_data:
            raise ValueError("LLM response missing 'module_name' field")
        
        if "files" not in module_data:
            raise ValueError("LLM response missing 'files' field")
        
        if not isinstance(module_data["files"], dict):
            raise ValueError("LLM response 'files' field must be a dictionary")
        
        # Validate each file entry
        print(f"Module name: {module_data['module_name']}")
        print(f"Number of files: {len(module_data['files'])}")
        
        for filepath, content in module_data["files"].items():
            if not isinstance(filepath, str):
                raise ValueError(f"File path must be a string, got {type(filepath)}")
            if not isinstance(content, str):
                raise ValueError(f"File content must be a string for {filepath}, got {type(content)}")
        
        print("Validation successful!")
        print(f"{'='*60}\n")
        
        return module_data

    def test_llm_call(self):
        """
        Perform a lightweight test call to the configured LLM provider.
        Returns a status dictionary without exposing full responses.
        """
        if self.ai_provider == "openai":
            try:
                prompt = "Reply with the single word 'pong'."
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a simple diagnostic bot."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=5
                )
                content = response.choices[0].message.content.strip() if response.choices else ""
                return {
                    "provider": "openai",
                    "model": self.model,
                    "status": "success",
                    "message": content[:50]
                }
            except Exception as e:
                return {
                    "provider": "openai",
                    "model": self.model,
                    "status": "error",
                    "error": str(e)
                }
        elif self.ai_provider == "gemini":
            try:
                model = self.client.GenerativeModel(self.model)
                response = model.generate_content("Reply with the single word 'pong'.")
                text = getattr(response, "text", "") or "OK"
                return {
                    "provider": "gemini",
                    "model": self.model,
                    "status": "success",
                    "message": text[:50]
                }
            except Exception as e:
                return {
                    "provider": "gemini",
                    "model": self.model,
                    "status": "error",
                    "error": str(e)
                }
        elif self.ai_provider == "groq":
            try:
                prompt = "Reply with the single word 'pong'."
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a simple diagnostic bot."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=5
                )
                content = response.choices[0].message.content.strip() if response.choices else ""
                return {
                    "provider": "groq",
                    "model": self.model,
                    "status": "success",
                    "message": content[:50]
                }
            except Exception as e:
                return {
                    "provider": "groq",
                    "model": self.model,
                    "status": "error",
                    "error": str(e)
                }
        else:
            return {
                "provider": self.ai_provider,
                "status": "error",
                "error": "Unsupported provider for test call"
            }

