"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiGet, apiPatch } from "@/lib/api";
import { useSession } from "@/lib/useSession";
import { KanbanBoard } from "@/components/KanbanBoard";
import { ApplicationDetailDialog } from "@/components/ApplicationDetailDialog";
import { ExportButton } from "@/components/ExportButton";
import type { Application } from "@/lib/types";

export default function TrackerPage() {
  const router = useRouter();
  const { user, loading } = useSession();
  const [applications, setApplications] = useState<Application[]>([]);
  const [selected, setSelected] = useState<Application | null>(null);

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  async function refresh() {
    const data = await apiGet<Application[]>("/applications");
    setApplications(data);
  }

  useEffect(() => {
    if (user) refresh();
  }, [user]);

  async function handleStatusChange(id: number, status: string) {
    setApplications((prev) =>
      prev.map((a) => (a.id === id ? { ...a, status } : a))
    );
    try {
      await apiPatch(`/applications/${id}`, { status });
    } catch (error) {
      console.error("Failed to update application status", error);
    } finally {
      refresh();
    }
  }

  async function handleSaveNotes(id: number, notes: string) {
    try {
      await apiPatch(`/applications/${id}`, { notes });
    } catch (error) {
      console.error("Failed to save application notes", error);
    } finally {
      setSelected(null);
      refresh();
    }
  }

  if (loading || !user) return null;

  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Application Tracker</h1>
        <div className="flex items-center gap-4">
          <ExportButton />
          <a href="/" className="text-sm underline underline-offset-4">
            Back to job board
          </a>
        </div>
      </div>
      <KanbanBoard
        applications={applications}
        onStatusChange={handleStatusChange}
        onOpen={setSelected}
      />
      <ApplicationDetailDialog
        application={selected}
        onClose={() => setSelected(null)}
        onSaveNotes={handleSaveNotes}
      />
    </main>
  );
}
