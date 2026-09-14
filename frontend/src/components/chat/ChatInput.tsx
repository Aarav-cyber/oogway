import React, { useState, useRef, useEffect } from 'react';
import { Send, CornerDownLeft } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [content, setContent] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [content]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const trimmed = content.trim();
    if (!trimmed || disabled) return;
    onSendMessage(trimmed);
    setContent('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="p-4 border-t border-slate-800 bg-slate-900/50 flex-shrink-0">
      <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto flex items-end bg-slate-900 border border-slate-800 focus-within:border-emerald-500/60 rounded-xl p-2 shadow-lg transition-all">
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about product, growth, retention, or request a Ship 30 essay..."
          rows={1}
          disabled={disabled}
          className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm px-3 py-1.5 focus:outline-none resize-none max-h-40 min-h-[38px] leading-relaxed"
        />

        <div className="flex items-center space-x-2 pl-2">
          <span className="hidden sm:inline-flex items-center text-[10px] text-slate-500 font-mono">
            <span>Shift + Enter</span>
            <CornerDownLeft className="w-3 h-3 ml-1" />
          </span>

          <button
            type="submit"
            disabled={!content.trim() || disabled}
            aria-label="Send message"
            className="w-9 h-9 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:hover:bg-emerald-600 text-white flex items-center justify-center transition-colors flex-shrink-0 shadow-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
