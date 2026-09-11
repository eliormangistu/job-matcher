"use client";

import { useState } from "react";

import { MatchResultsProps } from "@/types/match";

import MatchList from "./MatchList";
import JobDetails from "./JobDetails";

import "@/styles/shared/jobs-layout.scss";

export default function MatchResults({ matches }: MatchResultsProps) {
  const [selectedJob, setSelectedJob] = useState<
    MatchResultsProps["matches"][number]["job"] | null
  >(null);

  return (
    <section className="jobs-section">
      <div className="jobs-header">
        <h1>Jobs</h1>
        <p>Find your next opportunity.</p>
      </div>

      <div className="jobs-container">
        <h2 className="jobs-container-title">Matching Jobs</h2>
        <p>AI found {matches.length} opportunities that match your skills.</p>

        <MatchList matches={matches} onJobClick={setSelectedJob} />
      </div>

      {selectedJob && (
        <JobDetails job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </section>
  );
}
