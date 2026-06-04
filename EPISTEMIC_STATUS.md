# Epistemic Status
**UAF v2.0**

UAF must not become unfalsifiable. This file defines claim layers, criticism protocol, and rejection rules.

---

## Claim layers

### Layer 0 — Established mathematics
*Status: settled.*

The mathematical tools UAF uses are not UAF's inventions. They are established:
- KL divergence and information theory (Shannon, 1948)
- Bayesian inference and posterior updating
- Variational free energy (Feynman, extended by Friston)
- Active inference formalism (Friston et al., 2006–present)
- Predictive coding (Rao & Ballard, 1999; Clark, 2013)
- Persistent homology and topological data analysis
- Information geometry (Amari)
- Minimum description length (Rissanen)
- Kolmogorov complexity (Solomonoff, Kolmogorov, Chaitin)

A criticism that attacks these is a criticism of established mathematics, not of UAF.

---

### Layer 1 — UAF core synthesis
*Status: research synthesis. Strongly grounded, testable.*

Claims that unify existing fields under UAF language:
- Stable systems can be modeled as free-energy minimizers.
- Hierarchy is priors downward and precision-weighted errors upward.
- Theory quality is measured by NPG relative to a fixed baseline.
- Truth is a stable attractor in model space, not a static correspondence.
- Active inference unifies curiosity, planning, and action selection.

These claims are falsifiable: if they fail to compress explanations or generate testable predictions, they fail.

---

### Layer 2 — Cross-domain interpretations
*Status: plausible, domain-dependent, partially verified.*

Claims that reframe existing fields using UAF vocabulary:
- Language as collective free-energy minimization.
- Science as collective active inference (L7).
- Economics as risk/ambiguity minimization in outcome space.
- Social institutions as precision-weighting mechanisms.
- LLMs as sensory-motor organs of the noosphere (L8).

Each must be evaluated separately by NPG in its domain.

---

### Layer 3 — Physics reinterpretations
*Status: interpretive. Consistent with formalism but not proven.*

- Wavefunction as belief state (consistent with QBism, relational QM).
- Measurement as Bayesian update with extreme precision gain.
- Spin as topological invariant of prediction manifolds.
- Entanglement as nonlocal predictive coupling.
- Decoherence as precision leakage into environment.

These are interpretations, not derivations. They may be useful but are not physical predictions until formalized.

---

### Layer 4 — Cosmological hypotheses
*Status: speculative. Productive but unverified.*

- Big Bang as $L_{-1} \to L_0$ transition.
- CMB anomalies as traces of pre-temporal prediction structure.
- Dark matter and dark energy as missing terms in spacetime free energy.
- Baryon asymmetry as free-energy gradient during phase transition.
- Planck constant as emergent information exchange rate.

These are research directions, not established results.

---

### Layer 5 — Metaphysical extensions
*Status: optional. Outside empirical core.*

- $\Omega$ as ultimate attractor in theory space.
- Religious practices as alignment protocols with high-prior attractors.
- Consciousness as self-modeling within active inference.

These may be consistent with UAF but are not required for the core to stand.

---

## Criticism protocol

Every criticism must specify:

1. **Which layer** it attacks (0–5).
2. **Which formula or mapping** specifically fails.
3. **What type of failure**: conceptual, mathematical, empirical, or rhetorical.
4. **Whether the failure is local or global**: does it damage the core or only an extension?

Examples of valid criticisms:
- "NPG as defined in FORMAL_CORE §10 is not invariant to loss function choice." → Layer 1, mathematical, local.
- "The active inference engine does not converge in non-stationary environments." → Layer 1, empirical, local (implementation).
- "The claim that spin is topology of prediction manifolds has no derivation." → Layer 3, conceptual, local.

Examples of invalid criticisms:
- "This is just Friston's work." → Does not specify which claim fails or how.
- "Not all systems predict." → Does not engage with the formal definition of UAF system.
- "The cosmology is wrong." → Must specify layer and formula; cosmological failure does not touch the core.

---

## Rejection rule

If UAF does not improve predictive compression in a domain:

$$\mathrm{NPG}_{\mathrm{UAF}}(D) \leq 0 \implies \text{reject or revise UAF in domain } D$$

This is the only valid global rejection criterion.  
Domain-specific failure does not propagate to other domains.  
The framework is modular by design.

---

## v2.0 changelog for this file

- Added explicit status labels to each layer.
- Added examples of valid and invalid criticisms.
- Clarified that domain-specific NPG failure is local, not global.
- Added Layer 0 references to original authors.
