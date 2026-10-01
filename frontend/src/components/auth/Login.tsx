"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { login } from "@/api/auth";
import GoogleLoginButton from "@/components/auth/GoogleLoginButton";
import { useAuth } from "@/context/AuthContext";
import { routes } from "@/routes/routes";
import { useContent } from "@/hooks/content";

import "@/styles/pages/_login.scss";

export default function Login() {
  const router = useRouter();
  const { refreshUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { content, loading: contentLoading } = useContent();

  if (contentLoading || !content) {
    return null;
  }

  const loginContent = content.loginpage;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login({
        email,
        password,
      });

      await refreshUser();

      router.push(routes.profile);
    } catch (error) {
      console.error("Login failed:", error);
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  function handleGoogleLoginSuccess() {
    router.push(routes.profile);
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <h1>{loginContent.title}</h1>

        <form onSubmit={handleSubmit} className="login-form">
          <label htmlFor="email">{loginContent.emailLabel}</label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            autoComplete="email"
          />

          <label htmlFor="password">{loginContent.passwordLabel}</label>

          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            autoComplete="current-password"
          />

          {error && <p className="login-error">{error}</p>}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? loginContent.loadingText : loginContent.loginButton}
          </button>
        </form>

        <div className="login-divider">
          <span>{loginContent.dividerText}</span>
        </div>

        <div className="google-login">
          <GoogleLoginButton onLoginSuccess={handleGoogleLoginSuccess} />
        </div>

        <p className="register-prompt">{loginContent.registerPrompt}</p>

        <Link href="/register" className="register-link">
          {loginContent.registerLink}
        </Link>
      </section>
    </main>
  );
}
