import { ErrorStateProps } from "@/types/base";

import "@/styles/components/error/_error-state.scss";

export default function ErrorState({
  title,
  message,
  retryLabel = "Try again",
  onRetry,
}: ErrorStateProps) {
  return (
    <main className="error-page" aria-labelledby="error-title">
      <div className="error-page-card">
        <h1 id="error-title">{title}</h1>

        <p>{message}</p>

        {onRetry && (
          <button type="button" onClick={onRetry}>
            {retryLabel}
          </button>
        )}
      </div>
    </main>
  );
}
