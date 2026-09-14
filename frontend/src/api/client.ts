import { CustomApiError, ApiErrorResponse } from '../types/api';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorData: ApiErrorResponse | null = null;
    try {
      errorData = await response.json();
    } catch {
      // Failed to parse JSON error response
    }

    const code = errorData?.error?.code || 'UNKNOWN_ERROR';
    const message = errorData?.error?.message || `HTTP Error ${response.status}: ${response.statusText}`;
    const requestId = errorData?.error?.request_id;

    throw new CustomApiError(code, message, response.status, requestId);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const apiClient = {
  async get<T>(path: string, headers?: Record<string, string>): Promise<T> {
    try {
      const response = await fetch(`${BASE_URL}${path}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
      });
      return handleResponse<T>(response);
    } catch (err) {
      if (err instanceof CustomApiError) throw err;
      throw new CustomApiError(
        'NETWORK_ERROR',
        'Unable to connect to the backend server. Please make sure the backend is running.',
        0
      );
    }
  },

  async post<T>(path: string, body?: any, headers?: Record<string, string>): Promise<T> {
    try {
      const response = await fetch(`${BASE_URL}${path}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
        body: body ? JSON.stringify(body) : undefined,
      });
      return handleResponse<T>(response);
    } catch (err) {
      if (err instanceof CustomApiError) throw err;
      throw new CustomApiError(
        'NETWORK_ERROR',
        'Unable to connect to the backend server. Please make sure the backend is running.',
        0
      );
    }
  },
};
