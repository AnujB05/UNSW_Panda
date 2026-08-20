# Project Context: Panda vs. Chronos Forecasting Benchmark

UNSW Global Taste of Research Summer Practicum 2026, under Prof. Flora Salim
(UNSW Sydney), postdoc Toan as day-to-day collaborator. Project benchmarks
Panda (GilpinLab/panda, chaotic-ODE-pretrained transformer) against Chronos
(amazon/chronos-t5-small) and investigates why/how Panda generalizes beyond
its training distribution. Ran ~2 months (June-August 2026). Canonical record
is `experiment_log.tex` — strictly append-only, corrections are dated addenda,
never silent rewrites. This file exists so file organization respects that
same principle: don't relabel a retracted/retired result as if it were live.

## CRITICAL: Duplicate-file handling

Downloads almost certainly contains multiple copies of the same logical file
(re-downloads, Chrome/Windows auto-suffixing). Rules, in order:

1. **Detect duplicates by base name, ignoring OS/browser suffixes** — patterns
   like ` (1)`, ` (2)`, `__1_`, `__2_`, ` - Copy`, `-Copy` appended before the
   extension. `g1_correlation_dimension.ipynb`,
   `g1_correlation_dimension (1).ipynb`, and
   `g1_correlation_dimension__2_.ipynb` are the SAME logical file.
2. **Within a duplicate group, keep the one with the latest file-modified
   timestamp** (not the latest suffix number — download order and edit
   recency aren't guaranteed to match). Copy only that one into the new repo,
   named without the suffix (e.g. `g1_correlation_dimension.ipynb`).
3. **Before discarding, diff file sizes / content hashes across the group.**
   If they're identical, discard duplicates freely. If sizes/content
   genuinely differ (not just a re-download, but a real edited version vs an
   older draft), do NOT silently pick one — list the conflicting group
   (all paths, sizes, mtimes) in the final report so I can pick manually.
   This matters most for notebooks, since two versions with the same name but
   different cell content is a real "which one is current" decision, not a
   dedup decision.
4. Report a summary at the end: how many duplicate groups found, how many
   resolved automatically (identical content), how many need manual review
   (content differs).

## Master experiment index

Numbered experiments (1-45) plus named branches (A1-A3, B1-B4, G1-G5) from
`experiment_log.tex`. Status tags (established / active / mixed / null /
retired / retracted) are from the project's own experiment tree — use them to
decide whether a file represents a CURRENT finding or a SUPERSEDED one; don't
let a retracted result's file sit undifferentiated next to an established one
without a note.

| # | Topic | Status |
|---|---|---|
| 1 | Standard TS Benchmarks, initial (ETTh1/ETTh2/Weather) | retired (superseded by 8) |
| 2 | Double Pendulum Graded Noise | mixed |
| 3 | Lorenz Rho Sweep | mixed |
| 4 | dysts Systems, advantage vs lambda1 | mixed (p-hacked, confounded) |
| 5 | Burgers Viscosity Sweep, first version | retired (superseded by 10) |
| 6 | PCA vs Spatial Subsampling, first version | retired (superseded by 12) |
| 7 | Standard Horizon Evaluation, Week 1 | retired (invalid, oracle leakage) |
| 8 | Standard Horizon Evaluation, fixed | established |
| 9 | Univariate Ablation on Weather | null (1 of 4 channel-attention nulls) |
| 10 | Burgers Viscosity Sweep, fixed | established |
| 11 | FFT Decomposition Preprocessing, fixed | mixed |
| 12 | Subsampling Methods, fixed | null |
| 13 | Periodic Component Forecasting (constructed target) | retired (superseded by 18) |
| 14 | Lorenz Phase Surrogate Control | established — FLAGSHIP RESULT |
| 15 | Burgers lambda1 Estimation from PCA | retired (estimator invalid) |
| 16 | Multi-Seed Subsampling Variance | null |
| 17 | Improved Period Projection in Decomposition | active/mixed |
| 18 | Periodic Context with Real Targets | mixed |
| 19 | Complexity Continuum (5 systems) | mixed; Harmonic portion RETRACTED (see below) |
| 20 | Chronos Residual Ablation | mixed |
| 21 | Permutation Entropy as Complexity Predictor | retired |
| 22 | Node Identity Embeddings (scalar offset proxy) | null (channel-attention null) |
| 23 | Prediction Head Fine-Tuning | null |
| 24 | Heterogeneity Stratification on Weather | retired (part of collapsed finding) |
| 25 | Difficulty-Matched Heterogeneity Control | retired |
| 26 | Variance-CV Heterogeneity Control | retired |
| 27 | (channel-attention null, referenced alongside 9/22/33) | null |
| 28 | Koopman Ablation at 50k steps (preliminary) | mixed/preliminary |
| 29 | TDA Gate Validation v1-v3 | established (instrument only) |
| 30 | Real-Data Structure Statistic (Weather/ETTh1/ETTh2) | mixed |
| 31 | Weather Downsampling Control | retired (ARTIFACT verdict) |
| 32 | Structure-Heterogeneity Unification Check | retired |
| 33 | B2a Three-Arm Discriminator (n=20) | retired (heterogeneity COLLAPSE: 83%->4%) |
| 34 | Independent Replication R1+R2, closing verdict | retired (confirms 33's collapse, high confidence) |
| 35 | eDMD Reconstruction Residual | null (part of A3) |
| 36 | Jacobian Sensitivity of the Fixed Lift | null (part of A3) |
| 37 | A2a Probe 1 — Patch-Order Shuffling | mixed (ambiguous, not robust) |
| 38 | A2a Probe 2 — Context-Length Truncation | null |
| 39 | A2a Probe 3 — Attention-Map Inspection | mixed (descriptive only) |
| 40 | A2a Addendum — Trivial-Baseline Control | null |
| 41 | (Branch B design/intervention experiment) | mixed |
| 42 | Burgers representation test, initial (n=8) | mixed |
| 43 | Confirmatory rerun, nu=1.0 arm (n=20) | established |
| 44 | Weather Dose-Response | established |
| 45 | Univariate Panda vs Chronos, full 21-channel Weather | established (5th channel-attn null, cleanest sig.) |

**Named branches / gates (not numbered 1-45):**
- **G1**: Correlation-Dimension Revalidation + Rollout-Structure Preservation — ACTIVE, currently the strongest positive lead (Double Pendulum + Lorenz rho=10, published checkpoints; Rossler/Burgers/Harmonic, retrained checkpoints). Files: `g1_correlation_dimension*.ipynb`, `g1_part2a_*.csv`, `g1_part2b_*.csv`, `topology_analysis.csv` (earlier pilot).
- **G2**: Confirmatory n=20 reruns (established, overlaps Exp 33)
- **G3**: Chronos contamination check (established — ETT/Jena-Weather confirmed absent from Chronos training corpus)
- **G4**: Classical baseline column (established — seasonal-naive beats both models on ETTh2 H=96)
- **G5**: Chronos horizon-mismatch check (null)
- **A1**: Koopman Lifting Ablation, 100k campaign (mixed — established behavioral pattern, mechanism unexplained). Files reference `baseline_100k` / `ablation_100k` checkpoints.
- **A2a**: Temporal Attention Probes = Experiments 37-40 (null overall)
- **A2b**: Temporal Attention Ablation, retrain — NOT run, deprioritized (active/unpursued)
- **A3**: Koopman Feature-Space Geometry = Experiments 35-36 (null — falsifies Koopman-linearization theory)
- **B1**: Structure statistic / TDA investigation = Experiments 29-31 (retired, artifact)
- **B2a/B2b/B2c**: Sensor heterogeneity + node embeddings + XXLTraffic (ALL RETIRED — this was once "strongest finding," fully collapsed via Exp 33-34)
- **B3a**: Chronos attribution / periods-in-window (active lead — patch-size-alignment candidate)
- **B3b**: Burgers representation test = Experiments 42-43 (established)
- **B3c**: Downsampled Weather intervention (null)
- **B4**: Forward-looking interventions (active) — trainable Koopman lift, gating hybrid router, LoRA/fine-tune on ETTh, ERA5/BARRA-R real chaotic weather

**RETRACTED results — flag clearly, do not present as current findings:**
- **Harmonic Oscillator advantage** (originally part of Exp 19): explicit-Euler generator bug (unstable eigenvalue), advantage collapsed 98.8% and reversed sign under the corrected stable generator. Any file with "harmonic" data from BEFORE the stable-generator fix is retracted; only `*_stable*` or post-correction Harmonic files are current.
- **ETTh2 H=336 significant result**: did not replicate independently (p=0.013 -> p=0.088).

## Known CSV files -> experiment mapping (from files already confirmed in the project)

| Filename | Maps to |
|---|---|
| `panda_benchmark_results.csv`, `panda_benchmark_results_v2.csv` | Exp 1/8 |
| `week1_results.csv` | Exp 7 (retired/invalid) |
| `fixed_burgers_results.csv` | Exp 10 |
| `fixed_subsampling_results.csv` | Exp 12 |
| `p1_periodic_results.csv` | Exp 13/18 |
| `p2_lorenz_surrogate_results.csv` | Exp 14 (flagship) |
| `p3_burgers_lambda1_results.csv` | Exp 15 (retired) |
| `p4_subsampling_seeds_results.csv` | Exp 16 |
| `p5_improved_projection_results.csv` | Exp 17 |
| `exp19_complexity_continuum.csv` | Exp 19 (Harmonic portion retracted) |
| `exp20_chronos_residual.csv` | Exp 20 |
| `exp21_permutation_entropy.csv`, `fixed_exp21_results.csv` | Exp 21 |
| `exp22_node_embeddings.csv`, `fixed_exp22_results.csv` | Exp 22 |
| `exp23_head_finetuning.csv` | Exp 23 |
| `het_stratification_results.csv` | Exp 24 |
| `difficulty_matched_results.csv` | Exp 25 |
| `hetero_controlled_results.csv` | Exp 26 or the variance-CV control |
| `chronos_heterogeneity_results.csv` | Chronos heterogeneity calibration (near Section 6 revision) |
| `topology_analysis.csv` | Early corr-dim pilot, precursor to G1/Exp 29-31 |
| `burgers_univariate_ablation.csv` | Channel-attention null series (9/22/27/33), Burgers-specific |

Any CSV NOT in this table: infer from filename against the Master Experiment
Index above (e.g. `expNN_*` -> Experiment NN); if no match, put in
`data/unsorted/` and flag by name in the final report rather than guessing.

## Known non-CSV deliverables to look for

- `experiment_log.tex` — canonical log, root of repo
- A 23-slide Beamer presentation deck (LaTeX or PDF) with spoken script
- The 77-node D3 HTML experiment tree (`panda_experiment_tree*.html` —
  already provided as reference for this file, but Downloads may have an
  earlier/different-numbered version; keep the latest by mtime, per dedup rule)
- `g1_correlation_dimension*.ipynb` and Kaggle notebooks for: Exp 45
  (univariate Weather), Duffing integrator audit, 100k Koopman resume/eval
  (baseline/ablation), A2a temporal-attention probes
  (`a2a_temporal_attention_probes.ipynb`)
- `tda_persistent_homology_notebook.py` (Jupytext `# %%` format)
- MOMENT lift-transplant experiment plan (design doc, not yet run)
- A theory reference document (Koopman/eDMD, Takens, NG-RC, Lyapunov/attractor theory)
- `ideas_list*.pdf` — 24-idea discussion list, also may exist as markdown
- Meeting/brainstorm prep docs, chat transcripts (exported `.md`, often named
  like `Claude-<topic>.md`)

## Folder structure to build

```
UNSW_Panda/
  experiment_log.tex
  panda_experiment_tree.html
  presentation/              # slide deck + spoken script
  notebooks/
    benchmarking/            # Exp 1,2,3,5,6,7,8,10,11,12 and their p1-p5/fixed_* variants
    mechanistic/             # Exp 9,15,16,19-23,27,28,35-40 (A1/A2a/A3), 24-26,29-34 (heterogeneity+TDA, incl RETRACTED)
    rollout_topology/        # G1 notebooks and results
    intervention_plans/      # MOMENT transplant plan, B4 items (not-yet-run designs)
  data/
    raw_results/             # all CSVs, per mapping table above
    unsorted/                # CSVs not matched to a known experiment number
  docs/
    ideas_list.pdf
    theory_reference/
    meeting_notes/
    chat_transcripts/
  duplicate_review/          # anything from rule 3 above that needs manual resolution -- do NOT silently pick
```

## General rules

- Copy only, never move or delete from the original Downloads folder.
- Do not commit `.safetensors`, `.bin`, or any file over ~50MB to git; list
  checkpoint file paths (e.g. `panda-100k-baseline-checkpoint/`,
  `panda-100k-ablation-checkpoint/`) separately and add to `.gitignore`.
- Every file found should end up SOMEWHERE in the structure — unmatched files
  go to the relevant `unsorted/` folder with a note, not silently dropped.
- Before finishing: report total files found in Downloads (recursive count,
  by extension) vs. total files copied (including unsorted/), and the
  duplicate-resolution summary from the section above. These should
  reconcile; if they don't, say so explicitly.
