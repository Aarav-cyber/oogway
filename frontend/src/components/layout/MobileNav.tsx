import React from 'react';
import { Layers, MessageSquare } from 'lucide-react';
import { clsx } from 'clsx';

interface MobileNavProps {
  activeTab: 'chat' | 'artifact';
  onTabChange: (tab: 'chat' | 'artifact') => void;
  hasArtifact: boolean;
}

export const MobileNav: React.FC<MobileNavProps> = ({ activeTab, onTabChange, hasArtifact }) => {
  if (!hasArtifact) return null;

  return (
    <div className="md:hidden h-12 border-t border-slate-800 bg-slate-900 flex items-center justify-around flex-shrink-0 z-10">
      <button
        onClick={() => onTabChange('chat')}
        className={clsx(
          'flex items-center space-x-2 text-xs font-medium py-2 px-4 rounded-lg transition-colors',
          activeTab === 'chat' ? 'text-emerald-400 bg-slate-800' : 'text-slate-400 hover:text-slate-200'
        )}
      >
        <MessageSquare className="w-4 h-4" />
        <span>Chat</span>
      </button>

      <button
        onClick={() => onTabChange('artifact')}
        className={clsx(
          'flex items-center space-x-2 text-xs font-medium py-2 px-4 rounded-lg transition-colors',
          activeTab === 'artifact' ? 'text-emerald-400 bg-slate-800' : 'text-slate-400 hover:text-slate-200'
        )}
      >
        <Layers className="w-4 h-4" />
        <span>Artifact</span>
      </button>
    </div>
  );
};
