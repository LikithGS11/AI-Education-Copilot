/**
 * Modern File Preview component with premium markdown rendering
 */

import { useMemo, useEffect, useRef, memo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import python from 'highlight.js/lib/languages/python';
import javascript from 'highlight.js/lib/languages/javascript';
import json from 'highlight.js/lib/languages/json';
import markdown from 'highlight.js/lib/languages/markdown';
import bash from 'highlight.js/lib/languages/bash';
import xml from 'highlight.js/lib/languages/xml';
import css from 'highlight.js/lib/languages/css';
import { FileText, AlertTriangle, Eye } from 'lucide-react';
import 'highlight.js/styles/github.css';

const languageMap = {
  python,
  py: python,
  javascript,
  js: javascript,
  json,
  markdown,
  md: markdown,
  bash,
  sh: bash,
  shell: bash,
  html: xml,
  xml,
  css,
};

const FilePreview = ({ content, fileName, filePath }) => {
  const scrollContainerRef = useRef(null);

  // Reset scroll when file changes
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = 0;
    }
  }, [filePath]);

  const markdownContent = useMemo(() => {
    if (!content) {
      return null;
    }

    // Limit content size for performance (show warning for very large files)
    const MAX_CONTENT_LENGTH = 500000; // ~500KB
    if (typeof content === 'string' && content.length > MAX_CONTENT_LENGTH) {
      console.warn('[Preview] Large file detected, truncating for performance');
      return (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-3">
              <AlertTriangle className="w-6 h-6 text-amber-600" />
              <h3 className="text-lg font-semibold text-amber-800">Large File Detected</h3>
            </div>
            <p className="text-sm text-amber-700 leading-relaxed">
              This file is quite large ({Math.round(content.length / 1024)}KB).
              Showing the first {Math.round(MAX_CONTENT_LENGTH / 1024)}KB for optimal performance.
            </p>
          </div>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[[rehypeHighlight, { languages: languageMap, ignoreMissing: true }]]}
            className="prose prose-slate max-w-none"
          >
            {content.substring(0, MAX_CONTENT_LENGTH)}
          </ReactMarkdown>
        </div>
      );
    }

    try {
      return (
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[[rehypeHighlight, { languages: languageMap, ignoreMissing: true }]]}
          className="prose prose-slate max-w-none"
        >
          {content}
        </ReactMarkdown>
      );
    } catch (error) {
      console.error('[Preview] Markdown render error:', error);
      return (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-3">
              <AlertTriangle className="w-6 h-6 text-red-600" />
              <h3 className="text-lg font-semibold text-red-800">Render Error</h3>
            </div>
            <p className="text-sm text-red-700 leading-relaxed">
              Unable to render markdown content. Showing raw text below.
            </p>
          </div>
          <pre className="bg-slate-900 text-slate-100 rounded-2xl p-6 overflow-auto text-sm leading-relaxed shadow-soft">
            {content}
          </pre>
        </div>
      );
    }
  }, [content]);

  if (!content) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-500 bg-gradient-to-br from-slate-50 to-indigo-50 p-8">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto">
            <Eye className="w-8 h-8 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-700 mb-2">Preview Panel</h3>
            <p className="text-sm text-slate-500 max-w-xs">
              Select a file from the explorer to preview its content here.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (content === undefined || content === null || (typeof content === 'string' && content.trim() === '')) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-500 bg-gradient-to-br from-slate-50 to-indigo-50 p-8">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-br from-slate-100 to-slate-200 rounded-2xl flex items-center justify-center mx-auto">
            <FileText className="w-8 h-8 text-slate-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-700 mb-2">Empty File</h3>
            <p className="text-sm text-slate-500 max-w-xs">
              This file appears to be empty or contains no readable content.
            </p>
            {fileName && (
              <p className="text-xs text-slate-400 mt-2 font-mono">{fileName}</p>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-gradient-to-b from-white to-slate-50/30" ref={scrollContainerRef}>
      {/* Header */}
      <div className="sticky top-0 glass-effect border-b border-white/20 px-8 py-6 z-10 shadow-soft">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-glow">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <div>
            {fileName && (
              <h2 className="text-xl font-bold text-slate-800 truncate" title={filePath}>
                {fileName}
              </h2>
            )}
            <p className="text-sm text-slate-500 mt-1">
              File preview with syntax highlighting
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-8 max-w-4xl mx-auto">
        {markdownContent}
      </div>
    </div>
  );
};

export default memo(FilePreview);
