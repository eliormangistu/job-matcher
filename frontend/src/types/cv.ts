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

export interface CVResponse {
  id: number;
  user_id: number;
  filename: string;
  file_type: string;
  content: string | null;
  summary: string | null;
  skills: string[];
  job_titles: string[];
  years_of_experience: number | null;
  education: string[];
  languages: string[];
  industries: string[];
  created_at: string;
  updated_at: string;
}
