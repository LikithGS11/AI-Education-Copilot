/**
 * Modern Main App component with premium layout
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { generateModule, downloadModule } from './api/api';
import { filesToTree, findFileInTree } from './utils/tree';
import { useToast } from './components/Toast';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FileExplorer from './components/FileExplorer';
import FilePreview from './components/FilePreview';
import Loader from './components/Loader';

function App() {
  const { showSuccess, showError } = useToast();
  const [moduleData, setModuleData] = useState(null);
  const [tree, setTree] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState(null);
  const previewScrollRef = useRef(null);

  // Reset preview scroll when file changes
  useEffect(() => {
    if (previewScrollRef.current && selectedFile) {
      previewScrollRef.current.scrollTop = 0;
    }
  }, [selectedFile?.path]);

  const handleGenerate = useCallback(async (prompt) => {
    setIsGenerating(true);
    setError(null);
    setSelectedFile(null);
    setTree(null);
    setModuleData(null);

    try {
      console.log('[API] Generating module with prompt:', prompt);
      const response = await generateModule(prompt);

      console.log('[API] Response received:', {
        module_name: response.module_name,
        filesCount: response.files ? Object.keys(response.files).length : 0,
        files: response.files
      });

      const { module_name, files } = response;

      // Validate response
      if (!module_name) {
        throw new Error('Invalid response: missing module_name');
      }

      if (!files || typeof files !== 'object' || Object.keys(files).length === 0) {
        console.warn('[API] Empty files object received');
        setModuleData({ module_name, files: {} });
        setTree([]);
        showError('Module generated but no files were created. Please try again.');
        return;
      }

      // Convert files to tree structure
      console.log('[Tree] Converting files to tree structure...');
      const fileTree = filesToTree(files);
      console.log('[Tree] Tree conversion complete:', {
        rootItems: fileTree.length
      });

      setModuleData({ module_name, files });
      setTree(fileTree);

      // Auto-select first file if available (DFS)
      if (fileTree.length > 0) {
        const firstFile = findFirstFile(fileTree);
        if (firstFile) {
          console.log('[Selection] Auto-selecting first file:', firstFile.path);
          setSelectedFile(firstFile);
        } else {
          console.warn('[Selection] No files found in tree');
        }
      } else {
        console.warn('[Tree] Empty tree generated');
      }

      showSuccess('Module generated successfully!');
    } catch (err) {
      console.error('[Error] Generation failed:', err);
      const errorMessage = err.message || 'Failed to generate module. Check backend logs.';
      setError(errorMessage);
      showError(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  }, [showSuccess, showError]);


  const handleFileClick = useCallback((file) => {
    if (!file || !file.path) {
      console.warn('[Selection] Invalid file clicked:', file);
      showError('File not found');
      return;
    }

    // Verify file exists in tree
    if (tree) {
      const foundFile = findFileInTree(tree, file.path);
      if (foundFile) {
        console.log('[Selection] File selected:', file.path);
        setSelectedFile(foundFile);
      } else {
        console.warn('[Selection] File not found in tree:', file.path);
        showError('File not found');
      }
    } else {
      setSelectedFile(file);
    }
  }, [tree, showError]);

  const handleDownload = useCallback(async () => {
    if (!moduleData?.module_name) {
      showError('No module available to download');
      return;
    }

    setIsDownloading(true);
    setError(null);

    try {
      console.log('[Download] Starting download for module:', moduleData.module_name);
      await downloadModule(moduleData.module_name);
      console.log('[Download] Download completed successfully');
      showSuccess('ZIP downloaded successfully!');
    } catch (err) {
      console.error('[Download] Download failed:', err);
      let errorMessage = err.message || 'Could not download ZIP.';

      // Handle specific error cases
      if (errorMessage.includes('ZIP not found') || errorMessage.includes('404')) {
        errorMessage = 'ZIP not found. The module may not have been generated correctly.';
      } else if (errorMessage.includes('CORS')) {
        errorMessage = 'Network error. Please check if the backend is running.';
      }

      setError(errorMessage);
      showError(errorMessage);
    } finally {
      setIsDownloading(false);
    }
  }, [moduleData, showSuccess, showError]);

  // Helper to find first file in tree (DFS)
  const findFirstFile = useCallback((tree) => {
    for (const item of tree) {
      if (item.type === 'file') {
        return item;
      }
      if (item.type === 'folder' && item.children && item.children.length > 0) {
        const found = findFirstFile(item.children);
        if (found) return found;
      }
    }
    return null;
  }, []);

  return (
    <div className="h-screen flex flex-col gradient-bg">
      {/* Header */}
      <Header
        moduleName={moduleData?.module_name}
        onDownload={handleDownload}
        isDownloading={isDownloading}
        hasFiles={!!(moduleData?.files && Object.keys(moduleData.files).length > 0)}
        isGenerating={isGenerating}
      />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar onGenerate={handleGenerate} isGenerating={isGenerating} />

        {/* Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {isGenerating && (
            <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-md flex items-center justify-center z-50 animate-fade-in-up">
              <div className="bg-white/95 backdrop-blur-xl rounded-3xl p-12 shadow-2xl border border-white/20 max-w-lg mx-4">
                <div className="text-center space-y-6">
                  <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto shadow-glow animate-glow">
                    <Loader size="lg" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-800 mb-2">Generating Your Module</h3>
                    <p className="text-slate-600 leading-relaxed">
                      AI is creating comprehensive learning materials. This may take a few minutes...
                    </p>
                  </div>
                  <div className="flex justify-center">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          {error && !isGenerating ? (
            <div className="flex-1 flex items-center justify-center p-8">
              <div className="bg-gradient-to-br from-red-50 to-pink-50 border border-red-200 rounded-3xl p-8 max-w-lg shadow-soft">
                <div className="text-center space-y-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-rose-600 rounded-2xl flex items-center justify-center mx-auto">
                    <XCircle className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-red-800 mb-2">Generation Failed</h3>
                    <p className="text-red-700 leading-relaxed">{error}</p>
                  </div>
                  <div className="flex gap-3 justify-center">
                    <button
                      onClick={() => setError(null)}
                      className="px-6 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                    >
                      Dismiss
                    </button>
                    <button
                      onClick={() => {
                        setError(null);
                        // Could add retry logic here
                      }}
                      className="px-6 py-3 bg-slate-200 text-slate-700 rounded-xl hover:bg-slate-300 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex overflow-hidden">
              {/* File Explorer */}
              <div className="w-80 glass-effect shadow-soft border-r border-white/20 flex flex-col">
                <FileExplorer
                  tree={tree}
                  onFileClick={handleFileClick}
                  selectedPath={selectedFile?.path}
                />
              </div>

              {/* File Preview */}
              <div className="flex-1 flex flex-col overflow-hidden bg-white/50 backdrop-blur-sm" ref={previewScrollRef}>
                <FilePreview
                  content={selectedFile?.content}
                  fileName={selectedFile?.name}
                  filePath={selectedFile?.path}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
