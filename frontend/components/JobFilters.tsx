"use client";

import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export interface JobFilterState {
  q: string;
  location: string;
  remote: string; // "any" | "true" | "false"
  salaryMin: string;
}

export function JobFilters({
  value,
  onChange,
}: {
  value: JobFilterState;
  onChange: (next: JobFilterState) => void;
}) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
      <Input
        placeholder="Search title or company"
        value={value.q}
        onChange={(e) => onChange({ ...value, q: e.target.value })}
      />
      <Input
        placeholder="Location"
        value={value.location}
        onChange={(e) => onChange({ ...value, location: e.target.value })}
      />
      <Select
        value={value.remote}
        onValueChange={(remote) => onChange({ ...value, remote: remote ?? "any" })}
      >
        <SelectTrigger>
          <SelectValue placeholder="Remote?" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="any">Any</SelectItem>
          <SelectItem value="true">Remote only</SelectItem>
          <SelectItem value="false">On-site only</SelectItem>
        </SelectContent>
      </Select>
      <Input
        placeholder="Minimum salary"
        type="number"
        value={value.salaryMin}
        onChange={(e) => onChange({ ...value, salaryMin: e.target.value })}
      />
    </div>
  );
}
