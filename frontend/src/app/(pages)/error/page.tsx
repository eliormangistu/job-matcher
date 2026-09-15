"use client";

import ErrorState from "@/components/ErrorState";

import { useContent } from "@/hooks/content";

export default function ErrorPage() {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const error = content.errorpage;

  return (
    <ErrorState
      title={error.title}
      message={error.message}
      retryLabel={error.retryLabel}
    />
  );
}
