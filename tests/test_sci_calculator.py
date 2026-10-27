import unittest
from stagepilot.lifecycle_engine import StagePilotEngine
from stagepilot.sci_calculator import (
    calculate_lifecycle_sci,
    calculate_stage_carbon,
    render_sci_markdown_report,
)


class TestSCICalculator(unittest.TestCase):
    def test_stage_carbon_savings(self) -> None:
        opt_kwh, opt_gco2, base_gco2, model = calculate_stage_carbon("verify", region="us-central1")
        self.assertGreater(base_gco2, opt_gco2)
        self.assertGreater(opt_kwh, 0.0)
        self.assertIn("claude", model)

    def test_full_lifecycle_sci_formula_and_reduction(self) -> None:
        engine = StagePilotEngine(autonomy_mode="hands_off", region="us-central1")
        report = engine.run_full_lifecycle()
        sci = report.sci_report
        self.assertEqual(report.stages_covered_count, 9)
        self.assertGreater(sci.sci_score_baseline_gco2_per_r, sci.sci_score_optimized_gco2_per_r)
        self.assertGreater(sci.reduction_percentage, 65.0)
        self.assertAlmostEqual(
            sci.sci_score_optimized_gco2_per_r,
            round(sci.operational_emissions_o_gco2 + sci.embodied_emissions_m_gco2, 4),
            places=3,
        )

    def test_low_carbon_region_improves_sci(self) -> None:
        engine_us = StagePilotEngine(autonomy_mode="hands_off", region="us-central1")
        engine_eu = StagePilotEngine(autonomy_mode="hands_off", region="europe-north1")
        sci_us = engine_us.run_full_lifecycle().sci_report
        sci_eu = engine_eu.run_full_lifecycle().sci_report
        self.assertLess(sci_eu.sci_score_optimized_gco2_per_r, sci_us.sci_score_optimized_gco2_per_r)

    def test_render_sci_markdown(self) -> None:
        engine = StagePilotEngine(autonomy_mode="hands_off", region="us-central1")
        sci = calculate_lifecycle_sci(engine.run_full_lifecycle().stage_results)
        md = render_sci_markdown_report(sci)
        self.assertIn("ISO/IEC 21031:2024", md)
        self.assertIn("gCO2eq", md)


if __name__ == "__main__":
    unittest.main()
