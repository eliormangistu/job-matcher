"use client";

import { useEffect, useState } from "react";

import CVMatcher from "@/components/cv/CVMatcher";
import "@/styles/components/cv/_cv-auth.scss";

import { CVUploadData } from "@/types/cv";
import CVUpload from "@/components/cv/CVUpload";
import Loader from "@/components/ui/Loader";
import { useContent } from "@/hooks/content";
import GoogleLoginButton from "@/components/auth/GoogleLoginButton";
import { useAuth } from "@/context/AuthContext";
import { getCVMatches } from "@/api/cv";

export default function CVAuth() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [result, setResult] = useState<CVUploadData | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const { content, loading } = useContent();

  useEffect(() => {
    if (!isAuthenticated) {
      return;
    }

    getCVMatches()
      .then((response) => {
        if (response.data.length === 0) {
          return;
        }

        setResult({
          filename: "",
          profile: {
            summary: null,
            skills: [],
            roles: [],
            years_of_experience: null,
            education: [],
            languages: [],
            industries: [],
          },
          matches: response.data,
        });
      })
      .catch(() => {
        setResult(null);
      });
  }, [isAuthenticated]);

  if (loading || !content) {
    return <Loader text={content?.loaderpage.loadingText} />;
  }

  const cvContent = content.cvpage;

  if (authLoading) {
    return <Loader text={content.loaderpage.loadingText} />;
  }

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
    <main className="cv-auth" aria-labelledby="cv-auth-title">
      <div className="cv-auth-card">
        <h1 id="cv-auth-title">{cvContent.title}</h1>

        <p className="cv-auth-subtitle">{cvContent.subtitle}</p>

        <div className="cv-auth-login" aria-label="Google authentication">
          <GoogleLoginButton onLoginSuccess={() => window.location.reload()} />
        </div>
      </div>
    </main>
  );
}
