export interface ApiErrorDetail {
  code: string;
  message: string;
  request_id?: string;
}

export interface ApiErrorResponse {
  error: ApiErrorDetail;
}

export class CustomApiError extends Error {
  code: string;
  requestId?: string;
  status: number;

  constructor(code: string, message: string, status: number, requestId?: string) {
    super(message);
    this.name = 'CustomApiError';
    this.code = code;
    this.status = status;
    this.requestId = requestId;
  }
}

export interface ReadinessResponse {
  status: string;
  database: string;
  llm: string;
  provider: string;
  model: string;
}