import tempfile
import unittest
from pathlib import Path

from stagepilot.lifecycle_engine import StagePilotEngine
from stagepilot.models import DevSecOpsStage


class TestLifecycleEngine(unittest.TestCase):
    def test_all_9_stages_covered_in_hands_off_mode(self) -> None:
        engine = StagePilotEngine(autonomy_mode="hands_off")
        report = engine.run_full_lifecycle(trigger_event="gitlab_issue_hook")
        self.assertEqual(report.stages_covered_count, 9)
        self.assertEqual(report.overall_status, "completed_autonomous")
        executed_names = [s.stage for s in report.stage_results]
        self.assertEqual(executed_names, [s.value for s in DevSecOpsStage.ordered()])
        for res in report.stage_results:
            self.assertEqual(res.status, "completed")
            self.assertTrue(res.dco_signed_off)

    def test_supervised_mode_gates_only_release_stage(self) -> None:
        engine = StagePilotEngine(autonomy_mode="supervised")
        report = engine.run_full_lifecycle()
        self.assertEqual(report.overall_status, "completed_with_approval_gates")
        waiting = [s.stage for s in report.stage_results if s.status == "awaiting_human_approval"]
        self.assertEqual(waiting, ["release"])

    def test_assisted_mode_gates_all_stages(self) -> None:
        engine = StagePilotEngine(autonomy_mode="assisted")
        report = engine.run_full_lifecycle()
        waiting = [s.stage for s in report.stage_results if s.status == "awaiting_human_approval"]
        self.assertEqual(len(waiting), 9)

    def test_artifacts_and_cyclonedx_sbom_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = StagePilotEngine(autonomy_mode="hands_off")
            engine.run_full_lifecycle(artifacts_dir=tmpdir)
            self.assertTrue((Path(tmpdir) / "full_lifecycle_report.json").exists())
            self.assertTrue((Path(tmpdir) / "sci_sustainability_report.md").exists())
            self.assertTrue((Path(tmpdir) / "sbom.cyclonedx.json").exists())


if __name__ == "__main__":
    unittest.main()
