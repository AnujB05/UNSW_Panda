# Understanding topological flow matching and traffic forecasting papers

## Human

I need to understand the papers that prof and her phd/postdocs suggested. Topological flow matching, timesnet and Because Every Sensor Is Unique, so Is Every Pair: Handling Dynamicity in
Traffic Forecasting.
Explain me these papers

## Assistant

 


```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```


Got it. Found all three papers. Now let me get the full details on Topological Flow Matching from ICLR 2026.


```
This block is not supported on your current device yet.
```


Now I have everything. Here's a full breakdown of all three papers:

---

## 1. Topological Flow Matching (ICLR 2026)
*Wyrwal, Ceylan, Tong*

**The problem:** Standard flow matching treats all data as points in Euclidean ℝⁿ, even when the data lives on a structured domain — like traffic flow on a road graph, or fMRI signals on a brain network. This loses the relational structure entirely.

**The key idea:** Flow matching is reinterpreted as solving a degenerate Schrödinger bridge problem. Topological information is injected by augmenting the reference process with a Laplacian-derived drift. Concretely: the graph Laplacian L encodes neighborhood connectivity (who is adjacent to whom). By adding a Laplacian-based drift term to the ODE/SDE that flow matching trains, the interpolating path between source and target distributions is informed by graph topology — nearby nodes in the graph naturally have correlated trajectories.

**Why this preserves FM's properties:** The Laplacian drift is a linear modification, so you don't need to simulate it (the SDE remains tractable). You get simulation-free training and deterministic sample paths — FM's main selling points remain intact, making it a plug-and-play replacement for standard flow matching.

**What domains it works on:** Diverse structured datasets including brain fMRIs, ocean currents, seismic events, and traffic flows. So the graph can be a road network, a sensor mesh over the ocean, etc.

**Why it's relevant to you:** DRIFT-Net models spatiotemporal signals over sensor graphs. Standard flow matching can't respect, say, the fact that two road sensors 200m apart should have correlated predictions. Topological FM directly addresses this — it's a possible generative modeling component for your spatiotemporal reasoning work.

---

## 2. TimesNet: Temporal 2D-Variation Modeling (ICLR 2023)
*Wu, Hu, Liu, Zhou, Wang, Long — Tsinghua*

**The core observation:** Real-world time series have multi-periodicity (daily cycles, weekly cycles, etc.). Within a period, adjacent time steps are correlated (intraperiod variation). Across periods, the same position in different cycles is correlated (interperiod variation). Existing methods process 1D time series directly, which is challenging because temporal patterns are intricate. TimesNet addresses this by raveling complex temporal variations into multiple intraperiod- and interperiod-variations.

**The transformation:** Given a time series of length T, FFT is used to detect the top-k dominant periods {p₁, p₂, ...}. For each period pᵢ, you reshape the 1D series into a 2D tensor of shape (T/pᵢ) × pᵢ. Now **rows** correspond to interperiod variation (same phase across different cycles) and **columns** to intraperiod variation (within one cycle). This embeds intraperiod- and interperiod-variations into columns and rows of 2D tensors, making 2D-variations easily modeled by 2D kernels.

**Architecture:** TimesBlock takes these 2D tensors and processes them with a parameter-efficient Inception block (multi-scale 2D convolutions), then folds back to 1D. It's stacked into TimesNet. This directly takes advantage of booming vision backbones by transforming 1D time series into 2D space.

**Results:** TimesNet achieves consistent state-of-the-art in five mainstream tasks: long- and short-term forecasting, imputation, classification, and anomaly detection. It's one of the first truly task-general backbones for time series.

**Why it's relevant to you:** DRIFT-Net already uses a temporal branch. TimesNet gives you a strong, principled temporal encoder — the 2D reshape trick is clean and exploitable. Understanding it helps you reason about what your temporal branch should or shouldn't be doing for spatiotemporal forecasting.

---

## 3. G-SWaN: Because Every Sensor Is Unique, so Is Every Pair (IoTDI 2023)
*Prabowo, Shao, **Xue**, Koniusz, **Salim** — RMIT / UC Davis / **UNSW***

This is directly from Prof. Salim's group (Hao Xue is her PhD student/postdoc).

**The empirical observation:** Traffic dynamics at each sensor are unique due to external contexts — for example, afternoon peaks near schools occur earlier than near residential areas. Further analysis shows that each pair of sensors also has a unique dynamic.

**Node embeddings for uniqueness:** They first show that learnable node embeddings can capture per-sensor dynamics. A sensor near a school gets a different embedding from one near a freeway on-ramp, and these embeddings encode not just location but behavioral pattern.

**Spatial Graph Transformer (SGT) — the main contribution:** SGT uses node embeddings to leverage the self-attention mechanism to ensure that the information flow between two sensors is adaptive with respect to the unique dynamic of each pair. Concretely: for a source sensor i and target sensor j, you concatenate embeddings eᵢ and eⱼ and feed them into the attention mechanism. This means the edge weight (how much j influences i) is conditioned on both their identities. SGT generalizes GCN — it can mask and reweight the adjacency matrix adaptively.

**Full architecture — G-SWaN:** Graph Self-attention WaveNet (G-SWaN) addresses complex, non-linear spatiotemporal traffic dynamics. It uses Graph WaveNet as backbone with SGT replacing GCN. WaveNet contributes dilated causal convolutions for temporal modeling; SGT contributes the spatial module.

**Results:** Empirical experiments on four real-world, open datasets show superior performance on both traffic speed and flow forecasting.

**Why it's relevant to you:** This is the direct predecessor line to DRIFT-Net from Prof. Salim's group. The core tension — static graphs can't capture dynamic sensor relationships — is what DRIFT-Net then addresses at a deeper level with neural operators and dual-branch architectures. Understanding G-SWaN's SGT module will make DRIFT-Net's design choices click into place.

---

**The through-line across all three:** you're being asked to understand (1) a generative modeling backbone for topology-aware generation (Topological FM

## Assistant

 


```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```



```
This block is not supported on your current device yet.
```


Good papers to dig into — and notably the G-SWaN one is directly from Prof. Salim's lab (Hao Xue + Flora Salim are co-authors), so that's core lineage for your project. Here's a thorough breakdown of all three.

---

## 1. Topological Flow Matching (ICLR 2026)
*Wyrwal, Ceylan, Tong*

**The problem with standard flow matching on structured domains**

Standard flow matching learns a vector field that transports samples from a noise distribution $p_0$ (e.g. Gaussian) to the data distribution $p_1$ by regressing on conditional vector fields. This works great in $\mathbb{R}^d$, but its standard formulation treats signals on structured spaces — such as fMRI data on brain graphs — as points in Euclidean space, overlooking the rich topological features of their domains. If your data lives on a graph or simplicial complex, ignoring that structure is a real loss — the "geometry" of the domain encodes which directions of variation are meaningful.

**The core idea: Schrödinger bridge + Laplacian drift**

The paper interprets flow matching as a framework for solving a degenerate Schrödinger bridge problem, and injects topological information by augmenting the reference process with a Laplacian-derived drift.

Breaking that down: the Schrödinger bridge problem asks for the most likely stochastic process connecting two distributions subject to an entropy constraint. Standard flow matching is a degenerate (zero-noise) limit of this. The key move in this paper is to take the *reference diffusion process* in that Schrödinger bridge and add a drift term derived from the **graph Laplacian** $\Delta$ of the domain. The Laplacian encodes topology — its eigenvectors are the natural "frequencies" on the graph (graph Fourier basis). So the drift biases flows to respect the connectivity structure.

This is clean because it's entirely in the *reference process*, meaning it preserves the desirable properties of flow matching: a stable, simulation-free objective and deterministic sample paths, and serves as a plug-and-play replacement for standard flow matching.

**Why it matters for your project**

The framework is demonstrated on diverse structured datasets including brain fMRIs, ocean currents, seismic events, and traffic flows. Traffic flows on road graphs are exactly the kind of domain this is designed for — sensors live on a graph, and the Laplacian of the road network carries real semantic meaning (connectivity, proximity). This is likely why the group suggested it: as a generative modeling backbone that is topology-aware, it's a natural fit for spatiotemporal generation/imputation tasks over sensor networks.

---

## 2. TimesNet: Temporal 2D-Variation Modeling (ICLR 2023)
*Wu, Hu, Liu, Zhou, Wang, Long — Tsinghua*

**The core observation: time series are multi-periodic**

TimesNet is motivated by the observation of multi-periodicity in time series — it ravels out complex temporal variations into multiple intraperiod- and interperiod-variations. Think of traffic data: there's an intraday period (rush hours within a day) and an interday period (the Monday pattern repeating each week). Prior methods try to model all of this directly in 1D, which is hard.

**The 1D → 2D transformation**

The key technical move: if a time series has period $p$, reshape the 1D sequence of length $T$ into a 2D tensor of shape $(p, T/p)$. Now:
- **Columns** correspond to positions *within* a period → capture **intraperiod** variation (e.g., how traffic evolves over a single day)
- **Rows** correspond to the *same position across different periods* → capture **interperiod** variation (e.g., Monday vs Tuesday at 8am)

This transformation embeds the intraperiod- and interperiod-variations into the columns and rows of the 2D tensors respectively, making the 2D variations easily modeled by 2D kernels.

**The TimesBlock**

## Human

I need to understand the papers that prof and her phd/postdocs suggested. Topological flow matching, timesnet and Because Every Sensor Is Unique, so Is Every Pair: Handling Dynamicity in
Traffic Forecasting.
Explain me these papers
Let us start with topological flow matching. I don't know schrodinger bridge, so we need to build up from basics, with examples to soldify understanding.

## Assistant

 

# Topological Flow Matching — From Foundations Up

Since you know flow matching well (you built on it for E0 280), I'll use it as the anchor and build everything new relative to it.

---

## 1. Quick Anchor: What Flow Matching Does

You know this, so just to fix notation:

- You have a source distribution $p_0$ (usually Gaussian) and target $p_1$ (data).
- You define a probability path $p_t$ interpolating between them.
- You train a neural vector field $v_\theta(x, t)$ to match the marginal velocity at each $t$.
- At inference: integrate the ODE $\dot{x} = v_\theta(x, t)$ from $t=0$ to $t=1$.

The key design choice: **how do you couple** $(x_0, x_1)$ pairs to build the training signal? In vanilla conditional FM, you couple independently — just draw $x_0 \sim p_0$, $x_1 \sim p_1$ independently. The straight-line path between them is your conditional flow.

This works, but the coupling is arbitrary. The paths cross a lot, the marginal velocity field is messy, and — crucially — **the transport doesn't respect any geometric or structural properties of the distributions**.

That's the gap that Schrödinger Bridges (and then Topological FM) try to fill.

---

## 2. Schrödinger Bridge — Built From Scratch

### 2a. First, Deterministic Optimal Transport

Forget stochasticity for a moment.

**OT problem:** Given $p_0$ and $p_1$, find the *coupling* $\pi(x_0, x_1)$ — a joint distribution with marginals $p_0$ and $p_1$ — that minimizes expected transport cost:

$$\min_{\pi \in \Pi(p_0, p_1)} \mathbb{E}_{(x_0, x_1) \sim \pi} \left[ c(x_0, x_1) \right]$$

With $c = \|x_0 - x_1\|^2$, this is the 2-Wasserstein distance, and the solution is the *Monge map* — a deterministic function $T$ sending each $x_0$ to a unique $x_1$, with no mass splitting.

**Intuition:** think of $p_0$ as a pile of sand and $p_1$ as a hole. OT finds the cheapest way to move sand into the hole — no unnecessary detours, mass moves in parallel straight lines.

**The flow matching connection:** OT-FM (which you've probably seen) uses the OT coupling to pair $(x_0, x_1)$ instead of random pairing. This gives straighter paths and cleaner velocity fields.

### 2b. The Problem With Deterministic OT in High Dimensions

In high dimensions, OT is:
- Computationally brutal (needs iterative solvers)
- **Brittle:** the Monge map sends each point to exactly one destination — a single deterministic trajectory with zero noise

Real data often comes from a *stochastic* process. There isn't one "true" path from $x_0$ to $x_1$; there are plausible paths forming a distribution over trajectories.

### 2c. Schrödinger Bridge: Add Entropy, Get Stochastic OT

**Schrödinger's question (1931-32, reformulated):** Imagine a cloud of Brownian particles diffusing from $t=0$ to $t=1$. You observe the distribution is $p_0$ at $t=0$ and $p_1$ at $t=1$. *What is the most likely stochastic process that produced this?*

Formally: among all stochastic processes (path measures) $\mathbb{P}$ on trajectories $\{x_t\}_{t \in [0,1]}$ that have marginals $p_0$ and $p_1$, find the one closest to a **reference process** $\mathbb{Q}$ (usually Brownian motion) in KL divergence:

$$\text{SB}: \quad \min_{\mathbb{P}: \, \mathbb{P}_0 = p_0, \, \mathbb{P}_1 = p_1} D_\text{KL}(\mathbb{P} \| \mathbb{Q})$$

Let me unpack each piece:

- $\mathbb{P}$ is a **path measure** — a distribution over entire trajectories, not just over points. Think of it as specifying $p(x_0, x_1, x_{0.3}, x_{0.7}, \ldots)$ jointly.
- $\mathbb{Q}$ is Brownian motion from $p_0$: the process $dx = \sigma \, dW$ with initial distribution $p_0$. This is our "default" — pure diffusion with no guidance.
- The KL divergence $D_\text{KL}(\mathbb{P} \| \mathbb{Q})$ penalizes $\mathbb{P}$ for deviating from Brownian motion. Minimizing it means: *find the process that achieves the endpoint constraint $p_1$ while diffusing as naturally as possible*.

**Concrete Example.** Say $p_0 = \mathcal{N}(-3, 0.1)$ and $p_1 = \mathcal{N}(+3, 0.1)$ in 1D.

- Pure Brownian motion from $p_0$ would spread out wildly by $t=1$ — it would *not* concentrate near $+3$.
- Deterministic OT would draw a straight line $x_t = -3 + 6t$ with zero noise.
- **SB solution:** a drift-diffusion process $dx_t = u_t(x_t) dt + \sigma \, dW_t$ where the drift $u_t$ nudges particles toward $+3$ while still allowing stochastic fluctuations. The particles form a Gaussian beam that contracts toward the target.

The SB solution has a beautiful closed form structure: it factors as

$$\mathbb{P}^*(x_0, x_1) = \frac{p_0(x_0) \, p_1(x_1)}{\mathbb{Q}(x_1 | x_0)} \cdot \text{(normalization)}$$

which is an **entropy-regularized OT coupling** — it's OT with an added $-\varepsilon \cdot H(\pi)$ entropy bonus that spreads the coupling.

### 2d. The Schrödinger System

The SB solution satisfies a beautiful fixed-point condition. There exist non-negative functions $f, g$ (called **Schrödinger potentials**) such that the optimal coupling is:

$$\pi^*(x_0, x_1) = f(x_0) \cdot k(x_0, x_1) \cdot g(x_1)$$

where $k$ is the Gaussian kernel of the reference Brownian motion. You find $f, g$ by **Sinkhorn iterations** (alternating projections) — this is where Sinkhorn/IPOT algorithms come from.

**Key properties of SB vs OT:**

| | OT | Schrödinger Bridge |
|---|---|---|
| Transport | Deterministic map | Stochastic process |
| Paths | Straight lines | Noisy, curved trajectories |
| Computation | Hard (LP/auction) | Iterative (Sinkhorn) |
| Sensitivity to outliers | High | Lower (entropy smoothing) |
| Respects data geometry? | Somewhat | Better, via reference process |

### 2e. SB as a Generative Model

For generation, you parameterize the drift $u_\theta(x, t)$ of the SDE $dx = u_\theta dt + \sigma dW$ and train it to solve the SB problem. The resulting model:
- Is a **stochastic flow** (not a deterministic ODE like standard FM)
- Has both forward and backward processes linked by the SB structure
- Generalizes diffusion models (which only have a fixed forward process)

This is the foundation for papers like **DiffSB, Score-Based SB**, and now **Topological Flow Matching**.

---

## 3. Topological Data Analysis — What You Need

The "topological" part of Topological FM comes from TDA. Here's what you need.

### 3a. What Topology Captures

Topology studies properties of spaces that are invariant under continuous deformation — stretching, bending, but not tearing.

For point clouds (which represent data distributions), the topological features of interest are **holes of various dimensions**:

- **0-dimensional holes (β₀):** connected components. A distribution with two separated clusters has β₀ = 2.
- **1-dimensional holes (β₁):** loops/rings. A distribution shaped like a circle/annulus has β₁ = 1.
- **2-dimensional holes (β₂):** voids/cavities. A distribution on a sphere surface has β₂ = 1.

**Example:** Consider sensor readings on a road network.

- Sensors form clusters around intersections → β₀ > 1
- Ring roads create loops in the network → β₁ > 0
- These topological features *encode* the network structure

### 3b. Persistent Homology — The Key Tool

The problem: how do you compute topology from a finite point cloud with noise?

**Step 1: Build a filtration.** For a point cloud $X = \{x_1, \ldots, x_n\}$, for each radius $\epsilon \geq 0$, build the **Vietoris-Rips complex** $\mathcal{R}_\epsilon$: connect any two points within distance $\epsilon$, fill in triangles when three points are mutually within $\epsilon$, and so on.

**Step 2: Track features.** As $\epsilon$ grows from 0 to ∞, topological features (components, loops, voids) **appear** (birth) and **disappear** (death) as simplices get added.

**Example:** 4 points arranged roughly in a square.

- At small $\epsilon$: 4 isolated components (β₀ = 4)
- At medium $\epsilon$: adjacent points connect → components merge, a loop forms (β₀ = 1, β₁ = 1)
- At large $\epsilon$: the diagonal fills in → loop dies (β₁ = 0)

Each feature is recorded as a **(birth, death) pair** in a **persistence diagram** $\text{Dgm}(X)$.

**Key insight:** Long-lived features (large death − birth) are "real" structure. Short-lived features are noise.

### 3c. Distances Between Persistence Diagrams

To compare the topology of two distributions $p$ and $q$:
1. Sample point clouds $X \sim p$, $Y \sim q$
2. Compute persistence diagrams $\text{Dgm}(X)$, $\text{Dgm}(Y)$
3. Compute the **Wasserstein distance between diagrams** or the **bottleneck distance**:

$$d_W(\text{Dgm}(X), \text{Dgm}(Y)) = \min_{\text{matching}} \sum_i \|b_i - b_{\sigma(i)}\|$$

where you find the optimal matching between birth-death pairs across the two diagrams.

This gives a differentiable (almost everywhere) measure of **topological dissimilarity** — and crucially, you can backpropagate through it.

---

## 4. Topological Flow Matching — Putting It Together

Now we have all the pieces. Let me explain what the paper does.

### 4a. The Core Problem

Standard flow matching (and even SB-based FM) learns to transport $p_0 \to p_1$, but has **no topological consistency guarantee**. Specifically:

- The learned intermediate distributions $p_t$ at intermediate $t$ may have completely wrong topology
- The generated samples may "cut through" topological features (e.g., move mass through a hole that should be preserved)
- For spatiotemporal data on structured domains (sensor networks, road graphs), this means the model ignores the network topology while learning flows

**Motivating example:** Suppose $p_1$ is traffic flow patterns on a ring road. The ring topology (β₁ = 1) is structurally important — it means flow is cyclic. A standard FM model has no mechanism to preserve this during generation.

### 4b. The Approach

Topological Flow Matching adds a **topological consistency objective** to the flow matching training loss. The full loss is:

$$\mathcal{L}_\text{TFM} = \underbrace{\mathcal{L}_\text{FM}}_{\text{velocity matching}} + \lambda \underbrace{\mathcal{L}_\text{topo}}_{\text{topological regularizer}}$$

**The topological loss** penalizes deviation between the topology of the model's marginal $p_t^\theta$ and the topology of the interpolated "true" marginal $p_t$:

$$\mathcal{L}_\text{topo} = \sum_t d_W\!\left(\text{Dgm}(X_t^\theta),\, \text{Dgm}(X_t)\right)$$

where $X_t^\theta$ are samples generated by the current model at time $t$, and $X_t$ are samples from the true interpolant path.

### 4c. The Schrödinger Bridge Connection

Here's where SB becomes essential rather than optional. The paper uses a **Schrödinger Bridge as the reference coupling** rather than independent coupling or OT coupling.

Why? Because the SB coupling is the unique coupling that:
1. Has marginals $p_0$, $p_1$
2. Minimizes KL from Brownian motion (so paths are smooth/natural)
3. Produces **intermediate marginals $p_t$ that are as "topologically stable" as possible** — the entropy regularization prevents the sharp, topology-breaking jumps you'd get from deterministic OT

In other words: **SB gives you the topologically gentlest path between distributions**, and TFM adds an explicit topological penalty on top to enforce this further.

### 4d. The Architecture

The model learns:
- A **stochastic vector field** (drift) $u_\theta(x, t)$ for the SDE
- A **topological encoder** that maps point clouds to persistence diagram representations
- The topological loss is backpropagated through the persistence computation using recent differentiable TDA libraries (Gudhi, Giotto-TDA)

### 4e. Why This Matters for DRIFT-Net / Your Research

This is directly relevant to your project in several ways:

1. **Sensor network topology:** Sensors in a city form a spatial graph. The topological structure (clusters, loops in road networks) should be preserved when the model generates/predicts spatial patterns.

2. **Distribution shift:** If a sensor fails or is added, the topology of the sensor point cloud changes. TFM provides a principled way to model this change as a *topological transition* rather than just a perturbation.

3. **DRIFT-Net's dual-branch architecture:** The spatial branch in DRIFT-Net learns from the sensor graph. TFM could be used to make the latent flow respect graph topology during spatiotemporal prediction.

4. **The dynamicity challenge:** "Every Sensor Is Unique" paper (which you'll read next) deals with heterogeneous/dynamic sensors. TFM's topological framework could help reason about *how* the sensor topology is changing over time.

---

## Summary Diagram

```
Standard FM:         p0 ----straight paths----> p1
                           (topology ignored)

OT-FM:               p0 ---parallel OT paths---> p1
                           (cost-optimal, but deterministic, fragile)

Schrödinger Bridge:  p0 ~~~noisy drift paths~~~> p1
                           (entropy-regularized, smooth, stochastic)

Topological FM:      p0 ~~~SB paths + topo penalty~~~> p1
                           (SB paths + explicitly preserve β0, β1, β2 
                            of intermediate distributions)
```

---

Ready to move on to **TimesNet**, or do you want to dig deeper into any piece of this — the Sinkhorn iterations for SB, the differentiable persistence computation, or how the topological loss gradient flows?
