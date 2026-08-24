"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Job } from "@/lib/types";

export function JobCard({
  job,
  onTrack,
  isTracked = false,
}: {
  job: Job;
  onTrack: (job: Job) => void;
  isTracked?: boolean;
}) {
  const salary =
    job.salary_min && job.salary_max
      ? `$${job.salary_min.toLocaleString()} – $${job.salary_max.toLocaleString()}`
      : null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{job.title}</CardTitle>
        <p className="text-sm text-muted-foreground">{job.company}</p>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <div className="flex flex-wrap gap-2">
          {isTracked && <Badge>Tracked</Badge>}
          {job.remote && <Badge variant="secondary">Remote</Badge>}
          {job.location && <Badge variant="outline">{job.location}</Badge>}
          {salary && <Badge variant="outline">{salary}</Badge>}
        </div>
        <div className="flex items-center justify-between">
          <a
            href={job.url}
            target="_blank"
            rel="noreferrer"
            className="text-sm underline underline-offset-4"
          >
            View listing
          </a>
          <Button
            size="sm"
            variant={isTracked ? "outline" : "default"}
            disabled={isTracked}
            onClick={() => onTrack(job)}
          >
            {isTracked ? "Tracked" : "Track this job"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
