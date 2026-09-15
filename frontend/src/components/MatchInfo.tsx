"use client";

import { useContent } from "@/hooks/content";

import { MatchInfoProps } from "@/types/match";

import "@/styles/components/cv/match-info.scss";

export default function MatchInfo({ match }: MatchInfoProps) {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const matchContent = content.matchpage;

  return (
    <div className="match-info">
      <div className="match-score">
        <strong>{matchContent.matchLabel}</strong> {match.score}%
      </div>

      <div className="match-skills">
        <h4>{matchContent.matchedSkillsTitle}</h4>

        <p>
          {match.matched_skills.length > 0
            ? match.matched_skills.join(" · ")
            : matchContent.noneText}
        </p>
      </div>

      <div className="match-skills">
        <h4>{matchContent.missingSkillsTitle}</h4>

        <p>
          {match.missing_skills.length > 0
            ? match.missing_skills.join(" · ")
            : matchContent.noneText}
        </p>
      </div>
    </div>
  );
}
