"""
Module Zipper Service
Handles creation of ZIP archives for modules
"""

import os
import zipfile
from pathlib import Path


class ModuleZipper:
    """Creates ZIP archives of generated modules"""
    
    def __init__(self, output_dir="output"):
        # Get the project root directory (parent of services/)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(project_root, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_zip(self, module_name):
        """
        Create a ZIP file of the module
        
        Args:
            module_name: Name of the module to zip
        
        Returns:
            str: Path to the created ZIP file
        """
        # Sanitize module name
        safe_module_name = os.path.basename(module_name)
        safe_module_name = safe_module_name.replace("..", "_")
        
        module_path = os.path.join(self.output_dir, safe_module_name)
        zip_path = os.path.join(self.output_dir, f"{safe_module_name}.zip")
        
        # Check if module directory exists
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Module directory not found: {module_path}")
        
        # Remove existing ZIP if it exists
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # Create ZIP file
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Walk through all files in the module directory
                for root, dirs, files in os.walk(module_path):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith(".")]
                    
                    for file in files:
                        # Skip hidden files
                        if file.startswith("."):
                            continue
                        
                        file_path = os.path.join(root, file)
                        
                        # Calculate relative path for archive
                        arcname = os.path.relpath(file_path, module_path)
                        
                        # Add file to ZIP
                        zipf.write(file_path, arcname)
            
            print(f"Created ZIP file: {zip_path}")
            return zip_path
        
        except Exception as e:
            # Clean up partial ZIP if creation failed
            if os.path.exists(zip_path):
                os.remove(zip_path)
            raise Exception(f"Error creating ZIP file: {e}")

