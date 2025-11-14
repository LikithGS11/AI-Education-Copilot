/**
 * Premium Toast notification component with modern design
 */

import { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { X, CheckCircle, XCircle, AlertCircle, Info } from 'lucide-react';

const ToastContext = createContext(null);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

const Toast = ({ id, message, type, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(id);
    }, type === 'error' ? 6000 : 4000);

    return () => clearTimeout(timer);
  }, [id, type, onClose]);

  const getToastStyles = () => {
    switch (type) {
      case 'success':
        return {
          bg: 'bg-gradient-to-r from-emerald-500 to-green-600',
          icon: CheckCircle,
          glow: 'shadow-emerald-500/25'
        };
      case 'error':
        return {
          bg: 'bg-gradient-to-r from-red-500 to-rose-600',
          icon: XCircle,
          glow: 'shadow-red-500/25'
        };
      case 'warning':
        return {
          bg: 'bg-gradient-to-r from-amber-500 to-orange-600',
          icon: AlertCircle,
          glow: 'shadow-amber-500/25'
        };
      default:
        return {
          bg: 'bg-gradient-to-r from-blue-500 to-indigo-600',
          icon: Info,
          glow: 'shadow-blue-500/25'
        };
    }
  };

  const { bg, icon: Icon, glow } = getToastStyles();

  return (
    <div
      className={`${bg} text-white px-6 py-4 rounded-2xl shadow-xl ${glow} flex items-center gap-4 min-w-[320px] max-w-md animate-scale-in border border-white/20 backdrop-blur-sm`}
    >
      <div className="flex-shrink-0">
        <Icon className="w-6 h-6" />
      </div>
      <p className="flex-1 text-sm font-medium leading-relaxed">{message}</p>
      <button
        onClick={() => onClose(id)}
        className="flex-shrink-0 hover:bg-white/20 transition-colors duration-200 p-1 rounded-lg group"
        aria-label="Close notification"
      >
        <X className="w-4 h-4 group-hover:scale-110 transition-transform duration-200" />
      </button>

      {/* Progress bar */}
      <div className="absolute bottom-0 left-0 h-1 bg-white/30 rounded-b-2xl">
        <div
          className="h-full bg-white/60 rounded-b-2xl animate-pulse"
          style={{
            animation: `shrink ${type === 'error' ? 6 : 4}s linear forwards`
          }}
        />
      </div>
    </div>
  );
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const showSuccess = useCallback((message) => {
    return showToast(message, 'success');
  }, [showToast]);

  const showError = useCallback((message) => {
    return showToast(message, 'error');
  }, [showToast]);

  const showWarning = useCallback((message) => {
    return showToast(message, 'warning');
  }, [showToast]);

  const showInfo = useCallback((message) => {
    return showToast(message, 'info');
  }, [showToast]);

  return (
    <ToastContext.Provider value={{ showSuccess, showError, showWarning, showInfo }}>
      {children}
      <div className="fixed top-6 right-6 z-50 flex flex-col gap-3 pointer-events-none">
        {toasts.map((toast) => (
          <div key={toast.id} className="pointer-events-auto">
            <Toast
              id={toast.id}
              message={toast.message}
              type={toast.type}
              onClose={removeToast}
            />
          </div>
        ))}
      </div>

      <style jsx>{`
        @keyframes shrink {
          from { width: 100%; }
          to { width: 0%; }
        }
      `}</style>
    </ToastContext.Provider>
  );
};
