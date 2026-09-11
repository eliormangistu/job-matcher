"use client";

import { JobCardProps } from "@/types/job";

import "@/styles/components/job/job-card.scss";

export default function JobCard({ job, onClick }: JobCardProps) {
  return (
    <article className="job-card">
      <h3 className="job-card-title">{job.title}</h3>

      <p className="job-card-company">{job.company}</p>

      <div className="job-card-meta">
        {job.location?.join(", ") || "Location not specified"}
        {" · "}
        {job.remote ? "Remote" : "On-site"}
        {job.field && (
          <>
            {" · "}
            {job.field}
          </>
        )}
        {job.posted && (
          <>
            {" · "}
            {new Date(job.posted).toLocaleDateString("en-GB")}
          </>
        )}
        {job.min_experience != null && (
          <>
            {" · "}
            {job.min_experience}+ years
          </>
        )}
      </div>

      {job.description && (
        <p className="job-card-description">{job.description}</p>
      )}

      {job.required_skills?.length > 0 && (
        <p className="job-card-skills">{job.required_skills.join(" · ")}</p>
      )}

      <button type="button" className="job-card-button" onClick={onClick}>
        View Job ↗
      </button>
    </article>
  );
}
