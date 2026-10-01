"use client";

import { GoogleOAuthProvider } from "@react-oauth/google";

import { AuthProvider } from "@/context/AuthContext";
import { ContentProvider } from "@/context/ContentContext";
import { CONFIG } from "@/config";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <GoogleOAuthProvider clientId={CONFIG.cv.clientId}>
      <AuthProvider>
        <ContentProvider>{children}</ContentProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}
