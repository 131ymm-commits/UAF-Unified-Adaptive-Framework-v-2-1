# Roadmap
**UAF v2.0**

---

## Iteration II → III (next cycle)

### Priority 1 — Formalize NPG in a real domain
**Goal:** demonstrate NPG > 0 for UAF vs a standard baseline on real data.

Candidate domains:
- Physics: meson mass prediction (existing dataset). Baseline = naive neural net. UAF agent = free-energy-constrained predictor with explicit level structure.
- Language: next-token prediction with predictive coding hierarchy vs plain transformer.
- Economics: interest rate forecasting. Baseline = ARIMA. UAF = active inference agent.

**Deliverable:** `experiments/013_npg_real_domain.md` + working Python notebook.

---

### Priority 2 — Multi-agent UAF (Formula 131ym operational)
**Goal:** implement the multi-agent consistency penalty $C(\{Q_i\})$ in code.

System: 2–3 independent UAF agents processing different data streams converge to a shared theory.
Metric: $C$ decreases over iterations. NPG of the joint system > NPG of any single agent.

**Deliverable:** `src/uaf/multiagent.py` + `experiments/014_formula_131ym_operational.md`

---

### Priority 3 — Topological complexity term $\mathcal{T}_k$
**Goal:** implement a concrete topological penalty from persistent homology.

Candidate: ripser or giotto-tda for 0-dimensional persistence on belief trajectories.
Hypothesis: adding $\mathcal{T}_k$ to the loss improves convergence in high-dimensional state spaces.

**Deliverable:** `src/uaf/topology.py` + `experiments/015_topological_penalty.md`

---

### Priority 4 — CMB anomaly test (Experiment 004 operationalized)
**Goal:** run TDA on public CMB data (Planck 2018) and check for anomalies
consistent with L−1 → L0 prediction structure.

Tools: healpy, giotto-tda, CAMB for theoretical baselines.
Metric: Betti numbers of CMB temperature field vs ΛCDM simulation.

**Deliverable:** `experiments/016_cmb_tda.md` + Jupyter notebook.

---

### Priority 5 — Action policy improvement
**Current state:** v2.0 agent converges to "wait" 100% of the time in a stationary environment.
This is correct (lowest EFE = exploit the known stable state) but limits exploration.

**Fix:** introduce epistemic value term (information gain) explicitly into EFE:
$G(\pi) = \text{Risk} + \text{Ambiguity} - \kappa \cdot \text{InformationGain}(\pi)$

This is the standard active inference extension for curiosity-driven exploration.

---

## Long-term (Iteration IV+)

- Noosphere simulation: multi-agent belief convergence on a public knowledge graph.
- LLM interface: use an LLM as a prior-injection mechanism for the UAF hierarchy.
- Web interface: interactive NPG calculator for any domain.
- Paper: submit core claims (Layer 0–1) as a position paper to a workshop on unifying AI and cognitive science.

---

## What does NOT need to be done

- Solving quantum gravity via UAF (Layer 4 speculation — leave as-is).
- Proving UAF is the only valid framework — falsification rules exist for a reason.
- Making the repository bigger without making it better: $\mathcal{F}(\mathrm{repo}) \downarrow$ is the goal, not $K(\mathrm{repo}) \uparrow$.
