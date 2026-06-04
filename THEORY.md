# UAF Theory
**v2.0 — Iteration II — 03.06.2026**

---

## 1. Core intuition

UAF begins from a simple observation:

*Stable systems behave as if they maintain boundaries, update states, and reduce prediction error.*

This does not mean every system is conscious or agentic.  
It means every stable system has a structure that can be formally described as a predictive constraint.

A thermostat, a cell, a brain, a language, and a scientific community are not the same thing.  
But each can be modeled as a system that persists by reducing expected surprise.

This is not metaphor. It is a claim about the mathematical structure shared across substrates.

---

## 2. The basic unit

A UAF system at level $k$ is defined as:

$$S_k = (Q_k,\, P_k,\, B_k,\, \Delta_k,\, U_k)$$

where:
- $Q_k$: current belief/state distribution (the internal model),
- $P_k$: generative model or prior (what the system expects),
- $B_k$: boundary — what separates the system from environment,
- $\Delta_k$: prediction horizon — how far ahead the system models,
- $U_k$: update operator — the rule by which the system revises $Q_k$.

The basic cycle is:

$$Q_k(t) \xrightarrow{\text{predict}} \hat{o}_{t+\Delta} \xrightarrow{\text{observe}} o_{t+\Delta} \xrightarrow{\text{error}} \mathcal{S}_k \xrightarrow{\text{update}} Q_k(t + \Delta)$$

Every iteration either reduces surprise or the system destabilizes.

---

## 3. Surprise

$$\mathcal{S}_k(t) = -\ln P_k(o_t \mid Q_k)$$

Surprise is negative log-likelihood.  
It is not emotion. It is not subjective discomfort.  
It is the information-theoretic cost of observing $o_t$ given model $Q_k$.

**Key property:** minimizing expected surprise is equivalent to maximizing model evidence.  
A system that keeps surprise low has an accurate generative model of its environment.

---

## 4. Variational free energy

Because computing $-\ln P(o)$ directly requires marginalizing over all hidden states (often intractable), systems use a variational approximation. The variational free energy is:

$$\mathcal{F}[Q] = \mathbb{E}_{Q(s)}[\ln Q(s) - \ln P(o, s)]$$

This decomposes as:

$$\mathcal{F}[Q] = \underbrace{\mathbb{E}_{Q(s)}[-\ln P(o \mid s)]}_{\text{inaccuracy}} + \underbrace{D_{\mathrm{KL}}(Q(s) \| P(s))}_{\text{complexity}}$$

And satisfies:

$$\mathcal{F}[Q] \geq -\ln P(o)$$

Free energy is an upper bound on surprise.  
Minimizing $\mathcal{F}$ simultaneously reduces model inaccuracy and prevents the model from deviating unnecessarily from its prior (Occam's razor built in).

---

## 5. Active inference

Agents do not only update models to match observations.  
They also *act* to make future observations less surprising.

This is the key extension from passive Bayesian updating to active inference.

**Expected free energy** for policy $\pi$:

$$G(\pi) = \underbrace{D_{\mathrm{KL}}(Q(\tilde{o} \mid \pi) \| \tilde{P}(\tilde{o}))}_{\text{risk: how far predicted outcomes are from preferred}} + \underbrace{\mathbb{E}_{Q(\tilde{s} \mid \pi)} H[P(\tilde{o} \mid \tilde{s})]}_{\text{ambiguity: uncertainty in outcomes given states}}$$

Policy selection:

$$\pi^* = \arg\min_\pi G(\pi)$$

This gives a unified account of curiosity (seeking to reduce ambiguity), goal-directedness (minimizing risk), scientific inquiry, social coordination, and planning — all as special cases of EFE minimization.

---

## 6. Hierarchy

A single level cannot model everything.  
Hierarchy emerges when the prediction errors of one level become the inputs of the next.

**Bottom-up:** prediction errors propagate upward as signals requiring explanation.

$$\mathrm{input}_{k+1}(t) = \varepsilon_k(t) = o_k(t) - \hat{o}_k(t)$$

**Top-down:** higher-level beliefs constrain lower-level priors.

$$P_k(s) \leftarrow P_k(s \mid Q_{k+1})$$

Therefore hierarchy is not a ladder of substances.  
It is a ladder of prediction horizons — each level modeling what the level below cannot predict from within.

The multi-level coupling introduces cross-level coherence terms:

$$\mathcal{F}_{\mathrm{total}} = \sum_k \mathcal{F}_k + \sum_k \lambda_k \, D_{\mathrm{KL}}(\Pi_{k \to k+1} Q_k \| Q_{k+1}) + \sum_k \gamma_k \mathcal{T}_k$$

where $\Pi_{k \to k+1}$ is a representation map, $\mathcal{T}_k$ is a topological complexity term, and $\lambda_k, \gamma_k$ are coupling weights that can be learned.

---

## 7. Precision and attention

Not all prediction errors are weighted equally.  
**Precision** $\pi_k$ is the inverse variance assigned to a prediction error signal.

$$\pi_k = \frac{1}{\sigma_k^2}$$

High precision = the system trusts this error signal and updates strongly.  
Low precision = the system discounts this signal.

This gives a formal account of attention: attended stimuli receive high precision weighting. The precision itself is a parameter to be optimized — a system learns which signals to trust.

**Important constraint (v2.0 fix):** Precision must be bounded and learned on a slower timescale than the belief update. Unbounded precision growth leads to divergence, not convergence. In the implementation, precision is updated with a small learning rate and hard-clipped.

---

## 8. Truth as attractor

In UAF, truth is not merely a correspondence relation between statement and fact.  
Truth is a stable attractor in model space.

Let $Q(t)$ evolve by gradient descent on free energy with noise:

$$\dot{Q} = -\nabla_Q \mathcal{F} + \eta(t)$$

A truth-attractor is:

$$\mathcal{A} = \left\{ Q : \dot{Q} \approx 0, \quad Q \text{ stable under perturbation} \right\}$$

A model is "more true" if it lies in a larger and more stable basin of predictive attraction — a basin that persists across more diverse data, more agents, and more perturbations.

---

## 9. Normalized Predictive Gain (NPG)

NPG is the operational measure of theory quality. Given model $M$, baseline $B$, dataset $D$:

$$\boxed{\mathrm{NPG}(M; D, B) = \frac{L(B, D) - L(M, D)}{L(B, D) + \varepsilon}}$$

where $L$ is predictive loss (negative log-likelihood, cross-entropy, Brier score, or MDL description length).

Properties:
- $\mathrm{NPG} = 0$: model equals baseline.
- $\mathrm{NPG} \to 1$: model nearly eliminates the baseline's loss.
- $\mathrm{NPG} < 0$: model is worse than baseline — reject.

**Critical requirement (v2.0):** Baseline must be fixed before evaluation begins, not adapted during the run. An adaptive baseline that tracks model performance makes NPG meaningless as a metric.

---

## 10. UAF and mathematics (L−1)

Mathematics is treated as L−1: the structural substrate of possible prediction.

Mathematical structures are useful when they reduce description length:

$$M \text{ applies to domain } D \iff K(D \mid M) \ll K(D)$$

where $K$ is Kolmogorov complexity.

Thus mathematics is neither purely invented nor naively Platonic.  
It is the discovered language of compressible invariance — the set of structures that make prediction possible across diverse substrates.

Five deep problems reframed by UAF:
- **Wigner problem** (unreasonable effectiveness): mathematics = language of stable prediction, inevitable for any persistent structure.
- **Axiom of Choice**: decision under incomplete information = approximate inference.
- **Continuum Hypothesis**: undecidability = multiple compression schemes are equally valid.
- **Russell paradox**: self-reference without boundary = a UAF system without $B_k$.
- **Infinity**: limit of prediction horizon $\Delta_k \to \infty$.

---

## 11. Prediction homomorphism

Different systems implement the same abstract operation on different substrates:

$$-\ln P(o \mid Q)$$

A neuron predicting spike timing, a scientist predicting experimental outcomes, an LLM predicting the next token — these are not identical systems. But they are **homomorphic as predictors**: the mathematical structure of what they do is the same.

This is UAF's core claim. Not that everything is consciousness. Not that physics is "just Bayesian inference." But that prediction-error minimization is a genuine structural invariant across scales.

---

## 12. UAF is judged by the same criterion

$$\mathrm{NPG}_{\mathrm{UAF}} > 0$$

If UAF does not compress explanations relative to existing theories in a given domain, it fails in that domain.  
A flaw in the cosmological extension does not damage the core. A speculative metaphor is not allowed to masquerade as a theorem.

The framework protects itself from both arrogance and triviality by the epistemic layer system defined in `EPISTEMIC_STATUS.md`.
