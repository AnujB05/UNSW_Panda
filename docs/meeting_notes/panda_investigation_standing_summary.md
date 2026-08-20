# Panda Investigation — Standing Summary
*UNSW Global Taste of Research Practicum, July 2026*

## Context

This project tests whether Panda (Lai, Bao, Gilpin, ICLR 2026) — a 21M-parameter transformer pretrained only on synthetic chaotic ODEs — generalizes beyond that training distribution, benchmarked against Chronos-t5-small (20M params, trained on real-world time series). The original question was simple: does Panda beat Chronos outside chaotic dynamics, and if so, why? It has stayed simple on one side and gotten much harder on the other: **the "does it win" question has solid answers. The "why" question has now produced four consecutive negative results and remains open.**

This document reflects everything through the log's Section 16 (the Chronos horizon-mismatch check), superseding the previous version, which stopped at Section 14.

---

## Bottom line

Panda has a real, repeatedly-confirmed advantage over Chronos on Weather and on non-chaotic Burgers. Every specific explanation tested for *why* — channel attention, the Koopman lifting geometry, temporal attention, Weather's sampling resolution, and (most recently) Chronos being evaluated out of its trained horizon spec — has failed to explain it. Separately, and still the update most worth flagging to the group if it hasn't fully landed yet: **the sensor-heterogeneity finding, previously the strongest mechanistic result in this investigation, did not survive a proper-sample-size replication and has been retired**, along with the entire node-embedding/G-SWaN/XXLTraffic direction it motivated.

Two things are new since the last version of this document: the **Burgers advantage has now been checked for representation-dependence** (it mostly survives), and a **previously-unflagged confound — Chronos being evaluated well outside its trained horizon range for nearly the entire project — has been directly tested and ruled out**, at least for Weather.

---

## What's solid (high confidence, holds up under scrutiny)

- **Panda beats Chronos on Weather** at every tested horizon (H=96/192/336, n=20, p≤0.001), with a strikingly stable relative-skill ratio (~1.27–1.33×) across horizons. Both datasets are confirmed zero-shot for Chronos, so this isn't contamination (Section 1.1).
- **Chaos is not necessary for the advantage.** Panda wins on the plain Harmonic oscillator, the simplest possible periodic system, directly contradicting the original "chaos threshold" story (Experiment 19) — though see the open item below about this result's own sample size.
- **Channel attention does not drive any of this** — four independent null tests across four different experimental designs (Experiments 9, 22, 27, 33), including a proper n=20 rerun. This is now about as settled as anything in the log gets.
- **Panda's advantage is tied to genuine deterministic structure, not just signal statistics** — destroying temporal order while exactly preserving the power spectrum degrades Panda 13× versus Chronos's 2× (Experiment 14 revision). This is currently the single strongest piece of positive evidence in the whole investigation, though it says *that* structure matters, not *how* Panda uses it.
- **The Burgers advantage at ν=0.05 is representation-robust** across three independent spatial-to-channel encodings (PCA, spatial subsampling, Fourier modes) — it isn't an artifact of any one way of turning the PDE field into channels (Section 15).
- **Chronos's out-of-spec evaluation horizon does not explain Panda's Weather advantage.** Chronos is documented as recommending prediction lengths ≤64, and nearly every comparison in this log runs it at H≥96. Moving Chronos into spec (H=64) produced essentially no change in relative skill versus H=96 (1.272→1.273), and moving further in (H=32) moved relative skill the *wrong* direction for the hypothesis (Section 16). This closes a confound that, in principle, sat underneath almost every headline result in the log.

## Branch A: hunting for the positive mechanism — three tested, three failed

**A1 (Koopman lifting ablation, complete):** Established a real behavioral pattern — a fixed dynamics-lift helps on chaotic ODEs and Harmonic, hurts on non-chaotic Burgers. Robust to Bonferroni correction across multiple systems (Section 7). But this describes *that* the lift matters, not *why*.

**A3 (Koopman feature-space geometry, complete):** Directly tested the theoretical account behind A1 — that the lift's benefit comes from linearizing non-chaotic dynamics. Rejected on two independent measures: Burgers, the system this account predicts should show the *cleanest* linear structure, instead shows the *worst* fit of any tested class, and the lift's sensitivity to input perturbation shows no difference between chaotic and non-chaotic systems at all (Section 8).

**A2a (temporal-attention probes, complete):** Cheap inference-time tests found weak, partly self-contradicting evidence — the formal pre-registered gate flips verdict depending on whether you correct for a scale confound, and the one genuinely scale-free signal turned out to be reproducible by plain linear/mean baselines with no attention mechanism at all (Section 9, Experiment 40). Full retrain (A2b) was deprioritized rather than pursued, given this weak evidence base.

**Net effect:** all three tested architectural components have failed to explain A1's own pattern, let alone the broader Weather/Burgers advantage. The mechanism remains genuinely unknown.

## Branch B: mapping where the advantage does and doesn't hold

**B1 (attractor geometry) — retired.** A downsampling control found the Weather-vs-ETTh topological separation doesn't survive matching sampling rate, i.e., it was a measurement artifact, not real geometry (Experiment 31).

**B2 (sensor heterogeneity) — retired.** The original finding (heterogeneous Weather channels degrade Panda specifically, not Chronos) was the strongest convergent mechanistic result in the project for a long time, and directly motivated the node-embedding/G-SWaN/XXLTraffic direction discussed with the group previously. At n=20, run two independent ways, the effect collapsed: an 83% MAE increase at n=8 became a 4% increase at n=20, and at H=336 the direction *reversed entirely* (Experiments 33–34). Determinism, seasonal window clustering, and implementation drift were all directly checked and ruled out — this isn't a bug, it's small-sample noise in the original result. **B2b, B2c, and the associated interventions remain retired.**

**B3c (downsampled-Weather intervention, complete) — the fourth null, and the first that manipulates data rather than architecture.** If Panda's advantage depended on fine temporal structure, hourly-downsampled Weather should hurt Panda specifically. It doesn't: under the cleanest tested convention, neither model's MAE changes significantly (Section 14). Held at moderate confidence — the anchor result in this run is somewhat weaker than the original Weather benchmark for diagnosed, understood reasons — but no support for the hypothesis either way. **The underlying Weather advantage itself is untouched by this result.**

**B3b (Burgers representation test, complete) — mostly reassuring, one loose end.** Motivated by a side-finding in A3, where Burgers' PCA representation turned out to have 11 of 16 channels essentially dead, raising the question of whether the original Burgers advantage was a genuine PDE-generalization result or an artifact of that one representation choice.
- At ν=0.05, the advantage is **representation-robust**: significant and same-signed under PCA, spatial subsampling, and Fourier encodings.
- At ν=1.0, the formal verdict is **MIXED** at both n=8 and a confirmatory n=20 rerun — spatial subsampling stays significant, Fourier does not (p=0.115) — but the n=20 rerun meaningfully improved the picture: Fourier's advantage flipped from negative to positive, now agreeing in direction with the other two representations, just without enough power to prove it. Read together as "probably real everywhere, weakest signal in the Fourier encoding," not as a genuine disagreement between representations.
- Side finding: A3's "dead channel" result for Burgers is re-characterized. Effective rank — the one measure that's directly comparable across representations — turns out to be statistically identical between PCA and Fourier at ν=1.0, despite very different literal dead-channel counts. This points to intrinsic low-dimensionality of ν=1.0 Burgers dynamics (very few true degrees of freedom), not PCA-specific damage.

## A methodological throughline worth calling out explicitly

The heterogeneity retraction is the sharpest illustration of a pattern that shows up repeatedly in this log: **results run at n=8 windows are not reliable enough to build on**, and the project has now directly proven this rather than just worrying about it in the abstract. Several other n=8 results are still sitting in the log without a confirmatory rerun — most notably the Harmonic oscillator advantage (currently the same evidentiary tier the heterogeneity finding sat at before it collapsed) and the complexity-continuum/surrogate-control results.

A second, newer methodological item in the same family: **B3b surfaced evidence that Chronos itself may not be deterministic across repeated calls on an identical window** — one cell showed a ~10% MAE swing between two runs with no change in input, seed, or model. This has never been directly tested (the project's one existing determinism check, Experiment 34's R1, only verified Panda's own reproducibility). If Chronos genuinely varies run-to-run under this project's `num_samples=1` protocol, that's a source of noise sitting underneath every Chronos MAE in the log, not just the one cell where it happened to get noticed — worth a cheap, dedicated check before leaning too hard on any single borderline-significance Chronos comparison.

## What's still genuinely open

After four consecutive negative results on candidate mechanisms — channel attention, Koopman-lift geometry, temporal attention, and resolution-dependency — plus a fifth ruled-out confound (Chronos's horizon mismatch, at least on Weather), nothing in the log currently explains *why* Panda beats Chronos where it does. The leading untested candidate, not yet formally queued or even fully scoped as an experiment, is whether the advantage tracks statistical proximity to Panda's own pretraining distribution (skew40) rather than any single architectural component. This is currently a hypothesis in name only — a concrete pre-registered test (e.g., some distributional distance measure between skew40 and each eval dataset, correlated against measured advantage) still needs to be designed before it can be called more than "next on the list."

## Immediate next steps

1. **Chronos determinism check** — cheap, R1-style repeated-call test on `chronos_forecast`. Newly proposed; not yet in the log's formal queue, but flagged as worth doing before leaning further on borderline Chronos-side results.
2. **Confirmatory n=20 rerun of the Harmonic oscillator advantage** — same risk profile the heterogeneity finding had before it collapsed.
3. **B3a** (Chronos-alone attribution arm on Harmonic variants).
4. **G1/G4** (validity gates) — G1's scope was narrowed this cycle to rollout-horizon claims only (H>128), after checking against the published paper's own evaluation philosophy, and now also absorbs the question of whether those same long-horizon rows need the Chronos horizon-mismatch check extended to them (G5 covered only Weather at H≤96 so far).
