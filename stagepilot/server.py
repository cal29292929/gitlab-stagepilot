"""
Interactive Web Dashboard, GitLab Webhook Receiver & MCP HTTP Server for GitLab StagePilot.
Zero external runtime dependencies required (built on Python's standard http.server).
"""

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Tuple
from urllib.parse import parse_qs, urlparse

from stagepilot.lifecycle_engine import StagePilotEngine
from stagepilot.mcp_server import handle_mcp_request
from stagepilot.models import AutonomyLevel, DevSecOpsStage
from stagepilot.sci_calculator import render_sci_markdown_report


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GitLab StagePilot — 9-Stage Autonomous DevSecOps &amp; SCI GreenOps Engine</title>
  <style>
    :root {
      --bg: #0f111a;
      --panel: #171a26;
      --border: #2a2f45;
      --accent: #fc6d26;
      --accent2: #6b4fbb;
      --green: #2da44e;
      --teal: #38bdf8;
      --amber: #f59e0b;
      --text: #f1f5f9;
      --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
    }
    .container { max-width: 1280px; margin: 0 auto; }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
    }
    .title-group h1 { font-size: 1.65rem; display: flex; align-items: center; gap: 10px; }
    .badge {
      font-size: 0.75rem;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(252, 109, 38, 0.18);
      color: var(--accent);
      border: 1px solid var(--accent);
      font-weight: 600;
    }
    .controls {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    select, button {
      background: var(--panel);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 0.9rem;
      cursor: pointer;
    }
    button.primary {
      background: linear-gradient(135deg, var(--accent), #e24329);
      border: none;
      font-weight: 600;
      color: #fff;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .kpi-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
    }
    .kpi-label { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { font-size: 1.7rem; font-weight: 700; margin-top: 6px; color: var(--teal); }
    .kpi-sub { font-size: 0.82rem; color: var(--green); margin-top: 4px; }
    .stages-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }
    .stage-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stage-header { display: flex; justify-content: space-between; align-items: center; }
    .stage-name { font-weight: 700; color: var(--accent); text-transform: uppercase; font-size: 0.92rem; }
    .status-pill {
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
    }
    .status-completed { background: rgba(45, 164, 78, 0.2); color: #4ade80; border: 1px solid #2da44e; }
    .status-waiting { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
    .stage-meta { font-size: 0.78rem; color: var(--muted); }
    .stage-summary { font-size: 0.84rem; color: var(--text); }
    .bottom-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }
    @media (max-width: 900px) { .bottom-grid { grid-template-columns: 1fr; } }
    pre {
      background: #0b0d14;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      overflow-x: auto;
      font-size: 0.8rem;
      color: #cbd5e1;
      max-height: 420px;
    }
    h2 { font-size: 1.1rem; margin-bottom: 10px; color: var(--text); }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="title-group">
        <h1>
          <span>🦊 GitLab StagePilot</span>
          <span class="badge">9-Stage Autonomous DevSecOps + SCI GreenOps</span>
        </h1>
        <p style="color: var(--muted); font-size: 0.9rem; margin-top: 4px;">
          GitLab Duo Agent Platform · Anthropic Claude Sonnet 4.5 · Google Cloud Vertex AI · ISO/IEC 21031:2024 SCI
        </p>
      </div>
      <div class="controls">
        <select id="autonomySelect">
          <option value="hands_off" selected>Autonomy: Hands-off (Full Autonomous)</option>
          <option value="supervised">Autonomy: Supervised (Release Gate)</option>
          <option value="assisted">Autonomy: Assisted (Per-Stage Approval)</option>
        </select>
        <select id="regionSelect">
          <option value="us-central1" selected>GCP Region: us-central1 (142 gCO2/kWh)</option>
          <option value="europe-north1">GCP Region: europe-north1 (48 gCO2/kWh)</option>
        </select>
        <button class="primary" onclick="runLifecycle()">▶ Run 9-Stage Autonomous Flow</button>
      </div>
    </header>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">DevSecOps Stages Covered</div>
        <div class="kpi-value" id="kpiStages">9 / 9</div>
        <div class="kpi-sub">plan · create · verify · package · secure · release · configure · monitor · govern</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Optimized SCI Score (ISO/IEC 21031)</div>
        <div class="kpi-value" id="kpiSci">-- gCO2eq</div>
        <div class="kpi-sub" id="kpiSciDelta">Calculating carbon savings...</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Vulnerabilities Remediated</div>
        <div class="kpi-value" id="kpiSec">2 / 2</div>
        <div class="kpi-sub">CWE-89 (SQLi) &amp; CWE-347 (HMAC Timing) patched + DCO signed</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Post-Deploy SLO &amp; Governance</div>
        <div class="kpi-value" id="kpiSlo">HEALTHY</div>
        <div class="kpi-sub">p95 38.4ms · 0.00% errors · MIT &amp; SLSA L3 verified</div>
      </div>
    </div>

    <h2>9-Stage GitLab DevSecOps Execution Matrix</h2>
    <div class="stages-grid" id="stagesGrid"></div>

    <div class="bottom-grid">
      <div>
        <h2>GitLab Merge Request / Issue Autonomous Summary Comment</h2>
        <pre id="markdownPreview">Loading...</pre>
      </div>
      <div>
        <h2>ISO/IEC 21031:2024 SCI Telemetry &amp; Audit Payload (JSON)</h2>
        <pre id="jsonPreview">Loading...</pre>
      </div>
    </div>
  </div>

  <script>
    async function runLifecycle() {
      const autonomy = document.getElementById('autonomySelect').value;
      const region = document.getElementById('regionSelect').value;
      const resp = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ autonomy_mode: autonomy, region: region, trigger_event: 'web_dashboard_trigger' })
      });
      const data = await resp.json();
      renderDashboard(data);
    }

    function renderDashboard(data) {
      document.getElementById('kpiStages').textContent = `${data.stages_covered_count} / ${data.total_stages_available}`;
      const sci = data.sci_report;
      document.getElementById('kpiSci').textContent = `${sci.sci_score_optimized_gco2_per_r.toFixed(2)} gCO2eq`;
      document.getElementById('kpiSciDelta').textContent =
        `-${sci.reduction_percentage.toFixed(1)}% vs Baseline (${sci.sci_score_baseline_gco2_per_r.toFixed(2)} gCO2eq)`;

      const grid = document.getElementById('stagesGrid');
      grid.innerHTML = '';
      data.stage_results.forEach(s => {
        const pillClass = s.status === 'completed' ? 'status-completed' : 'status-waiting';
        const card = document.createElement('div');
        card.className = 'stage-card';
        card.innerHTML = `
          <div class="stage-header">
            <span class="stage-name">${s.stage_index}. ${s.stage}</span>
            <span class="status-pill ${pillClass}">${s.status}</span>
          </div>
          <div class="stage-meta">Agent: <b>${s.agent_name}</b><br/>Model: <code>${s.model_used}</code></div>
          <div class="stage-summary">${s.summary}</div>
          <div class="stage-meta" style="color:#4ade80;">
            ⚡ ${s.energy_kwh.toFixed(4)} kWh · 🌱 ${s.carbon_gco2eq.toFixed(2)} gCO2eq (base ${s.baseline_carbon_gco2eq.toFixed(2)})
          </div>
        `;
        grid.appendChild(card);
      });

      document.getElementById('markdownPreview').textContent = data.gitlab_summary_comment_markdown;
      document.getElementById('jsonPreview').textContent = JSON.stringify(data.sci_report, null, 2);
    }

    window.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(window.location.search);
      if (params.get('autonomy')) document.getElementById('autonomySelect').value = params.get('autonomy');
      if (params.get('region')) document.getElementById('regionSelect').value = params.get('region');
      runLifecycle();
    });
  </script>
</body>
</html>
"""


def dispatch_http_request(
    method: str,
    path: str,
    body_bytes: bytes = b"",
    headers: Dict[str, str] = {},
) -> Tuple[int, str, bytes]:
    """Pure request dispatcher used by both ThreadingHTTPServer and automated tests."""
    parsed = urlparse(path)
    route = parsed.path
    qs = parse_qs(parsed.query)

    if method == "GET" and route == "/":
        return 200, "text/html; charset=utf-8", DASHBOARD_HTML.encode("utf-8")

    if method == "GET" and route in ("/api/health", "/healthz"):
        payload = {
            "status": "ok",
            "service": "gitlab-stagepilot",
            "version": "1.0.0",
            "stages_supported": [s.value for s in DevSecOpsStage.ordered()],
            "autonomy_modes": [m.value for m in AutonomyLevel],
        }
        return 200, "application/json", json.dumps(payload).encode("utf-8")

    if method == "GET" and route == "/api/stages":
        payload = {
            "stages": [s.value for s in DevSecOpsStage.ordered()],
            "count": 9,
        }
        return 200, "application/json", json.dumps(payload).encode("utf-8")

    if method == "GET" and route == "/api/sci":
        region = qs.get("region", ["us-central1"])[0]
        engine = StagePilotEngine(autonomy_mode="hands_off", region=region)
        report = engine.run_full_lifecycle(trigger_event="api_sci_query")
        payload = {
            "sci_report": report.sci_report.to_dict(),
            "markdown": render_sci_markdown_report(report.sci_report),
        }
        return 200, "application/json", json.dumps(payload).encode("utf-8")

    if method == "POST" and route == "/api/run":
        body = json.loads(body_bytes.decode("utf-8") or "{}")
        autonomy = body.get("autonomy_mode", "hands_off")
        region = body.get("region", "us-central1")
        stage = body.get("stage")
        engine = StagePilotEngine(autonomy_mode=autonomy, region=region)
        if stage:
            res = engine.execute_stage(stage)
            return 200, "application/json", json.dumps(res.to_dict()).encode("utf-8")
        rep = engine.run_full_lifecycle(
            trigger_event=body.get("trigger_event", "api_run_lifecycle"),
            project_name=body.get("project_name", "gitlab-stagepilot/payment-webhook-service"),
        )
        return 200, "application/json", json.dumps(rep.to_dict()).encode("utf-8")

    if method == "POST" and route == "/api/webhook/gitlab":
        body = json.loads(body_bytes.decode("utf-8") or "{}")
        gl_event = headers.get("X-Gitlab-Event") or headers.get("x-gitlab-event") or body.get("object_kind", "push")
        autonomy = body.get("autonomy_mode", os.environ.get("STAGEPILOT_AUTONOMY_MODE", "hands_off"))
        region = body.get("region", os.environ.get("GCP_REGION", "us-central1"))
        engine = StagePilotEngine(autonomy_mode=autonomy, region=region)
        rep = engine.run_full_lifecycle(
            trigger_event=f"gitlab_webhook:{gl_event}",
            context={
                "issue_iid": body.get("object_attributes", {}).get("iid", 42),
                "mr_iid": body.get("merge_request", {}).get("iid", 108),
                "commit_sha": body.get("checkout_sha", "9f4b2c8e")[:8],
            },
        )
        return 200, "application/json", json.dumps(rep.to_dict()).encode("utf-8")

    if method == "POST" and route == "/api/mcp":
        req = json.loads(body_bytes.decode("utf-8") or "{}")
        resp = handle_mcp_request(req)
        return 200, "application/json", json.dumps(resp).encode("utf-8")

    return 404, "application/json", json.dumps({"error": "Not found", "path": route}).encode("utf-8")


class StagePilotHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        status, ctype, data = dispatch_http_request("GET", self.path, b"", dict(self.headers))
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length > 0 else b""
        status, ctype, data = dispatch_http_request("POST", self.path, body, dict(self.headers))
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GitLab StagePilot Web Dashboard & Webhook Server")
    parser.add_argument("--host", default=os.environ.get("STAGEPILOT_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8080")))
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), StagePilotHTTPRequestHandler)
    print(f"[StagePilot] Listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
