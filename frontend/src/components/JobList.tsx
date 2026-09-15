"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { getJobs } from "@/api/jobs";

import { Job } from "@/types/job";

import JobCard from "./JobCard";
import JobDetails from "./JobDetails";
import Loader from "./Loader";
import { routes } from "@/routes/routes";

import { setErrorState } from "@/lib/api-error";

import "@/styles/shared/jobs-layout.scss";

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);

  const pageSize = 20;
  const totalPages = Math.ceil(total / pageSize);

  const router = useRouter();

  useEffect(() => {
    const offset = (currentPage - 1) * pageSize;

    setIsLoading(true);

    getJobs(pageSize, offset)
      .then((response) => {
        setJobs(response.data.items);
        setTotal(response.data.total);
      })
      .catch((error) => {
        console.error("Failed to load jobs:", error);

        setErrorState({
          title: "Could not load jobs",
          message:
            "We couldn't load the jobs right now. Please try again later.",
        });

        router.push(routes.error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [currentPage, router]);

  if (isLoading) {
    return (
      <section className="jobs-section">
        <Loader text="Loading jobs..." />
      </section>
    );
  }

  return (
    <section className="jobs-section">
      <div className="jobs-header">
        <h1>Tech Jobs</h1>
        <p>
          Explore opportunities designed for the early stages of your tech
          career.
        </p>
      </div>

      <div className="jobs-container">
        <h2 className="jobs-container-title">Available Jobs</h2>

        <div className="jobs-list">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onClick={() => setSelectedJob(job)}
            />
          ))}
        </div>

        <div className="jobs-pagination">
          <button
            type="button"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((page) => page - 1)}
          >
            ← Prev
          </button>

          <span>
            Page {currentPage} of {totalPages}
          </span>

          <button
            type="button"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((page) => page + 1)}
          >
            Next →
          </button>
        </div>
      </div>

      {selectedJob && (
        <JobDetails job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </section>
  );
}
