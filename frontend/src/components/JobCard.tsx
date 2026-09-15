"use client";

import { useContent } from "@/hooks/content";

import { JobCardProps } from "@/types/job";

import "@/styles/components/job/job-card.scss";

export default function JobCard({ job, onClick }: JobCardProps) {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const jobsContent = content.jobspage;

  return (
    <article className="job-card">
      <h3 className="job-card-title">{job.title}</h3>

      <p className="job-card-company">{job.company}</p>

      <div className="job-card-meta">
        {job.location?.join(", ") || jobsContent.locationNotSpecified}

        {" · "}

        {job.remote ? jobsContent.remote : jobsContent.onSite}

        {job.field && (
          <>
            {" · "}
            {job.field}
          </>
        )}

        {job.posted && (
          <>
            {" · "}
            {jobsContent.postedLabel}{" "}
            {new Date(job.posted).toLocaleDateString("en-GB")}
          </>
        )}

        {job.min_experience != null && (
          <>
            {" · "}
            {job.min_experience}+ {jobsContent.yearsSuffix}
          </>
        )}
      </div>

      {job.required_skills?.length > 0 && (
        <p className="job-card-skills">{job.required_skills.join(" · ")}</p>
      )}

      <button type="button" className="job-card-button" onClick={onClick}>
        {jobsContent.viewJobButton}
      </button>
    </article>
  );
}
