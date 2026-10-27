import json
import unittest
from pathlib import Path

from stagepilot.mcp_server import handle_mcp_request


ROOT = Path(__file__).resolve().parent.parent


class TestMCPAndConfigs(unittest.TestCase):
    def test_mcp_initialize_and_tools_list(self) -> None:
        init_resp = handle_mcp_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(init_resp["result"]["serverInfo"]["name"], "stagepilot-mcp")

        list_resp = handle_mcp_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tool_names = [t["name"] for t in list_resp["result"]["tools"]]
        self.assertEqual(
            set(tool_names),
            {
                "evaluate_stage",
                "run_full_lifecycle",
                "remediate_vulnerability",
                "heal_ci_pipeline",
                "calculate_sci_score",
                "generate_sbom",
            },
        )

    def test_mcp_tool_calls(self) -> None:
        call_resp = handle_mcp_request(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "evaluate_stage", "arguments": {"stage": "secure"}},
            }
        )
        self.assertFalse(call_resp["result"]["isError"])
        self.assertEqual(call_resp["result"]["structuredContent"]["stage"], "secure")

    def test_required_repository_files_exist(self) -> None:
        required_files = [
            "LICENSE",
            ".gitlab-ci.yml",
            "Dockerfile",
            "cloudbuild.yaml",
            ".gitlab/duo/mcp.json",
            ".gitlab/duo/tool-governance.yaml",
            ".gitlab/duo/agents/stagepilot_orchestrator.yaml",
            ".gitlab/duo/agents/secops_remediator.yaml",
            ".gitlab/duo/agents/ci_self_healer.yaml",
            ".gitlab/duo/agents/greenops_sci_optimizer.yaml",
            ".gitlab/duo/flows/full_lifecycle_transcend_flow.yaml",
        ]
        for rel in required_files:
            self.assertTrue((ROOT / rel).exists(), f"Missing required file: {rel}")

        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)

        mcp_cfg = json.loads((ROOT / ".gitlab/duo/mcp.json").read_text(encoding="utf-8"))
        self.assertIn("stagepilot-mcp", mcp_cfg["mcpServers"])


if __name__ == "__main__":
    unittest.main()
