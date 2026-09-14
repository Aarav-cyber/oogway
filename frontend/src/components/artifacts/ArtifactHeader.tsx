import React from 'react';
import { Layers, Copy, Check, X, Code } from 'lucide-react';

interface ArtifactHeaderProps {
  title: string;
  type: 'markdown' | 'html';
  onClose: () => void;
  content: string;
}

export const ArtifactHeader: React.FC<ArtifactHeaderProps> = ({
  title,
  type,
  onClose,
  content,
}) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="h-14 px-4 border-b border-slate-800 bg-slate-900 flex items-center justify-between flex-shrink-0">
      <div className="flex items-center space-x-2.5 truncate">
        <div className="w-6 h-6 rounded-md bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
          {type === 'html' ? <Code className="w-3.5 h-3.5" /> : <Layers className="w-3.5 h-3.5" />}
        </div>
        <span className="font-semibold text-sm text-slate-100 truncate">{title}</span>
        <span className="text-[10px] font-mono uppercase bg-slate-800 border border-slate-700 text-slate-400 px-2 py-0.5 rounded flex-shrink-0">
          {type}
        </span>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={handleCopy}
          className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors text-xs flex items-center space-x-1"
          title="Copy content"
        >
          {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
        </button>

        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
          title="Close Artifact Viewer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
