import json
import unittest

from stagepilot.server import dispatch_http_request


class TestAPIServer(unittest.TestCase):
    def test_health_and_dashboard_routes(self) -> None:
        status, ctype, body = dispatch_http_request("GET", "/api/health")
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(len(data["stages_supported"]), 9)

        status_html, ctype_html, html_bytes = dispatch_http_request("GET", "/")
        self.assertEqual(status_html, 200)
        self.assertIn("GitLab StagePilot", html_bytes.decode("utf-8"))

    def test_post_run_and_gitlab_webhook(self) -> None:
        status, _, body = dispatch_http_request(
            "POST",
            "/api/run",
            json.dumps({"autonomy_mode": "hands_off", "region": "us-central1"}).encode("utf-8"),
        )
        self.assertEqual(status, 200)
        rep = json.loads(body.decode("utf-8"))
        self.assertEqual(rep["stages_covered_count"], 9)

        status_wh, _, wh_body = dispatch_http_request(
            "POST",
            "/api/webhook/gitlab",
            json.dumps({"object_kind": "merge_request", "merge_request": {"iid": 204}}).encode("utf-8"),
            headers={"X-Gitlab-Event": "Merge Request Hook"},
        )
        self.assertEqual(status_wh, 200)
        wh_rep = json.loads(wh_body.decode("utf-8"))
        self.assertEqual(wh_rep["trigger_event"], "gitlab_webhook:Merge Request Hook")

    def test_post_mcp_over_http(self) -> None:
        status, _, body = dispatch_http_request(
            "POST",
            "/api/mcp",
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 99,
                    "method": "tools/call",
                    "params": {"name": "calculate_sci_score", "arguments": {"region": "europe-north1"}},
                }
            ).encode("utf-8"),
        )
        self.assertEqual(status, 200)
        mcp_resp = json.loads(body.decode("utf-8"))
        self.assertGreater(mcp_resp["result"]["structuredContent"]["reduction_percentage"], 70.0)


if __name__ == "__main__":
    unittest.main()
