"use client";

import { ContentProvider } from "@/context/ContentContext";

export default function Providers({ children }: { children: React.ReactNode }) {
  return <ContentProvider>{children}</ContentProvider>;
}
