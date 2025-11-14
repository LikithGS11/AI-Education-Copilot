"""
Quick verification script to check if the backend is properly configured
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found")
        print("  Create .env file with at least one of:")
        print("    OPENAI_API_KEY=your_key_here")
        print("    GOOGLE_API_KEY=your_key_here")
        print("    GEMINI_API_KEY=your_key_here")
        return False

def check_prompt_files():
    """Check if prompt files exist"""
    prompts_dir = Path(__file__).parent / "prompts"
    curriculum = prompts_dir / "curriculum.md"
    pedagogy = prompts_dir / "pedagogy.md"
    
    if curriculum.exists() and pedagogy.exists():
        print("✓ Prompt files exist (curriculum.md, pedagogy.md)")
        return True
    else:
        print("✗ Prompt files missing")
        if not curriculum.exists():
            print(f"  Missing: {curriculum}")
        if not pedagogy.exists():
            print(f"  Missing: {pedagogy}")
        return False

def check_output_dir():
    """Check if output directory exists or can be created"""
    output_dir = Path(__file__).parent / "output"
    try:
        output_dir.mkdir(exist_ok=True)
        print("✓ Output directory ready")
        return True
    except Exception as e:
        print(f"✗ Cannot create output directory: {e}")
        return False

def check_imports():
    """Check if required packages can be imported"""
    missing = []
    
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("✗ Flask not installed")
        missing.append("flask")
    
    try:
        import flask_cors
        print("✓ flask-cors installed")
    except ImportError:
        print("✗ flask-cors not installed")
        missing.append("flask-cors")
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("✗ python-dotenv not installed")
        missing.append("python-dotenv")
    
    try:
        import openai
        print("✓ openai package installed")
    except ImportError:
        print("⚠ openai package not installed (optional if using Gemini)")
    
    try:
        import google.generativeai
        print("✓ google-generativeai installed")
    except ImportError:
        print("⚠ google-generativeai not installed (optional if using OpenAI)")
    
    if missing:
        print(f"\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("AI Copilot Backend Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Environment File", check_env_file),
        ("Prompt Files", check_prompt_files),
        ("Output Directory", check_output_dir),
        ("Python Packages", check_imports),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    if all_passed:
        print("\n✓ All checks passed! Backend is ready to run.")
        print("\nStart the server with:")
        print("  python app.py")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

