"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";

import { routes } from "@/routes/routes";
import { useAuth } from "@/context/AuthContext";
import { useContent } from "@/hooks/content";
import { handleEscape } from "@/utils/accessibility";
import { useRouter } from "next/navigation";

import DesktopNav from "@/components/navigation/DesktopNav";
import MobileNav from "@/components/navigation/MobileNav";

import "@/styles/layout/_header.scss";

export default function Header() {
  const router = useRouter();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);
  const mobileMenuRef = useRef<HTMLDivElement>(null);

  const { isAuthenticated, loading: authLoading, user, logout } = useAuth();
  const { content, loading } = useContent();

  useEffect(() => {
    function handleDocumentClick(event: MouseEvent) {
      const target = event.target as Node;

      if (userMenuRef.current && !userMenuRef.current.contains(target)) {
        setIsUserMenuOpen(false);
      }

      if (mobileMenuRef.current && !mobileMenuRef.current.contains(target)) {
        setIsMobileMenuOpen(false);
      }
    }

    function handleDocumentKeyDown(event: KeyboardEvent) {
      handleEscape(event, () => {
        setIsUserMenuOpen(false);
        setIsMobileMenuOpen(false);
      });
    }

    document.addEventListener("mousedown", handleDocumentClick);
    document.addEventListener("keydown", handleDocumentKeyDown);

    return () => {
      document.removeEventListener("mousedown", handleDocumentClick);
      document.removeEventListener("keydown", handleDocumentKeyDown);
    };
  }, []);

  if (loading || !content) {
    return null;
  }

  const header = content.header;

  async function handleLogout() {
    await logout();

    setIsUserMenuOpen(false);
    setIsMobileMenuOpen(false);

    router.push(routes.login);
  }

  return (
    <header className="site-header">
      <Link href={routes.home} className="logo">
        {header.logo}
      </Link>

      <DesktopNav
        header={header}
        isUserMenuOpen={isUserMenuOpen}
        setIsUserMenuOpen={setIsUserMenuOpen}
        isAuthenticated={isAuthenticated}
        authLoading={authLoading}
        user={user}
        onLogout={handleLogout}
        userMenuRef={userMenuRef}
      />

      <MobileNav
        header={header}
        isOpen={isMobileMenuOpen}
        setIsOpen={setIsMobileMenuOpen}
        isAuthenticated={isAuthenticated}
        authLoading={authLoading}
        onLogout={handleLogout}
        menuRef={mobileMenuRef}
      />
    </header>
  );
}
