# Result-status notes

Per CLAUDE.md: a retracted or retired result must not sit undifferentiated next to
an established one. Statuses below are taken from the project's own experiment tree
in `experiment_log.tex` / the `panda_experiment_tree.html` at repo root. Files were
organised by topic, **not** by status — this file is the status overlay.

## ⛔ RETRACTED — do not present as current findings

**Harmonic Oscillator advantage** (originally part of Experiment 19). Cause: an
explicit-Euler generator bug produced an unstable eigenvalue. Under the corrected
stable generator the advantage collapsed 98.8% and reversed sign.

| File | Status |
|---|---|
| `notebooks/mechanistic/harmonic_n20_confirmatory.ipynb` (2026-07-17 15:26) | ⛔ **RETRACTED** — pre-stable-generator |
| `data/raw_results/harmonic_n20_confirmatory_results.csv` | ⛔ **RETRACTED** — pre-stable-generator |
| `data/raw_results/koopman_ablation_harmonic.csv` (2026-06-29) | ⛔ **RETRACTED** — predates the fix |
| `data/raw_results/exp19_complexity_continuum.csv` | ⚠️ **MIXED** — the Harmonic rows only are retracted; the rest of the continuum stands |
| `notebooks/mechanistic/harmonic_n20_stable_generator.ipynb` (2026-07-17 19:36) | ✅ **CURRENT** — post-correction |
| `data/raw_results/harmonic_n20_stable_generator_results.csv` | ✅ **CURRENT** — post-correction |
| `data/raw_results/a1_harmonic_recheck_stable.csv` | ✅ **CURRENT** — `*_stable*`, post-correction |

**ETTh2 H=336 significant result**: did not replicate independently (p=0.013 → p=0.088).
Affects rows inside `data/raw_results/overnight_results/04_etth2_h336_replication.csv`
and any ETTh2 H=336 row in the Experiment 8 benchmark CSVs.

## 🔻 RETIRED / superseded

| File | Status |
|---|---|
| `notebooks/benchmarking/week1_experiments.ipynb`, `data/raw_results/week1_results.csv` | Exp 7 — **retired, invalid (oracle leakage)**. Superseded by Exp 8. |
| `data/raw_results/panda_benchmark_results.csv` | Exp 1 — **retired**, superseded by Exp 8 / `_v2` |
| `data/raw_results/p3_burgers_lambda1_results.csv` | Exp 15 — **retired**, estimator invalid |
| `data/raw_results/exp21_permutation_entropy.csv`, `fixed_exp21_results.csv` | Exp 21 — **retired** |
| `data/raw_results/het_stratification_results.csv` | Exp 24 — **retired** |
| `data/raw_results/difficulty_matched_results.csv` | Exp 25 — **retired** |
| `data/raw_results/hetero_controlled_results.csv` | Exp 26 — **retired** |
| `data/raw_results/b2a_results.csv`, `b2a_per_channel.csv`, `notebooks/mechanistic/b2a_univariate_hetero_discriminator.ipynb` | Exp 33 — **retired, COLLAPSED** (heterogeneity 83% → 4%) |
| `data/raw_results/r1_r2_results.csv`, `notebooks/mechanistic/r1_r2_heterogeneity_replication.ipynb`, `docs/meeting_notes/r1_r2_summary.txt` | Exp 34 — **retired**; confirms 33's collapse, high confidence |
| all `data/raw_results/tda_*` + `notebooks/mechanistic/tda_*` | B1 / Exp 29–31 — **retired, ARTIFACT verdict**. Exp 29 stands as *instrument only*. |
| `data/unsorted/raw_predictions/b2a_raw_predictions/` | Raw predictions behind the retired Exp 33 |

⚠️ The entire **B2a/B2b/B2c sensor-heterogeneity branch** — once the project's
"strongest finding" — is fully retired. That is a large fraction of
`notebooks/mechanistic/` and `data/raw_results/`.

## ⭐ Flagship / established

| File | Status |
|---|---|
| `data/raw_results/p2_lorenz_surrogate_results.csv` | **Exp 14 — FLAGSHIP RESULT** (Lorenz phase surrogate control) |
| `data/raw_results/panda_benchmark_results_v2.csv` | Exp 8 — established |
| `data/raw_results/fixed_burgers_results.csv` | Exp 10 — established |
| `data/raw_results/b3b_representation_results.csv`, `b3b_unified_results.csv` | Exp 42–43 / B3b — established |
| `data/raw_results/weather_univariate_advantage.csv` + notebook | Exp 45 — established, cleanest of the 5 channel-attention nulls |
| `data/raw_results/g1_part2a_published_checkpoints.csv`, `g1_part2b_retrained_checkpoints.csv`, `g1ext_part{A,B}_*.csv` | **G1 — ACTIVE, strongest current positive lead** |
| `data/raw_results/topology_analysis.csv` | Early corr-dim pilot, precursor to G1 |

## Note on version-suffixed files
`tda_gate_validation_v3` supersedes `_v2` supersedes the unsuffixed original;
`b3b_burgers_representation_test_v4` supersedes `_v2`; `panda_benchmark_results_v2`
supersedes `panda_benchmark_results`. All versions were kept — these are
author-assigned versions, not download duplicates.
