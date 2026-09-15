"use client";

import { useContent } from "@/hooks/content";

import { JobDetailsProps } from "@/types/job";

import { useEffect, useRef } from "react";

import { handleDialogKeyDown } from "@/utils/accessibility";

import "@/styles/components/job/job-details.scss";

export default function JobDetails({ job, onClose }: JobDetailsProps) {
  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const jobsContent = content.jobspage;

  const dialogRef = useRef<HTMLElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const previousActiveElement = document.activeElement as HTMLElement | null;

    closeButtonRef.current?.focus();

    function handleKeyDown(event: KeyboardEvent) {
      const dialog = dialogRef.current;

      if (!dialog) {
        return;
      }

      handleDialogKeyDown(event, dialog, onClose);
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);

      previousActiveElement?.focus();
    };
  }, [onClose]);

  return (
    <div className="job-details-overlay" role="presentation">
      <article
        ref={dialogRef}
        className="job-details"
        role="dialog"
        aria-modal="true"
        aria-labelledby="job-details-title"
        tabIndex={-1}
      >
        <button
          ref={closeButtonRef}
          type="button"
          className="job-details-close"
          onClick={onClose}
          aria-label={jobsContent.closeLabel}
        >
          ×
        </button>

        <h1 id="job-details-title">{job.title}</h1>

        <h2>{job.company}</h2>

        <p>
          <strong>{jobsContent.locationLabel}</strong>{" "}
          {job.location?.join(", ") || jobsContent.locationNotSpecified}
        </p>

        <p>
          <strong>{jobsContent.workModeLabel}</strong>{" "}
          {job.remote ? jobsContent.remote : jobsContent.onSite}
        </p>

        <p>
          <strong>{jobsContent.fieldLabel}</strong> {job.field}
        </p>

        {job.min_experience != null && (
          <p>
            <strong>{jobsContent.minExperienceLabel}</strong>{" "}
            {job.min_experience}+ {jobsContent.yearsExperience}
          </p>
        )}

        {job.posted && (
          <p>
            <strong>
              {jobsContent.postedLabel}{" "}
              {new Date(job.posted).toLocaleDateString("en-GB")}
            </strong>
          </p>
        )}

        {job.description && (
          <section>
            <h3>{jobsContent.aboutRoleTitle}</h3>
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
                      <h3>{jobsContent.requirementsTitle}</h3>
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
            <h3>{jobsContent.skillsTitle}</h3>
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
            {jobsContent.viewOriginalJob}
          </a>
        )}
      </article>
    </div>
  );
}
