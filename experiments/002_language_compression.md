# Experiment 002 — Language as Collective Free Energy Minimization
**Layer:** L4–L6 (Neural → Social)
**Epistemic status:** Layer 2 (cross-domain interpretation)
**Date:** 2025-07-13 / revised 2026-06-03

## Problem
There are ~10 major linguistic theories (Chomsky's generative grammar, usage-based linguistics, optimality theory, construction grammar, etc.) that appear incompatible. Can UAF reduce them to one equation?

## UAF Answer
Language is a collective active inference system at L5–L6. A language community is a set of agents {A_i} with shared prior P(utterance | context) that jointly minimizes:

F_language = Σᵢ F_i(Q_i || P_shared) + λ · C({Q_i})

where C is the cross-agent consistency penalty (FORMAL_CORE §12).

Each linguistic theory captures one aspect:
| Theory | UAF component |
|--------|--------------|
| Chomsky UG | Prior structure P_shared (innate bias) |
| Usage-based | Likelihood P(o|s) learned from data |
| Optimality Theory | Constraint = F minimization under competing priors |
| Construction grammar | Chunked beliefs in Q (reusable prediction units) |
| Gricean maxims | EFE minimization: say what reduces listener's F most |
| Language change | Drift in P_shared as generations update the collective prior |

All are projections of F_language onto different components of the variational decomposition.

## NPG estimate
Qualitative compression: 10 theories → 1 equation.
Formal NPG requires specifying a prediction task and a dataset. Candidate: predict pragmatic inference from syntactic form, UAF vs. each individual theory.

## Implications
- Grice's cooperative principle = EFE minimization by the speaker.
- Zipf's law = the power law that minimizes expected description length in a communication system.
- Language death = collapse of shared prior when cross-agent consistency pressure drops to zero.
