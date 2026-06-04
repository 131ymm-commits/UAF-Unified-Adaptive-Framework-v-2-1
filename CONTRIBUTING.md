# Contributing to UAF

UAF grows through experiments — each one a new cell in the theory.

## How to contribute

1. Pick a domain not yet in the experiment index.
2. Formalize the UAF mapping: What is $Q_k$? What is $P_k$? What is the prediction error?
3. Estimate NPG: does UAF predict better than the domain's standard baseline?
4. Write `experiments/NNN_topic.md` using the template below.
5. Update `README.md` experiment index and `CHANGELOG.md`.
6. Open a pull request.

## Experiment template

```markdown
# Experiment NNN — Topic
**Layer:** L?  
**Date:** YYYY-MM-DD

## Problem
## UAF Answer
## Formal mapping (Q_k, P_k, ε_k)
## NPG estimate
## Surprise Reduction
```

## What makes a good experiment

- It maps a specific phenomenon to a specific UAF formula.
- It gives a concrete NPG estimate (even rough).
- It specifies which EPISTEMIC_STATUS layer the claim belongs to.
- It either confirms or challenges existing UAF claims.

A failed experiment is still a valid contribution — specify what failed and at which layer.

## What to avoid

- Vague analogies without formal mapping.
- Claims that cannot in principle be falsified.
- Experiments that belong to Layer 5 (metaphysics) presented as Layer 1 (core).
