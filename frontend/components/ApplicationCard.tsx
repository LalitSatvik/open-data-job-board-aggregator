"use client";

import { useDraggable } from "@dnd-kit/core";
import { motion } from "motion/react";
import type { Application } from "@/lib/types";

export function ApplicationCard({
  application,
  onOpen,
}: {
  application: Application;
  onOpen: (application: Application) => void;
}) {
  const { attributes, listeners, setNodeRef, transform, isDragging } =
    useDraggable({ id: application.id });

  const dragStyle = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
        zIndex: 20,
      }
    : undefined;

  return (
    <motion.div
      ref={setNodeRef}
      layoutId={`application-${application.id}`}
      layout={!isDragging}
      style={dragStyle}
      {...listeners}
      {...attributes}
      onClick={() => onOpen(application)}
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 420, damping: 34 }}
      className="glass-panel cursor-grab rounded-xl px-3 py-2.5 active:cursor-grabbing"
    >
      <p className="text-sm font-medium">
        {application.job?.title ?? "Untitled application"}
      </p>
      <p className="text-xs text-muted-foreground">
        {application.job?.company ?? ""}
      </p>
    </motion.div>
  );
}
