"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import type { Application } from "@/lib/types";

export function ApplicationDetailDialog({
  application,
  onClose,
  onSaveNotes,
}: {
  application: Application | null;
  onClose: () => void;
  onSaveNotes: (id: number, notes: string) => void;
}) {
  const [notes, setNotes] = useState(application?.notes ?? "");

  useEffect(() => {
    setNotes(application?.notes ?? "");
  }, [application?.id, application?.notes]);

  if (!application) return null;

  return (
    <Dialog open={!!application} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>
            {application.job?.title ?? "Untitled application"}
          </DialogTitle>
          {application.job?.company && (
            <p className="text-sm text-muted-foreground">
              {application.job.company}
            </p>
          )}
        </DialogHeader>
        <div className="flex flex-col gap-4">
          <div>
            <h3 className="mb-2 text-sm font-medium">Status history</h3>
            {application.history.length > 0 ? (
              <ul className="flex flex-col gap-2 border-l border-border/70 pl-3 text-sm">
                {application.history.map((entry, i) => (
                  <li key={i} className="relative text-muted-foreground">
                    <span className="absolute -left-[1.05rem] top-1.5 size-1.5 rounded-full bg-navy" />
                    <span className="font-medium text-foreground">
                      {entry.from_status ?? "start"} → {entry.to_status}
                    </span>
                    <br />
                    {new Date(entry.changed_at).toLocaleString()}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted-foreground">
                No status changes yet.
              </p>
            )}
          </div>
          <div>
            <h3 className="mb-2 text-sm font-medium">Notes</h3>
            <Textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={4}
            />
            <Button
              size="sm"
              className="mt-2"
              onClick={() => onSaveNotes(application.id, notes)}
            >
              Save notes
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
