# Resolving KeyError in Burgers mechanism investigation

## Human

ok so organised everything into this project
first go through our chats once to gain the understanding, where we were latest. (understading non-linear dynamics was our first chat, continuing previous chat was the next chat, understanding topological flow was just a secondary chat.) I have attached .md files of them. Other things are csvs of all the experiments done till now, and report and ppt. Also, I have attached chatgpt's chat where he analysed our ongoing project.

So, recently, our last cell of new_experiments notebook was running (burgers mechanism investigation)
It ran:

```
Burgers Non-Chaotic PDE Mechanism: Univariate Ablation
Question: Is channel attention driving the non-chaotic Burgers advantage?
----------------------------------------------------------------------

  nu=2.0:
```


```
Burgers_nu2.0_multi                                 H=  96  panda=0.0094[±0.0042]  chronos=0.0152[±0.0205]  Adv=+0.0058  p=0.055 ~
```


```
Burgers_nu2.0_uni                                   H=  96  panda_uni=0.0078[±0.0059]  chronos=0.0088[±0.0107]  Adv=+0.0010  p=0.273

```

then this error came:

```
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[29], line 50
     46     if r_multi and r_uni:
     47         adv_multi = r_multi['advantage_mae']
     48         adv_uni   = r_uni['advantage_mae']
     49         p_multi   = r_multi['panda_mae']
---> 50         p_uni     = r_uni['panda_mae']
     51         delta     = p_uni - p_multi  # positive = channel attention helps
     52 
     53         print(f'    Panda multi MAE: {p_multi:.4f}  adv={adv_multi:.4f}')

KeyError: 'panda_mae'
```

let us first resolve this before any other analysis. First tell me do you remember the code (it is in the chats)

## Assistant

 Looking at the error, the issue is that when `name_a="panda_uni"`, the result dict has key `"panda_uni_mae"` not `"panda_mae"`. The `evaluate` function constructs keys dynamically using `name_a`.

Run this fix cell:

```python
# Fixed cell — replace r_uni['panda_mae'] with dynamic key lookup

burgers_uni_results = []

for nu in [2.0, 1.0, 0.5]:
    print(f'\n  nu={nu}:')
    U        = simulate_burgers_stable(T=1500, N_x=128, nu=nu)
    pca_data = pca_reduction(U, 16)
    data_CT  = pca_data.T  # (16, T)

    r_multi = evaluate(data_CT, PRED_LEN, n_windows=N_WINDOWS,
                       label=f'Burgers_nu{nu}_multi')

    r_uni = evaluate(data_CT, PRED_LEN, n_windows=N_WINDOWS,
                     label=f'Burgers_nu{nu}_uni',
                     fn_a=panda_forecast_univariate_burgers,
                     fn_b=chronos_forecast,
                     name_a='panda_uni', name_b='chronos')

    if r_multi and r_uni:
        adv_multi = r_multi['advantage_mae']
        adv_uni   = r_uni['advantage_mae']
        p_multi   = r_multi['panda_mae']
        p_uni     = r_uni['panda_uni_mae']   # <-- fix: use name_a prefix
        delta     = p_uni - p_multi

        print(f'    Panda multi MAE: {p_multi:.4f}  adv={adv_multi:.4f}')
        print(f'    Panda uni   MAE: {p_uni:.4f}  adv={adv_uni:.4f}')
        print(f'    Delta (uni-multi): {delta:+.4f}  '
              f'(negative = channel attention helps)')

        burgers_uni_results.append({
            'nu': nu, 'panda_multi': p_multi, 'panda_uni': p_uni,
            'adv_multi': adv_multi, 'adv_uni': adv_uni, 'delta': delta,
            'p_multi': r_multi['wilcoxon_p'], 'p_uni': r_uni['wilcoxon_p'],
        })
```

The nu=2.0 results are already printed so you have those. This cell will rerun from nu=2.0 — if you want to skip it and start from nu=1.0 to save time, just change the loop to `for nu in [1.0, 0.5]:` and manually append the nu=2.0 row first.

## Human

I have already given you the results of nu = 2. Hard code it directly and give me the cell to run directly so that final csv gives all required resuls

## Assistant

 ```python
# Nu=2.0 results already observed — hardcode them
burgers_uni_results = [
    {
        'nu': 2.0,
        'panda_multi': 0.0094, 'panda_uni': 0.0078,
        'adv_multi': 0.0058,   'adv_uni': 0.0010,
        'delta': 0.0078 - 0.0094,  # = -0.0016
        'p_multi': 0.055,           'p_uni': 0.273,
    }
]

for nu in [1.0, 0.5]:
    print(f'\n  nu={nu}:')
    U        = simulate_burgers_stable(T=1500, N_x=128, nu=nu)
    pca_data = pca_reduction(U, 16)
    data_CT  = pca_data.T

    r_multi = evaluate(data_CT, PRED_LEN, n_windows=N_WINDOWS,
                       label=f'Burgers_nu{nu}_multi')

    r_uni = evaluate(data_CT, PRED_LEN, n_windows=N_WINDOWS,
                     label=f'Burgers_nu{nu}_uni',
                     fn_a=panda_forecast_univariate_burgers,
                     fn_b=chronos_forecast,
                     name_a='panda_uni', name_b='chronos')

    if r_multi and r_uni:
        adv_multi = r_multi['advantage_mae']
        adv_uni   = r_uni['advantage_mae']
        p_multi   = r_multi['panda_mae']
        p_uni     = r_uni['panda_uni_mae']
        delta     = p_uni - p_multi

        print(f'    Panda multi MAE: {p_multi:.4f}  adv={adv_multi:.4f}')
        print(f'    Panda uni   MAE: {p_uni:.4f}  adv={adv_uni:.4f}')
        print(f'    Delta (uni-multi): {delta:+.4f}')

        burgers_uni_results.append({
            'nu': nu, 'panda_multi': p_multi, 'panda_uni': p_uni,
            'adv_multi': adv_multi, 'adv_uni': adv_uni, 'delta': delta,
            'p_multi': r_multi['wilcoxon_p'], 'p_uni': r_uni['wilcoxon_p'],
        })

df_bu = pd.DataFrame(burgers_uni_results)
df_bu.to_csv('burgers_univariate_ablation.csv', index=False)
print('\nSaved burgers_univariate_ablation.csv')

print('\n=== Burgers Univariate Ablation Summary ===')
print(f'{"nu":>6} | {"p_multi":>8} | {"p_uni":>8} | '
      f'{"adv_multi":>10} | {"adv_uni":>9} | {"delta":>7}')
print('-' * 60)
for _, row in df_bu.iterrows():
    print(f'{row.nu:>6} | {row.panda_multi:>8.4f} | {row.panda_uni:>8.4f} | '
          f'{row.adv_multi:>10.4f} | {row.adv_uni:>9.4f} | {row.delta:>+7.4f}')
```

## Human

ok sure
now
till this cell is running
we have completed all other experiments that we had planned (check the results in the project files) - confirm this, if there's anything I missed.
What is the overall narrative

## Assistant

 Let me read through all the result files first.


```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```


Good. I have all the data. Now the picture is clear.

**What is missing:** The Burgers univariate ablation CSV (`burgers_univariate_ablation.csv`) — that cell is still running. Everything else is done.

---

## Overall Narrative — Observations Only First, Then Patterns, Then Hypotheses

### What is completed

Every planned experiment is done except the currently running Burgers univariate ablation. That result will add one more piece to the Burgers mechanism question.

---

### What the data collectively shows

**[OBS] P1 — Periodic context, real targets (Option A already known):**
The periodic-only results show Panda advantage amplifies when evaluated against FFT-constructed targets (not real targets). This was already identified as a target-construction artifact. The full-signal advantage at H=96: +0.189, H=336: +0.103.

**[OBS] P2 — Lorenz surrogate:**
Chaotic: advantage=0.384, p=0.004. Phase-shuffled surrogate: advantage=0.172, p=0.320. Advantage drops ~55% and loses significance on the surrogate. With n=8 this is underpowered.

**[OBS] P3 — Burgers lambda1:**
All lambda1 estimates are negative or NaN across all nu values, including nu=0.005. The estimator is not working reliably on PCA modes of this PDE — as established earlier, this is because PCA components are not generic Takens observables and embedding dimension is too small. The advantage pattern shows p<0.05 at nu≥1.0 but not at nu=2.0 (p=0.19).

**[OBS] P4 — Subsampling seeds:**
Panda MAE is essentially constant across all 10 seeds for both methods (diversity: 0.026–0.030, stratified: 0.028 every seed since it's deterministic). Chronos MAE varies substantially across seeds (0.054–0.145 for diversity). The ordering of diversity vs stratified reverses across seeds.

**[OBS] P5 — Improved projection:**
After using a better seasonal projection, Panda advantage on Weather collapses: vanilla +0.159 → improved proj -0.038 at H=96. At H=336: +0.122 → +0.030. On ETTh1 and ETTh2 both vanilla and improved proj show inconsistent, mostly non-significant results.

**[OBS] Exp19 — Complexity continuum:**
Harmonic oscillator: advantage=+0.370, p=0.004. VanderPol limit cycle: +0.011, p=0.027. Duffing: +0.214, p=0.055. Rossler: +0.304, p=0.004. Lorenz: +0.476, p=0.004. Panda wins on the harmonic oscillator — the simplest possible non-chaotic signal.

**[OBS] Exp20 — Chronos residual:**
Chronos MAE on Weather increases by +0.277 at H=96 and +0.245 at H=336 after decomposition. Panda degraded by similar magnitude in P5. Both models degrade approximately equally after decomposition.

**[OBS] Exp21 — Permutation entropy:**
PE values at order=3 cannot distinguish Lorenz rho=10 from rho=28 (all cluster 0.46–0.49). Burgers PE values (0.024–0.132) are far lower than real datasets (0.75–0.95). The metric failed to discriminate the relevant regimes.

**[OBS] Exp22 — Node embeddings:**
On hetero_controlled: delta_panda at H=96 = +0.037 (offsets *help* Panda — lower MAE with offsets). On homo_matched: delta_panda = -0.085 (offsets *hurt* Panda). The offsets help on heterogeneous channels and hurt on homogeneous ones — directionally consistent with H1.

**[OBS] Exp23 — Head finetuning:**
At H=96: panda_base=0.609, panda_ft=0.699 — finetuning *hurts* by 0.090. At H=336: essentially unchanged (-0.012). Head finetuning does not improve performance.

**[OBS] Topology:**
Correlation dimension: Weather=0.89, Lorenz=0.86, Burgers=0.74, ETTh1=1.54, ETTh2=1.62. Weather and Lorenz cluster together, ETTh datasets are substantially higher. This is a single noisy estimate per dataset with a known unreliable estimator on real data.

---

### Empirical Patterns

**[PAT]** Panda MAE is essentially invariant to subsampling method and seed on Burgers — Chronos MAE drives the advantage differences.

**[PAT]** Decomposition hurts both models approximately equally on Weather. Neither benefits from the residual-only framing.

**[PAT]** Panda advantage drops monotonically with increasing sensor heterogeneity on Weather, even after difficulty matching and variance-CV matching.

**[PAT]** Node offsets help on heterogeneous channels, hurt on homogeneous ones — small effects but directionally consistent.

**[PAT]** Weather and Lorenz have similar topology estimates; ETTh datasets are structurally different. This is consistent with the hypothesis that Panda transfers to Weather partly due to geometric similarity to training distribution — but the estimator is unreliable.

---

### What Is Not Yet Answered

One piece missing before the narrative is complete: **why does Panda win on Burgers even at non-chaotic viscosities, and is it channel attention or the temporal architecture?** That is exactly what the running cell will tell us. Once you have those numbers, share them and we can close the loop on the Burgers mechanism — the last open question.

## Human

so our whole goal was to identify things in architecture through ablations and other experiments, that what things can be modified in order to achieve generalisation? Is it even possible? Are there any things which point towards suggestions given by the prof and her team?are there any other things to try out apart from these suggestions?
where do we exactly stand now (apart from the last cell for now)?
what is the whole narrative?
we had already done the mapping of experiments to architecture componets eariler

## Assistant

 Let me be precise and work from the actual data rather than constructing a narrative first.

---

## What the experiments collectively establish about each architectural component

---

### Component 1: Channel Attention

**What the data shows:**

[OBS] Univariate Panda ≈ multivariate Panda on Weather (advantage difference ~0.057 at H=96, p=0.074; ~0.030 at H=336, p=0.371). Neither significant.

[OBS] Panda advantage drops monotonically with sensor heterogeneity after difficulty matching and CV matching (hetero_controlled H=96: +0.261 vs mixed_matched: +0.333).

[OBS] Node offsets help on hetero_controlled (+0.037), hurt on homo_matched (-0.085) at H=96.

[OBS] Chronos is largely insensitive to heterogeneity level; Panda degrades.

[OBS] Panda MAE is invariant to subsampling method across 10 seeds on Burgers — Chronos drives advantage differences.

**What this establishes:**

Channel attention is not clearly the *driver* of Panda's Weather advantage (univariate ablation non-significant). However, there is evidence it becomes a *bottleneck* on heterogeneous sensor data — Panda degrades with heterogeneity while Chronos does not, and node identity offsets provide small directional relief specifically on heterogeneous subsets.

**Competing explanations for the heterogeneity degradation:**
1. Channel attention assumes homogeneous ODE-like coupling — real sensors violate this, producing incoherent joint representations. [Medium confidence, consistent with direction]
2. Heterogeneous subsets contain more complex multivariate interaction structure that is harder regardless of identity. [Medium confidence — partially controlled by difficulty matching but interaction complexity is not the same as marginal difficulty]
3. The effect size is small and n=8 for the ablation is insufficient to draw strong conclusions. [Medium confidence]

**Connection to Flora's suggestions:** G-SWaN/XXLTraffic direction is motivated by this component. The evidence is directional but not conclusive. The node offset result is the weakest possible version of node embeddings (scalar offsets, not learned) and still shows the right direction.

**Confidence that channel attention modification would help:** Low-medium. Direction is right, causal evidence is not established.

---

### Component 2: Prediction Head (Fixed Linear)

**What the data shows:**

[OBS] Head finetuning at H=96: panda_base=0.609, panda_ft=0.699 — finetuning *hurts* by 0.090, p values not reported.

[OBS] At H=336: essentially no change (-0.012).

**What this establishes:**

The fixed chaotic ODE head prior is not a recoverable bottleneck via simple finetuning. This is a negative result. Finetuning the head without the encoder adapting makes things worse — the head and encoder are coupled in ways that finetuning the head alone cannot repair.

**Competing explanations:**
1. The head and encoder co-adapted during pretraining — finetuning the head alone introduces a mismatch. [Medium confidence]
2. 50 gradient steps is insufficient. [Low confidence — 50 steps with ground truth context should show some improvement if the head were the bottleneck]
3. The head is not the bottleneck; the representation upstream is. [Medium confidence]

**Connection to Flora's suggestions:** This does not directly support any of Flora's directions. It suggests that lightweight head-only adaptation is not viable.

**Confidence that head modification would help:** Low. The result is negative.

---

### Component 3: Koopman Lifting (RFF + Polynomial Features)

**What the data shows:**

[OBS] Exp21 PE estimator failed to discriminate systems — PE at order=3 cannot distinguish Lorenz rho=10 from rho=28, and Burgers PE is in a completely different scale range from real datasets. The Koopman lifting hypothesis remains **untested** — Exp21 was the intended test and the metric was inadequate.

[OBS] Topology analysis: Weather corr_dim=0.89, Lorenz=0.86, ETTh1=1.54, ETTh2=1.62. Weather and Lorenz group together, ETTh datasets separate. This is consistent with but does not prove a lifting/geometry hypothesis.

[OBS] Exp19 Harmonic oscillator: advantage=+0.370, p=0.004. Panda wins on a pure sinusoid. This is **not** explained by chaos and is the most anomalous result in the dataset.

**What this does not establish:**

There is no ablation of the Koopman lifting component. We cannot distinguish "lifting drives the advantage" from "pretraining drives the advantage" from "patching drives the advantage."

**The Harmonic oscillator result specifically:**

[OBS] Panda advantage on Harmonic=+0.370, on VanderPol (limit cycle)=+0.011. This non-monotone pattern — pure periodic gives large advantage, limit cycle gives tiny advantage — is unexplained by any current hypothesis.

Possible explanations include:
1. Chronos specifically fails on pure sinusoidal signals (tokenization artifact) — the advantage reflects Chronos weakness, not Panda strength. [Medium confidence]
2. The Koopman lifting produces useful representations even for periodic signals due to the nonlinear feature expansion. [Low confidence, speculative]
3. The VanderPol result reflects a genuine regime where neither model has advantage, not a property of Panda specifically. [Low confidence]

**Connection to Flora's suggestions:** The topology analysis result points toward topological flow matching — Weather geometrically resembles Lorenz more than ETTh does. However the estimator is unreliable and this is a single noisy observation. This needs proper TDA tools (persistent homology) to be taken seriously.

**Confidence that lifting modification would help:** Low — untested. It remains the most plausible positive mechanism but has no direct ablation evidence.

---

### Component 4: Patching

**What the data shows:**

[OBS] P5 improved projection: decomposition with better seasonal projection collapses Panda's Weather advantage (vanilla +0.159 → improved proj -0.038 at H=96).

[OBS] Exp20 Chronos residual: Chronos also degrades +0.277 after decomposition. Both models degrade equally.

**What this establishes:**

The decomposition result no longer supports "Panda needs the full signal" specifically — both models need it equally. The advantage collapse after decomposition reflects that the forecasting task changes fundamentally (projecting a poor seasonal estimate adds errors to both), not that patching specifically requires the mixed signal.

**Competing explanations for the decomposition result:**
1. Both models benefit from the original signal's full complexity — removing structure makes the residual harder to forecast. [Medium confidence]
2. The projection introduces correlated errors that hurt metric computation for both. [Medium confidence]
3. The periodic+residual decomposition is not the right factorization for Weather — the structure is more entangled. [Low confidence]

**Connection to Flora's suggestions:** TimesNet-inspired pretraining was motivated by the idea that Panda struggles with periodic structure. The current evidence suggests both models degrade similarly on decomposed signals — this does not specifically implicate patching as the bottleneck for non-periodic generalization.

**Confidence that patching modification would help:** Low — no direct evidence it is the bottleneck.

---

### Component 5: Pretraining Distribution

**What the data shows:**

[OBS] P2 surrogate: advantage drops from 0.384 to 0.172 and loses significance on phase-shuffled Lorenz. Underpowered (n=8) but directional.

[OBS] P3 Burgers: lambda1 estimates are all negative or NaN — estimator unreliable on PCA modes. Cannot conclude about chaos threshold for PDEs from this.

[OBS] Exp19 continuum: Harmonic=+0.370, VanderPol=+0.011, Duffing=+0.214, Rossler=+0.304, Lorenz=+0.476. Non-monotone pattern — periodic beats limit cycle in terms of Panda advantage.

[OBS] P4: Panda absolute MAE is invariant across seeds and subsampling methods — the model extracts the same quality representation regardless of which spatial channels it receives.

**What this establishes:**

The pretraining distribution clearly matters — Panda transfers to systems resembling its training data. But the pattern is not simply "chaos = advantage." The Harmonic oscillator result, the non-monotone continuum, and the Burgers non-chaotic wins all indicate the relationship is more complex.

**What is not established:** Whether expanding the pretraining distribution to include periodic/stochastic/PDE systems would improve generalization without degrading chaos performance. This requires retraining — untestable without compute.

**Connection to Flora's suggestions:** Mixed pretraining with TimesNet datasets was proposed. The evidence base for this direction is weak from our experiments — we cannot tell if the training distribution is the bottleneck versus the architecture (lifting, channel attention) being the bottleneck.

---

## Where We Stand

**The honest answer about generalizability:**

[PAT] Panda generalizes to Weather and Burgers beyond its chaotic ODE training distribution. The mechanism is unknown.

[PAT] Panda does not generalize well to ETTh1/ETTh2 at short horizons. At longer horizons both models degrade and the comparison is inconclusive.

[PAT] Heterogeneous sensor data is a specific failure mode — established with medium confidence via difficulty matching + variance control + Chronos comparison.

**What we cannot yet say:**

We cannot identify which architectural component is responsible for any of these patterns with causal confidence. Every experiment shows correlations. None establishes a mechanism. The univariate ablation (channel attention) and head finetuning are the only direct component ablations, and both gave weak or negative results.

---

## Connection to Flora's Suggestions — Honest Assessment

| Suggestion | What our experiments show | Confidence it would help |
|---|---|---|
| G-SWaN / node embeddings | Heterogeneity is a failure mode; node offsets directionally help | Low-medium |
| XXLTraffic | Heterogeneous sensor bottleneck is established | Cannot test yet |
| Topological flow matching | Topology analysis consistent but estimator unreliable | Low |
| TimesNet pretraining | No specific evidence this would help; decomposition hurts both models equally | Low |

---

## What Is Not Yet Tried That Could Discriminate

Three things would move us from correlation to something closer to mechanism:

**1. Proper TDA topology analysis** — persistent homology on Weather, ETTh, Lorenz, Burgers rather than correlation dimension. The topology analysis result is tantalizing (Weather ≈ Lorenz ≠ ETTh) but the estimator is too unreliable to act on.

**2. A proper Koopman lifting ablation** — run Panda with the lifting replaced by a simple linear projection of equal dimension. If advantage drops, lifting is the positive mechanism. This requires code access to Panda's architecture, not just inference.

**3. The Burgers univariate ablation now running** — this is the last piece. If channel attention drives the non-chaotic Burgers advantage, that changes the entire heterogeneity story (channel attention would be both helping on homogeneous PDEs and hurting on heterogeneous sensors — which is actually coherent and maps directly onto the G-SWaN motivation).

Once the Burgers univariate result is in, the narrative will either unify or further fragment. Share it when it finishes.

## Human

ok uploaded burgers univariate ablation in project files. Now everything we planned is compelte

## Assistant

Let me read the final result first.


```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```

