"use client";

import { GoogleLogin } from "@react-oauth/google";

export default function GoogleLoginButton() {
  return (
    <GoogleLogin
      onSuccess={(credentialResponse) => {
        if (credentialResponse.credential) {
          localStorage.setItem(
            "google_id_token",
            credentialResponse.credential,
          );

          window.location.reload();
        }
      }}
      onError={() => {
        console.error("Google Login Failed");
      }}
    />
  );
}
