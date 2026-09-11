import { ErrorStateProps } from "@/types/base";

export class ApiError extends Error {
  statusCode: number;

  constructor(statusCode: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
  }
}

export function setErrorState({ title, message }: ErrorStateProps) {
  sessionStorage.setItem(
    "error_state",
    JSON.stringify({
      title,
      message,
    }),
  );
}
