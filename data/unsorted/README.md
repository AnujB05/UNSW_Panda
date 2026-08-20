# data/unsorted

Files that did not map to a known experiment number or to any folder CLAUDE.md
defines. Nothing was guessed, and nothing was dropped.

| Item | Count | Why it's here |
|---|---|---|
| `input_datasets/{ETTh1,ETTh2,weather}.csv` | 3 | Input datasets (12.2 MB), not experiment results. `data/raw_results/` is defined as results-only. Sources for Exp 8/9/24/30/31/44/45 and G3/G4. |
| `raw_predictions/b3c_raw_predictions/*.npz` | 120 | Raw per-window prediction arrays behind B3c (null). |
| `raw_predictions/b2a_raw_predictions/*.npz` | 7 | Raw prediction arrays behind Exp 33 (B2a) — ⛔ retired, see `STATUS_NOTES.md`. |
| `figures/*.png` | 23 | Experiment figures (`results_*`, `exp*_*`, `tda_*`, `a2a_*`, `b2a_summary`, `spatio_*`). CLAUDE.md's structure defines no figures folder. |
| `a2a_full_results.json` | 1 | The only JSON result artefact; A2a probes (Exp 37–40). |
| `loss_history_baseline_seg2.csv` | 1 | Training-loss trace from `panda-80k-baseline-checkpoint/`, not an experiment result. |

If you want any of these promoted (e.g. `figures/` to a top-level `figures/`, or
the datasets to `data/input/`), it's a rename away — they're grouped, not scattered.
