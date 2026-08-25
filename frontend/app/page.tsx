"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "motion/react";
import { BookmarkCheck, Globe, Search } from "lucide-react";
import { apiGet, apiPost } from "@/lib/api";
import { useSession } from "@/lib/useSession";
import { Button } from "@/components/ui/button";
import { AppShell } from "@/components/AppShell";
import { StatTile } from "@/components/StatTile";
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

const gridVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.05 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0 },
};

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
  const remoteOnPage = jobs.filter((job) => job.remote).length;

  return (
    <AppShell user={user}>
      <div className="flex flex-col gap-1">
        <h1 className="font-heading text-2xl font-semibold tracking-tight sm:text-3xl">
          Job Board
        </h1>
        <p className="text-sm text-muted-foreground">
          Search open roles pulled from every source we track.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <StatTile label="Results" value={total} icon={Search} delay={0} />
        <StatTile
          label="Remote (this page)"
          value={remoteOnPage}
          icon={Globe}
          delay={0.05}
        />
        <StatTile
          label="Tracked"
          value={trackedIds.size}
          icon={BookmarkCheck}
          delay={0.1}
        />
      </div>

      <div className="glass-panel rounded-2xl p-4">
        <JobFilters value={filters} onChange={handleFiltersChange} />
      </div>

      <motion.div
        className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
        initial="hidden"
        animate="show"
        variants={gridVariants}
      >
        {jobs.map((job) => (
          <motion.div
            key={job.id}
            variants={cardVariants}
            transition={{ duration: 0.35, ease: "easeOut" }}
            whileHover={{ y: -4 }}
          >
            <JobCard
              job={job}
              isTracked={trackedIds.has(job.id)}
              onTrack={handleTrack}
            />
          </motion.div>
        ))}
      </motion.div>

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
        <div className="glass-panel flex items-center justify-between rounded-2xl px-4 py-3">
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
    </AppShell>
  );
}
