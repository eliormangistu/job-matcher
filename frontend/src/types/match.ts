import { Job } from "./job";

export interface MatchResult {
  job_id: number;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  job: Job;
}

export interface MatchResultsProps {
  matches: MatchResult[];
}

export interface MatchListProps {
  matches: MatchResult[];
  onJobClick: (job: MatchResult["job"]) => void;
}

export interface MatchInfoProps {
  match: MatchResult;
}
