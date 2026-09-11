"use client";

import { MatchResult } from "@/types/match";

import "@/styles/components/cv/match-info.scss";

interface MatchInfoProps {
  match: MatchResult;
}

export default function MatchInfo({ match }: MatchInfoProps) {
  return (
    <div className="match-info">
      <div className="match-score">
        <strong>Match:</strong> {match.score}%
      </div>

      <div className="match-skills">
        <h4>Matched skills</h4>
        <p>
          {match.matched_skills.length > 0
            ? match.matched_skills.join(" · ")
            : "None"}
        </p>
      </div>

      <div className="match-skills">
        <h4>Missing skills</h4>
        <p>
          {match.missing_skills.length > 0
            ? match.missing_skills.join(" · ")
            : "None"}
        </p>
      </div>
    </div>
  );
}
