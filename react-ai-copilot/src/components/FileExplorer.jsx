/**
 * Modern File Explorer component with premium VS Code-like design
 */

import { useState, useEffect, memo } from 'react';
import { ChevronRight, ChevronDown, File, Folder, FileText, Code, Image, Settings, BookOpen } from 'lucide-react';

const getFileIcon = (fileName) => {
  const ext = fileName.split('.').pop()?.toLowerCase();

  switch (ext) {
    case 'md':
      return <BookOpen className="w-4 h-4 text-blue-600" />;
    case 'py':
    case 'js':
    case 'jsx':
    case 'ts':
    case 'tsx':
    case 'java':
    case 'cpp':
    case 'c':
    case 'go':
    case 'rs':
      return <Code className="w-4 h-4 text-green-600" />;
    case 'json':
    case 'yaml':
    case 'yml':
      return <Settings className="w-4 h-4 text-purple-600" />;
    case 'png':
    case 'jpg':
    case 'jpeg':
    case 'gif':
    case 'svg':
      return <Image className="w-4 h-4 text-pink-600" />;
    case 'txt':
    case 'md':
      return <FileText className="w-4 h-4 text-slate-600" />;
    default:
      return <File className="w-4 h-4 text-slate-500" />;
  }
};

const FileItem = ({ item, level = 0, onFileClick, selectedPath }) => {
  const [expanded, setExpanded] = useState(item.expanded ?? true);
  const isSelected = selectedPath === item.path;

  // Update expanded state when item changes
  useEffect(() => {
    if (item.expanded !== undefined) {
      setExpanded(item.expanded);
    }
  }, [item.expanded]);

  const handleClick = (e) => {
    e.stopPropagation();
    if (item.type === 'folder') {
      setExpanded(!expanded);
    } else {
      if (item.content === undefined) {
        console.warn('[Explorer] File clicked but content is undefined:', item.path);
      }
      onFileClick(item);
    }
  };

  return (
    <div className="animate-fade-in-up">
      <div
        onClick={handleClick}
        className={`
          group flex items-center gap-2 px-3 py-2 cursor-pointer rounded-lg transition-all duration-200 hover:scale-[1.02]
          ${isSelected
            ? 'bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-900 shadow-sm border border-indigo-200'
            : 'text-slate-700 hover:bg-slate-50 hover:shadow-sm'
          }
        `}
        style={{ paddingLeft: `${level * 20 + 12}px` }}
        title={item.path}
      >
        {/* Expand/Collapse Icon */}
        {item.type === 'folder' && (
          <div className="w-4 h-4 flex items-center justify-center transition-transform duration-200">
            {expanded ? (
              <ChevronDown className="w-4 h-4 text-slate-500 group-hover:text-slate-700" />
            ) : (
              <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-slate-700" />
            )}
          </div>
        )}
        {item.type === 'file' && <div className="w-4 h-4" />}

        {/* File/Folder Icon */}
        {item.type === 'folder' ? (
          <Folder className={`w-4 h-4 transition-colors duration-200 ${
            expanded ? 'text-blue-600' : 'text-blue-500'
          }`} />
        ) : (
          getFileIcon(item.name)
        )}

        {/* File/Folder Name */}
        <span className={`text-sm font-medium truncate transition-colors duration-200 ${
          isSelected ? 'text-indigo-900' : 'text-slate-700 group-hover:text-slate-900'
        }`}>
          {item.name}
        </span>

        {/* Selection Indicator */}
        {isSelected && (
          <div className="ml-auto w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></div>
        )}
      </div>

      {/* Children */}
      {item.type === 'folder' && expanded && item.children && item.children.length > 0 && (
        <div className="transition-all duration-300 ease-in-out">
          {item.children.map((child) => (
            <FileItem
              key={child.path}
              item={child}
              level={level + 1}
              onFileClick={onFileClick}
              selectedPath={selectedPath}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const FileExplorer = ({ tree, onFileClick, selectedPath }) => {
  if (!tree || tree.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-500 bg-gradient-to-br from-slate-50 to-indigo-50 p-8">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto">
            <Folder className="w-8 h-8 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-700 mb-2">No Files Yet</h3>
            <p className="text-sm text-slate-500 max-w-xs">
              Generate a learning module to explore the file structure and preview content.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-auto h-full bg-gradient-to-b from-white to-slate-50/50 border-r border-slate-200/60">
      <div className="p-4 border-b border-slate-200/60 bg-white/80 backdrop-blur-sm">
        <h3 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
          <Folder className="w-4 h-4 text-indigo-600" />
          Module Files
          <span className="text-xs text-slate-500 font-normal ml-auto">
            {tree.reduce((acc, item) => acc + (item.type === 'file' ? 1 : 0), 0)} files
          </span>
        </h3>
      </div>
      <div className="p-2 space-y-1">
        {tree.map((item) => (
          <FileItem
            key={item.path}
            item={item}
            onFileClick={onFileClick}
            selectedPath={selectedPath}
          />
        ))}
      </div>
    </div>
  );
};

export default memo(FileExplorer);
