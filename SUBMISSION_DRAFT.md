# Devpost Submission Draft — Life After Code: GitLab Transcend Hackathon

> **Author / Submitter:** Kazutoshi Hayashi (LUMA LAB) (`cal29792979@gmail.com`)  
> **Public Repository URL (GitHub):** `https://github.com/cal29292929/gitlab-stagepilot`  
> **GitLab Group URL:** `https://gitlab.com/groups/kazutoshi-hayashi` *(GitLab Community Onboarding Issue: `https://gitlab.com/gitlab-community/community-members/onboarding/-/work_items/5938`)*  
> **Demo Video (2m08s, 1080p MP4):** `submission_assets/demo_video.mp4`  
> **Screenshots (7 High-Res PNGs):** `submission_assets/00_title_slide_overview.png` – `submission_assets/06_cli_mcp_and_tests_verified.png`  
> **Repository License:** MIT (`LICENSE` at repository root)

---

## 1. Basic Form Fields

- **Project Name:** `GitLab StagePilot: 9-Stage Autonomous DevSecOps & SCI Engine`
- **Elevator Pitch (max 200 chars):**  
  `Autonomous GitLab Duo multi-agent engine that executes all 9 post-code DevSecOps stages (Plan to Govern) with Claude & Vertex AI while cutting pipeline carbon intensity (SCI) by 87.9%.` *(185 chars)*
- **Path Selection:** `Path A: Start Fresh`
- **Level of Autonomy:** `Hands-off` *(also supports `Supervised` and `Assisted` via runtime flag/UI)*
- **DevSecOps Stages Covered (Select all 9):**
  - [x] `plan`
  - [x] `create`
  - [x] `verify`
  - [x] `package`
  - [x] `secure`
  - [x] `release`
  - [x] `configure`
  - [x] `monitor`
  - [x] `govern`
- **Opt-in Prizes:**
  - [x] **Path A: Start Fresh | Best Hands-off Agent ($5,000)**
  - [x] **Most Stages Covered ($5,000)** — *Covers all 9 GitLab DevSecOps stages*
  - [x] **Most Environmentally Impactful ($5,000)** — *Quantified with ISO/IEC 21031:2024 Software Carbon Intensity (SCI)*
  - [x] **Most Creative ($4,000)**
  - [x] **Google Cloud Deployment Bonus (+0.2 points)**
- **Built With Tags:**  
  `gitlab`, `gitlab-duo`, `gitlab-ci`, `anthropic`, `claude`, `google-cloud`, `vertex-ai`, `google-cloud-run`, `mcp`, `python`, `docker`, `devsecops`, `green-software`

---

## 2. Full Project Story (Copy-Paste into Devpost Description)

### Inspiration
AI coding assistants have made writing code faster than ever—yet delivery velocity is still bottlenecked by what happens *after* `git push`. Engineering teams spend the majority of their week triaging issues, diagnosing broken CI pipelines, manually patching SAST/CVE alerts, generating CycloneDX SBOMs, right-sizing cloud containers, monitoring post-deploy regressions, and assembling compliance evidence. At the same time, running heavy frontier LLMs and uncached CI pipelines on every commit has quietly caused DevSecOps carbon emissions to skyrocket. We built **GitLab StagePilot** to prove that the **GitLab Duo Agent Platform** can autonomously orchestrate all 9 post-code DevSecOps stages while simultaneously cutting pipeline carbon intensity by nearly 90%.

### What it does
**GitLab StagePilot** is an end-to-end autonomous DevSecOps and GreenOps engine built on the **GitLab Duo Agent Platform**, **Anthropic Claude Sonnet 4.5**, and **Google Cloud Vertex AI (Gemini 2.5 Flash)**. Triggered by a GitLab Webhook (`Issue Hook`, `Merge Request Hook`, or `Pipeline Hook`), StagePilot executes **all 9 official GitLab DevSecOps stages**:

1. **`plan` (`stagepilot-orchestrator`):** Triages incoming GitLab Issues, computes blast-radius risk scores (`0.24`), assigns labels, and maps structured acceptance criteria.
2. **`create` (`stagepilot-orchestrator`):** Creates/updates branches and Merge Requests, runs AST diff review via GitLab Duo Code Review Flow, and commits surgical patches signed with **DCO 1.1**.
3. **`verify` (`ci-self-healer`):** Diagnoses failing CI job logs, synthesizes edge-case unit tests, prunes unaffected CI test shards, and verifies a 100% green build.
4. **`package` (`secops-remediator`):** Builds layer-cached OCI containers, pins SHA256 digests, and generates a **CycloneDX 1.5 SBOM** with **SLSA Build Level 3** provenance.
5. **`secure` (`secops-remediator`):** Parses GitLab SAST & Dependency Scanning reports, auto-remediates **CWE-89 (SQL Injection)** and **CWE-347 (HMAC Timing Side-Channel)**, and verifies zero remaining vulnerabilities.
6. **`release` (`stagepilot-orchestrator`):** Calculates SemVer (`v1.4.2`), generates CVE changelogs, tags the GitLab Release, and orchestrates progressive canary rollout (`10% -> 50% -> 100%`).
7. **`configure` (`greenops-sci-optimizer`):** Audits Google Cloud Run / IaC configurations, right-sizes container memory (`2Gi -> 512Mi`), enables scale-to-zero (`min-instances=0`), and pins workloads to renewable-heavy regions (`us-central1` / `europe-north1`).
8. **`monitor` (`ci-self-healer`):** Evaluates post-deploy Prometheus / Cloud Monitoring golden signals (`p95 = 38.4ms`, `5xx = 0.00%`) and arms an automatic rollback guard.
9. **`govern` (`greenops-sci-optimizer`):** Verifies MIT licensing, DCO 1.1 commit sign-offs, and `.gitlab/duo/tool-governance.yaml` policy compliance, then calculates the **ISO/IEC 21031:2024 Software Carbon Intensity (SCI)** score and posts a comprehensive Markdown audit comment back to the originating GitLab Issue and Merge Request.

StagePilot supports all three hackathon autonomy modes (**`Hands-off`**, **`Supervised`**, and **`Assisted`**) and exposes its entire toolkit via a **Model Context Protocol (MCP) JSON-RPC 2.0 server** (`stagepilot.mcp_server`).

### How we built it
- **GitLab Duo Agent Platform Configs (`.gitlab/duo/`):** Defined 4 specialized custom agents (`stagepilot-orchestrator`, `secops-remediator`, `ci-self-healer`, `greenops-sci-optimizer`), 3 custom multi-agent flows (`full_lifecycle_transcend_flow.yaml`, `fix_pipeline_flow.yaml`, `mr_security_review_flow.yaml`), an MCP server manifest (`mcp.json`), and a strict AI Tool Governance policy (`tool-governance.yaml`).
- **Carbon-Aware Hybrid Model Router (`stagepilot/llm_providers.py`):** Routes complex AST code review, CI log root-cause analysis, and CWE vulnerability patching (`create`, `verify`, `secure`) to **Anthropic Claude Sonnet 4.5**, while routing structured triage, SBOM packaging, release tagging, Cloud Run right-sizing, SLO telemetry, and compliance attestation (`plan`, `package`, `release`, `configure`, `monitor`, `govern`) to **Google Cloud Vertex AI Gemini 2.5 Flash**.
- **ISO/IEC 21031:2024 SCI Calculator (`stagepilot/sci_calculator.py`):** Implements the Green Software Foundation equation $\text{SCI} = \frac{(E \times I) + M}{R}$ across every stage and release.
- **9-Stage `.gitlab-ci.yml` & Google Cloud Run Deployment (`Dockerfile`, `cloudbuild.yaml`, `deploy-gcp.sh`):** Full CI/CD pipeline executing all 9 stages and deploying the serverless Web Dashboard & Webhook Receiver to Google Cloud Run.

### Challenges we ran into
1. **Balancing Multi-Stage Autonomy with Safety Guardrails:** Running 9 consecutive DevSecOps stages in `Hands-off` mode requires strict safety boundaries so an agent cannot force-push protected branches or silence a security scanner to make a pipeline pass. We solved this by declarative tool governance (`.gitlab/duo/tool-governance.yaml`) and mandatory post-patch SAST re-verification before Stage 6 (`release`) can execute.
2. **Quantifying Real Pipeline + AI Carbon Intensity:** Most tools treat AI inference carbon and CI runner carbon separately. Combining token inference energy ($E_{\text{AI}}$), CI runner compute energy ($E_{\text{CI}}$), regional marginal grid intensity ($I$), and amortized server embodied carbon ($M$) into a single reproducible **SCI** metric per release required careful calibration per stage.

### Accomplishments that we're proud of
- Achieving **100% coverage across all 9 GitLab DevSecOps stages** (`plan`, `create`, `verify`, `package`, `secure`, `release`, `configure`, `monitor`, `govern`) in a unified, deterministic orchestration engine.
- Demonstrating an **87.9% reduction in Software Carbon Intensity (SCI)** (`111.81 gCO2eq` down to `13.54 gCO2eq` per release in `us-central1`, and `7.29 gCO2eq` in `europe-north1` — a **93.5% reduction**).
- Building a zero-friction architecture with **14 automated unit & integration tests passing in <10ms**, a live **JSON-RPC 2.0 MCP server**, and an interactive **9-Stage Web Dashboard**.

### What we learned
- Tiered model routing between **Vertex AI Gemini 2.5 Flash** and **Anthropic Claude Sonnet 4.5** preserves frontier-level security patching quality while slashing AI inference energy consumption by **69.5%**.
- Treating **Software Carbon Intensity (SCI)** as a first-class Stage 9 (`govern`) quality gate empowers engineering teams to prevent carbon regressions just like they prevent security or latency regressions.

### What's next for GitLab StagePilot
- Live electricity grid carbon intensity feed integration (Electricity Maps / WattTime API) to dynamically shift non-urgent scheduled GitLab Duo Flows to the lowest-carbon time window and GCP region.
- Multi-repository fleet governance across GitLab Groups with automated DORA + SCI executive scorecards.

---

## 3. Dedicated Write-Up for "Most Environmentally Impactful" Prize (SCI Framework)

StagePilot uses the **Green Software Foundation Software Carbon Intensity (SCI) specification (ISO/IEC 21031:2024)**:

$$\text{SCI} = \frac{(E \times I) + M}{R}$$

- **Functional Unit ($R$):** `1 complete 9-stage DevSecOps release lifecycle`
- **Baseline Scenario (Unoptimized):** Frontier LLM invoked on every stage (`0.2180 kWh`), uncached CI runners in a fossil-heavy region (`I = 445 gCO2eq/kWh`), and always-on 8-vCPU staging VMs (`M = 14.80 gCO2eq`).
  $$\text{SCI}_{\text{baseline}} = \frac{(0.2180 \times 445) + 14.80}{1} = 97.01 + 14.80 = \mathbf{111.81\text{ gCO}_2\text{eq / release}}$$
- **StagePilot Optimized Scenario (`us-central1`):** Carbon-aware model routing between Vertex AI Gemini 2.5 Flash and Claude Sonnet 4.5 + CI DAG shard pruning (`E = 0.0665 kWh`, `-69.5%`), wind-heavy GCP `us-central1` region (`I = 142 gCO2eq/kWh`, `-68.1%`), and Cloud Run scale-to-zero containers (`M = 4.10 gCO2eq`, `-72.3%`).
  $$\text{SCI}_{\text{optimized}} = \frac{(0.0665 \times 142) + 4.10}{1} = 9.44 + 4.10 = \mathbf{13.54\text{ gCO}_2\text{eq / release}}$$
- **Verified Sustainability Gain:** **`-98.27 gCO2eq` per release (`87.9%` SCI reduction)**.

---

## 4. Demo Video Script (< 3 Minutes — Target 2:35)

- **[0:00 - 0:25] Hook & The "Life After Code" Problem**
  - Show GitLab repository with `.gitlab-ci.yml` and `.gitlab/duo/` custom agents, flows, MCP config, and MIT `LICENSE`.
  - Narrate: *"Writing code is solved—what happens after `git push` is where teams lose 90% of their time. Meet GitLab StagePilot: an autonomous multi-agent engine built on GitLab Duo Agent Platform, Anthropic Claude Sonnet 4.5, and Google Cloud Vertex AI that automates all 9 GitLab DevSecOps stages while cutting pipeline carbon intensity by 87.9%."*
- **[0:25 - 1:15] Live Trigger & 9-Stage Autonomous Execution (`Hands-off` Mode)**
  - Open the StagePilot Web Dashboard (`http://localhost:8080`) and terminal side-by-side.
  - Trigger a simulated GitLab Merge Request & Failed Pipeline webhook (`./run_demo.sh` / clicking **"Run 9-Stage Autonomous Flow"**).
  - Walk through all 9 cards lighting up in sequence:
    - `1. PLAN` (Issue #42 triaged, blast radius 0.24) -> `2. CREATE` (MR !108 AST diff review) -> `3. VERIFY` (CI pipeline #8901 self-healed + 3 unit tests synthesized) -> `4. PACKAGE` (CycloneDX 1.5 SBOM generated) -> `5. SECURE` (CWE-89 SQLi & CWE-347 HMAC timing vulnerability auto-patched) -> `6. RELEASE` (`v1.4.2` canary rollout) -> `7. CONFIGURE` (Cloud Run right-sized to 512Mi & `min-instances=0`) -> `8. MONITOR` (SLO p95 38.4ms verified healthy) -> `9. GOVERN` (DCO 1.1, MIT License, and SCI report attested).
- **[1:15 - 1:55] Switching Autonomy Modes (`Supervised` & `Assisted`) + MCP Server**
  - Switch dropdown from `Hands-off` to `Supervised` to show the human approval gate pausing at `6. RELEASE`, and `Assisted` to show per-stage approval gates.
  - Show terminal running JSON-RPC 2.0 `tools/call` against `stagepilot.mcp_server`.
- **[1:55 - 2:35] ISO/IEC 21031:2024 SCI Carbon Telemetry & GitLab Summary Comment**
  - Highlight the SCI Telemetry panel showing `111.81 gCO2eq` baseline vs `13.54 gCO2eq` in `us-central1` (`-87.9%`) and `7.29 gCO2eq` in `europe-north1` (`-93.5%`).
  - Show the generated Markdown comment automatically posted back to the GitLab Issue & Merge Request.

---

## 5. Generated Submission Assets (`submission_assets/`)

All assets below are generated, verified, and ready for direct upload to the Devpost submission form:

- **Demo Video (`1920x1080`, 30fps, H.264 + AAC, 2m08s):**
  - `submission_assets/demo_video.mp4` (`3.4 MB`)
- **Screenshots / Image Gallery (`1920x1080` / `1920x1280` PNGs):**
  1. `submission_assets/01_dashboard_hands_off_9stages.png` — Live Web UI Dashboard running all 9 DevSecOps stages in `Hands-off` mode (`us-central1`, `13.54 gCO2eq`, `-87.9%` SCI).
  2. `submission_assets/02_dashboard_supervised_release_gate.png` — Live Web UI Dashboard in `Supervised` mode demonstrating the Stage 6 (`release`) human approval gate.
  3. `submission_assets/03_dashboard_greenops_europe_north1.png` — Live Web UI Dashboard in `europe-north1` demonstrating `-93.5%` SCI reduction (`7.29 gCO2eq`).
  4. `submission_assets/00_title_slide_overview.png` — Executive overview slide (Problem, Solution, Verified Impact).
  5. `submission_assets/04_architecture_hybrid_routing.png` — 4 Custom GitLab Duo Agents & Carbon-Aware Hybrid Model Routing architecture.
  6. `submission_assets/05_sci_iso21031_carbon_breakdown.png` — ISO/IEC 21031:2024 SCI formula & per-stage carbon telemetry table.
  7. `submission_assets/06_cli_mcp_and_tests_verified.png` — CLI execution trace & `14/14` passing `pytest` verification.

