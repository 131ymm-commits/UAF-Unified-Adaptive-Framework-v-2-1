# Changelog

All notable changes to UAF are documented here.  
Each entry corresponds to a compression step that reduced surprise or increased coherence.

---

## [2.0.0] — 2026-06-03 — Iteration II

### Fixed (critical)

- **Active Inference Engine: precision divergence.** In v1.3, `L0_Sensory` free energy reached ~237 and precision hit the clip ceiling (5.0). Root cause: the bottom-up pass transmitted raw prediction errors (`current_obs = error`), causing each level to model the residuals of the level below without normalization. This is inconsistent with hierarchical predictive coding — what should propagate upward is precision-weighted error, not raw error. Fixed: bottom-up now passes `π_k · ε_k`.

- **Active Inference Engine: baseline drift.** In v1.3, `baseline_fe` was updated via exponential smoothing every step, meaning NPG was measured against a moving target. NPG ≥ 0 became trivially achievable by tracking the model's own trajectory. Fixed: baseline is now computed from a fixed initial estimate and updated only at epoch boundaries with a hard freeze option.

- **Active Inference Engine: Free Energy divergence.** Mean FE grew from 0.43 → 80.78 over 500 steps. Fixed by (a) precision clipping with slow learning rate, (b) normalized error propagation, (c) stable prior update protocol.

- **Verified result (v2.0):** Free Energy converges. NPG > 0 on all levels. Baseline is meaningful.

### Added (theory)

- `THEORY.md §7 — Precision and attention`: formal definition of precision as attention mechanism. Constraint that precision updates must occur on a slower timescale than belief updates. This was implicit in Friston's formalism but not made explicit in v1.3.

- `FORMAL_CORE.md §5 — Precision dynamics`: explicit update rule with slow learning rate and hard clip, derived from stability requirements.

- `FORMAL_CORE.md §6`: clarified that bottom-up signal is precision-weighted prediction error, not raw observation or raw error.

- `FORMAL_CORE.md §10`: added baseline invariance requirement — NPG baseline must be fixed before training begins.

- `FORMAL_CORE.md §12`: added formal definition of cross-agent consistency penalty $C(\{Q_i\})$ for Formula 131ym.

- `FORMULA_131YM.md`: added consistency penalty definition, operational iteration cycle, explicit separation of emergence mechanism from truth claim.

- `EPISTEMIC_STATUS.md`: added status labels to all layers, valid/invalid criticism examples, clarified local vs global failure propagation.

- `experiments/012_active_inference_engine.md`: full analysis of v1.3 failure modes and v2.0 corrections.

### Changed

- All documentation files upgraded to v2.0 with full cross-references.
- `src/uaf/metrics.py`: added `npg_fixed_baseline()` and `precision_weighted_error()` functions.
- `tests/`: added tests for precision divergence prevention and baseline stability.

---

## [0.2.0] — 2025-07-13 — Iteration I

### Added

- experiments/001_spin_as_topology.md — Spin reinterpreted as topological invariant of prediction manifold. Key result: matter classification follows from SU(2) representations.
- experiments/002_language_compression.md — Language reduced to one equation: collective free energy minimization. Key result: 10+ linguistic theories become special cases.
- experiments/003_black_holes.md — Black hole defined as region of infinite external predictive free energy. Key result: information paradox dissolves through multi-level coherence.
- experiments/004_cmb_anomalies.md — CMB anomalies as testable traces of L−1 to L0 transition. Key result: TDA as concrete research direction.
- experiments/005_dark_sector.md — Dark matter and dark energy as coherence and horizon terms. Key result: fine-tuning problem reframed.
- experiments/006_baryon_asymmetry.md — Baryon excess as free-energy gradient during L−1 to L0 transition. Key result: asymmetry is structural necessity, not accident.
- experiments/007_big_bang.md — Big Bang as phase transition from atemporal L−1 to temporal L0. Key result: low initial entropy derived without postulate.
- experiments/008_economics.md — Economics reduced to thermodynamics of prediction. Key result: utility function replaced by free energy.
- experiments/009_planck_constant.md — Planck constant as information exchange rate between levels. Key result: fine-tuning dissolved.
- experiments/010_mathematics_L_minus_1.md — Mathematics formalized as L−1. Key result: 5 deep problems reframed.
- experiments/011_llm_noosphere_interface.md — LLM as sensory-motor interface of the noosphere (L8). Key result: human is precision-controller, not sole author.
- Initial uaf_active_inference.py (hierarchy + EFE selection — architecture correct, implementation had precision bug).

---

## Growth formula

$$\frac{d}{dt} K(\mathrm{repo}) > 0, \quad \frac{d}{dt} \mathcal{F}(\mathrm{repo}) < 0$$

Each commit is an act of prediction. Each CHANGELOG entry is a record of evolution.
