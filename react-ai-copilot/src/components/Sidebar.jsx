/**
 * Modern Sidebar component with premium card-based design
 */

import { useState, memo } from 'react';
import { Send, Loader2, Sparkles, Lightbulb, Clock, Target } from 'lucide-react';

const Sidebar = ({ onGenerate, isGenerating = false }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || isGenerating) return;

    try {
      await onGenerate(prompt);
      setPrompt(''); // Clear input on success
    } catch (error) {
      // Error handling is done in App.jsx with toast
    }
  };

  const examplePrompts = [
    "RAG module, intermediate, 5 days",
    "Python basics, beginner, 3 days",
    "Cloud computing fundamentals, 2 days"
  ];

  return (
    <aside className="w-96 glass-effect shadow-soft border-r border-white/20 flex flex-col h-full animate-slide-in-left">
      {/* Header Section */}
      <div className="p-8 border-b border-white/20">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Generate Module</h2>
            <p className="text-sm text-slate-600 mt-1">
              Create comprehensive learning modules with AI
            </p>
          </div>
        </div>
      </div>

      {/* Main Form */}
      <form onSubmit={handleSubmit} className="flex-1 flex flex-col p-8">
        <div className="flex-1 flex flex-col space-y-6">
          {/* Prompt Input Card */}
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-soft border border-white/40">
            <label htmlFor="prompt" className="block text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <Target className="w-4 h-4 text-indigo-600" />
              Instructor Prompt
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your learning module..."
              className="w-full px-4 py-4 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none text-sm bg-white/80 backdrop-blur-sm transition-all duration-200 placeholder:text-slate-400"
              rows={6}
              disabled={isGenerating}
            />
            <div className="mt-3 text-xs text-slate-500 flex items-center gap-1">
              <Lightbulb className="w-3 h-3" />
              Be specific about topic, level, and duration
            </div>
          </div>

          {/* Example Prompts */}
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-100">
            <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              Example Prompts
            </h3>
            <div className="space-y-2">
              {examplePrompts.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setPrompt(example)}
                  disabled={isGenerating}
                  className="w-full text-left px-3 py-2 text-xs bg-white/60 hover:bg-white/80 rounded-lg border border-indigo-200 hover:border-indigo-300 transition-all duration-200 text-slate-600 hover:text-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <div className="mt-8">
          <button
            type="submit"
            disabled={!prompt.trim() || isGenerating}
            className={`
              w-full relative flex items-center justify-center gap-3 px-6 py-4 rounded-xl font-semibold text-sm transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] overflow-hidden
              ${!prompt.trim() || isGenerating
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white shadow-lg hover:shadow-xl hover:shadow-indigo-500/25'
              }
            `}
          >
            {/* Animated background */}
            {!isGenerating && prompt.trim() && (
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600 opacity-0 hover:opacity-100 transition-opacity duration-300 animate-glow"></div>
            )}

            <div className="relative z-10 flex items-center gap-3">
              {isGenerating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Generating Module...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Generate Module</span>
                </>
              )}
            </div>
          </button>

          {/* Status Indicator */}
          {isGenerating && (
            <div className="mt-4 flex items-center justify-center gap-2 text-sm text-slate-600">
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></div>
              <span>AI is creating your learning module...</span>
            </div>
          )}
        </div>
      </form>

      {/* Footer Tips */}
      <div className="p-8 border-t border-white/20 bg-gradient-to-t from-white/40 to-transparent">
        <div className="bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-white/40">
          <div className="flex items-center gap-2 mb-3">
            <Clock className="w-4 h-4 text-indigo-600" />
            <span className="text-sm font-semibold text-slate-700">Pro Tips</span>
          </div>
          <ul className="text-xs text-slate-600 space-y-2">
            <li className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full mt-1.5 flex-shrink-0"></div>
              Specify topic, difficulty level, and duration
            </li>
            <li className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full mt-1.5 flex-shrink-0"></div>
              Include specific learning objectives
            </li>
            <li className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full mt-1.5 flex-shrink-0"></div>
              Mention any special requirements or tools
            </li>
          </ul>
        </div>
      </div>
    </aside>
  );
};

export default memo(Sidebar);
