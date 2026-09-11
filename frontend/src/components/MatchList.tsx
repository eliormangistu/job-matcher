import { MatchListProps } from "@/types/match";

import JobCard from "./JobCard";
import MatchInfo from "./MatchInfo";

// import "@/styles/match-list.css";

export default function MatchList({ matches, onJobClick }: MatchListProps) {
  return (
    <div className="match-list">
      {matches.map((match) => (
        <div className="match-item" key={match.job_id}>
          <MatchInfo match={match} />

          <JobCard job={match.job} onClick={() => onJobClick(match.job)} />
        </div>
      ))}
    </div>
  );
}
