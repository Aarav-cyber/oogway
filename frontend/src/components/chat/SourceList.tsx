import React from 'react';
import { ExternalLink, BookOpen } from 'lucide-react';
import { Source } from '../../types';

interface SourceListProps {
  sources: Source[];
}

export const SourceList: React.FC<SourceListProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-800/80">
      <div className="flex items-center space-x-1.5 text-xs font-semibold text-slate-400 mb-2">
        <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
        <span>TRANSCRIPT SOURCES ({sources.length})</span>
      </div>

      <div className="flex flex-wrap gap-2">
        {sources.map((src, idx) => (
          <div
            key={src.chunk_id || idx}
            className="group flex items-center space-x-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 rounded-lg px-3 py-1.5 text-xs transition-colors"
          >
            <span className="font-medium text-slate-200 truncate max-w-[220px]">
              {src.title}
            </span>
            {src.source_url ? (
              <a
                href={src.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 group-hover:text-emerald-400 transition-colors"
                title="Open Source"
              >
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
};
