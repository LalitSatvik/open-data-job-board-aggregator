import csv
import io
import json
from typing import List


def _history_str(history: List[dict]) -> str:
    parts = []
    for h in history:
        from_label = h["from_status"] or "start"
        parts.append(f"{from_label}→{h['to_status']} ({h['changed_at']})")
    return "; ".join(parts)


def to_json(applications: List[dict]) -> str:
    return json.dumps(applications, default=str)


def to_csv(applications: List[dict]) -> str:
    output = io.StringIO()
    fieldnames = [
        "id", "job_title", "company", "status", "notes",
        "created_at", "updated_at", "history",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for application in applications:
        job = application.get("job") or {}
        writer.writerow(
            {
                "id": application["id"],
                "job_title": job.get("title", ""),
                "company": job.get("company", ""),
                "status": application["status"],
                "notes": application["notes"] or "",
                "created_at": application["created_at"],
                "updated_at": application["updated_at"],
                "history": _history_str(application["history"]),
            }
        )
    return output.getvalue()
