export type ArtifactType = 'markdown' | 'html';

export interface Artifact {
  id: string;
  session_id: string;
  message_id?: string | null;
  title: string;
  type: ArtifactType;
  content: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ArtifactListResponse {
  artifacts: Artifact[];
}

export interface ArtifactCreatePayload {
  title?: string;
  type: ArtifactType;
  content: string;
  message_id?: string;
}
