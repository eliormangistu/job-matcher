"use client";

import { RefObject } from "react";
import Link from "next/link";

import { routes } from "@/routes/routes";

import { MobileNavProps } from "@/types/navbar";

export default function MobileNav({
  header,
  isOpen,
  setIsOpen,
  isAuthenticated,
  authLoading,
  onLogout,
  menuRef,
}: MobileNavProps) {
  return (
    <>
      <div ref={menuRef}>
        <button
          type="button"
          className="mobile-menu-button"
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={isOpen}
        >
          ☰
        </button>

        {isOpen && (
          <nav className="mobile-nav" aria-label="Mobile navigation">
            <Link
              href={routes.home}
              className="mobile-nav-button"
              onClick={() => setIsOpen(false)}
            >
              {header.home}
            </Link>

            <Link
              href={routes.jobs}
              className="mobile-nav-button"
              onClick={() => setIsOpen(false)}
            >
              {header.jobs}
            </Link>

            <Link
              href={routes.cv}
              className="mobile-nav-button"
              onClick={() => setIsOpen(false)}
            >
              {header.cvMatcher}
            </Link>

            {!authLoading && isAuthenticated ? (
              <>
                <Link
                  href={routes.profile}
                  className="mobile-nav-link"
                  onClick={() => setIsOpen(false)}
                >
                  Profile
                </Link>

                <button
                  type="button"
                  className="mobile-nav-link"
                  onClick={onLogout}
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                href={routes.login}
                className="mobile-nav-link"
                onClick={() => setIsOpen(false)}
              >
                Log in
              </Link>
            )}
          </nav>
        )}
      </div>
    </>
  );
}
