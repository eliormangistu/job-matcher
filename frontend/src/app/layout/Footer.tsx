"use client";

import Image from "next/image";

import { useContent } from "@/hooks/content";

import "@/styles/layout/footer.scss";

export default function Footer() {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const footer = content.footer;

  return (
    <footer className="site-footer">
      <p>
        {footer.copyright}

        <Image src="/icon.svg" alt="" width={24} height={24} />
      </p>
    </footer>
  );
}
