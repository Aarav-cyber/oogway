import React from 'react';
import { Menu, Sparkles, Cpu, Layers } from 'lucide-react';
import { Button } from '../common/Button';

interface HeaderProps {
  onToggleSidebar: () => void;
  activeProvider?: string;
  activeModel?: string;
  isArtifactOpen: boolean;
  onToggleArtifact: () => void;
  hasArtifact: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  activeProvider = 'ollama',
  activeModel = 'llama3.2',
  isArtifactOpen,
  onToggleArtifact,
  hasArtifact,
}) => {
  return (
    <header className="h-14 border-b border-slate-800 bg-slate-900/80 backdrop-blur px-4 flex items-center justify-between flex-shrink-0 z-10">
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleSidebar}
          className="md:hidden p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg"
          aria-label="Open sidebar menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="font-semibold text-slate-100 text-sm tracking-tight hidden sm:inline">
            Lenny Growth Assistant
          </span>
        </div>
      </div>

      {/* Provider / Model Indicator */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-800/80 border border-slate-700/60 text-slate-300 px-3 py-1 rounded-full">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <Cpu className="w-3.5 h-3.5 text-emerald-400" />
          <span className="capitalize">{activeProvider}</span>
          <span className="text-slate-500">•</span>
          <span className="text-slate-400">{activeModel}</span>
        </div>

        {hasArtifact && (
          <Button
            size="sm"
            variant={isArtifactOpen ? 'primary' : 'outline'}
            onClick={onToggleArtifact}
            leftIcon={<Layers className="w-3.5 h-3.5" />}
          >
            {isArtifactOpen ? 'Hide Artifact' : 'View Artifact'}
          </Button>
        )}
      </div>
    </header>
  );
};
