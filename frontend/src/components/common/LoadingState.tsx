import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-slate-400 space-y-3">
      <Loader2 className="w-6 h-6 animate-spin text-emerald-500" />
      <span className="text-sm font-medium">{message}</span>
    </div>
  );
};
