import { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from '../components/layout/AppLayout';
import { ChatWindow } from '../components/chat/ChatWindow';
import { ArtifactViewer } from '../components/artifacts/ArtifactViewer';
import { useSessions, useSessionMessages } from '../hooks/useSessions';
import { useChat } from '../hooks/useChat';
import { useArtifact } from '../hooks/useArtifacts';
import { apiClient } from '../api/client';
import { ReadinessResponse } from '../types/api';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function MainApp() {
  const { sessions, createSession, isCreating } = useSessions();
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);

  useEffect(() => {
    apiClient
      .get<ReadinessResponse>('/ready')
      .then(setReadiness)
      .catch((err) => {
        console.error('Failed to fetch backend readiness:', err);
      });
  }, []);

  // Auto-select first session or auto-create one if none exist
  useEffect(() => {
    if (sessions.length > 0 && !activeSessionId) {
      setActiveSessionId(sessions[0].id);
    }
  }, [sessions, activeSessionId]);

  const { data: messages = [], isLoading: isLoadingMessages } =
    useSessionMessages(activeSessionId);

  const {
    sendMessage,
    isSending,
    error,
    lastResponseSources,
    activeArtifactId,
    setActiveArtifactId,
  } = useChat();

  const { data: activeArtifact, isLoading: isLoadingArtifact } =
    useArtifact(activeArtifactId);

  const handleNewChat = async () => {
    try {
      const newSession = await createSession({ title: 'New Chat' });
      setActiveSessionId(newSession.id);
      setActiveArtifactId(null);
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  const handleSendMessage = async (content: string) => {
    let currentSessionId = activeSessionId;

    if (!currentSessionId) {
      const newSession = await createSession({
        title: content.slice(0, 30),
      });

      currentSessionId = newSession.id;
      setActiveSessionId(currentSessionId);
    }

    await sendMessage({
      sessionId: currentSessionId,
      content,
    });
  };

  return (
    <AppLayout
      sessions={sessions}
      activeSessionId={activeSessionId}
      onSelectSession={(id) => {
        setActiveSessionId(id);
        setActiveArtifactId(null);
      }}
      onNewChat={handleNewChat}
      isCreatingSession={isCreating}
      activeProvider={readiness?.provider || 'unknown'}
      activeModel={readiness?.model || 'unknown'}
      hasArtifact={!!activeArtifactId || isLoadingArtifact}
      artifactComponent={
        <ArtifactViewer
          artifact={activeArtifact || null}
          isLoading={isLoadingArtifact}
          onClose={() => setActiveArtifactId(null)}
        />
      }
    >
      <ChatWindow
        messages={messages}
        isLoadingMessages={isLoadingMessages}
        isSendingMessage={isSending}
        error={error}
        sourcesMap={lastResponseSources}
        onSendMessage={handleSendMessage}
        onOpenArtifact={(artId) => setActiveArtifactId(artId)}
      />
    </AppLayout>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MainApp />
    </QueryClientProvider>
  );
}