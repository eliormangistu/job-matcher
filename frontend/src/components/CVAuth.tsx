"use client";

import { useEffect, useState } from "react";

import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";

import CVMatcher from "./CVMatcher";

import { CONFIG } from "@/config";

import "../styles/components/cv/cv-auth.scss";
import { CVUploadData } from "@/types/cv";
import CVUpload from "./CVUpload";
import Loader from "./Loader";

export default function CVAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [result, setResult] = useState<CVUploadData | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    localStorage.removeItem("google_id_token");
    setIsAuthenticated(false);
  }, []);

  if (isAuthenticated) {
    if (result) {
      return <CVMatcher matches={result.matches} />;
    }

    if (isUploading) {
      return <Loader />;
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
      <main className="cv-auth">
        <section className="cv-auth-card">
          <h1>CV MATCHER</h1>

          <p className="cv-auth-subtitle">
            Match your skills with your next opportunity.
          </p>

          <div className="cv-auth-login">
            <GoogleLogin
              onSuccess={(credentialResponse) => {
                const token = credentialResponse.credential;

                if (!token) {
                  console.error("Google token is missing");
                  return;
                }

                localStorage.setItem("google_id_token", token);
                setIsAuthenticated(true);
              }}
              onError={() => {
                console.error("Google Login Failed");
              }}
            />
          </div>
        </section>
      </main>
    </GoogleOAuthProvider>
  );
}
