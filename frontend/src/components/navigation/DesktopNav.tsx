"use client";

import { RefObject } from "react";
import Image from "next/image";
import Link from "next/link";

import userIcon from "@/assets/images/red-yellow-flower.png";
import { routes } from "@/routes/routes";

import { DesktopNavProps } from "@/types/navbar";

export default function DesktopNav({
  header,
  isUserMenuOpen,
  setIsUserMenuOpen,
  isAuthenticated,
  authLoading,
  user,
  onLogout,
  userMenuRef,
}: DesktopNavProps) {
  return (
    <nav className="main-nav desktop-nav" aria-label="Main navigation">
      <Link href={routes.home}>{header.home}</Link>

      <Link href={routes.jobs}>{header.jobs}</Link>

      <Link href={routes.cv}>{header.cvMatcher}</Link>

      <div className="user-menu" ref={userMenuRef}>
        <button
          type="button"
          className="user-icon-button"
          onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
          aria-label="Open user menu"
          aria-expanded={isUserMenuOpen}
        >
          <Image src={userIcon} alt="User" width={24} height={24} />
        </button>

        {isUserMenuOpen && (
          <div className="user-dropdown">
            {!authLoading && isAuthenticated ? (
              <>
                <div className="user-email">{user?.email}</div>

                <Link
                  href={routes.profile}
                  className="profile-link"
                  onClick={() => setIsUserMenuOpen(false)}
                >
                  Profile
                </Link>

                <button
                  type="button"
                  className="logout-button"
                  onClick={onLogout}
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                href={routes.login}
                className="user-login"
                onClick={() => setIsUserMenuOpen(false)}
              >
                Log in
              </Link>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
