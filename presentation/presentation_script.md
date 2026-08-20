# Panda Continued Investigation — Verbatim Script

## Opening: The Tree Walkthrough (before Slide 1)

*Open the tree in a browser tab, project it, keep it mostly collapsed at first.*

"Before I get into slides — this is a full map of every experiment I've run, old and new, about 77 nodes. I'm not going to read through it now, but I want you to have it as a reference, because I'll compress a lot in the slides and I'd rather show you where the detail lives than pretend it doesn't exist."

*Click to expand "Branch B: Generalisation Boundary" → "Sensor Heterogeneity."*

"Quick example of how to read it — color is status. Green is established, gray is retired, red is retracted. This whole heterogeneity branch here is gray — that's a finding I presented last time that didn't survive, and I'll walk through why in a few slides."

*Click "Standalone Flagship Findings" → "Harmonic Oscillator Saga."*

"And this one's red — an actual retraction, also coming up."

*Collapse back down.*

"I'll leave this open in a tab. If anything I skip over is something you want more on, just say so and I'll pull it up live rather than guessing what to include."

---

## Slide 1 — Title

"Thanks for having me back. This is a continuation from last time — I'll walk through everything that's happened since, including two things I got wrong and caught myself on, and where I'm headed next."

## Slide 2 — Outline

"Roughly nine parts. Recap of what held up and what didn't, a quick confidence map, my strongest single result, the mechanism hunt across the architecture, two hard methodological lessons, some genuinely new leads, a quick methods check, and then where I'm pivoting next. I'll move fast through the light sections so I have time on the ones that matter."

---

## Slide 3 — What Held Up

**Motivation:** "Before anything new, I want to tell you what from last meeting is still standing."

**Result:** "Three things. The Weather advantage — still solid, and now confirmed through three independent routes rather than one. Channel attention — still not the driver of that advantage; I've gone from two null results to five. And the two directions you suggested last time — testing the Koopman lifting through an ablation, and trying persistent homology — I actually built and ran both. I'll cover what each one found."

**Supersession:** "One new thing worth flagging now: a trivial seasonal-naive baseline, no learned parameters at all, beats *both* Panda and Chronos on one ETTh test. That reframes part of the ETTh story — it's not that Panda fails to generalize there, it's that ETTh may just favor simple models entirely."

## Slide 4 — What Didn't Hold Up

**Motivation:** "Now the harder part — I want to walk through three things from last time that don't hold anymore, before I go any further."

**Method/Result, item by item:**

"First — sensor heterogeneity. Last time this was my most controlled finding, three converging experiments. At proper sample size, twenty windows instead of eight, it collapsed from an eighty-three percent effect down to four percent, and at one horizon the direction actually flipped. I confirmed this collapse two separate ways, independently.

Second — the Harmonic oscillator result, which I'd presented as key evidence against chaos being necessary for Panda's advantage. That turned out to be a bug in how I generated the signal — an unstable integration method let the amplitude grow uncontrolled. Fixed, the advantage collapses by ninety-nine percent.

Third — one ETTh2 result, p equals point-oh-one-three at the time. I flagged it as exploratory when I first saw it, and a rerun at proper sample size didn't replicate. This one's actually good news about my own process — I called it uncertain before I knew it wouldn't hold up."

**Supersession:** "Why this matters beyond just correcting the record: the heterogeneity finding was the entire motivation for one of your suggested directions last time, node embeddings. That motivation is gone now, and I'll explain why later."

---

## Slide 5 — Confidence Tiers: High & Medium

**Motivation:** "Quick map before I go deep — where everything sits today."

**Result:** "High confidence: the Weather advantage, the Burgers advantage, channel attention being ruled out five separate times, my strongest result — which is coming up next — and a new full-scale confirmation of that channel attention finding. Medium confidence: the Koopman ablation's behavioral pattern, which is real but unexplained; a geometric test of that explanation, which came back negative; temporal attention, weak evidence; and a new, promising finding about how well Panda's rollouts preserve attractor structure. Each of these gets its own slide."

## Slide 6 — Confidence Tiers: Retired & Retracted

**Motivation:** "And here's what's closed."

**Result:** "Retired: heterogeneity, an early geometry hypothesis, a couple of failed statistical estimators, and a resolution-dependency test that found nothing. Retracted: Harmonic, which I just covered."

**Supersession — this is the headline of the whole first half:** "Put together: five separate candidate mechanisms tested for what actually drives Panda's advantage — channel attention, the Koopman lift's geometry, temporal attention, resolution, and similarity to its own training distribution. None of them cleanly explains it. But — and this is the important part — the advantage itself is untouched by any of this. It's still there, still real. What's missing is the mechanism, not the phenomenon."

---

## Slide 7 — The Flagship Result: Lorenz Phase-Surrogate

**What it is:** "Quick concept first. Any signal can be broken down into a sum of sine waves at different frequencies — the power spectrum just says how much of each frequency is present overall. Separately, each of those waves also has a phase — where in its cycle it starts. If I keep every wave's amplitude exactly the same but randomize where each one starts, the signal's overall statistics — variance, frequency content — stay completely identical, but the actual moment-to-moment shape gets scrambled beyond recognition. That's the surrogate: statistically indistinguishable from the real signal, but with no genuine rule connecting one point to the next anymore."

**Motivation:** "This is new since last time, and it's my strongest single result. The question: does Panda's advantage actually require real deterministic structure in the data, or could it just be exploiting simpler signal statistics — variance, frequency content — without anything to do with dynamics specifically?"

**Method:** "I took the real chaotic Lorenz system and built a controlled version of it where every frequency component's phase gets randomized but every magnitude stays exactly the same. That preserves the power spectrum — the signal's overall statistical fingerprint — exactly, while destroying all the real temporal structure. There's a real theorem behind why this isolates exactly what I want — happy to go into it if anyone's curious — but the short version is: same statistics, no real dynamics left."

**Result:** "On the real chaotic signal, Panda's advantage is point-four-eight, highly significant. On the surrogate, it drops to point-two-five — still significant, but roughly half. Decomposing which model moved: Panda's own error grows almost sixteen-fold when the structure is destroyed. Chronos's error only grows about two-fold. Same statistics, wildly different sensitivity — Panda is clearly relying on something real and dynamical, not just surface-level signal properties."

**Supersession:** "This motivates everything in the next section. I now know Panda needs this kind of structure. What I don't know yet is *which part of the architecture* is responsible for that sensitivity — that's the question the next several slides chase, and mostly fail to answer."

---

## Slide 8 — A1: Koopman Lifting Ablation

**What it is:** "Two quick pieces before this one. First, the lift itself — before the rest of the model sees the raw window of numbers, it gets expanded into a much larger set of nonlinear features, polynomial combinations and wave-like transforms of the original values. The idea, borrowed from a technique for approximating chaotic systems, is that something complicated in its raw form can look much simpler — almost linear — once it's projected into this bigger feature space. In Panda, these features are fixed at random and never updated during training. Second, 'ablation' here means retraining the entire model from scratch with this lift swapped out for a plain, ordinary linear layer instead, and comparing the two fully-trained models directly."

**Motivation:** "This is the direct execution of something you suggested last time — testing whether the Koopman lifting component is the positive mechanism. It required retraining from scratch, since you can't remove this piece just by changing how the model is run at inference."

**Method:** "I replaced the fixed random-feature lift with a plain linear layer of the same size, and retrained both versions to a hundred thousand steps. Full campaign — three different evaluation protocols on Lorenz to rule out fragile setup choices, two held-out systems the model never saw during training, and proper significance testing with correction for running many comparisons."

**Result:** "Clear, replicated pattern: the version *without* the lift beats the version *with* it on chaotic systems and on Harmonic. But on non-chaotic Burgers, it's the opposite — the fixed lift helps there. Five of six comparisons survive strict correction."

**Supersession:** "This is a real behavioral finding — but the reason behind it wasn't yet known. That's the next slide."

## Slide 9 — A3: Does the Lift Do What the Theory Says?

**What it is:** "This slide doesn't touch forecasting accuracy at all — it tests the lift's internal math directly. First check: can one single straight-line transformation reliably predict how the lift's features change from one moment to the next? If the underlying theory is right, that should work well. Second check: does the lift react more sensitively to small input changes on chaotic signals than on calm ones? Again, that's exactly what the theory predicts if it's genuinely tracking chaos-specific structure rather than just expanding the input into a bigger space."

**Motivation:** "The lift's own design is explicitly motivated by a mathematical idea — Koopman operator theory, essentially trying to make a chaotic system look linear in a higher-dimensional space. Given A1's pattern, the natural question: is that actually what's happening?"

**Method:** "Two direct geometric tests, run only on the lift's own internal features, no forecasting accuracy involved. First — does a single linear operator fit the lift's transformation well, the way the theory predicts? Second — does the lift's sensitivity to small input changes differ meaningfully between chaotic and non-chaotic inputs, which the theory would also predict?"

**Result:** "Neither test supports the theory. Burgers — the case the theory says should show the cleanest linear structure — is actually the *worst* fit of everything tested. And sensitivity shows no real separation between chaotic and non-chaotic classes at all."

**Supersession:** "So A1's pattern is real and stands as reported. What doesn't stand is the explanation the architecture's own documentation offers for it. That mechanism is now genuinely open."

## Slide 10 — A2a: Temporal Attention Probes

**What it is:** "Temporal attention is the part of the model that lets different time-steps in the input window look at each other and share information across time. A cheap way to test whether that's doing real work, without retraining anything, is to break the ordering directly — literally shuffle the input patches into a random sequence before showing them to the model, and see how much worse the forecast gets. If temporal attention is genuinely using the order, scrambling it should hurt substantially."

**Motivation:** "With channel attention and the lift's theory both ruled out, temporal attention was the last major untested candidate. I tested it cheaply, without a full retrain."

**Method:** "Three probes on the existing checkpoints: shuffling the order of patches before feeding them in, shrinking how much context the model sees, and directly inspecting attention maps."

**Result:** "The shuffling test's literal pass/fail gate says escalate to a full retrain — but a natural rescaling of the same result reverses that verdict entirely, so it's not trustworthy either way. The context-shrinking result looked cleaner, but a completely non-learned baseline — just a linear fit, no attention mechanism at all — reproduces the same pattern almost exactly."

**Supersession:** "So this is weak and partly self-undermining evidence. I chose not to invest in the expensive full retrain given how shaky the cheap evidence is — that's a deliberate deprioritization, not a final rejection."

## Slide 11 — Structure Statistic / TDA

**What it is:** "Quick definition before I get into this one, since it's a less familiar tool. Persistent homology looks for genuine loops in a cloud of data points. The mechanism: grow a small ball around every point, and watch how they connect as the balls get bigger. If the points trace out something like a ring, at some point the connections form a closed loop with a real hole in the middle — and if that hole survives across a wide range of ball sizes before finally closing up, that's a genuine, robust feature, not noise. I'm applying this to windows of a single time series, reconstructed the same way Panda's own patches are built — so a strong, long-lived loop here means the signal has real periodic or rotational structure, and a weak one means it doesn't."

**Motivation:** "This is the other direction you proposed last time — persistent homology, essentially asking whether there's real geometric or topological signal distinguishing where Panda wins from where it doesn't."

**Method:** "I built this carefully — three rounds of validating the tool on signals with known answers before ever touching real data, since two earlier attempts at similar geometric estimators had failed silently in this project before. That validation process itself caught real bugs in the pipeline before they could produce a misleading result."

**Result:** "On real data, I found something real: Weather's twenty-one channels split cleanly — temperature and humidity-type channels show strong structure, wind and radiation channels don't. But the more exciting claim — that this explains the Weather-versus-ETTh difference — didn't survive a control where sampling rate was matched between the two datasets. That separation turned out to be a sampling-rate artifact, not a real difference in the underlying dynamics."

**Supersession:** "So this direction is real but narrower than hoped — a genuine finding about Weather's internal structure, not the broader topological story originally set out to test."

## Slide 12 — Branch B Nulls, Plus One Active Lead

**What it is:** "This table covers four separate 'maybe it's actually this instead' explanations for the advantage — whether it depends on how finely the data is sampled in time, how the raw signal gets encoded into channels, whether Chronos was evaluated on forecast lengths longer than it was built for, or how close a dataset looks statistically to what Panda originally trained on. Plus, on the right, one pattern that isn't a null at all."

**Motivation:** "A few smaller candidate explanations also tested."

**Result:** "Resolution — does the advantage depend on fine sampling detail? No support. Representation — does it depend on how the Burgers field is encoded? Mostly robust, doesn't depend on encoding choice. Whether Chronos was evaluated outside its trained horizon range — not supported either. And whether the advantage tracks how similar a dataset is to Panda's own training distribution — weak, never reaches real significance."

"One exception, genuinely different in kind — a pattern in how many periods of a signal fit in the context window. This one's *replicated* across two separate random seeds, and there's a concrete, testable reason it might be happening, tied to Panda's own patch size. Still an open, active lead, not a closed result."

## Slide 13 — Headline

**Motivation/Result, stated plainly:** "So here's where the mechanism hunt lands. Five separate candidates tested — channel attention, the lift's geometry, temporal attention, resolution, and distributional similarity. None of them cleanly explains Panda's advantage. And I want to be precise about what that does and doesn't mean: the advantage itself, which I just showed strong evidence is real and dynamical, is completely untouched by any of these nulls. What's unresolved is *where in the architecture* that sensitivity lives — not whether it exists."

**Supersession:** "Given that, a decision was made: rather than keep testing individual components one at a time, the strategy shifts. That's the second half of this talk."

---

## Slide 14 — Heterogeneity Collapse, Part 1

**What it is:** "Quick definition first. Weather's twenty-one channels aren't interchangeable copies of the same measurement — they're physically different quantities: temperature, humidity, wind speed, pressure, radiation, each with its own characteristic behavior over time. A 'homogeneous' subset here means channels that behave dynamically similarly to each other — say, several temperature-related quantities that all move together. A 'heterogeneous' subset means channels that are dynamically dissimilar — pairing something slow and smooth, like temperature, with something spiky and different in character, like wind. The question was whether Panda specifically struggles when it's forced to jointly attend across channels that don't behave alike."

**Motivation:** "Back to last meeting's strongest finding, in more detail. The original claim: Panda specifically struggles when Weather's channels are dynamically dissimilar from each other — different physical quantities, different behavior — even after controlling for how individually difficult each channel is to forecast."

**Method:** "Three converging experiments at the time, each adding another statistical control, all at eight evaluation windows."

**Result:** "At eight windows, Panda's error nearly doubled going from homogeneous to heterogeneous channel subsets — an eighty-three percent increase. At twenty windows, the same exact channels, same protocol: four percent. And at one horizon, the direction of the effect actually reverses."

## Slide 15 — Heterogeneity Collapse, Part 2

**Method continued:** "The collapse wasn't just accepted at face value — every alternative explanation got ruled out. Could the model itself be non-deterministic between calls? No, confirmed bit-for-bit identical. Could the smaller sample have happened to cluster in one season? Checked directly, not the case. Could the channel indices have been mismatched between the two runs? Verified byte-identical against the original source code."

**Result:** "None of it. The honest conclusion is that the original finding was small-sample noise in which windows happened to get selected, not a real property of the architecture."

**Supersession:** "Direct consequence: your suggested next step from last time, node embeddings for sensor identity, was built entirely on this finding being real. It isn't, so that direction is retired — not paused, retired, since there's nothing left for it to explain."

---

## Slide 16 — Harmonic Retraction, Part 1

**What it is:** "Simulating any smooth trajectory means numerically stepping forward in tiny discrete jumps in time, since you can't compute it continuously. The simplest such method takes a step using the trajectory's current velocity and re-evaluates from there. For most systems that's fine at a small enough step size — but for an object oscillating with no friction at all, this specific method has a mathematical guarantee of instability: each step overshoots by a tiny amount, and that tiny overshoot compounds every single cycle, forever."

**Motivation:** "Second hard lesson. Last time, I told you Panda beats Chronos badly on a plain, simple sine wave — the cleanest evidence I had against chaos being a necessary condition for the advantage."

**Method:** "The way I generated that signal used a simple, fixed-step numerical integration method. For an undamped oscillator specifically, that method is mathematically guaranteed to be unstable — the signal's amplitude grows without bound, slowly but surely, for purely numerical reasons that have nothing to do with the true dynamics."

**Result:** "I measured it directly. Within a single evaluation window — the exact five-hundred-and-twelve-step chunk the model actually sees — the signal's amplitude grows by thirty-seven percent. Across the full trajectory, forty-two times."

## Slide 17 — Harmonic Retraction, Part 2

**Result continued:** "On a corrected, numerically stable version of the same signal, the advantage collapses by ninety-nine percent and stops being reliably significant. Decomposing which model actually moved once the fix was in: Chronos's error dropped about twenty-seven fold; Panda's only dropped about seven fold. Chronos improved four times more than Panda did — meaning the original result was mostly about Chronos failing badly on a broken, runaway signal, not genuine Panda capability on a clean one."

**Supersession:** "Consequence: the claim that chaos isn't necessary for Panda's advantage now rests entirely on the Burgers result alone, not on Harmonic anymore. And given this bug's specific cause — an unstable integrator — I went back and checked every other place in the project using a similar integration method, to make sure this wasn't hiding elsewhere too. That's coming up in a couple slides."

---

## Slide 18 — G1: Rollout-Structure Preservation

**What it is:** "Two things worth defining here. First, 'rollout' — Panda's native forecast only covers a fixed number of steps, so getting a longer forecast means feeding the model's own output back in as new input and calling it again, chaining several forecasts together. Second, the measure used to check the result — it estimates how many effective dimensions a cloud of points fills. A real chaotic attractor has a specific, often fractional, dimension, and a forecast that stays faithful to the true dynamics should reconstruct a point cloud with close to that same dimension, rather than collapsing into something simpler or blowing up into shapeless noise."

**Motivation:** "A genuinely new, positive lead. All the accuracy metrics so far measure pointwise error — did the model get the right number at each step. This asks a different question: when Panda forecasts many steps ahead by chaining its own predictions forward, does the resulting trajectory still trace out the *correct shape* of the underlying attractor, not just individually accurate points?"

**Method:** "I used a classical geometric measure of attractor dimension, validated carefully against known cases before trusting it — this is the first time in the project's history this particular family of estimator actually passed its own validation."

**Result:** "On the two systems tested, Panda's multi-step forecasts preserve the correct attractor dimension far better than Chronos's — between two and eight and a half times better, depending on the system."

**Supersession:** "One honest caveat: this is only two systems, one trajectory each — a real, promising signal, but not yet at the same evidentiary tier as the other high-confidence findings. Along the way, a genuine physics bug got caught and fixed in one of the simulations, and one of the retrained checkpoints turned out to behave slightly differently across separate computing sessions — a hardware-level quirk, not a scientific finding, but worth knowing about."

## Slide 19 — Full-Scale Univariate Confirmation

**What it is:** "Quick reminder — univariate here means each of the twenty-one channels gets run through the model completely separately, one at a time, with zero information about any other channel. Whatever error each channel produces then gets pooled together into one overall number, rather than any single channel being cherry-picked as a representative case."

**Motivation:** "One clean gap noticed and closed. Channel attention had been tested four separate times, but never at full scale — twenty-one channels — directly against Chronos, matching the original benchmark protocol exactly."

**Method:** "Same protocol as the very first Weather benchmark, just with channel attention effectively switched off by construction — each channel is fed to the model on its own, one at a time, so there's nothing for the attention mechanism to attend across."

**Result:** "The advantage holds at every horizon tested, with the strongest statistical significance anywhere in this entire investigation."

**Supersession:** "This is now the fifth and strongest independent piece of evidence that channel attention isn't what's driving Panda's advantage."

## Slide 20 — Duffing Integrator Audit

**What it is:** "Same numerical-stepping concern as Harmonic, but this oscillator has a friction-like damping term built into its equations. Damping actively removes energy from the system every step, which can cancel out the small artificial energy the stepping method keeps injecting — so the same kind of bug doesn't necessarily produce the same kind of runaway growth here."

**Motivation:** "Given what was just found with Harmonic, the obvious next question: does that same bug exist anywhere else in the project? One other system uses the identical style of numerical integration."

**Method:** "The same two checks that caught the Harmonic problem got run here too — how much does the signal's amplitude grow within one evaluation window, and does its long-run statistical behavior match a numerically trustworthy reference."

**Result:** "Both checks pass cleanly, well within safe limits. No caveat needed — that result stands exactly as reported."

**Supersession:** "None — this confirms an existing result rather than changing anything. The likely reason it survived where Harmonic didn't is that this system has damping, which actively cancels out the kind of numerical error that broke Harmonic's undamped case — which is itself a useful, predictive way to think about where else this kind of bug could hide."

---

## Slide 21 — The Pivot

**What it is:** "Right now, the lift's expanded features are computed once from fixed random weights and never touched again during training — only the layers after it actually learn. Making it 'trainable' means letting gradient descent adjust those specific weights too, the same way every other part of the network already gets trained, instead of leaving them frozen at their original random values."

**Motivation:** "So — five nulls on explaining the advantage, one genuinely open behavioral pattern from the ablation work. The decision was to stop asking 'why' and start asking 'can this be made better.' First target: making the Koopman lift trainable instead of fixed."

**Method:** "A1 showed the fixed lift helps on chaotic systems and hurts on Burgers. A3 showed the fixed lift isn't even doing the kind of mathematical operation its own theory claims. So the live question is: is the fixedness itself the problem? The plan is to unfreeze just the random Fourier features, keep everything else the same, and compare three versions — the original baseline, the ablated version, and this new trainable version. Validation happens on data the model has seen the shape of before anything out of distribution gets looked at."

**Result/honesty:** "Predictions were written down before running this. Given how the last several tests have gone, honestly — a clean win doesn't seem like the most likely outcome. But even a negative result here would be informative, and that's exactly what this was designed to produce either way."

## Slide 22 — Next Steps

**Result:** "The trainable lift is ready to run. Separately, Professor Salim suggested looking at ERA5 and BARRA-R — real reanalysis weather data. That fills a real gap in everything done so far: every real-world dataset tested is non-chaotic, and every chaotic system tested is synthetic. This would be the first chance to test the original question on data that's both."

**Ask:** "I'd value the group's thinking on priority between the trainable lift, the real-chaotic-data direction, and a joint ablation testing multiple components at once — and anything from the tree that's been mischaracterized or compressed too much tonight."

## Slide 23 — Thank You

"That's everything. Happy to take questions, and I have the full experiment tree open if there's anything you'd like me to go into further."
