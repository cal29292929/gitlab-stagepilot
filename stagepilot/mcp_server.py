"""
Model Context Protocol (MCP) JSON-RPC 2.0 Server for GitLab Duo Agent Platform.
Exposes StagePilot's 9-stage DevSecOps and ISO/IEC 21031 SCI sustainability tools.
"""

import json
import sys
from typing import Any, Dict

from stagepilot.lifecycle_engine import StagePilotEngine
from stagepilot.models import AutonomyLevel, DevSecOpsStage


MCP_TOOLS_SCHEMA = [
    {
        "name": "evaluate_stage",
        "description": "Execute and evaluate one of the 9 GitLab DevSecOps stages (plan, create, verify, package, secure, release, configure, monitor, govern).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stage": {"type": "string", "enum": [s.value for s in DevSecOpsStage.ordered()]},
                "autonomy_mode": {"type": "string", "enum": [m.value for m in AutonomyLevel], "default": "hands_off"},
                "region": {"type": "string", "default": "us-central1"},
            },
            "required": ["stage"],
        },
    },
    {
        "name": "run_full_lifecycle",
        "description": "Run all 9 GitLab DevSecOps stages end-to-end and return full execution + SCI sustainability report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "autonomy_mode": {"type": "string", "enum": [m.value for m in AutonomyLevel], "default": "hands_off"},
                "region": {"type": "string", "default": "us-central1"},
                "trigger_event": {"type": "string", "default": "mcp_tool_invocation"},
            },
        },
    },
    {
        "name": "remediate_vulnerability",
        "description": "Analyze SAST/CVE finding and produce surgical DCO-signed code patch + regression test.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cwe": {"type": "string", "default": "CWE-89"},
                "file_path": {"type": "string", "default": "src/db/audit_store.py"},
            },
        },
    },
    {
        "name": "heal_ci_pipeline",
        "description": "Diagnose failing GitLab CI pipeline job log and synthesize self-healing patch + unit tests.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pipeline_id": {"type": "integer", "default": 8901},
            },
        },
    },
    {
        "name": "calculate_sci_score",
        "description": "Calculate ISO/IEC 21031:2024 Software Carbon Intensity (SCI = ((E * I) + M) / R) across stages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region": {"type": "string", "default": "us-central1"},
            },
        },
    },
    {
        "name": "generate_sbom",
        "description": "Generate CycloneDX 1.5 Software Bill of Materials (SBOM) with SLSA Level 3 provenance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "default": "gitlab-stagepilot/payment-webhook-service"},
                "commit_sha": {"type": "string", "default": "9f4b2c8e"},
            },
        },
    },
]


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single JSON-RPC 2.0 MCP request and return a JSON-RPC 2.0 response."""
    req_id = request.get("id", 1)
    method = request.get("method", "")
    params = request.get("params", {}) or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-06-18",
                "serverInfo": {"name": "stagepilot-mcp", "version": "1.0.0"},
                "capabilities": {"tools": {"listChanged": False}},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS_SCHEMA},
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {}) or {}
        autonomy = args.get("autonomy_mode", "hands_off")
        region = args.get("region", "us-central1")
        engine = StagePilotEngine(autonomy_mode=autonomy, region=region)

        if tool_name == "evaluate_stage":
            stage = args.get("stage", "plan")
            res = engine.execute_stage(stage)
            payload = res.to_dict()
        elif tool_name == "run_full_lifecycle":
            rep = engine.run_full_lifecycle(trigger_event=args.get("trigger_event", "mcp_tool_call"))
            payload = rep.to_dict()
        elif tool_name == "remediate_vulnerability":
            res = engine.execute_stage("secure")
            payload = {
                "tool": "remediate_vulnerability",
                "requested_cwe": args.get("cwe", "CWE-89"),
                "remediation_result": res.to_dict(),
            }
        elif tool_name == "heal_ci_pipeline":
            res = engine.execute_stage("verify")
            payload = {
                "tool": "heal_ci_pipeline",
                "pipeline_id": args.get("pipeline_id", 8901),
                "healing_result": res.to_dict(),
            }
        elif tool_name == "calculate_sci_score":
            rep = engine.run_full_lifecycle()
            payload = rep.sci_report.to_dict()
        elif tool_name == "generate_sbom":
            payload = engine.generate_cyclonedx_sbom(
                args.get("project_name", "gitlab-stagepilot/payment-webhook-service"),
                args.get("commit_sha", "9f4b2c8e"),
            )
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown MCP tool: {tool_name}"},
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(payload, indent=2)}],
                "structuredContent": payload,
                "isError": False,
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    """Stdio JSON-RPC 2.0 loop for MCP hosts (GitLab Duo Agent Platform)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_mcp_request(req)
        except Exception as exc:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
