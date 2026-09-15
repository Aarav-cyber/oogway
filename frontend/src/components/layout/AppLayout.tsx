import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { MobileNav } from './MobileNav';
import { Session } from '../../types';

interface AppLayoutProps {
  children: React.ReactNode;
  artifactComponent?: React.ReactNode;
  sessions: Session[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewChat: () => void;
  isCreatingSession: boolean;
  activeProvider: string;
  activeModel: string;
  onSelectProvider: (provider: string) => Promise<void>;
  isSwitchingProvider?: boolean;
  hasArtifact?: boolean;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  children,
  artifactComponent,
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  isCreatingSession,
  activeProvider,
  activeModel,
  onSelectProvider,
  isSwitchingProvider = false,
  hasArtifact = false,
}) => {
  const [isSidebarOpenMobile, setIsSidebarOpenMobile] = useState(false);
  const [isArtifactOpen, setIsArtifactOpen] = useState(true);
  const [mobileTab, setMobileTab] = useState<'chat' | 'artifact'>('chat');

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950 text-slate-100">
      <Header
        onToggleSidebar={() => setIsSidebarOpenMobile(!isSidebarOpenMobile)}
        activeProvider={activeProvider}
        activeModel={activeModel}
        onSelectProvider={onSelectProvider}
        isSwitchingProvider={isSwitchingProvider}
        isArtifactOpen={isArtifactOpen}
        onToggleArtifact={() => setIsArtifactOpen(!isArtifactOpen)}
        hasArtifact={hasArtifact}
      />

      <div className="flex-1 flex overflow-hidden relative">
        <Sidebar
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={onSelectSession}
          onNewChat={onNewChat}
          isCreating={isCreatingSession}
          isOpenMobile={isSidebarOpenMobile}
          onCloseMobile={() => setIsSidebarOpenMobile(false)}
        />

        {/* Main Content Area: Chat + Artifact Split View */}
        <main className="flex-1 flex overflow-hidden relative">
          {/* Chat Panel */}
          <div
            className={`flex-1 flex flex-col h-full overflow-hidden ${
              hasArtifact && mobileTab === 'artifact' ? 'hidden md:flex' : 'flex'
            }`}
          >
            {children}
          </div>

          {/* Artifact Side Panel (Desktop Split + Mobile Tab) */}
          {hasArtifact && artifactComponent && (
            <div
              className={`h-full border-l border-slate-800 bg-slate-900/90 flex flex-col overflow-hidden transition-all duration-300 ${
                mobileTab === 'artifact' ? 'w-full flex' : 'hidden'
              } ${isArtifactOpen ? 'md:flex md:w-[480px] lg:w-[600px]' : 'md:hidden'}`}
            >
              {artifactComponent}
            </div>
          )}
        </main>
      </div>

      <MobileNav
        activeTab={mobileTab}
        onTabChange={(tab) => setMobileTab(tab)}
        hasArtifact={hasArtifact}
      />
    </div>
  );
};
