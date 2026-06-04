# Experiment 012 — Active Inference Engine
**Layer:** L4–L5 (Cognitive / Active Inference)
**Date:** 2026-06-03
**Version:** v2.0

---

## Problem

Does a hierarchical predictive coding system with Active Inference policy selection
actually minimize free energy and achieve positive NPG?

In v1.3 the implementation claimed to do this but did not.
This experiment documents the failure modes and the v2.0 corrections.

---

## UAF Answer

A hierarchical system minimizes free energy if and only if:

1. Bottom-up signals are precision-weighted (not raw) prediction errors.
2. The baseline for NPG is fixed before training begins.
3. Precision is updated on a slower timescale than beliefs and is bounded.
4. The environment is mean-reverting (or the system has sufficient capacity to track drift).

These conditions follow directly from FORMAL_CORE §4–6, §10.

---

## v1.3 Failure Analysis

### Failure 1 — Raw error propagation
**Code:** `current_obs = error` in the bottom-up loop.
**Effect:** L1 received the raw prediction error of L0 as its "observation."
This error grew without bound because L0's environment state drifted cumulatively.
L0's free energy reached ~237; precision hit the clip ceiling.
**Theoretical source:** FORMAL_CORE §6 — the upward signal must be
precision-weighted and normalized to remain informative.

### Failure 2 — Moving baseline
**Code:** `self.baseline_fe = 0.95 * self.baseline_fe + 0.05 * avg_fe`
**Effect:** baseline tracked the model's own trajectory.
NPG > 0 became trivially achievable since both model and baseline grew together.
When L0 diverged, baseline grew with it, masking the divergence.
**Theoretical source:** FORMAL_CORE §10 — baseline must be fixed.
NPG measures compression *relative to a reference*, not self-relative improvement.

### Failure 3 — Unbounded environment drift
**Code:** `self.state += self.drift + ...`
**Effect:** environment state grew without bound (random walk with drift).
Even a perfect model cannot track an unbounded random walk with bounded precision.
**Fix:** AR(1) mean-reverting dynamics: `state = 0.95 * state + noise`.

---

## v2.0 Corrections

### Fix 1 — Normalized upward signal
```python
norm = np.linalg.norm(e) + 1e-8
current_input = np.tanh(e / norm)  # bounded to [-1, 1]
```
This normalizes the error before passing it to the next level.
Each level now receives a signal of consistent scale.

### Fix 2 — Fixed baseline
```python
self._baseline_fe = self._estimate_initial_baseline(n=20)
# Never updated during training.
```
Baseline is estimated from n=20 random-policy steps before training begins.

### Fix 3 — Mean-reverting environment
```python
self.state = 0.95 * self.state + action_effect + noise
```
AR(1) coefficient 0.95 keeps the state distribution stationary.

### Fix 4 — Slow precision learning
```python
self._precision_lr = 0.01   # 10x slower than belief lr = 0.1
```
Precision adapts on a longer timescale, preventing instability.

---

## Results (v2.0, 500 steps, seed=42)

| Level | NPG (last 50 steps) | FE (last 50 steps) | Precision |
|-------|--------------------|--------------------|-----------|
| L0_Sensory   | +0.833 | 0.084 | 0.263 |
| L1_Cognitive | +0.896 | 0.052 | 0.156 |
| L2_Social    | +0.928 | 0.036 | 0.100 |

FE trajectory: 0.26 → 0.057 (**↓ converged**)
All NPG > 0 (**all levels better than fixed baseline**)

---

## Surprise Reduction

The key insight is that **architectural choices in the implementation are not engineering details — they are expressions of the theory.** Specifically:

- Raw error propagation violates the hierarchical message-passing protocol of predictive coding.
- Moving baseline violates the operational definition of NPG as a fixed-reference measure.
- Unbounded random walk violates the assumption that observations come from a stationary generative process that the system can, in principle, learn.

These are not bugs. They are theory failures: the code was not derived from FORMAL_CORE; it was written independently and then justified post-hoc. v2.0 corrects this by tracing every function to a section of FORMAL_CORE.

**NPG estimate for this experiment:** > 0.8 on all levels.
