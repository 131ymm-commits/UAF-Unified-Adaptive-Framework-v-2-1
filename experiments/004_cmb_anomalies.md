# Experiment 004 — CMB Anomalies as L−1→L0 Prediction Residue
**Layer:** L−1 → L0
**Epistemic status:** Layer 4 (speculative, testable direction)
**Date:** 2025-07-13 / revised 2026-06-03

## Problem
The CMB power spectrum from Planck 2018 shows several anomalies not predicted by ΛCDM:
1. Low quadrupole power (l=2 suppressed by ~10×)
2. Hemispherical asymmetry (power asymmetry between two hemispheres)
3. Cold spot (anomalously cold region ~5° across)
4. Alignment of low multipoles (quadrupole and octupole are aligned)

ΛCDM treats these as statistical flukes (p ~ 0.1–5%). UAF asks: are they traces of prediction structure from the L−1 → L0 transition?

## UAF Answer
The CMB is the earliest accessible observation at L0 — the first level where temporal prediction becomes defined. The prior P_{L0} was set at the L−1 → L0 transition.

If the L−1 structure had non-trivial topology (e.g., compact spatial sections, or anisotropic initial coherence), the CMB would show:
- Suppressed large-angle correlations (consistent with low quadrupole)
- Topological alignment (consistent with multipole alignment)
- Localized cold spots (consistent with specific L−1 boundary conditions)

## Concrete research direction (Roadmap Priority 4)

Tools: healpy, giotto-tda, CAMB

Protocol:
1. Compute Betti numbers β₀, β₁, β₂ of the CMB temperature field at each threshold.
2. Construct persistence diagrams of the filtration.
3. Compare persistence diagrams of Planck 2018 data vs. 1000 ΛCDM simulations.
4. Test: are the anomalous features stable under the TDA filtration (high persistence) or noise (low persistence)?

Hypothesis: the anomalies have higher topological persistence than predicted by ΛCDM. This would be a falsifiable signal of non-trivial L−1 structure.

## NPG estimate
Currently 0 (no implementation). If the TDA comparison yields statistically significant differences: NPG > 0 against ΛCDM as baseline.
