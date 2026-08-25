"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ClipboardList, Send, Users, Trophy } from "lucide-react";
import { apiGet, apiPatch } from "@/lib/api";
import { useSession } from "@/lib/useSession";
import { AppShell } from "@/components/AppShell";
import { StatTile } from "@/components/StatTile";
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

  const count = (status: string) =>
    applications.filter((a) => a.status === status).length;

  return (
    <AppShell user={user}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-col gap-1">
          <h1 className="font-heading text-2xl font-semibold tracking-tight sm:text-3xl">
            Application Tracker
          </h1>
          <p className="text-sm text-muted-foreground">
            Drag a card between stages to update its status.
          </p>
        </div>
        <ExportButton />
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatTile
          label="Tracked"
          value={applications.length}
          icon={ClipboardList}
          delay={0}
        />
        <StatTile label="Applied" value={count("applied")} icon={Send} delay={0.05} />
        <StatTile
          label="Interviewing"
          value={count("interviewing")}
          icon={Users}
          delay={0.1}
        />
        <StatTile label="Offers" value={count("offer")} icon={Trophy} delay={0.15} />
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
    </AppShell>
  );
}
