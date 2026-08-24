export interface Job {
  id: number;
  source: string;
  title: string;
  company: string;
  location: string | null;
  remote: boolean;
  salary_min: number | null;
  salary_max: number | null;
  url: string;
  description: string | null;
  posted_at: string | null;
}

export interface JobsResponse {
  items: Job[];
  total: number;
  page: number;
  page_size: number;
}

export interface StatusHistoryEntry {
  from_status: string | null;
  to_status: string;
  changed_at: string;
}

export interface Application {
  id: number;
  job_id: number | null;
  job: { id: number; title: string; company: string; url: string } | null;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
  history: StatusHistoryEntry[];
}
