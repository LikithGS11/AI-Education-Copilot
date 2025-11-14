"""
Check .env file configuration without exposing API keys
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Check .env file and verify API keys are loaded"""
    env_path = Path(__file__).parent / ".env"
    
    print("=" * 60)
    print("Checking .env File Configuration")
    print("=" * 60)
    print()
    
    # Check if .env exists
    if not env_path.exists():
        print("[ERROR] .env file NOT FOUND")
        print("\nCreate a .env file with the following format:")
        print("-" * 60)
        print("OPENAI_API_KEY=sk-...")
        print("# OR")
        print("GOOGLE_API_KEY=...")
        print("# OR")
        print("GEMINI_API_KEY=...")
        print("# OR")
        print("GROQ_API_KEY=...")
        print("-" * 60)
        return False
    
    print("[OK] .env file exists")
    print(f"  Location: {env_path}")
    print()
    
    # Load environment variables
    load_dotenv(env_path)
    
    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    print("Checking API Keys:")
    print("-" * 60)
    
    # Check OpenAI key
    if openai_key:
        # Show first 8 and last 4 characters for verification
        masked = f"{openai_key[:8]}...{openai_key[-4:]}" if len(openai_key) > 12 else "***"
        print(f"[OK] OPENAI_API_KEY: Present ({masked})")
        print(f"  Length: {len(openai_key)} characters")
    else:
        print("[ERROR] OPENAI_API_KEY: Not found")
    
    # Check Google/Gemini key
    if google_key:
        masked = f"{google_key[:8]}...{google_key[-4:]}" if len(google_key) > 12 else "***"
        print(f"[OK] GOOGLE_API_KEY: Present ({masked})")
        print(f"  Length: {len(google_key)} characters")
    elif gemini_key:
        masked = f"{gemini_key[:8]}...{gemini_key[-4:]}" if len(gemini_key) > 12 else "***"
        print(f"[OK] GEMINI_API_KEY: Present ({masked})")
        print(f"  Length: {len(gemini_key)} characters")
    else:
        print("[ERROR] GOOGLE_API_KEY: Not found")
        print("[ERROR] GEMINI_API_KEY: Not found")

    # Check Groq key
    if groq_key:
        masked = f"{groq_key[:8]}...{groq_key[-4:]}" if len(groq_key) > 12 else "***"
        print(f"[OK] GROQ_API_KEY: Present ({masked})")
        print(f"  Length: {len(groq_key)} characters")
    else:
        print("[ERROR] GROQ_API_KEY: Not found")
    
    print("-" * 60)
    print()
    
    # Check if at least one key is present
    has_key = bool(openai_key or google_key or gemini_key or groq_key)
    
    if has_key:
        print("[OK] At least one API key is configured")
        
        # Check AI provider preference
        ai_provider = os.getenv("AI_PROVIDER", "").lower()
        if ai_provider:
            print(f"  AI_PROVIDER set to: {ai_provider}")
        else:
            if openai_key:
                print("  Will use: OpenAI (default)")
            elif google_key or gemini_key:
                print("  Will use: Google Gemini (default)")
            elif groq_key:
                print("  Will use: Groq (default)")

        # Check model settings
        if openai_key:
            openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
            print(f"  OpenAI Model: {openai_model}")

        if google_key or gemini_key:
            gemini_model = os.getenv("GEMINI_MODEL") or os.getenv("GOOGLE_MODEL", "gemini-1.5-pro")
            print(f"  Gemini Model: {gemini_model}")

        if groq_key:
            groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            print(f"  Groq Model: {groq_model}")
        
        print()
        print("=" * 60)
        print("[OK] .env file is properly configured!")
        print("=" * 60)
        return True
    else:
        print("[ERROR] NO API KEYS FOUND")
        print()
        print("Add at least one of the following to your .env file:")
        print("-" * 60)
        print("OPENAI_API_KEY=sk-your-openai-key-here")
        print("# OR")
        print("GOOGLE_API_KEY=your-google-api-key-here")
        print("# OR")
        print("GEMINI_API_KEY=your-gemini-api-key-here")
        print("# OR")
        print("GROQ_API_KEY=your-groq-api-key-here")
        print("-" * 60)
        print()
        print("Optional settings:")
        print("AI_PROVIDER=openai  # or 'gemini' or 'groq'")
        print("OPENAI_MODEL=gpt-4  # or 'gpt-3.5-turbo'")
        print("GEMINI_MODEL=gemini-1.5-pro  # or 'gemini-pro'")
        print("GROQ_MODEL=llama-3.1-8b-instant  # or other Groq models")
        print("=" * 60)
        return False

if __name__ == "__main__":
    try:
        check_env_file()
    except Exception as e:
        print(f"\n[ERROR] Error checking .env file: {e}")
        print("\nMake sure python-dotenv is installed:")
        print("  pip install python-dotenv")

