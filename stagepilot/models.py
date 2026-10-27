"""Data models for GitLab StagePilot across all 9 DevSecOps stages and 3 autonomy levels."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class DevSecOpsStage(str, Enum):
    """All 9 official GitLab DevSecOps lifecycle stages."""
    PLAN = "plan"
    CREATE = "create"
    VERIFY = "verify"
    PACKAGE = "package"
    SECURE = "secure"
    RELEASE = "release"
    CONFIGURE = "configure"
    MONITOR = "monitor"
    GOVERN = "govern"

    @classmethod
    def ordered(cls) -> List["DevSecOpsStage"]:
        return [
            cls.PLAN,
            cls.CREATE,
            cls.VERIFY,
            cls.PACKAGE,
            cls.SECURE,
            cls.RELEASE,
            cls.CONFIGURE,
            cls.MONITOR,
            cls.GOVERN,
        ]


class AutonomyLevel(str, Enum):
    """GitLab Transcend Hackathon official autonomy levels."""
    ASSISTED = "assisted"        # Human approves each stage action
    SUPERVISED = "supervised"    # Multi-step agent execution; human approves production release gate
    HANDS_OFF = "hands_off"      # Fully autonomous end-to-end execution + summary posted back


@dataclass
class SecurityFinding:
    finding_id: str
    cve_or_cwe: str
    severity: str
    title: str
    file_path: str
    line_number: int
    vulnerable_snippet: str
    remediated_snippet: str
    status: str = "detected"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StageExecutionResult:
    stage: str
    stage_index: int
    agent_name: str
    model_used: str
    autonomy_mode: str
    status: str  # "completed", "awaiting_human_approval", "rolled_back"
    requires_human_approval: bool
    approved_automatically: bool
    summary: str
    actions_taken: List[str]
    artifacts: Dict[str, Any]
    energy_kwh: float
    carbon_gco2eq: float
    baseline_carbon_gco2eq: float
    duration_ms: int
    dco_signed_off: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SCIBreakdown:
    """ISO/IEC 21031:2024 Software Carbon Intensity (SCI) metrics: SCI = ((E * I) + M) / R"""
    functional_unit_r: str
    energy_kwh_optimized: float
    energy_kwh_baseline: float
    grid_intensity_gco2_kwh_optimized: float
    grid_intensity_gco2_kwh_baseline: float
    operational_emissions_o_gco2: float
    embodied_emissions_m_gco2: float
    sci_score_optimized_gco2_per_r: float
    sci_score_baseline_gco2_per_r: float
    carbon_saved_gco2: float
    reduction_percentage: float
    optimizations_applied: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LifecycleRunReport:
    run_id: str
    project_name: str
    trigger_event: str
    autonomy_mode: str
    started_at_utc: str
    completed_at_utc: str
    stages_covered_count: int
    total_stages_available: int
    overall_status: str
    stage_results: List[StageExecutionResult]
    sci_report: SCIBreakdown
    gitlab_summary_comment_markdown: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "project_name": self.project_name,
            "trigger_event": self.trigger_event,
            "autonomy_mode": self.autonomy_mode,
            "started_at_utc": self.started_at_utc,
            "completed_at_utc": self.completed_at_utc,
            "stages_covered_count": self.stages_covered_count,
            "total_stages_available": self.total_stages_available,
            "overall_status": self.overall_status,
            "stage_results": [s.to_dict() for s in self.stage_results],
            "sci_report": self.sci_report.to_dict(),
            "gitlab_summary_comment_markdown": self.gitlab_summary_comment_markdown,
        }
