"""
Green Software Foundation Software Carbon Intensity (SCI) Engine (ISO/IEC 21031:2024).

Formula:
    SCI = ((E * I) + M) / R

Where:
    E = Energy consumed by the software system (kWh) across CI runners, containers, and AI inference
    I = Location-based marginal carbon intensity of electricity grid (gCO2eq / kWh)
    M = Embodied emissions of hardware amortized over time-share & lifespan (gCO2eq)
    R = Functional unit (1 complete 9-stage DevSecOps lifecycle release)
"""

from typing import Dict, List, Tuple
from stagepilot.models import SCIBreakdown, StageExecutionResult


# Regional grid carbon intensities (gCO2eq / kWh)
GRID_CARBON_INTENSITY_GCO2_KWH: Dict[str, float] = {
    "us-east-1-unoptimized": 445.0,     # High-carbon fossil-heavy baseline grid
    "us-central1": 142.0,               # Google Cloud Iowa wind-powered low-carbon region
    "europe-north1": 48.0,              # Google Cloud Finland hydro/wind region
}

# Per-call AI model inference + CI runner energy profile (kWh)
STAGE_ENERGY_PROFILE_KWH: Dict[str, Tuple[float, float, str]] = {
    # stage: (baseline_kwh, optimized_kwh, selected_model)
    "plan": (0.0180, 0.0042, "vertex_ai/gemini-2.5-flash"),
    "create": (0.0260, 0.0115, "anthropic/claude-sonnet-4-5"),
    "verify": (0.0420, 0.0140, "anthropic/claude-sonnet-4-5 + cached-ci-runner"),
    "package": (0.0310, 0.0085, "vertex_ai/gemini-2.5-flash + layer-cache"),
    "secure": (0.0290, 0.0120, "anthropic/claude-sonnet-4-5"),
    "release": (0.0150, 0.0038, "vertex_ai/gemini-2.5-flash"),
    "configure": (0.0220, 0.0050, "vertex_ai/gemini-2.5-flash + cloud-run-scale-to-zero"),
    "monitor": (0.0190, 0.0040, "vertex_ai/gemini-2.5-flash"),
    "govern": (0.0160, 0.0035, "vertex_ai/gemini-2.5-flash"),
}

# Hardware embodied carbon amortized per 9-stage pipeline execution (gCO2eq)
BASELINE_EMBODIED_M_GCO2 = 14.80    # Dedicated unshared 8-vCPU CI VM + idle staging server
OPTIMIZED_EMBODIED_M_GCO2 = 4.10    # Ephemeral right-sized 1-vCPU runner + Cloud Run scale-to-zero


def calculate_stage_carbon(
    stage: str,
    region: str = "us-central1",
) -> Tuple[float, float, float, str]:
    """
    Return (optimized_energy_kwh, optimized_carbon_gco2, baseline_carbon_gco2, model_used)
    for a single DevSecOps stage.
    """
    baseline_kwh, opt_kwh, model_used = STAGE_ENERGY_PROFILE_KWH.get(
        stage, (0.0200, 0.0060, "vertex_ai/gemini-2.5-flash")
    )
    baseline_intensity = GRID_CARBON_INTENSITY_GCO2_KWH["us-east-1-unoptimized"]
    opt_intensity = GRID_CARBON_INTENSITY_GCO2_KWH.get(region, 142.0)

    stage_baseline_m = BASELINE_EMBODIED_M_GCO2 / 9.0
    stage_opt_m = OPTIMIZED_EMBODIED_M_GCO2 / 9.0

    baseline_gco2 = round((baseline_kwh * baseline_intensity) + stage_baseline_m, 4)
    opt_gco2 = round((opt_kwh * opt_intensity) + stage_opt_m, 4)
    return opt_kwh, opt_gco2, baseline_gco2, model_used


def calculate_lifecycle_sci(
    stage_results: List[StageExecutionResult],
    region: str = "us-central1",
    functional_units: int = 1,
) -> SCIBreakdown:
    """
    Compute the full ISO/IEC 21031:2024 SCI breakdown across executed stages.
    SCI = ((E * I) + M) / R
    """
    r = max(1, functional_units)
    baseline_intensity = GRID_CARBON_INTENSITY_GCO2_KWH["us-east-1-unoptimized"]
    opt_intensity = GRID_CARBON_INTENSITY_GCO2_KWH.get(region, 142.0)

    total_opt_energy_kwh = round(sum(s.energy_kwh for s in stage_results), 6)
    total_base_energy_kwh = round(
        sum(STAGE_ENERGY_PROFILE_KWH.get(s.stage, (0.02, 0.006, ""))[0] for s in stage_results),
        6,
    )

    scale = len(stage_results) / 9.0 if stage_results else 1.0
    embodied_opt = round(OPTIMIZED_EMBODIED_M_GCO2 * scale, 4)
    embodied_base = round(BASELINE_EMBODIED_M_GCO2 * scale, 4)

    operational_opt = round(total_opt_energy_kwh * opt_intensity, 4)
    operational_base = round(total_base_energy_kwh * baseline_intensity, 4)

    sci_opt = round((operational_opt + embodied_opt) / r, 4)
    sci_base = round((operational_base + embodied_base) / r, 4)

    saved = round(max(0.0, sci_base - sci_opt), 4)
    reduction_pct = round((saved / sci_base) * 100.0, 2) if sci_base > 0 else 0.0

    return SCIBreakdown(
        functional_unit_r="1 complete 9-stage DevSecOps release lifecycle",
        energy_kwh_optimized=total_opt_energy_kwh,
        energy_kwh_baseline=total_base_energy_kwh,
        grid_intensity_gco2_kwh_optimized=opt_intensity,
        grid_intensity_gco2_kwh_baseline=baseline_intensity,
        operational_emissions_o_gco2=operational_opt,
        embodied_emissions_m_gco2=embodied_opt,
        sci_score_optimized_gco2_per_r=sci_opt,
        sci_score_baseline_gco2_per_r=sci_base,
        carbon_saved_gco2=saved,
        reduction_percentage=reduction_pct,
        optimizations_applied=[
            "Carbon-Aware Model Routing: Tiered inference routing between Vertex AI Gemini 2.5 Flash (stages: plan, package, release, configure, monitor, govern) and Anthropic Claude Sonnet 4.5 (stages: create, verify, secure), cutting AI inference energy by 69.5%.",
            "Selective CI DAG Pruning & Dependency Layer Caching: Avoided redundant container rebuilds and skipped unaffected test shards in Verify/Package stages.",
            f"Low-Carbon Cloud Region Pinning ({region}): Scheduled CI runners and Cloud Run workloads on renewable-heavy grid ({opt_intensity} vs {baseline_intensity} gCO2eq/kWh).",
            "Scale-to-Zero Serverless Execution: Eliminated idle staging VM embodied & operational emissions via Google Cloud Run min-instances=0.",
        ],
    )


def render_sci_markdown_report(sci: SCIBreakdown) -> str:
    """Format an ISO/IEC 21031:2024 SCI Markdown table for GitLab Merge Request & Release notes."""
    lines = [
        "### 🌱 Software Carbon Intensity (SCI) Sustainability Report (ISO/IEC 21031:2024)",
        "",
        "$$\\text{SCI} = \\frac{(E \\times I) + M}{R}$$",
        "",
        f"- **Functional Unit ($R$):** {sci.functional_unit_r}",
        f"- **Baseline SCI Score:** `{sci.sci_score_baseline_gco2_per_r:.2f} gCO2eq / release`",
        f"- **StagePilot Optimized SCI Score:** `{sci.sci_score_optimized_gco2_per_r:.2f} gCO2eq / release`",
        f"- **Net Carbon Reduction:** **`-{sci.carbon_saved_gco2:.2f} gCO2eq` (`{sci.reduction_percentage:.1f}%` reduction)**",
        "",
        "| Metric | Unoptimized Baseline | StagePilot GreenOps | Delta |",
        "| :--- | :---: | :---: | :---: |",
        f"| Energy Consumed ($E$) | `{sci.energy_kwh_baseline:.4f} kWh` | `{sci.energy_kwh_optimized:.4f} kWh` | `-{((1 - sci.energy_kwh_optimized / sci.energy_kwh_baseline) * 100):.1f}%` |",
        f"| Grid Carbon Intensity ($I$) | `{sci.grid_intensity_gco2_kwh_baseline:.0f} gCO2eq/kWh` | `{sci.grid_intensity_gco2_kwh_optimized:.0f} gCO2eq/kWh` | `-{((1 - sci.grid_intensity_gco2_kwh_optimized / sci.grid_intensity_gco2_kwh_baseline) * 100):.1f}%` |",
        f"| Operational Emissions ($E \\times I$) | `{sci.energy_kwh_baseline * sci.grid_intensity_gco2_kwh_baseline:.2f} gCO2eq` | `{sci.operational_emissions_o_gco2:.2f} gCO2eq` | `-{((1 - sci.operational_emissions_o_gco2 / (sci.energy_kwh_baseline * sci.grid_intensity_gco2_kwh_baseline)) * 100):.1f}%` |",
        f"| Embodied Emissions ($M$) | `{BASELINE_EMBODIED_M_GCO2:.2f} gCO2eq` | `{sci.embodied_emissions_m_gco2:.2f} gCO2eq` | `-{((1 - sci.embodied_emissions_m_gco2 / BASELINE_EMBODIED_M_GCO2) * 100):.1f}%` |",
        f"| **Total SCI Score** | **`{sci.sci_score_baseline_gco2_per_r:.2f} gCO2eq`** | **`{sci.sci_score_optimized_gco2_per_r:.2f} gCO2eq`** | **`-{sci.reduction_percentage:.1f}%`** |",
        "",
        "#### Applied GreenOps Optimizations",
    ]
    for opt in sci.optimizations_applied:
        lines.append(f"- {opt}")
    return "\n".join(lines)
