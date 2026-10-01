"use client";

import { FormEvent, useState } from "react";

import { useRouter } from "next/navigation";

import Link from "next/link";

import { routes } from "@/routes/routes";

import { register } from "@/api/auth";

import GoogleLoginButton from "@/components/auth/GoogleLoginButton";

import { useAuth } from "@/context/AuthContext";

import { useContent } from "@/hooks/content";

import "@/styles/pages/_register.scss";

export default function Register() {
  const router = useRouter();

  const { refreshUser } = useAuth();

  const { content, loading: contentLoading } = useContent();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (contentLoading || !content) {
    return null;
  }

  const registerContent = content.registerpage;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await register({
        name,
        email,
        password,
      });

      await refreshUser();

      router.push(routes.profile);
    } catch (error) {
      console.error("Registration failed:", error);

      setError(registerContent.registrationError);
    } finally {
      setLoading(false);
    }
  }

  function handleGoogleLoginSuccess() {
    router.push(routes.profile);
  }

  return (
    <main className="register-page">
      <section className="register-card">
        <h1>{registerContent.title}</h1>

        <form onSubmit={handleSubmit} className="register-form">
          <label htmlFor="name">{registerContent.nameLabel}</label>

          <input
            id="name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            autoComplete="name"
          />

          <label htmlFor="email">{registerContent.emailLabel}</label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            autoComplete="email"
          />

          <label htmlFor="password">{registerContent.passwordLabel}</label>

          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            minLength={8}
            autoComplete="new-password"
          />

          {error && <p className="register-error">{error}</p>}

          <button type="submit" className="register-button" disabled={loading}>
            {loading
              ? registerContent.loadingText
              : registerContent.registerButton}
          </button>
        </form>

        <div className="register-divider">
          <span>{registerContent.dividerText}</span>
        </div>

        <div className="google-register">
          <GoogleLoginButton onLoginSuccess={handleGoogleLoginSuccess} />
        </div>

        <p className="login-prompt">{registerContent.loginPrompt}</p>

        <Link href="/login" className="login-link">
          {registerContent.loginLink}
        </Link>
      </section>
    </main>
  );
}
