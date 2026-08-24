"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiGet, apiPost } from "@/lib/api";
import { useSession } from "@/lib/useSession";
import { JobCard } from "@/components/JobCard";
import { JobFilters, type JobFilterState } from "@/components/JobFilters";
import type { Job, JobsResponse } from "@/lib/types";

const EMPTY_FILTERS: JobFilterState = {
  q: "",
  location: "",
  remote: "any",
  salaryMin: "",
};

export default function JobBoardPage() {
  const router = useRouter();
  const { user, loading } = useSession();
  const [filters, setFilters] = useState<JobFilterState>(EMPTY_FILTERS);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [jobsLoading, setJobsLoading] = useState(true);
  const [trackedIds, setTrackedIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  useEffect(() => {
    if (!user) return;
    const params = new URLSearchParams();
    if (filters.q) params.set("q", filters.q);
    if (filters.location) params.set("location", filters.location);
    if (filters.remote !== "any") params.set("remote", filters.remote);
    if (filters.salaryMin) params.set("salary_min", filters.salaryMin);

    setJobsLoading(true);
    apiGet<JobsResponse>(`/jobs?${params.toString()}`).then((res) => {
      setJobs(res.items);
      setJobsLoading(false);
    });
  }, [user, filters]);

  async function handleTrack(job: Job) {
    await apiPost("/applications", { job_id: job.id, status: "saved" });
    setTrackedIds((prev) => new Set(prev).add(job.id));
  }

  if (loading || !user) return null;

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Job Board</h1>
        <a href="/tracker" className="text-sm underline underline-offset-4">
          Go to tracker
        </a>
      </div>
      <JobFilters value={filters} onChange={setFilters} />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            onTrack={handleTrack}
          />
        ))}
      </div>
      {jobsLoading && (
        <p className="text-sm text-muted-foreground">Loading jobs…</p>
      )}
      {!jobsLoading && jobs.length === 0 && (
        <p className="text-sm text-muted-foreground">
          No jobs match these filters yet.
        </p>
      )}
    </main>
  );
}
