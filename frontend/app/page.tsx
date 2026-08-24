"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiGet, apiPost } from "@/lib/api";
import { useSession } from "@/lib/useSession";
import { Button } from "@/components/ui/button";
import { JobCard } from "@/components/JobCard";
import { JobFilters, type JobFilterState } from "@/components/JobFilters";
import type { Job, JobsResponse } from "@/lib/types";

const EMPTY_FILTERS: JobFilterState = {
  q: "",
  location: "",
  remote: "any",
  salaryMin: "",
};

const PAGE_SIZE = 20;

export default function JobBoardPage() {
  const router = useRouter();
  const { user, loading } = useSession();
  const [filters, setFilters] = useState<JobFilterState>(EMPTY_FILTERS);
  const [page, setPage] = useState(1);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [total, setTotal] = useState(0);
  const [jobsLoading, setJobsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [trackedIds, setTrackedIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  useEffect(() => {
    if (!user) return;
    let cancelled = false;

    const params = new URLSearchParams();
    if (filters.q) params.set("q", filters.q);
    if (filters.location) params.set("location", filters.location);
    if (filters.remote !== "any") params.set("remote", filters.remote);
    if (filters.salaryMin) params.set("salary_min", filters.salaryMin);
    params.set("page", String(page));
    params.set("page_size", String(PAGE_SIZE));

    setJobsLoading(true);
    setError(null);
    apiGet<JobsResponse>(`/jobs?${params.toString()}`)
      .then((res) => {
        if (cancelled) return;
        setJobs(res.items);
        setTotal(res.total);
        setJobsLoading(false);
      })
      .catch(() => {
        if (cancelled) return;
        setJobs([]);
        setTotal(0);
        setError("Couldn't load jobs. Try refreshing.");
        setJobsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [user, filters, page]);

  function handleFiltersChange(next: JobFilterState) {
    setFilters(next);
    setPage(1);
  }

  async function handleTrack(job: Job) {
    await apiPost("/applications", { job_id: job.id, status: "saved" });
    setTrackedIds((prev) => new Set(prev).add(job.id));
  }

  if (loading || !user) return null;

  const firstResult = total === 0 ? 0 : (page - 1) * PAGE_SIZE + 1;
  const lastResult = Math.min(page * PAGE_SIZE, total);
  const hasNextPage = page * PAGE_SIZE < total;

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Job Board</h1>
        <a href="/tracker" className="text-sm underline underline-offset-4">
          Go to tracker
        </a>
      </div>
      <JobFilters value={filters} onChange={handleFiltersChange} />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            isTracked={trackedIds.has(job.id)}
            onTrack={handleTrack}
          />
        ))}
      </div>
      {jobsLoading && (
        <p className="text-sm text-muted-foreground">Loading jobs…</p>
      )}
      {error && <p className="text-sm text-destructive">{error}</p>}
      {!jobsLoading && !error && jobs.length === 0 && (
        <p className="text-sm text-muted-foreground">
          No jobs match these filters yet.
        </p>
      )}
      {!error && total > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {firstResult}–{lastResult} of {total}
          </p>
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              disabled={page === 1 || jobsLoading}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Previous
            </Button>
            <Button
              size="sm"
              variant="outline"
              disabled={!hasNextPage || jobsLoading}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </main>
  );
}
