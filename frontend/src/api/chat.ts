import { apiClient } from './client';
import { ChatResponse, MessageCreatePayload } from '../types';

export const chatApi = {
  sendMessage: (sessionId: string, payload: MessageCreatePayload, provider?: string): Promise<ChatResponse> => {
    const query = provider ? `?provider=${encodeURIComponent(provider)}` : '';
    return apiClient.post<ChatResponse>(`/sessions/${sessionId}/messages${query}`, payload);
  },
};
