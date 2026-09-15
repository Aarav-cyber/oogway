import { apiClient } from './client';

export interface LLMConfigResponse {
  provider: string;
  model: string;
}

export interface ReadyStatusResponse {
  status: string;
  database: string;
  llm: string;
  provider: string;
  model: string;
}

export const configApi = {
  getLLMConfig: (): Promise<LLMConfigResponse> => {
    return apiClient.get<LLMConfigResponse>('/config/llm');
  },

  switchLLM: (provider: string): Promise<LLMConfigResponse> => {
    return apiClient.post<LLMConfigResponse>('/config/llm', { provider });
  },

  getReadyStatus: (): Promise<ReadyStatusResponse> => {
    return apiClient.get<ReadyStatusResponse>('/ready');
  },
};
