import { apiClient } from './client';
import { Session, SessionListResponse, SessionCreatePayload, Message } from '../types';

export const sessionsApi = {
  createSession: (payload?: SessionCreatePayload): Promise<Session> => {
    return apiClient.post<Session>('/sessions', payload || {});
  },

  listSessions: (userId?: string): Promise<SessionListResponse> => {
    const query = userId ? `?user_id=${encodeURIComponent(userId)}` : '';
    return apiClient.get<SessionListResponse>(`/sessions${query}`);
  },

  getSession: (sessionId: string): Promise<Session> => {
    return apiClient.get<Session>(`/sessions/${sessionId}`);
  },

  getSessionMessages: (sessionId: string): Promise<Message[]> => {
    return apiClient.get<Message[]>(`/sessions/${sessionId}/messages`);
  },
};
