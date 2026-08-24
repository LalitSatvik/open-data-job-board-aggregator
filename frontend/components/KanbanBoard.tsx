"use client";

import {
  DndContext,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
  useDroppable,
} from "@dnd-kit/core";
import { ApplicationCard } from "@/components/ApplicationCard";
import type { Application } from "@/lib/types";

const STAGES: { key: string; label: string }[] = [
  { key: "saved", label: "Saved" },
  { key: "applied", label: "Applied" },
  { key: "interviewing", label: "Interviewing" },
  { key: "offer", label: "Offer" },
  { key: "accepted", label: "Accepted" },
  { key: "rejected", label: "Rejected" },
  { key: "withdrawn", label: "Withdrawn" },
];

function Column({
  stage,
  applications,
  onOpen,
}: {
  stage: { key: string; label: string };
  applications: Application[];
  onOpen: (application: Application) => void;
}) {
  const { setNodeRef, isOver } = useDroppable({ id: stage.key });

  return (
    <div
      ref={setNodeRef}
      className={`flex min-w-[220px] flex-col gap-2 rounded-lg border p-3 ${
        isOver ? "bg-muted" : ""
      }`}
    >
      <h2 className="text-sm font-semibold">{stage.label}</h2>
      <div className="flex min-h-16 flex-col gap-2">
        {applications.map((application) => (
          <ApplicationCard
            key={application.id}
            application={application}
            onOpen={onOpen}
          />
        ))}
        {applications.length === 0 && (
          <p className="rounded-lg border border-dashed p-3 text-center text-xs text-muted-foreground">
            No applications
          </p>
        )}
      </div>
    </div>
  );
}

export function KanbanBoard({
  applications,
  onStatusChange,
  onOpen,
}: {
  applications: Application[];
  onStatusChange: (id: number, status: string) => void;
  onOpen: (application: Application) => void;
}) {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: { distance: 8 },
    })
  );

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (!over) return;
    const newStatus = String(over.id);
    onStatusChange(Number(active.id), newStatus);
  }

  return (
    <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
      <div className="flex gap-3 overflow-x-auto pb-4">
        {STAGES.map((stage) => (
          <Column
            key={stage.key}
            stage={stage}
            applications={applications.filter((a) => a.status === stage.key)}
            onOpen={onOpen}
          />
        ))}
      </div>
    </DndContext>
  );
}
