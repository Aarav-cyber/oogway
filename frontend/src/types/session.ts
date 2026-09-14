export interface Session {
  id: string;
  user_id?: string | null;
  title?: string | null;
  created_at: string;
  updated_at: string;
}

export interface SessionListResponse {
  sessions: Session[];
}

export interface SessionCreatePayload {
  title?: string;
  user_id?: string;
}
