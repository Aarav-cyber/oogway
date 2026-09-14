import React from 'react';
import { Plus, MessageSquare, Sparkles, X } from 'lucide-react';
import { Button } from '../common/Button';
import { Session } from '../../types';
import { clsx } from 'clsx';

interface SidebarProps {
  sessions: Session[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewChat: () => void;
  isCreating: boolean;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  isCreating,
  isOpenMobile,
  onCloseMobile,
}) => {
  const content = (
    <div className="flex flex-col h-full bg-slate-900 border-r border-slate-800 w-64 flex-shrink-0">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 rounded-md bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <Sparkles className="w-3.5 h-3.5" />
          </div>
          <span className="font-bold text-slate-100 text-sm tracking-wide">LENNY ASSISTANT</span>
        </div>
        <button
          onClick={onCloseMobile}
          className="md:hidden text-slate-400 hover:text-slate-200 p-1"
          aria-label="Close sidebar"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <Button
          onClick={onNewChat}
          isLoading={isCreating}
          className="w-full justify-start"
          leftIcon={<Plus className="w-4 h-4" />}
        >
          New Chat
        </Button>
      </div>

      {/* Recent Sessions List */}
      <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
        <div className="px-2 py-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Recent Chats
        </div>

        {sessions.length === 0 ? (
          <div className="px-3 py-4 text-xs text-slate-500 text-center">
            No previous chats
          </div>
        ) : (
          sessions.map((session) => {
            const isActive = session.id === activeSessionId;
            return (
              <button
                key={session.id}
                onClick={() => {
                  onSelectSession(session.id);
                  onCloseMobile();
                }}
                className={clsx(
                  'w-full flex items-center space-x-2.5 px-3 py-2 rounded-lg text-left text-xs transition-colors duration-150',
                  isActive
                    ? 'bg-slate-800 text-emerald-400 font-medium border border-slate-700/80 shadow-sm'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                )}
              >
                <MessageSquare className={clsx('w-3.5 h-3.5 flex-shrink-0', isActive ? 'text-emerald-400' : 'text-slate-500')} />
                <span className="truncate">{session.title || 'Untitled Chat'}</span>
              </button>
            );
          })
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:block h-full">{content}</aside>

      {/* Mobile Drawer */}
      {isOpenMobile && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm" onClick={onCloseMobile} />
          <div className="relative z-10">{content}</div>
        </div>
      )}
    </>
  );
};
