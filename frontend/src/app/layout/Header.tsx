"use client";

import Link from "next/link";

import { useContent } from "@/hooks/content";

import "@/styles/layout/header.scss";

export default function Header() {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const header = content.header;

  return (
    <header className="site-header">
      <Link href="/" className="logo">
        {header.logo}
      </Link>

      <nav className="main-nav">
        <Link href="/">{header.home}</Link>

        <Link href="/jobs">{header.jobs}</Link>

        <Link href="/cv">{header.cvMatcher}</Link>
      </nav>
    </header>
  );
}
