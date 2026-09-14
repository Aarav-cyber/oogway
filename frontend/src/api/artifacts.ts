import { apiClient } from './client';
import { Artifact, ArtifactListResponse, ArtifactCreatePayload } from '../types';

export const artifactsApi = {
  createArtifact: (sessionId: string, payload: ArtifactCreatePayload): Promise<Artifact> => {
    return apiClient.post<Artifact>(`/artifacts?session_id=${encodeURIComponent(sessionId)}`, payload);
  },

  getArtifact: (artifactId: string): Promise<Artifact> => {
    return apiClient.get<Artifact>(`/artifacts/${artifactId}`);
  },

  listSessionArtifacts: (sessionId: string): Promise<ArtifactListResponse> => {
    return apiClient.get<ArtifactListResponse>(`/artifacts/session/${sessionId}`);
  },
};
