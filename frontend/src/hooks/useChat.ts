import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { chatApi } from '../api/chat';
import { ChatResponse, Message, Source } from '../types';

interface SendMessageArgs {
  sessionId: string;
  content: string;
  provider?: string;
}

export function useChat() {
  const queryClient = useQueryClient();
  const [lastResponseSources, setLastResponseSources] = useState<Record<string, Source[]>>({});
  const [activeArtifactId, setActiveArtifactId] = useState<string | null>(null);

  const sendMessageMutation = useMutation({
    mutationFn: ({ sessionId, content, provider }: SendMessageArgs) =>
      chatApi.sendMessage(sessionId, { content }, provider),

    onMutate: async ({ sessionId, content }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['messages', sessionId] });

      const previousMessages = queryClient.getQueryData<Message[]>(['messages', sessionId]) || [];

      // Optimistically add user message
      const tempUserMessage: Message = {
        id: `temp-${Date.now()}`,
        session_id: sessionId,
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };

      queryClient.setQueryData<Message[]>(['messages', sessionId], [
        ...previousMessages,
        tempUserMessage,
      ]);

      return { previousMessages };
    },

    onError: (_err, { sessionId }, context) => {
      if (context?.previousMessages) {
        queryClient.setQueryData(['messages', sessionId], context.previousMessages);
      }
    },

    onSuccess: (data: ChatResponse, { sessionId }) => {
      // Refresh messages and sessions list
      queryClient.invalidateQueries({ queryKey: ['messages', sessionId] });
      queryClient.invalidateQueries({ queryKey: ['sessions'] });

      // Save sources for this response message
      if (data.sources && data.sources.length > 0) {
        setLastResponseSources((prev) => ({
          ...prev,
          [data.message.id]: data.sources,
        }));
      }

      // If response generated an artifact, set it active
      if (data.artifact_id) {
        setActiveArtifactId(data.artifact_id);
        queryClient.invalidateQueries({ queryKey: ['artifacts', sessionId] });
      }
    },
  });

  return {
    sendMessage: sendMessageMutation.mutateAsync,
    isSending: sendMessageMutation.isPending,
    error: sendMessageMutation.error,
    lastResponseSources,
    activeArtifactId,
    setActiveArtifactId,
  };
}
