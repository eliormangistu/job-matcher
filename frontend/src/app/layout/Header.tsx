"use client";

import Link from "next/link";
import "@/styles/layout/header.scss";

export default function Header() {
  return (
    <header className="site-header">
      <Link href="/" className="logo">
        Job Matcher
      </Link>

      <nav className="main-nav">
        <Link href="/">Home</Link>
        <Link href="/jobs">Jobs</Link>
        <Link href="/cv">CV Matcher</Link>
      </nav>
    </header>
  );
}
