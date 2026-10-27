#!/usr/bin/env bash
# ==============================================================================
# GitLab StagePilot — One-Command Demo & Verification Script
# Life After Code: GitLab Transcend Hackathon (2026)
# Author: Kazutoshi Hayashi (LUMA LAB) | License: MIT
# ==============================================================================
set -euo pipefail

cd "$(dirname "$0")"

echo "================================================================================"
echo " 🦊 GitLab StagePilot — 9-Stage Autonomous DevSecOps & SCI GreenOps Engine"
echo "    GitLab Duo Agent Platform + Anthropic Claude + Google Cloud Vertex AI"
echo "================================================================================"
echo ""

echo "▶ [Step 1/4] Running Automated Test Suite (9 Stages, 3 Autonomy Modes, MCP, SCI)..."
python3 -m unittest discover -s tests -v
echo ""

echo "▶ [Step 2/4] Executing Full 9-Stage Hands-Off DevSecOps Lifecycle..."
python3 -m stagepilot.cli run-lifecycle \
  --autonomy hands_off \
  --region us-central1 \
  --trigger "gitlab_webhook:merge_request_and_pipeline_event" \
  --output artifacts/full_lifecycle_report.json \
  --artifacts-dir artifacts
echo ""

echo "▶ [Step 3/4] Generating ISO/IEC 21031:2024 Software Carbon Intensity (SCI) Report..."
python3 -m stagepilot.cli sci-report --region us-central1
echo ""

echo "▶ [Step 4/4] Verifying Model Context Protocol (MCP) JSON-RPC 2.0 Tool Invocation..."
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"evaluate_stage","arguments":{"stage":"secure"}}}' \
  | python3 -m stagepilot.mcp_server | python3 -m json.tool | head -n 28
echo "  ... (MCP JSON-RPC 2.0 response verified)"
echo ""
echo "================================================================================"
echo " ✅ Demo complete! Artifacts generated in ./artifacts/"
echo "    - ./artifacts/full_lifecycle_report.json"
echo "    - ./artifacts/sci_sustainability_report.md"
echo "    - ./artifacts/sbom.cyclonedx.json"
echo " 🌐 To launch the interactive Web Dashboard: python3 -m stagepilot.server --port 8080"
echo "================================================================================"
