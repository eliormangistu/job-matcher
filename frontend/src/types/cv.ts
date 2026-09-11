import { MatchResult } from "./match";

export interface CvCandidateProfile {
  summary: string | null;
  skills: string[];
  roles: string[];
  years_of_experience: number | null;
  education: string[];
  languages: string[];
  industries: string[];
}

export interface CVUploadData {
  filename: string;
  profile: CvCandidateProfile;
  matches: MatchResult[];
}

export interface CVUploadProps {
  onUploadStart: () => void;
  onUploadComplete: (result: CVUploadData) => void;
  onUploadError: () => void;
}
