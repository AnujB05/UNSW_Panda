# Burgers univariate ablation completed

## Human

ok uploaded burgers univariate ablation in project files. Now everything we planned is compelte. See our last chat (keyerror in Burgers) for where we left off.

## Assistant

Let me read the final result.


```
This block is not supported on your current device yet.
```


## Analysis: Burgers Univariate Ablation

**[OBS]** Complete table:

| nu | panda_multi | panda_uni | delta (uni−multi) | adv_multi | adv_uni | p_multi | p_uni |
|---|---|---|---|---|---|---|---|
| 2.0 | 0.0094 | 0.0078 | **−0.0016** | 0.0058 | 0.0010 | 0.055 | 0.273 |
| 1.0 | 0.0165 | 0.0126 | **−0.0040** | −0.0019 | 0.0034 | 0.320 | 0.004 |
| 0.5 | 0.0235 | 0.0241 | **+0.0006** | 0.0331 | 0.0231 | 0.004 | 0.004 |

**[OBS — critical]** At nu=2.0 and nu=1.0, panda_uni has *lower* MAE than panda_multi (delta negative — channel attention makes things worse). At nu=0.5, they are essentially tied (delta +0.0006, negligible).

**[OBS]** At nu=1.0: panda_multi shows no significant advantage over Chronos (p=0.320, adv=−0.0019), but panda_uni does show significant advantage (p=0.004, adv=+0.0034). Channel attention is actively harming the Burgers non-chaotic advantage at this viscosity.

**[OBS]** At nu=0.5: both multi and uni show significant Panda advantage (p=0.004 for both). Channel attention is neutral here.

---

## What This Changes

**[PAT — strong]** Across all three tested viscosity levels, channel attention does not help Panda on Burgers. At non-chaotic viscosities (nu=2.0, nu=1.0), it actively hurts. This is the same direction as the Weather univariate ablation result (panda_uni slightly better than panda_multi there too).

**This directly challenges the hypothesis that channel attention drives any of Panda's advantage.** The pattern is consistent across two completely different datasets — Weather (heterogeneous real sensors) and Burgers (homogeneous PDE channels).

**[OBS — cross-reference]** From exp22_node_embeddings: node offsets help on hetero_controlled (+0.037) and hurt on homo_matched (−0.085). From the Burgers univariate ablation: suppressing channel attention helps at non-chaotic nu. These two results are directionally consistent — channel attention is doing something, but it is *not* helping.

---

## Revised Narrative — What the Full Dataset Now Shows

Stating what is observed, not what is explained.

**Across all ablations touching channel attention:**

| Experiment | Dataset | Effect of suppressing/modifying channel attention |
|---|---|---|
| Univariate ablation (Weather) | H=96: uni better by 0.057 (p=0.074); H=336: uni better by 0.030 (p=0.371) | Channel attention marginal negative |
| Node offsets (hetero_controlled) | H=96: offsets help (+0.037) | Channel attention modification directionally useful |
| Node offsets (homo_matched) | H=96: offsets hurt (−0.085) | Channel attention modification context-dependent |
| Burgers univariate (nu=2.0) | delta=−0.0016, uni wins | Channel attention marginal negative |
| Burgers univariate (nu=1.0) | delta=−0.0040, uni wins | Channel attention negative — and kills the advantage |
| Burgers univariate (nu=0.5) | delta=+0.0006, effectively tied | Channel attention neutral |

**[PAT]** Channel attention consistently fails to help and often hurts. The positive Panda advantage over Chronos — on Weather, on Burgers, on Lorenz — is **not explained by channel attention**. Something else in the temporal architecture (patching, Koopman lifting, non-causal encoder) is the positive mechanism.

**Competing explanations for why channel attention hurts:**

1. Channel attention was trained on chaotic ODE state variables where coupling is strong, deterministic, and homogeneous. On PDE modes and real sensors, the cross-channel signal is weaker or structured differently — attention adds noise. [Medium confidence]
2. The permutation-equivariant attention with no positional encoding cannot distinguish which channel is which, so it cannot exploit the spatial/semantic structure of the channels — it scrambles information. [Medium confidence, consistent with node offset result]
3. The effect size is small and n=8 is underpowered — what looks like "channel attention hurts" may be noise. [Medium confidence — cannot rule out]

---

## Honest Summary of Where We Stand

**What is established with some confidence:**

- [PAT, medium] Channel attention does not drive Panda's advantage on any tested dataset. Univariate Panda is competitive or better on Weather and Burgers.
- [PAT, medium] Sensor heterogeneity degrades Panda but not Chronos, even after difficulty and variance matching. This is a genuine failure mode.
- [OBS, high] The positive mechanism — why Panda beats Chronos at all — is not identified. No ablation has isolated it.
- [OBS, medium] Head finetuning hurts. Prediction head alone is not the bottleneck that can be recovered cheaply.
- [OBS, low-medium] Weather and Lorenz have similar topology estimates; ETTh is different. Single noisy measurement, insufficient to act on.

**What is not established:**

- Why Panda beats Chronos on Weather, Burgers, and Lorenz. The temporal architecture (Koopman lifting, patching, non-causal encoder) is the remaining candidate but has no direct ablation.
- Whether the Harmonic oscillator advantage (+0.370) reflects Panda strength or Chronos weakness on sinusoidal inputs.
- Whether any of Flora's suggested directions (G-SWaN, topological flow matching, TimesNet pretraining) would actually improve generalization.

**The central open question going into the Tuesday meeting** is: if channel attention is not the positive mechanism and not the primary bottleneck, what is? The Koopman lifting is the last major untested component, and it cannot be ablated without code access to Panda's internals. That is the honest gap.

## Human

ok so every planned experiment complete. Let us first update our experiment log. I will give you the current latex code
First tell me, do you remember the instructions to write the log?

## Assistant

Yes. The instructions for writing the log are:

1. Written in third person
2. No hyphens (avoid `---` em-dashes throughout)
3. Use the label commands: `\obs{}`, `\pat{}`, `\hyp{}`, `\spec{}`, `\est{}`
4. Separate observation from explanation explicitly
5. Assign confidence levels using `\highconf`, `\medconf`, `\lowconf`, `\verylow`
6. Generate competing explanations for every major claim
7. Maintain the same level of detail and structure as the existing sections

The new experiments to add (from the last chat) are:

- **Exp 19**: Complexity continuum (Harmonic → VanderPol → Duffing → Rossler → Lorenz)
- **Exp 20**: Chronos residual ablation on Weather
- **Exp 21**: Permutation entropy predictor (failed — PE at order=3 cannot discriminate)
- **Exp 22**: Node embeddings (scalar offset proxy)
- **Exp 23**: Head finetuning
- **Topology analysis**
- **Heterogeneity stratification** (het_stratification, difficulty_matched, hetero_controlled, chronos_heterogeneity)
- **Burgers univariate ablation** (the final cell that just completed)

Let me read all the CSVs to get exact numbers before writing.


```
This block is not supported on your current device yet.
```

