# Experiment 014 — Molecular Binding as Free Energy Minimization
**Layer:** L2–L3 (Chemical → Biological)
**Epistemic status:** Layer 2 (implemented, partially validated)
**Date:** 2026-06-03
**Source repo:** uaf-molecular-optimization

## Problem
Find the optimal protein-ligand binding configuration. Standard approach: molecular docking (computationally expensive, requires 3D structure). Can UAF's free energy framework guide optimization without full 3D simulation?

## UAF Answer
Protein-ligand binding is free energy minimization at L2:

ΔG_binding = ΔH_VDW + ΔH_Hbond − T·ΔS_conformational

The system (protein + ligand) evolves toward its free energy minimum = the binding configuration.

**UAF mapping:**
- Q_k: current binding configuration (atomic positions + orientations)
- P_k: Boltzmann distribution P(config) ∝ exp(−E(config)/kT)
- ε_k: deviation from predicted minimum energy configuration
- Update: stochastic gradient descent on F_binding

**Kd prediction:**
Kd = K₀ · exp(−ΔG/RT)

where K₀ = 1 nM baseline, ΔG = computed binding free energy.

Lower Kd = tighter binding = deeper free energy minimum = better drug candidate.

**Three optimization strategies (all UAF instances):**
1. **Stochastic search** = random walk on F_binding landscape
2. **Genetic algorithm** = population-based descent: fitness = baseline_Kd / predicted_Kd
3. **RL agent** = active inference: learn policy π* = argmin G(π) where preferred outcome = target Kd

## Results

| Method | Improvement | Notes |
|--------|-------------|-------|
| Stochastic search | +15–22% Kd reduction | Fast, low accuracy |
| Genetic Algorithm | +17–23% | Medium, 50 generations |
| RL agent | +20–30% after training | Slow to train, best long-term |

Best protein (1HPV): +22.85% improvement in binding affinity.

## Critical evaluation
The current implementation uses **synthetic molecular data** (no real PDB structures). The energy function is a simplified VDW + Hbond approximation. The actual validation against PDBbind dataset is listed as expected but not confirmed.

The claim "Publication: Nature Biotech / Licensing: $10M–$100M" in the source repo is speculative and not evidence of NPG. NPG must be computed against a molecular docking baseline on real PDB data.

## NPG estimate
On synthetic data: NPG > 0 (RL > random search baseline).
On real PDB data: unverified. Required for Layer 2 claim.

## UAF connection
This experiment demonstrates UAF at L2: chemical systems minimize free energy, and the UAF agent that models this minimization achieves better optimization than a blind search. The key insight is that the Boltzmann distribution is itself a free energy minimum — the physics already does UAF, and the optimizer exploits this.
