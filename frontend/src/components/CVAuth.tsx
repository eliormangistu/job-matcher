"use client";

import { useEffect, useState } from "react";

import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";

import CVMatcher from "./CVMatcher";

import { CONFIG } from "@/config";

import "../styles/components/cv/cv-auth.scss";

import { CVUploadData } from "@/types/cv";

import CVUpload from "./CVUpload";

import Loader from "./Loader";

import { useContent } from "@/hooks/content";

import { routes } from "@/routes/routes";

import { useRouter } from "next/navigation";

export default function CVAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [result, setResult] = useState<CVUploadData | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const { content, loading } = useContent();

  const router = useRouter();

  useEffect(() => {
    localStorage.removeItem("google_id_token");
    setIsAuthenticated(false);
  }, []);

  if (loading || !content) {
    return <Loader text={content?.loaderpage.loadingText} />;
  }

  const cvContent = content.cvpage;

  if (isAuthenticated) {
    if (result) {
      return <CVMatcher matches={result.matches} />;
    }

    if (isUploading) {
      return <Loader text={content.loaderpage.loadingText} />;
    }

    return (
      <CVUpload
        onUploadStart={() => setIsUploading(true)}
        onUploadError={() => setIsUploading(false)}
        onUploadComplete={(data) => {
          setResult(data);
          setIsUploading(false);
        }}
      />
    );
  }

  return (
    <GoogleOAuthProvider clientId={CONFIG.cv.clientId}>
      <section className="cv-auth" aria-labelledby="cv-auth-title">
        <div className="cv-auth-card">
          <h1 id="cv-auth-title">{cvContent.title}</h1>

          <p className="cv-auth-subtitle">{cvContent.subtitle}</p>

          <div className="cv-auth-login" aria-label="Google authentication">
            ```tsx
            <GoogleLogin
              onSuccess={(credentialResponse) => {
                const token = credentialResponse.credential;

                if (!token) {
                  console.error("Google token is missing");
                  router.push(routes.error);
                  return;
                }

                localStorage.setItem("google_id_token", token);
                setIsAuthenticated(true);
              }}
              onError={() => {
                console.error("Google Login Failed");
                router.push(routes.error);
              }}
            />
          </div>
        </div>
      </section>
    </GoogleOAuthProvider>
  );
}
