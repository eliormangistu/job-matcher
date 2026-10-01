"use client";

import { GoogleLogin } from "@react-oauth/google";

import { googleLogin } from "@/api/auth";

interface GoogleLoginButtonProps {
  onLoginSuccess: () => void;
}

export default function GoogleLoginButton({
  onLoginSuccess,
}: GoogleLoginButtonProps) {
  return (
    <GoogleLogin
      onSuccess={async (credentialResponse) => {
        const credential = credentialResponse.credential;

        if (!credential) {
          console.error("Google token is missing");
          return;
        }

        try {
          await googleLogin(credential);
          onLoginSuccess();
        } catch (error) {
          console.error("Google Login Failed:", error);
        }
      }}
      onError={() => {
        console.error("Google Login Failed");
      }}
    />
  );
}
