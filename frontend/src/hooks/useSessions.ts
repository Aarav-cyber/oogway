import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sessionsApi } from '../api/sessions';
import { Session, SessionCreatePayload } from '../types';

export function useSessions() {
  const queryClient = useQueryClient();

  const sessionsQuery = useQuery({
    queryKey: ['sessions'],
    queryFn: () => sessionsApi.listSessions(),
    staleTime: 1000 * 60 * 5, // 5 mins
  });

  const createSessionMutation = useMutation({
    mutationFn: (payload?: SessionCreatePayload) => sessionsApi.createSession(payload),
    onSuccess: (newSession: Session) => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.setQueryData(['session', newSession.id], newSession);
      queryClient.setQueryData(['messages', newSession.id], []);
    },
  });

  return {
    sessions: sessionsQuery.data?.sessions || [],
    isLoading: sessionsQuery.isLoading,
    isError: sessionsQuery.isError,
    error: sessionsQuery.error,
    createSession: createSessionMutation.mutateAsync,
    isCreating: createSessionMutation.isPending,
  };
}

export function useSessionMessages(sessionId: string | null) {
  return useQuery({
    queryKey: ['messages', sessionId],
    queryFn: () => (sessionId ? sessionsApi.getSessionMessages(sessionId) : Promise.resolve([])),
    enabled: !!sessionId,
    staleTime: 1000 * 60,
  });
}
