"use client";

import { useDraggable } from "@dnd-kit/core";
import { Card, CardContent } from "@/components/ui/card";
import type { Application } from "@/lib/types";

export function ApplicationCard({
  application,
  onOpen,
}: {
  application: Application;
  onOpen: (application: Application) => void;
}) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: application.id,
  });

  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
        zIndex: 10,
      }
    : undefined;

  return (
    <Card
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      onClick={() => onOpen(application)}
      className="cursor-grab active:cursor-grabbing"
    >
      <CardContent className="p-3">
        <p className="text-sm font-medium">
          {application.job?.title ?? "Untitled application"}
        </p>
        <p className="text-xs text-muted-foreground">
          {application.job?.company ?? ""}
        </p>
      </CardContent>
    </Card>
  );
}
