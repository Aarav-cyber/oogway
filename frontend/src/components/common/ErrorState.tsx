import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './Button';
import { CustomApiError } from '../../types';

interface ErrorStateProps {
  error: Error | CustomApiError | null;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  let title = 'Something went wrong';
  let message = 'An unexpected error occurred. Please try again.';
  let requestId: string | undefined = undefined;

  if (error instanceof CustomApiError) {
    requestId = error.requestId;
    if (error.code === 'NETWORK_ERROR') {
      title = 'Backend Service Unavailable';
      message = 'Unable to connect to the assistant backend. Please ensure the backend server is running.';
    } else if (error.code === 'LLM_UNAVAILABLE') {
      title = 'LLM Provider Unavailable';
      message = error.message || 'The configured LLM provider (Ollama/Anthropic/OpenAI) is not reachable.';
    } else if (error.code === 'SESSION_NOT_FOUND') {
      title = 'Session Not Found';
      message = 'The requested chat session could not be found.';
    } else {
      message = error.message;
    }
  } else if (error) {
    message = error.message;
  }

  return (
    <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-900/50 text-rose-200 my-3 flex items-start space-x-3">
      <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
      <div className="flex-1 text-sm">
        <h4 className="font-semibold text-rose-300 mb-1">{title}</h4>
        <p className="text-rose-200/90 leading-relaxed mb-2">{message}</p>
        {requestId && (
          <span className="text-xs font-mono text-rose-400/70 block mb-2">
            Request ID: {requestId}
          </span>
        )}
        {onRetry && (
          <Button
            size="sm"
            variant="outline"
            onClick={onRetry}
            className="border-rose-800 text-rose-200 hover:bg-rose-900/40"
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Try Again
          </Button>
        )}
      </div>
    </div>
  );
};
