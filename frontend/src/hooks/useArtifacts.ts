import { useQuery } from '@tanstack/react-query';
import { artifactsApi } from '../api/artifacts';

export function useArtifact(artifactId: string | null) {
  return useQuery({
    queryKey: ['artifact', artifactId],
    queryFn: () => (artifactId ? artifactsApi.getArtifact(artifactId) : Promise.resolve(null)),
    enabled: !!artifactId,
    staleTime: 1000 * 60 * 10,
  });
}

export function useSessionArtifacts(sessionId: string | null) {
  return useQuery({
    queryKey: ['artifacts', sessionId],
    queryFn: () => (sessionId ? artifactsApi.listSessionArtifacts(sessionId) : Promise.resolve({ artifacts: [] })),
    enabled: !!sessionId,
  });
}
