"use client";

import { useState } from "react";

import { useContent } from "@/hooks/content";

import { MatchResultsProps } from "@/types/match";

import MatchList from "./MatchList";
import JobDetails from "./JobDetails";

import "@/styles/shared/jobs-layout.scss";

export default function MatchResults({ matches }: MatchResultsProps) {
  const [selectedJob, setSelectedJob] = useState<
    MatchResultsProps["matches"][number]["job"] | null
  >(null);

  const { content, loading } = useContent();

  if (loading || !content) {
    return null;
  }

  const matchContent = content.matchpage;

  const matchDescription = matchContent.matchDescription.replace(
    "{count}",
    String(matches.length),
  );

  return (
    <section className="jobs-section">
      <div className="jobs-header">
        <h1>{matchContent.title}</h1>

        <p>{matchContent.subtitle}</p>
      </div>

      <div className="jobs-container">
        <h2 className="jobs-container-title">{matchContent.containerTitle}</h2>

        <p>{matchDescription}</p>

        <MatchList matches={matches} onJobClick={setSelectedJob} />
      </div>

      {selectedJob && (
        <JobDetails job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </section>
  );
}
