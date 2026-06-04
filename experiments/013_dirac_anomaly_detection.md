# Experiment 013 — Dirac Anomaly Detection as UAF Level-0 Surprise Detector
**Layer:** L0–L4
**Epistemic status:** Layer 2 (implemented, benchmarked)
**Date:** 2026-06-03
**Source repo:** uaf-dirac-anomaly

## Problem
Online anomaly detection in time series: detect regime shifts, spikes, and collective anomalies in real-time without retraining, with low false positive rate.

## UAF Answer
An anomaly is a spike in surprise S_k(t) = −ln P_k(o_t | Q_k) at some level k.

The UAF Dirac Agent implements this by modeling the time series as a 2-component spinor (a, b) evolving under a Dirac-like Hamiltonian:

H = p·σ_x + κ·σ_y + m·σ_z

where:
- **p** (momentum) = present flow pressure (first derivative of signal)
- **κ** (curvature) = local reorientation rate (second derivative)
- **m** (mass) = structural inertia from regime history (EMA of past values)
- σ_i = Pauli matrices acting on the spinor state

**UAF mapping:**
- Q_k: spinor state (a, b) = belief about current regime
- P_k: Dirac generative model = expected spinor evolution
- ε_k: anomaly score = weighted combination of gap breach, inversion, zitter

**Anomaly components (three surprise channels):**
1. **Gap breach**: |p² + κ²| / m > 1 → mass-gap violation = regime change surprise
2. **Inversion**: |a|² − |b|² < 0 → spinor polarization flip = structural inversion
3. **Zitter** (Zitterbewegung): |dE/dt| spike = energy jump = sudden prediction error

**Composite surprise score:**
score = w_gap · gap_breach + w_inv · inversion + w_zit · zitter

**Precision weighting:** precision π = 1/σ²_baseline determines the threshold for flagging anomalies. This is exactly the UAF precision mechanism (FORMAL_CORE §5).

## Results (from benchmarks)

| Dataset | Category | F1-Score |
|---------|----------|----------|
| Machine Temp | realKnownCause | 0.60–0.75 |
| NYC Taxi | realKnownCause | 0.45–0.65 |
| Market Data | realKnownCause | 0.55–0.70 |
| EC2 CPU | realAWSCloudwatch | 0.50–0.70 |
| NAB standard score | aggregate | ~84.2 |

Reported to exceed ARTime baseline (74.85) on NAB standard scoring.

Processing speed: ~5,000–10,000 points/second. Memory: <1 MB per 10k points.

## UAF interpretation of the Dirac spinor
The two-component spinor is not a formal physics analogy — it is a concrete implementation of UAF's binary belief state at L0:
- Component a = "structure" amplitude (mass/past regime dominates)
- Component b = "motion" amplitude (momentum/present flow dominates)
- Polarization |a|² − |b|² = balance between crystallized past and present prediction

A negative polarization (inversion anomaly) means the system's present state is more uncertain than its past model predicts — exactly the definition of UAF surprise.

## NPG estimate
Against constant-threshold baseline: NPG > 0.4 on NAB.
Against ARTime (74.85 NAB standard): NPG > 0 if reported ~84.2 is reproducible.

**v2.0 note:** The Dirac agent uses a moving baseline for its z-score normalization. This is acceptable for anomaly detection (where the goal is detecting changes relative to recent history), unlike the Active Inference Engine where the baseline must be fixed for NPG to be meaningful as a theory metric.
