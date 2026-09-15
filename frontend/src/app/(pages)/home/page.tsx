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
      <header>
        <h1>{home.title}</h1>
        <h2>{home.subtitle}</h2>
      </header>

      <section aria-labelledby="home-description">
        <p>{home.description}</p>
      </section>

      <section aria-labelledby="home-opportunities">
        <p>{home.opportunitiesText}</p>
      </section>

      <section aria-labelledby="home-skills">
        <p>{home.skillsText}</p>
      </section>

      <section aria-labelledby="home-career">
        <p>{home.careerText}</p>
      </section>
    </main>
  );
}
