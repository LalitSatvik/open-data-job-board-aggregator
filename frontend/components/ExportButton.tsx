"use client";

import { Button } from "@/components/ui/button";

export function ExportButton() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";

  return (
    <div className="flex gap-2">
      <Button variant="outline" size="sm" asChild>
        <a href={`${apiUrl}/export?format=csv`}>Export CSV</a>
      </Button>
      <Button variant="outline" size="sm" asChild>
        <a href={`${apiUrl}/export?format=json`}>Export JSON</a>
      </Button>
    </div>
  );
}
