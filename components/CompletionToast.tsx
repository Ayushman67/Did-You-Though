'use client';

import { useEffect } from 'react';
import { useStore } from '@/lib/store';
import { CheckCircle, X } from 'lucide-react';

export default function CompletionToast() {
  const { justCompleted, clearJustCompleted } = useStore();

  useEffect(() => {
    if (justCompleted) {
      const timer = setTimeout(clearJustCompleted, 3000);
      return () => clearTimeout(timer);
    }
  }, [justCompleted, clearJustCompleted]);

  if (!justCompleted) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-slide-up">
      <div className="flex items-center gap-3 px-4 py-3 bg-surface rounded-xl shadow-lg border border-success/20 max-w-sm">
        <div className="w-8 h-8 rounded-full bg-success-light flex items-center justify-center flex-shrink-0">
          <CheckCircle className="w-4 h-4 text-success" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-success">Task completed!</p>
          <p className="text-xs text-text-muted truncate">{justCompleted}</p>
        </div>
        <button
          onClick={clearJustCompleted}
          className="p-1 rounded-md hover:bg-gray-100 transition-colors"
        >
          <X className="w-4 h-4 text-text-muted" />
        </button>
      </div>
    </div>
  );
}
