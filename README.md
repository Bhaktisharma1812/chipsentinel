# ChipSentinel 🛡️
### AI-driven Program Health & Early Warning for Chip Design Programs

**Researcher:** Bhakti Sharma | M25AI2173 | M.Tech AI | IIT Jodhpur  
**Supervisor:** Dr. Binod Kumar | IIT Jodhpur  
**Project Start:** May 15, 2026 | **Phase 1 Target:** June 15, 2026

---

## The Problem

Chip design programs span 11 phases from architecture to tape-out, involving 8–12 parallel teams. By the time a risk shows red on a dashboard, the schedule has already slipped. A single tape-out respin costs $1M–$30M.

ChipSentinel reads across three AI-powered signals and tells senior leadership — in plain English — what is actually at risk before it becomes a crisis.

---

## Workflow Coverage

| Design Phase | Coverage | Signal |
|---|---|---|
| Architecture & Spec | ❌ Gap | Phase 2 scope |
| RTL Design | ⚠️ Partial | RTL churn rate after freeze → Pillar 1 feature |
| Functional Verification | ✅ Covered | Pillar 1 + Pillar 2 — core of ChipSentinel |
| Logic Synthesis | ❌ Gap | Phase 2 scope |
| DFT Insertion | ⚠️ Partial | Explicit high-risk node in Pillar 3 |
| Physical Design | ⚠️ Partial | Team node in Pillar 3 + DRC count input |
| Timing Closure | ❌ Gap | Phase 2 scope |
| DRC / LVS Signoff | ⚠️ Partial | DRC rate feeds Pillar 3 readiness score |
| Tape-out & Foundry | ⚠️ Partial | Tape-out readiness score |
| Post-Silicon | ➖ Out of scope | Pre-silicon tool only |

---

## Three Pillars

| Pillar | What it does | Key signals |
|---|---|---|
| **P1 — Validation Gap Risk Scorer** | Flags which coverage gaps are likely to cause a tape-out escape | Bug density, block criticality, RTL churn after freeze, DRC violation rate |
| **P2 — Buried Blocker Detection** | Surfaces Jira threads where dependencies are going nowhere | NLP on ticket text, escalation failure patterns, ownership gaps |
| **P3 — Dependency Graph & Readiness Score** | Models inter-team dependencies, flags critical path slip | DFT as high-risk node, dependency health, DRC closure rate |

All three feed a **single LLM-generated 60-second plain-English brief** for senior leadership.

---

## DFT — Explicitly Modelled as High-Risk Node

DFT is the most commonly delayed team in chip programs. Pillar 3 flags three specific early warnings:
- RTL freeze delayed → DFT start at risk
- DFT sign-off not started at 80% DV coverage → critical path alert
- DFT team blockers with no response for 5+ days → escalate

---

## Data Sources

- **OpenTitan** — Google's open-source SoC. Real coverage reports, bug logs, PR history, RTL commit history (2021–present)
- **DARPA OpenROAD** — DRC violation counts and synthesis QoR data
- **Synthetic dataset** — 500–1,000 labelled Jira tickets and standup notes from practitioner interviews

---

## Phase 1 Progress (May 15 – June 15, 2026)

- [x] Proposal submitted to Dr. Binod Kumar
- [x] GitHub repository created and structured
- [ ] OpenTitan data extracted and labelled
- [ ] Pillar 1 baseline model running
- [ ] Synthetic Jira dataset generated
- [ ] Pillar 2 NLP classifier running
- [ ] Pillar 3 dependency graph with DFT node
- [ ] Streamlit dashboard — end-to-end demo
- [ ] Phase 1 report submitted

## Phase 2 (Post June 15)

- [ ] Timing closure risk model
- [ ] Architecture/spec freeze risk signal
- [ ] Full GNN for Pillar 3
- [ ] Joint model + ablation study
- [ ] Conference paper — MLCAD / DAC AI track
- [ ] Provisional patent filing
## Folder Structure

chipsentinel/
├── data/               # OpenTitan + synthetic datasets
├── pillar1/            # Validation gap risk scorer
├── pillar2/            # Buried blocker NLP detector
├── pillar3/            # Dependency graph + readiness score
├── dashboard/          # Streamlit demo app
└── report/             # Project report
