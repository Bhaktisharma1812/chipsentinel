# ChipSentinel

AI-driven program health and early-warning prototype for chip design programs.

**Author:** Bhakti Sharma (M25AI2173), M.Tech. Artificial Intelligence, IIT Jodhpur
**Supervisor:** Dr. Binod Kumar
**Status:** MTP 1 and MTP 2 complete (final report submitted November 2026)

## What it is

ChipSentinel combines three signals into one programme-health view:

| Pillar | What it does | Method |
|---|---|---|
| P1: Validation-gap risk scorer | Flags issues likely to become post-freeze defects | Random forest on OpenTitan issue metadata |
| P2: Buried-blocker detector | Flags stalled dependencies in comment text | TF-IDF + random forest (trained on synthetic text) |
| P3: Dependency graph | Models cross-team dependencies and computes a tape-out readiness score | NetworkX graph + weighted score |

## Main findings (MTP 2)

- Label: a defect reported after an assumed functional freeze (median issue date, 2025-08-22), evaluated on a temporal split (250 issues before, 250 after).
- Pillar 1 under this split: defect F1 = 0.25. The earlier F1 of 0.915 (MTP 1) came from a heuristic label that overlapped with the model inputs.
- Ablation (average precision, chance = 0.17): P1 0.285, P2 0.134, P3 0.221, P1+P2 0.213, P1+P3 0.288, P2+P3 0.146, joint 0.222. The joint model did not beat Pillar 1 alone, and the confidence intervals overlap.
- Simulation proof of concept: an 8-bit ALU with 14 injected bugs, run with iverilog and cocotb. Bugs in poorly covered regions tended to surface late or escape. This is a toy experiment, not evidence about real chips.

## Repository contents

- `Chipsentinel - MTP Project.ipynb`: the full notebook (data extraction, the three pillars, temporal relabelling, joint table, ablation, simulation experiment, dashboard).
- `dashboard/app.py`: Streamlit dashboard.
- `data/`: OpenTitan issue snapshot (June 2026) and synthetic communication data.
- `pillar1/`, `pillar2/`, `pillar3/`: trained models and result figures.
- `sim_results.csv`: output of the iverilog + cocotb experiment.

## How to run

1. Open the notebook in Google Colab.
2. Create your own free GitHub token (Settings, Developer settings, Personal access tokens, scope `public_repo`) and enter it when the notebook asks. Do not share or commit your token.
3. Run the cells in order. Experiments load the saved June 2026 snapshot from this repository, so results match the report.
4. To view the dashboard, run the Streamlit cell. For a public link from Colab, use the ngrok cell with your own free ngrok token.
5. The simulation cell installs Icarus Verilog and cocotb itself and takes about a minute.

## Limitations

- The defect label is a proxy (bug label or failure keyword), and the freeze date is assumed.
- Only 43 positive test cases, so confidence intervals are wide.
- Pillar 2 is trained on synthetic text and did not transfer to real comments.
- The Pillar 3 scenario is hand-specified and illustrative.
- No practitioner interview responses were received.

## Data and tools

OpenTitan (lowRISC) issue data, scikit-learn, NetworkX, Streamlit, Plotly, Icarus Verilog, cocotb.
