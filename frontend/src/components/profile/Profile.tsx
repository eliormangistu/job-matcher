"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import CVMatcher from "@/components/cv/CVMatcher";
import Loader from "@/components/ui/Loader";
import Modal from "@/components/ui/Modal";

import { useAuth } from "@/context/AuthContext";
import { useContent } from "@/hooks/content";

import { routes } from "@/routes/routes";
import { MatchResult } from "@/types/match";
import { CVResponse } from "@/types/cv";

import { deleteAccount } from "@/api/user";
import { getCV, getCVMatches } from "@/api/cv";

import "@/styles/pages/_profile.scss";

export default function Profile() {
  const { user, logout } = useAuth();
  const { content, loading: contentLoading } = useContent();

  const [cv, setCV] = useState<CVResponse | null>(null);
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  useEffect(() => {
    async function loadProfile() {
      try {
        const [cvResponse, matchesResponse] = await Promise.all([
          getCV(),
          getCVMatches(),
        ]);

        setCV(cvResponse.data);
        setMatches(matchesResponse.data);
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  async function handleDeleteAccount() {
    await deleteAccount();
    await logout();
    window.location.href = routes.login;
  }

  if (loading || contentLoading || !content) {
    return null;
  }

  const profile = content.profilepage;

  return (
    <main className="profile-page">
      <section className="profile-header">
        <div>
          <p className="profile-eyebrow">{profile.profileEyebrow}</p>

          <h1>
            {profile.welcomeText}
            {user?.name ? `, ${user.name}` : ""}
          </h1>

          <p className="profile-subtitle">{profile.subtitle}</p>
        </div>
      </section>

      <section className="profile-info">
        <article className="profile-card">
          <p className="profile-eyebrow">{profile.accountEyebrow}</p>

          <h2>{profile.yourDetailsTitle}</h2>

          <div className="profile-details">
            <div>
              <span>{profile.nameLabel}</span>
              <strong>{user?.name || "—"}</strong>
            </div>

            <div>
              <span>{profile.emailLabel}</span>
              <strong>{user?.email || "—"}</strong>
            </div>
          </div>
        </article>

        <article className="profile-card">
          <p className="profile-eyebrow">{profile.cvEyebrow}</p>

          <h2>{profile.cvTitle}</h2>

          {cv ? (
            <>
              <p className="profile-card-text">{cv.filename}</p>

              <Link href={routes.cv} className="profile-cv-button">
                {profile.updateCVButton}
              </Link>
            </>
          ) : (
            <>
              <p className="profile-card-text">{profile.noCVText}</p>

              <Link href={routes.cv} className="profile-cv-button">
                {profile.uploadCVButton}
              </Link>
            </>
          )}
        </article>
      </section>

      <section className="profile-matches">
        <div className="profile-section-header">
          <div>
            <p className="profile-eyebrow">{profile.resultsEyebrow}</p>

            <h2>{profile.matchedJobsTitle}</h2>
          </div>

          <span className="profile-match-count">
            {matches.length} {profile.matchesLabel}
          </span>
        </div>

        {matches.length > 0 ? (
          <CVMatcher matches={matches} />
        ) : (
          <div className="profile-empty">
            <h3>{profile.noMatchesTitle}</h3>

            <p>{profile.noMatchesText}</p>

            <Link href={routes.cv} className="profile-cv-button">
              {profile.uploadCVButton}
            </Link>
          </div>
        )}
      </section>

      <section className="profile-danger-zone">
        <div>
          <p className="profile-eyebrow">{profile.dangerZoneEyebrow}</p>

          <h2>{profile.deleteAccountTitle}</h2>

          <p>{profile.deleteAccountMessage}</p>
        </div>

        <button
          type="button"
          className="profile-delete-button"
          onClick={() => setIsDeleteModalOpen(true)}
        >
          {profile.deleteAccountButton}
        </button>
      </section>

      <Modal
        isOpen={isDeleteModalOpen}
        title={profile.deleteModalTitle}
        message={profile.deleteModalMessage}
        confirmLabel={profile.deleteModalConfirm}
        cancelLabel={profile.deleteModalCancel}
        onCancel={() => setIsDeleteModalOpen(false)}
        onConfirm={handleDeleteAccount}
      />
    </main>
  );
}
