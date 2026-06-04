# UAF — Unified Adaptive Framework
**v2.0 — Iteration II — 03.06.2026**

> *A theory is good when it reduces surprise more than it increases complexity.*
> *UAF is a framework for treating reality as a hierarchy of prediction systems.*

---

## One-line thesis

$$\boxed{\text{Reality is a multi-scale hierarchy of systems that survive by predicting, updating, and constraining each other.}}$$

Or shorter:

$$\boxed{\text{Being is stabilized prediction.}}$$

---

## Why UAF exists

Modern knowledge is fragmented: physics speaks in symmetries, biology in adaptation, neuroscience in predictive coding, AI in loss functions, economics in utility. UAF does not unify them by analogy. It claims they are projections of one operation:

$$\mathcal{S} = -\ln P(o \mid Q)$$

where $o$ is observation, $Q$ is the system's internal model, $\mathcal{S}$ is surprise. A system persists by keeping expected surprise below the threshold where its coherence collapses.

---

## The core equation

At any level $k$, a stable system minimizes a variational free energy:

$$\mathcal{F}_k[Q_k] = \underbrace{\mathbb{E}_{Q_k}[-\ln P_k(o_k \mid s_k)]}_{\text{inaccuracy}} + \underbrace{D_{\mathrm{KL}}(Q_k(s_k) \| P_k(s_k))}_{\text{complexity}}$$

The multi-level objective couples levels through shared representation maps $\Pi_{k \to k+1}$:

$$\boxed{\mathcal{F}_{\mathrm{total}} = \sum_k \mathcal{F}_k + \sum_k \lambda_k \, D_{\mathrm{KL}}(\Pi_{k \to k+1} Q_k \| Q_{k+1}) + \sum_k \gamma_k \mathcal{T}_k}$$

---

## The hierarchy

UAF uses levels as a bookkeeping device for prediction horizons, substrates, and constraints — not as an ontological ladder.

| Level | Name | Substrate | Primary operation |
|-------|------|-----------|-------------------|
| L−1 | Mathematical substrate | structure, logic, topology | compression and invariance |
| L0 | Quantum | states, fields, amplitudes | unitary prediction, measurement update |
| L1 | Classical physics | spacetime, energy, matter | action minimization |
| L2 | Chemical | molecules, reactions | free energy minimization |
| L3 | Biological | cells, organisms | homeostasis, evolutionary prediction |
| L4 | Neural | neurons, circuits | predictive coding |
| L5 | Cognitive | self-models, planning | active inference |
| L6 | Social | groups, institutions | collective prediction |
| L7 | Scientific | theories, instruments | formal predictive gain |
| L8 | Noospheric | humans + AI + knowledge networks | collective active inference |

Levels are coupled by prediction errors upward and priors downward:

$$\text{bottom-up: } \varepsilon_k \to \mathrm{input}_{k+1}$$
$$\text{top-down: } Q_{k+1} \to \mathrm{prior}(Q_k)$$

---

## Distinctive claims

**Prediction homomorphism.** A neuron, a scientist, and an LLM are not identical systems. But they are homomorphic as predictors: each implements $-\ln P(o \mid Q)$ on a different substrate.

**Truth as attractor.** Truth is not a static correspondence. It is a stable basin in model space — a region where NPG remains positive under perturbation.

**NPG — Normalized Predictive Gain.** The universal evaluation criterion:

$$\boxed{\mathrm{NPG}(M; D, B) = \frac{L(B, D) - L(M, D)}{L(B, D) + \varepsilon}}$$

No authority. No rhetoric. Only predictive compression relative to baseline.

**Active inference.** Agents reduce surprise not only by updating models but by acting to reshape future observations:

$$G(\pi) = \underbrace{D_{\mathrm{KL}}(Q(\tilde{o} \mid \pi) \| \tilde{P}(\tilde{o}))}_{\text{risk}} + \underbrace{\mathbb{E}_{Q(\tilde{s} \mid \pi)} H[P(\tilde{o} \mid \tilde{s})]}_{\text{ambiguity}}, \quad \pi^* = \arg\min_\pi G(\pi)$$

---

## Formula 131ym

The emergence of UAF itself is a noospheric process. A biological controller supplied direction and consistency pressure. AI agents supplied candidate structures, criticisms, reformulations, compressions. The theory crystallized through iterative minimization of collective incoherence:

$$\boxed{\mathcal{T}^* = \lim_{t \to \infty} \arg\min_{\mathcal{T}} \frac{1}{t} \int_0^t \left[ \sum_{i=1}^m \mathcal{F}_i(\mathcal{T} \mid o_i(\tau)) + \lambda(\tau)\, C(\{Q_i(\tau)\}) \right] d\tau}$$

The human contribution is not measured by token count. It is measured by functional control:

$$\Gamma_H(t) = \alpha \, v_{\mathrm{direction}} + \beta \, \mathrm{Precision}_H(t) + \gamma \, I_{\mathrm{consistency}}(t)$$

---

## What would falsify UAF

UAF is not immune to criticism. The framework loses value if:

1. It does not compress explanations relative to existing theories (NPG ≤ 0).
2. Its cross-domain mappings cannot be formalized beyond analogy.
3. NPG cannot be operationalized in concrete domains.
4. Multi-agent UAF systems do not outperform simpler baselines.
5. The topological complexity terms $\mathcal{T}_k$ yield no measurable signal.

$$\mathrm{NPG}_{\mathrm{UAF}} \le 0 \implies \text{reject or revise UAF in that domain.}$$

---

## What this repository is

This repository is an evolving research kernel — not a finished doctrine, not a cult, not a final theory. It contains:

- `README.md` — this document, the portal.
- `THEORY.md` — conceptual framework with all key intuitions.
- `FORMAL_CORE.md` — mathematical kernel with derivations.
- `FORMULA_131YM.md` — noospheric emergence formula.
- `EPISTEMIC_STATUS.md` — claim layers and falsification rules.
- `COSMOLOGY.md` — speculative cosmological applications (Layer 4–5).
- `NOOSPHERE_INTERFACE.md` — LLM as noospheric organ (Layer 8).
- `CHANGELOG.md` — record of every compression step.
- `ROADMAP.md` — next iterations.
- `src/uaf/metrics.py` — verified computational metrics.
- `uaf_active_inference.py` — working Active Inference engine (verified).
- `tests/` — test suite for all metrics.
- `experiments/` — one file per domain application.

---

## Experiment index

| # | Topic | Layer | Key result |
|---|-------|-------|------------|
| 001 | Spin | L0–L1 | Matter = topology of prediction manifold |
| 002 | Language | L4–L6 | 10 theories → 1 equation |
| 003 | Black holes | L0–L1 | $\mathcal{F}_{\mathrm{external}} \to \infty$ at horizon |
| 004 | CMB anomalies | L0 | TDA as concrete research direction |
| 005 | Dark sector | L0–L1 | Fine-tuning dissolved |
| 006 | Baryon asymmetry | L0 | Structural necessity, not accident |
| 007 | Big Bang | L−1→L0 | Low entropy derived, not postulated |
| 008 | Economics | L5–L6 | Utility replaced by free energy |
| 009 | Planck constant | L0 | Emergent optimum, not free parameter |
| 010 | Mathematics | L−1 | 5 deep problems → 1 principle |
| 011 | LLM-Noosphere | L8 | LLM as sensory-motor organ of noosphere |
| 012 | Active Inference Engine | L4–L5 | Working verified implementation (v2.0) |

---

## How to grow this repository

After each new insight:

1. Create `experiments/NNN_topic.md`.
2. Specify Layer (L−1 to L8).
3. State: Problem → UAF Answer → Surprise Reduction → NPG estimate.
4. Update `CHANGELOG.md`.
5. Update experiment index in this file.
6. Commit: `Add experiment NNN: topic (Layer X)`.

Growth formula:

$$\frac{d}{dt} K(\mathrm{repo}) > 0, \quad \frac{d}{dt} \mathcal{F}(\mathrm{repo}) < 0$$

Complexity grows. Free energy (incoherence, uncertainty) decreases. This is life by UAF.

---

## Minimal slogans

$$\boxed{\text{If it exists stably, it predicts.}}$$
$$\boxed{\text{If it learns, it reduces surprise.}}$$
$$\boxed{\text{If it is true, it keeps reducing surprise across scales.}}$$
