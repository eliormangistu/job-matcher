import { ErrorStateProps } from "@/types/base";

import "@/styles/components/error/error-state.scss";

export default function ErrorState({
  title,
  message,
  onRetry,
}: ErrorStateProps) {
  return (
    <main className="error-page">
      <section className="error-page-card">
        <h1>{title}</h1>

        <p>{message}</p>

        {onRetry && (
          <button type="button" onClick={onRetry}>
            Try again
          </button>
        )}
      </section>
    </main>
  );
}
