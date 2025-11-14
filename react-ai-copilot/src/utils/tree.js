/**
 * Utility functions for converting file maps to tree structures
 */

// Helper to count files in tree
const countFilesInTree = (tree) => {
  let count = 0;
  const traverse = (items) => {
    items.forEach(item => {
      if (item.type === 'file') count++;
      if (item.type === 'folder' && item.children) {
        traverse(item.children);
      }
    });
  };
  traverse(tree);
  return count;
};

/**
 * Convert a flat file map to a nested tree structure
 * @param {Object} files - Object with file paths as keys and content as values
 * @returns {Array} Nested tree structure
 * 
 * Example:
 * Input: {
 *   "Day1/lesson.md": "content",
 *   "Day1/slides.md": "content",
 *   "Day2/exercises.md": "content",
 *   "summary.md": "content"
 * }
 * 
 * Output: [
 *   { name: "summary.md", path: "summary.md", type: "file", content: "content" },
 *   { 
 *     name: "Day1", 
 *     path: "Day1", 
 *     type: "folder", 
 *     expanded: true,
 *     children: [
 *       { name: "lesson.md", path: "Day1/lesson.md", type: "file", content: "content" },
 *       { name: "slides.md", path: "Day1/slides.md", type: "file", content: "content" }
 *     ]
 *   },
 *   {
 *     name: "Day2",
 *     path: "Day2",
 *     type: "folder",
 *     expanded: true,
 *     children: [
 *       { name: "exercises.md", path: "Day2/exercises.md", type: "file", content: "content" }
 *     ]
 *   }
 * ]
 */
export const filesToTree = (files) => {
  if (!files || typeof files !== 'object') {
    console.warn('[Tree] Invalid input, expected object:', typeof files);
    return [];
  }
  
  console.log('[Tree] Building tree from', Object.keys(files).length, 'files');
  
  const tree = [];

  /**
   * Recursively add a file/folder to the tree
   * @param {Array} parent - Parent array to add to
   * @param {Array} parts - Path parts array
   * @param {string} fullPath - Full original path
   * @param {string} content - File content
   */
  const addToTree = (parent, parts, fullPath, content) => {
    if (parts.length === 0) return;
    
    const currentName = parts[0];
    const isLastPart = parts.length === 1;
    
    if (isLastPart) {
      // This is a file
      parent.push({
        name: currentName,
        path: fullPath,
        type: 'file',
        content: content,
      });
    } else {
      // This is a folder (or intermediate folder)
      // Find or create the folder
      let folder = parent.find(item => item.name === currentName && item.type === 'folder');
      
      if (!folder) {
        folder = {
          name: currentName,
          path: parts.slice(0, 1).join('/'), // Path up to this folder
          type: 'folder',
          children: [],
          expanded: true, // Default to expanded
        };
        parent.push(folder);
      }
      
      // Recursively add the rest of the path
      addToTree(folder.children, parts.slice(1), fullPath, content);
    }
  };

  // Process each file path
  Object.entries(files).forEach(([filePath, content]) => {
    const parts = filePath.split('/').filter(Boolean);
    
    if (parts.length === 0) return; // Skip empty paths
    
    // Add to tree starting from root
    addToTree(tree, parts, filePath, content);
  });

  // Sort: folders first, then files, both alphabetically
  const sortTree = (items) => {
    return items.sort((a, b) => {
      if (a.type === 'folder' && b.type === 'file') return -1;
      if (a.type === 'file' && b.type === 'folder') return 1;
      return a.name.localeCompare(b.name);
    });
  };

  // Recursively sort the entire tree
  const sortRecursive = (items) => {
    sortTree(items);
    items.forEach(item => {
      if (item.type === 'folder' && item.children) {
        sortRecursive(item.children);
      }
    });
  };

  sortRecursive(tree);
  
  console.log('[Tree] Tree build complete:', {
    rootItems: tree.length,
    totalFiles: countFilesInTree(tree)
  });
  
  return tree;
};

/**
 * Find a file in the tree by path
 * @param {Array} tree - Tree structure
 * @param {string} path - File path to find
 * @returns {Object|null} File object or null if not found
 */
export const findFileInTree = (tree, path) => {
  for (const item of tree) {
    if (item.path === path) {
      return item;
    }
    if (item.type === 'folder' && item.children) {
      const found = findFileInTree(item.children, path);
      if (found) return found;
    }
  }
  return null;
};

/**
 * Flatten tree structure back to file map
 * @param {Array} tree - Tree structure
 * @returns {Object} File map with paths as keys
 */
export const treeToFiles = (tree) => {
  const files = {};
  
  const traverse = (items) => {
    items.forEach(item => {
      if (item.type === 'file') {
        files[item.path] = item.content || '';
      } else if (item.type === 'folder' && item.children) {
        traverse(item.children);
      }
    });
  };
  
  traverse(tree);
  return files;
};

