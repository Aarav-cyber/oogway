export type MessageRole = 'user' | 'assistant' | 'system';

export interface Source {
  document_id: string;
  chunk_id: string;
  title: string;
  source_url?: string | null;
  episode_date?: string | null;
  snippet?: string | null;
}

export interface MessageMetadata {
  provider?: string;
  skill?: string;
  sources_count?: number;
  artifact_id?: string | null;
  [key: string]: any;
}

export interface Message {
  id: string;
  session_id: string;
  role: MessageRole;
  content: string;
  metadata?: MessageMetadata;
  created_at: string;
}

export interface ChatResponse {
  message: Message;
  sources: Source[];
  provider: string;
  model: string;
  skill: string;
  artifact_id?: string | null;
}

export interface MessageCreatePayload {
  content: string;
}
