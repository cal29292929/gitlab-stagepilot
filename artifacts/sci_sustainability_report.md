### 🌱 Software Carbon Intensity (SCI) Sustainability Report (ISO/IEC 21031:2024)

$$\text{SCI} = \frac{(E \times I) + M}{R}$$

- **Functional Unit ($R$):** 1 complete 9-stage DevSecOps release lifecycle
- **Baseline SCI Score:** `111.81 gCO2eq / release`
- **StagePilot Optimized SCI Score:** `13.54 gCO2eq / release`
- **Net Carbon Reduction:** **`-98.27 gCO2eq` (`87.9%` reduction)**

| Metric | Unoptimized Baseline | StagePilot GreenOps | Delta |
| :--- | :---: | :---: | :---: |
| Energy Consumed ($E$) | `0.2180 kWh` | `0.0665 kWh` | `-69.5%` |
| Grid Carbon Intensity ($I$) | `445 gCO2eq/kWh` | `142 gCO2eq/kWh` | `-68.1%` |
| Operational Emissions ($E \times I$) | `97.01 gCO2eq` | `9.44 gCO2eq` | `-90.3%` |
| Embodied Emissions ($M$) | `14.80 gCO2eq` | `4.10 gCO2eq` | `-72.3%` |
| **Total SCI Score** | **`111.81 gCO2eq`** | **`13.54 gCO2eq`** | **`-87.9%`** |

#### Applied GreenOps Optimizations
- Carbon-Aware Model Routing: Tiered inference routing between Vertex AI Gemini 2.5 Flash (stages: plan, package, release, configure, monitor, govern) and Anthropic Claude Sonnet 4.5 (stages: create, verify, secure), cutting AI inference energy by 69.5%.
- Selective CI DAG Pruning & Dependency Layer Caching: Avoided redundant container rebuilds and skipped unaffected test shards in Verify/Package stages.
- Low-Carbon Cloud Region Pinning (us-central1): Scheduled CI runners and Cloud Run workloads on renewable-heavy grid (142.0 vs 445.0 gCO2eq/kWh).
- Scale-to-Zero Serverless Execution: Eliminated idle staging VM embodied & operational emissions via Google Cloud Run min-instances=0.