export interface Job {
  id: number;
  title: string;
  company: string;
  location: string[] | null;
  remote: boolean;
  description: string | null;
  url: string | null;
  field: string | null;
  company_industry: string[] | null;
  min_experience: number | null;
  requirements: string | null;
  required_skills: string[];
  language_requirement: string[] | null;
  education_requirements: string | null;
  posted: string | null;
}

export interface JobsResponse {
  items: Job[];
  total: number;
}

export interface JobCardProps {
  job: Job;
  onClick: () => void;
  match?: {
    score: number;
    matched_skills: string[];
    missing_skills: string[];
  };
}

export interface JobDetailsProps {
  jobId: number;
}
