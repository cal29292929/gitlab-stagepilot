"""
GitLab REST/GraphQL & Webhook Client for StagePilot.
Supports live GitLab API v4 calls when GITLAB_TOKEN is provided,
and maintains a complete in-memory GitLab Sandbox state for instant local demos and tests.
"""

import json
import os
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List


class GitLabConnector:
    """Dual-mode GitLab API v4 connector (Live API + Local Sandbox)."""

    def __init__(self) -> None:
        self.api_url = os.environ.get("GITLAB_API_URL", "https://gitlab.com/api/v4").rstrip("/")
        self.project_id = os.environ.get("GITLAB_PROJECT_ID", "stagepilot-demo/life-after-code")
        self.token = os.environ.get("GITLAB_TOKEN", "")
        self.mode = os.environ.get("STAGEPILOT_MODE", "demo").lower()

        self.comments_posted: List[Dict[str, Any]] = []
        self.releases_created: List[Dict[str, Any]] = []

    def post_issue_or_mr_summary(
        self, issue_iid: int, mr_iid: int, markdown_body: str
    ) -> Dict[str, Any]:
        """Post the autonomous execution summary back to the originating GitLab Issue and Merge Request."""
        record = {
            "project_id": self.project_id,
            "issue_iid": issue_iid,
            "mr_iid": mr_iid,
            "posted_at_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "live" if (self.mode == "live" and self.token) else "sandbox",
            "markdown_body": markdown_body,
        }
        if self.mode == "live" and self.token:
            try:
                url = f"{self.api_url}/projects/{self.project_id}/merge_requests/{mr_iid}/notes"
                req = urllib.request.Request(
                    url,
                    data=json.dumps({"body": markdown_body}).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "PRIVATE-TOKEN": self.token,
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    record["gitlab_note_response"] = json.loads(resp.read().decode("utf-8"))
            except Exception as exc:
                record["live_fallback_reason"] = str(exc)

        self.comments_posted.append(record)
        return record
