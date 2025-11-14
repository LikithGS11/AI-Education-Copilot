/**
 * Modern Header component with premium design
 */

import { memo } from 'react';
import { Download, Loader2, Sparkles } from 'lucide-react';

const Header = ({ moduleName, onDownload, isDownloading = false, hasFiles = false, isGenerating = false }) => {
  const isDisabled = !moduleName || !hasFiles || isGenerating || isDownloading;

  return (
    <header className="glass-effect shadow-soft border-b border-white/20 px-8 py-6">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo and Title Section */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-glow">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
              AI Education Copilot
            </h1>
            {moduleName && (
              <p className="text-sm text-slate-500 mt-1 font-medium">
                Module: <span className="text-indigo-600 font-semibold">{moduleName}</span>
              </p>
            )}
          </div>
        </div>

        {/* Download Section */}
        {moduleName && (
          <div className="flex flex-col items-end gap-2">
            <button
              onClick={onDownload}
              disabled={isDisabled}
              className={`
                group relative flex items-center gap-3 px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-300 transform hover:scale-105 active:scale-95
                ${isDisabled
                  ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg hover:shadow-xl hover:from-indigo-700 hover:to-purple-700'
                }
              `}
              title={isDisabled ? 'Generate a module first to download' : 'Download module as ZIP file'}
            >
              {isDownloading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Downloading...</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5 group-hover:translate-y-0.5 transition-transform" />
                  <span>Download Module</span>
                </>
              )}

              {/* Subtle glow effect */}
              {!isDisabled && !isDownloading && (
                <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-600/20 to-purple-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10 blur-xl"></div>
              )}
            </button>

            {!isDownloading && (
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Ready to download</span>
              </div>
            )}
          </div>
        )}
      </div>
    </header>
  );
};

export default memo(Header);
