"use client";

import { createContext, useEffect, useState, type ReactNode } from "react";

import { getContent } from "@/api/content";
import { Content, ContentContextValue } from "@/types/content";

export const ContentContext = createContext<ContentContextValue>({
  content: null,
  loading: true,
  error: false,
});

export function ContentProvider({ children }: { children: ReactNode }) {
  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function loadContent() {
      try {
        const response = await getContent();

        if (!response.success) {
          setError(true);
          return;
        }

        setContent(response.data);
      } catch {
        setError(true);
      } finally {
        setLoading(false);
      }
    }

    loadContent();
  }, []);

  return (
    <ContentContext.Provider
      value={{
        content,
        loading,
        error,
      }}
    >
      {children}
    </ContentContext.Provider>
  );
}
