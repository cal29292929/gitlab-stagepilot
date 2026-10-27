"""Command-line interface for GitLab StagePilot."""

import argparse
import json
from pathlib import Path
from typing import List, Optional

from stagepilot.lifecycle_engine import StagePilotEngine
from stagepilot.models import AutonomyLevel, DevSecOpsStage
from stagepilot.sci_calculator import render_sci_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stagepilot",
        description="GitLab StagePilot: 9-Stage Autonomous DevSecOps & SCI GreenOps CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_stage = sub.add_parser("run-stage", help="Execute a single GitLab DevSecOps stage")
    p_stage.add_argument("--stage", required=True, choices=[s.value for s in DevSecOpsStage.ordered()])
    p_stage.add_argument("--autonomy", default="hands_off", choices=[m.value for m in AutonomyLevel])
    p_stage.add_argument("--region", default="us-central1")
    p_stage.add_argument("--output", default="")

    p_life = sub.add_parser("run-lifecycle", help="Execute all 9 GitLab DevSecOps stages end-to-end")
    p_life.add_argument("--autonomy", default="hands_off", choices=[m.value for m in AutonomyLevel])
    p_life.add_argument("--region", default="us-central1")
    p_life.add_argument("--trigger", default="cli_manual_trigger")
    p_life.add_argument("--output", default="")
    p_life.add_argument("--artifacts-dir", default="artifacts")

    p_sci = sub.add_parser("sci-report", help="Print ISO/IEC 21031:2024 SCI Markdown report")
    p_sci.add_argument("--region", default="us-central1")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run-stage":
        engine = StagePilotEngine(autonomy_mode=args.autonomy, region=args.region)
        res = engine.execute_stage(args.stage)
        data = res.to_dict()
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            if args.stage == "package":
                sbom_path = out_path.parent / "sbom.cyclonedx.json"
                sbom_path.write_text(
                    json.dumps(engine.generate_cyclonedx_sbom("gitlab-stagepilot", "9f4b2c8e"), indent=2),
                    encoding="utf-8",
                )
        print(json.dumps(data, indent=2))
        return 0

    if args.command == "run-lifecycle":
        engine = StagePilotEngine(autonomy_mode=args.autonomy, region=args.region)
        report = engine.run_full_lifecycle(
            trigger_event=args.trigger,
            artifacts_dir=args.artifacts_dir,
        )
        data = report.to_dict()
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[StagePilot] Run ID: {report.run_id}")
        print(f"[StagePilot] Autonomy Mode: {report.autonomy_mode.upper()}")
        print(f"[StagePilot] DevSecOps Stages Covered: {report.stages_covered_count}/9")
        print(
            f"[StagePilot] SCI Score: {report.sci_report.sci_score_optimized_gco2_per_r:.2f} gCO2eq/release "
            f"(Baseline: {report.sci_report.sci_score_baseline_gco2_per_r:.2f} gCO2eq, "
            f"-{report.sci_report.reduction_percentage:.1f}% reduction)"
        )
        return 0

    if args.command == "sci-report":
        engine = StagePilotEngine(autonomy_mode="hands_off", region=args.region)
        report = engine.run_full_lifecycle()
        print(render_sci_markdown_report(report.sci_report))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
