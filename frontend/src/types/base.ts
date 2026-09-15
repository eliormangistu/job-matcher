export interface BaseResponse<T> {
  success: boolean;
  status_code: number;
  message: string;
  data: T;
}

export interface ErrorStateProps {
  title: string;
  message: string;
  retryLabel?: string;
  onRetry?: () => void;
}
