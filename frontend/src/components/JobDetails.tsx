"use client";

import { Job } from "@/types/job";

import "@/styles/components/job/job-details.scss";

interface JobDetailsProps {
  job: Job;
  onClose: () => void;
}

export default function JobDetails({ job, onClose }: JobDetailsProps) {
  return (
    <div className="job-details-overlay">
      <article className="job-details">
        <button
          className="job-details-close"
          onClick={onClose}
          aria-label="Close"
        >
          ×
        </button>

        <h1>{job.title}</h1>

        <h2>{job.company}</h2>

        <p>
          <strong>Location:</strong>{" "}
          {job.location?.join(", ") || "Not specified"}
        </p>

        <p>
          <strong>Work mode:</strong> {job.remote ? "Remote" : "On-site"}
        </p>

        <p>
          <strong>Field:</strong> {job.field}
        </p>

        {job.min_experience != null && (
          <p>
            <strong>Min experience:</strong> {job.min_experience}+ of years
            experience
          </p>
        )}

        {job.posted && (
          <p>
            <strong>
              Posted: {new Date(job.posted).toLocaleDateString("en-GB")}
            </strong>
          </p>
        )}
        {job.description && (
          <section>
            <h3>About the role</h3>
            <p>{job.description}</p>
          </section>
        )}

        {job.requirements && (
          <section>
            {(() => {
              const [before, after] = job.requirements.split(/Requirements/i);

              return (
                <>
                  {before && <p>{before}</p>}

                  {after !== undefined && (
                    <>
                      <h3>Requirements</h3>
                      <p>{after}</p>
                    </>
                  )}
                </>
              );
            })()}
          </section>
        )}
        {job.required_skills?.length > 0 && (
          <section>
            <h3>Skills</h3>
            <p>{job.required_skills.join(" · ")}</p>
          </section>
        )}

        {job.url && (
          <a
            className="job-details-external-link"
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            View original job ↗
          </a>
        )}
      </article>
    </div>
  );
}
