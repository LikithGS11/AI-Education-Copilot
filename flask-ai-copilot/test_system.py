"""
Comprehensive End-to-End System Test for AI Copilot
Tests all backend endpoints and validates module generation
"""

import os
import sys
import json
import time
import requests
import zipfile
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_PROMPTS = [
    {"instructor_prompt": "RAG module, intermediate, 5 days"},
    {"instructor_prompt": "Python basics, beginner, 5 days"},
    {"instructor_prompt": "SQL crash course, intermediate, 3 days"},
    {"instructor_prompt": "Cloud computing fundamentals, 2 days"},
]

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=300)
        else:
            return False, f"Unsupported method: {method}"
        
        if response.status_code == expected_status:
            return True, response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused. Is the Flask server running?"
    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except Exception as e:
        return False, str(e)

def test_health_check():
    """Test health check endpoint"""
    print_header("1. Testing Health Check")
    success, result = test_endpoint(f"{BASE_URL}/")
    if success:
        print_success("Health check passed")
        print_info(f"Response: {result}")
        return True
    else:
        print_error(f"Health check failed: {result}")
        return False

def test_check_keys():
    """Test API key check endpoint"""
    print_header("2. Testing API Key Check")
    success, result = test_endpoint(f"{BASE_URL}/check-keys")
    if success:
        print_success("API key check endpoint accessible")
        if isinstance(result, dict):
            print_info(f"OpenAI key present: {result.get('openai_key_present', False)}")
            print_info(f"Google/Gemini key present: {result.get('google_key_present', False)}")
            print_info(f"Generator initialized: {result.get('generator_initialized', False)}")
            
            if not result.get('generator_initialized', False):
                print_warning("Generator not initialized. Check API keys in .env file.")
                return False
            return True
        else:
            print_error(f"Unexpected response format: {result}")
            return False
    else:
        print_error(f"API key check failed: {result}")
        return False

def test_test_llm():
    """Test LLM test endpoint"""
    print_header("3. Testing LLM Test Endpoint")
    success, result = test_endpoint(f"{BASE_URL}/test-llm")
    if success:
        print_success("LLM test endpoint accessible")
        if isinstance(result, dict):
            print_info(f"API key loaded: {result.get('api_key_loaded', False)}")
            print_info(f"Generator initialized: {result.get('generator_initialized', False)}")
            return True
        else:
            print_error(f"Unexpected response format: {result}")
            return False
    else:
        print_error(f"LLM test failed: {result}")
        return False

def test_test_llm_call():
    """Test actual LLM call"""
    print_header("4. Testing LLM Call")
    success, result = test_endpoint(f"{BASE_URL}/test-llm-call")
    if success:
        print_success("LLM call endpoint accessible")
        if isinstance(result, dict):
            status = result.get('status', 'unknown')
            provider = result.get('provider', 'unknown')
            model = result.get('model', 'unknown')
            
            if status == 'success':
                print_success(f"LLM call successful using {provider} ({model})")
                return True
            else:
                error = result.get('error', 'Unknown error')
                print_error(f"LLM call failed: {error}")
                print_warning("This may be due to API key issues or network problems")
                return False
        else:
            print_error(f"Unexpected response format: {result}")
            return False
    else:
        print_error(f"LLM call test failed: {result}")
        return False

def test_generate_module(prompt_data):
    """Test module generation"""
    print_header(f"5. Testing Module Generation: {prompt_data['instructor_prompt']}")
    success, result = test_endpoint(f"{BASE_URL}/generate-module", method="POST", data=prompt_data, expected_status=200)
    
    if success:
        if isinstance(result, dict):
            if result.get('status') == 'success':
                module_name = result.get('module_name')
                files = result.get('files', {})
                file_tree = result.get('file_tree', [])
                
                print_success(f"Module generated: {module_name}")
                print_info(f"Files count: {len(files)}")
                print_info(f"File tree entries: {len(file_tree)}")
                
                # Validate module structure
                if not module_name:
                    print_error("Module name is missing")
                    return False, None
                
                if not files or len(files) == 0:
                    print_error("No files generated")
                    return False, None
                
                # Check for expected files
                expected_files = ['summary.md', 'Day1', 'Day2']
                found_files = []
                for filepath in files.keys():
                    if 'summary' in filepath.lower():
                        found_files.append('summary.md')
                    if 'day1' in filepath.lower():
                        found_files.append('Day1')
                    if 'day2' in filepath.lower():
                        found_files.append('Day2')
                
                print_info(f"Found expected files: {set(found_files)}")
                
                # Validate file structure
                for filepath, content in list(files.items())[:5]:  # Check first 5 files
                    if not isinstance(content, str):
                        print_error(f"File {filepath} has invalid content type")
                        return False, None
                    if len(content) == 0:
                        print_warning(f"File {filepath} is empty")
                
                return True, module_name
            else:
                error_msg = result.get('message', 'Unknown error')
                print_error(f"Module generation failed: {error_msg}")
                return False, None
        else:
            print_error(f"Unexpected response format: {result}")
            return False, None
    else:
        print_error(f"Module generation request failed: {result}")
        return False, None

def test_validate_files(module_name):
    """Validate that files were written to disk"""
    print_header(f"6. Validating Files on Disk: {module_name}")
    
    project_root = Path(__file__).parent
    output_dir = project_root / "output" / module_name
    
    if not output_dir.exists():
        print_error(f"Module directory not found: {output_dir}")
        return False
    
    print_success(f"Module directory exists: {output_dir}")
    
    # Count files
    files = list(output_dir.rglob("*"))
    files = [f for f in files if f.is_file()]
    
    print_info(f"Total files found: {len(files)}")
    
    if len(files) == 0:
        print_error("No files found in module directory")
        return False
    
    # Check for expected files
    file_names = [f.name for f in files]
    if 'summary.md' in file_names or any('summary' in f.name.lower() for f in files):
        print_success("Summary file found")
    else:
        print_warning("Summary file not found")
    
    return True

def test_validate_zip(module_name):
    """Validate ZIP file creation"""
    print_header(f"7. Validating ZIP File: {module_name}")
    
    project_root = Path(__file__).parent
    zip_path = project_root / "output" / f"{module_name}.zip"
    
    if not zip_path.exists():
        print_error(f"ZIP file not found: {zip_path}")
        return False
    
    print_success(f"ZIP file exists: {zip_path}")
    
    # Check file size
    zip_size = zip_path.stat().st_size
    print_info(f"ZIP file size: {zip_size} bytes")
    
    if zip_size == 0:
        print_error("ZIP file is empty")
        return False
    
    # Validate ZIP structure
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            print_info(f"ZIP contains {len(file_list)} files")
            
            if len(file_list) == 0:
                print_error("ZIP file is empty")
                return False
            
            # Check for expected files
            has_summary = any('summary' in f.lower() for f in file_list)
            has_day1 = any('day1' in f.lower() for f in file_list)
            
            if has_summary:
                print_success("ZIP contains summary file")
            if has_day1:
                print_success("ZIP contains Day1 files")
            
            return True
    except zipfile.BadZipFile:
        print_error("ZIP file is corrupted")
        return False
    except Exception as e:
        print_error(f"Error reading ZIP: {e}")
        return False

def test_download_module(module_name):
    """Test ZIP download endpoint"""
    print_header(f"8. Testing ZIP Download: {module_name}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/download-module",
            params={"module": module_name},
            timeout=30
        )
        
        if response.status_code == 200:
            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'application/zip' in content_type or 'zip' in content_type:
                print_success("ZIP download successful")
                print_info(f"Content-Type: {content_type}")
                print_info(f"Content-Length: {response.headers.get('content-length', 'unknown')} bytes")
                
                # Validate blob
                if len(response.content) > 0:
                    print_success("Downloaded ZIP is not empty")
                    return True
                else:
                    print_error("Downloaded ZIP is empty")
                    return False
            else:
                print_error(f"Unexpected content type: {content_type}")
                return False
        elif response.status_code == 404:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            error_msg = error_data.get('error', 'ZIP not found')
            print_error(f"ZIP not found: {error_msg}")
            return False
        else:
            print_error(f"Download failed with status {response.status_code}: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Connection refused. Is the Flask server running?")
        return False
    except Exception as e:
        print_error(f"Download test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print_header("AI COPILOT END-TO-END SYSTEM TEST")
    print_info("Make sure the Flask server is running on http://localhost:5000")
    print_info("Press Ctrl+C to cancel\n")
    
    time.sleep(2)
    
    results = {
        'health_check': False,
        'check_keys': False,
        'test_llm': False,
        'test_llm_call': False,
        'module_generations': [],
        'file_validations': [],
        'zip_validations': [],
        'download_tests': [],
    }
    
    # Basic endpoint tests
    results['health_check'] = test_health_check()
    if not results['health_check']:
        print_error("\nServer is not running. Please start Flask server first.")
        return results
    
    results['check_keys'] = test_check_keys()
    results['test_llm'] = test_test_llm()
    results['test_llm_call'] = test_test_llm_call()
    
    # Module generation tests
    for i, prompt_data in enumerate(TEST_PROMPTS, 1):
        print(f"\n{Colors.BOLD}Testing Module {i}/{len(TEST_PROMPTS)}{Colors.END}")
        success, module_name = test_generate_module(prompt_data)
        
        if success and module_name:
            results['module_generations'].append({
                'prompt': prompt_data['instructor_prompt'],
                'module_name': module_name,
                'success': True
            })
            
            # Validate files
            file_valid = test_validate_files(module_name)
            results['file_validations'].append({
                'module_name': module_name,
                'success': file_valid
            })
            
            # Validate ZIP
            zip_valid = test_validate_zip(module_name)
            results['zip_validations'].append({
                'module_name': module_name,
                'success': zip_valid
            })
            
            # Test download
            download_valid = test_download_module(module_name)
            results['download_tests'].append({
                'module_name': module_name,
                'success': download_valid
            })
            
            # Wait between tests to avoid rate limiting
            if i < len(TEST_PROMPTS):
                print_info("Waiting 5 seconds before next test...")
                time.sleep(5)
        else:
            results['module_generations'].append({
                'prompt': prompt_data['instructor_prompt'],
                'module_name': None,
                'success': False
            })
    
    # Print summary
    print_header("TEST SUMMARY")
    
    print(f"\n{Colors.BOLD}Basic Endpoints:{Colors.END}")
    print(f"  Health Check: {'✓' if results['health_check'] else '✗'}")
    print(f"  Check Keys: {'✓' if results['check_keys'] else '✗'}")
    print(f"  Test LLM: {'✓' if results['test_llm'] else '✗'}")
    print(f"  Test LLM Call: {'✓' if results['test_llm_call'] else '✗'}")
    
    print(f"\n{Colors.BOLD}Module Generations:{Colors.END}")
    successful = sum(1 for m in results['module_generations'] if m['success'])
    print(f"  Successful: {successful}/{len(results['module_generations'])}")
    for m in results['module_generations']:
        status = '✓' if m['success'] else '✗'
        print(f"  {status} {m['prompt']}")
        if m['module_name']:
            print(f"    → {m['module_name']}")
    
    print(f"\n{Colors.BOLD}File Validations:{Colors.END}")
    successful = sum(1 for v in results['file_validations'] if v['success'])
    print(f"  Successful: {successful}/{len(results['file_validations'])}")
    
    print(f"\n{Colors.BOLD}ZIP Validations:{Colors.END}")
    successful = sum(1 for v in results['zip_validations'] if v['success'])
    print(f"  Successful: {successful}/{len(results['zip_validations'])}")
    
    print(f"\n{Colors.BOLD}Download Tests:{Colors.END}")
    successful = sum(1 for d in results['download_tests'] if d['success'])
    print(f"  Successful: {successful}/{len(results['download_tests'])}")
    
    # Overall status
    all_basic = all([
        results['health_check'],
        results['check_keys'],
        results['test_llm'],
    ])
    
    all_modules = len(results['module_generations']) > 0 and all(m['success'] for m in results['module_generations'])
    
    print(f"\n{Colors.BOLD}Overall Status:{Colors.END}")
    if all_basic and all_modules:
        print_success("All tests passed! System is production-ready.")
    elif all_basic:
        print_warning("Basic endpoints work, but some module generations failed.")
    else:
        print_error("Some basic endpoints failed. Check server configuration.")
    
    return results

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

