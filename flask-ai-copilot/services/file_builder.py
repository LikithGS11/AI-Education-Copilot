"""
File Builder Service
Handles creation of module files and directories
"""

import os
from pathlib import Path


class FileBuilder:
    """Builds module file structure"""
    
    def __init__(self, output_dir="output"):
        # Get the project root directory (parent of services/)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(project_root, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _sanitize_module_name(self, module_name):
        """Sanitize module name for filesystem safety"""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        sanitized = module_name
        for char in invalid_chars:
            sanitized = sanitized.replace(char, "_")
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(". ")
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "module"
        
        return sanitized
    
    def _ensure_directory(self, file_path):
        """Ensure parent directory exists"""
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
    
    def build_module(self, module_name, files):
        """
        Build module file structure
        
        Args:
            module_name: Name of the module
            files: Dictionary of {filepath: content}
        
        Returns:
            list: File tree structure
        """
        # Sanitize module name
        safe_module_name = self._sanitize_module_name(module_name)
        module_path = os.path.join(self.output_dir, safe_module_name)
        
        # Create module directory
        os.makedirs(module_path, exist_ok=True)
        
        file_tree = []
        
        # Write each file
        for filepath, content in files.items():
            try:
                # Sanitize file path to prevent directory traversal
                # Remove leading slashes and normalize
                safe_filepath = filepath.lstrip("/\\")
                safe_filepath = os.path.normpath(safe_filepath)
                
                # Prevent path traversal
                if ".." in safe_filepath or safe_filepath.startswith("/"):
                    print(f"Warning: Skipping unsafe file path: {filepath}")
                    continue
                
                # Build full path
                full_path = os.path.join(module_path, safe_filepath)
                
                # Ensure directory exists
                self._ensure_directory(full_path)
                
                # Write file with UTF-8 encoding
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Track in file tree
                file_tree.append({
                    "path": filepath,
                    "full_path": full_path,
                    "size": len(content.encode("utf-8"))
                })
                
            except Exception as e:
                print(f"Error writing file {filepath}: {str(e)}")
                # Continue with other files even if one fails
        
        # Create a file tree markdown file
        tree_md = self._generate_file_tree_markdown(file_tree)
        tree_path = os.path.join(module_path, "FILE_TREE.md")
        with open(tree_path, "w", encoding="utf-8") as f:
            f.write(tree_md)
        
        file_tree.append({
            "path": "FILE_TREE.md",
            "full_path": tree_path,
            "size": len(tree_md.encode("utf-8"))
        })
        
        return file_tree
    
    def _generate_file_tree_markdown(self, file_tree):
        """Generate a markdown representation of the file tree"""
        lines = ["# Module File Tree\n", "```"]
        
        # Group files by directory
        dirs = {}
        root_files = []
        
        for file_info in sorted(file_tree, key=lambda x: x["path"]):
            path = file_info["path"]
            if "/" in path or "\\" in path:
                # File in a subdirectory
                parts = path.replace("\\", "/").split("/")
                dir_name = "/".join(parts[:-1])
                if dir_name not in dirs:
                    dirs[dir_name] = []
                dirs[dir_name].append(parts[-1])
            else:
                root_files.append(path)
        
        # Add root files
        for file in sorted(root_files):
            lines.append(f"├── {file}")
        
        # Add directories
        for dir_name in sorted(dirs.keys()):
            lines.append(f"├── {dir_name}/")
            for file in sorted(dirs[dir_name]):
                lines.append(f"│   └── {file}")
        
        lines.append("```")
        
        return "\n".join(lines)

