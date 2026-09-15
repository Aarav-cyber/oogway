import React, { useState, useRef, useEffect } from 'react';
import { Menu, Sparkles, Cpu, ChevronDown, Check, Layers, Loader2 } from 'lucide-react';
import { Button } from '../common/Button';

export interface ProviderOption {
  id: string;
  name: string;
  model: string;
}

export const PROVIDER_OPTIONS: ProviderOption[] = [
  { id: 'ollama', name: 'Ollama', model: 'llama3.2' },
  { id: 'groq', name: 'Groq', model: 'openai/gpt-oss-20b' },
  { id: 'gemini', name: 'Gemini', model: 'gemini-2.5-flash' },
];

interface HeaderProps {
  onToggleSidebar: () => void;
  activeProvider: string;
  activeModel: string;
  onSelectProvider: (provider: string) => Promise<void>;
  isSwitchingProvider?: boolean;
  isArtifactOpen: boolean;
  onToggleArtifact: () => void;
  hasArtifact: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  activeProvider,
  activeModel,
  onSelectProvider,
  isSwitchingProvider = false,
  isArtifactOpen,
  onToggleArtifact,
  hasArtifact,
}) => {
  const [isOpenDropdown, setIsOpenDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpenDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleProviderClick = async (providerId: string) => {
    if (providerId === activeProvider) {
      setIsOpenDropdown(false);
      return;
    }
    setIsOpenDropdown(false);
    await onSelectProvider(providerId);
  };

  const currentOption = PROVIDER_OPTIONS.find((p) => p.id === activeProvider.toLowerCase()) || {
    id: activeProvider,
    name: activeProvider,
    model: activeModel,
  };

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

      {/* Interactive LLM Selector Dropdown */}
      <div className="flex items-center space-x-3">
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsOpenDropdown(!isOpenDropdown)}
            disabled={isSwitchingProvider}
            aria-label="Select LLM provider"
            className="flex items-center space-x-2 text-xs font-mono bg-slate-800 hover:bg-slate-700/80 border border-slate-700 text-slate-200 px-3 py-1.5 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
          >
            {isSwitchingProvider ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-400" />
            ) : (
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            )}
            <Cpu className="w-3.5 h-3.5 text-emerald-400" />
            <span className="capitalize font-semibold">{currentOption.name}</span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400">{activeModel || currentOption.model}</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 ml-1" />
          </button>

          {/* Dropdown Menu */}
          {isOpenDropdown && (
            <div className="absolute right-0 mt-2 w-56 bg-slate-900 border border-slate-800 rounded-xl shadow-xl py-2 z-50 animate-fade-in">
              <div className="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500 border-b border-slate-800/80 mb-1">
                SELECT LLM
              </div>

              {PROVIDER_OPTIONS.map((opt) => {
                const isActive = opt.id === activeProvider.toLowerCase();
                return (
                  <button
                    key={opt.id}
                    onClick={() => handleProviderClick(opt.id)}
                    className={`w-full text-left px-3 py-2 flex items-center justify-between hover:bg-slate-800 transition-colors ${
                      isActive ? 'bg-slate-800/60 text-emerald-400 font-medium' : 'text-slate-300'
                    }`}
                  >
                    <div>
                      <div className="text-xs font-semibold capitalize flex items-center space-x-1.5">
                        <span>{opt.name}</span>
                      </div>
                      <div className="text-[11px] text-slate-500 font-mono mt-0.5">{opt.model}</div>
                    </div>
                    {isActive && <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />}
                  </button>
                );
              })}
            </div>
          )}
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
