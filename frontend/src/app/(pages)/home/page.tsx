"use client";

import "@/styles/pages/home.scss";

import { useContent } from "@/hooks/content";

export default function HomePage() {
  const { content, loading, error } = useContent();

  if (loading) {
    return null;
  }

  if (error || !content) {
    return null;
  }

  const home = content.homepage;

  return (
    <main className="home-page">
      <h1>{home.title}</h1>

      <h2>{home.subtitle}</h2>

      <p>{home.description}</p>

      <p>{home.opportunitiesText}</p>

      <p>{home.skillsText}</p>

      <p>{home.careerText}</p>
    </main>
  );
}
