"""
UAF v2.0 — Computational Metrics
src/uaf/metrics.py

All functions here correspond directly to definitions in FORMAL_CORE.md.
Each docstring cites the relevant section.

Verified: all functions pass tests in tests/test_metrics.py
Requires: numpy
"""

import numpy as np
from typing import Union, Optional


# =============================================================================
# SURPRISE  (FORMAL_CORE §2)
# =============================================================================

def surprise(log_likelihood: float) -> float:
    """
    Compute surprise from log-likelihood.

    S(o) = -ln P(o | Q)

    FORMAL_CORE §2

    Parameters
    ----------
    log_likelihood : float
        ln P(o | Q) — the log probability of observation o under model Q.

    Returns
    -------
    float
        Surprise S = -log_likelihood. Always >= 0 when probability <= 1.
    """
    return -log_likelihood


def gaussian_surprise(obs: np.ndarray, mean: np.ndarray, precision: np.ndarray) -> float:
    """
    Gaussian surprise: S = 0.5 * π * ||o - μ||²  (up to constants).

    For a Gaussian with precision π = 1/σ²:
        -ln P(o | μ, σ²) = 0.5 * (o - μ)ᵀ diag(π) (o - μ) + const

    FORMAL_CORE §2, §4

    Parameters
    ----------
    obs       : np.ndarray  — observation vector
    mean      : np.ndarray  — predicted mean (belief)
    precision : np.ndarray  — precision vector (1/σ²), same shape as obs

    Returns
    -------
    float — precision-weighted squared prediction error (half)
    """
    error = obs - mean
    return 0.5 * float(np.dot(precision * error, error))


# =============================================================================
# FREE ENERGY  (FORMAL_CORE §3)
# =============================================================================

def free_energy_gaussian(
    obs: np.ndarray,
    mean: np.ndarray,
    prior_mean: np.ndarray,
    precision: np.ndarray,
    prior_precision: Optional[np.ndarray] = None,
) -> float:
    """
    Variational free energy for a Gaussian model.

    F = inaccuracy + complexity
      = 0.5 * π * ||o - μ||²  +  0.5 * π_prior * ||μ - μ_prior||²

    FORMAL_CORE §3

    Parameters
    ----------
    obs           : observation
    mean          : current belief mean Q(s)
    prior_mean    : prior mean from level above P(s)
    precision     : likelihood precision
    prior_precision: prior precision (defaults to ones if None)

    Returns
    -------
    float — variational free energy
    """
    if prior_precision is None:
        prior_precision = np.ones_like(precision)

    inaccuracy = gaussian_surprise(obs, mean, precision)
    kl = 0.5 * float(np.dot(prior_precision * (mean - prior_mean), (mean - prior_mean)))
    return inaccuracy + kl


# =============================================================================
# KL DIVERGENCE  (FORMAL_CORE §3, §6)
# =============================================================================

def kl_gaussian(
    mu_q: np.ndarray,
    sigma_q: np.ndarray,
    mu_p: np.ndarray,
    sigma_p: np.ndarray,
) -> float:
    """
    KL divergence KL(Q || P) between two diagonal Gaussians.

    KL(Q||P) = 0.5 * [ln(|Σ_P|/|Σ_Q|) - d + tr(Σ_P⁻¹ Σ_Q) + (μ_P - μ_Q)ᵀ Σ_P⁻¹ (μ_P - μ_Q)]

    FORMAL_CORE §3, §6

    Parameters
    ----------
    mu_q, sigma_q : mean and std of Q (diagonal covariance)
    mu_p, sigma_p : mean and std of P (diagonal covariance)

    Returns
    -------
    float — KL(Q||P), always >= 0
    """
    d = len(mu_q)
    var_q = sigma_q ** 2
    var_p = sigma_p ** 2
    log_term = np.sum(np.log(var_p / var_q))
    trace_term = np.sum(var_q / var_p)
    quad_term = np.sum((mu_p - mu_q) ** 2 / var_p)
    return 0.5 * (log_term - d + trace_term + quad_term)


# =============================================================================
# PRECISION-WEIGHTED ERROR  (FORMAL_CORE §6)
# =============================================================================

def precision_weighted_error(
    obs: np.ndarray,
    mean: np.ndarray,
    precision: np.ndarray,
) -> np.ndarray:
    """
    Compute the precision-weighted prediction error for bottom-up propagation.

    ξ = π * (o - μ)

    This is what should propagate upward in the hierarchy, NOT the raw error.
    See FORMAL_CORE §6 for the v2.0 correction.

    FORMAL_CORE §6

    Parameters
    ----------
    obs       : observation
    mean      : current belief mean
    precision : precision vector

    Returns
    -------
    np.ndarray — precision-weighted error vector
    """
    return precision * (obs - mean)


# =============================================================================
# NPG — NORMALIZED PREDICTIVE GAIN  (FORMAL_CORE §10)
# =============================================================================

def npg(
    model_loss: float,
    baseline_loss: float,
    epsilon: float = 1e-8,
) -> float:
    """
    Normalized Predictive Gain.

    NPG(M; D, B) = (L(B, D) - L(M, D)) / (L(B, D) + ε)

    FORMAL_CORE §10

    Interpretation:
        NPG = 0  → model equals baseline
        NPG → 1  → model eliminates baseline loss entirely
        NPG < 0  → model is worse than baseline

    CRITICAL: baseline_loss must be computed on a fixed reference, not adapted
    during training. See FORMAL_CORE §10 "Baseline invariance".

    Parameters
    ----------
    model_loss    : L(M, D) — loss of the model being evaluated
    baseline_loss : L(B, D) — fixed baseline loss (computed before training)
    epsilon       : numerical stability term

    Returns
    -------
    float — NPG in (-∞, 1]
    """
    return (baseline_loss - model_loss) / (baseline_loss + epsilon)


def npg_fixed_baseline(
    model_losses: np.ndarray,
    baseline_loss: float,
    epsilon: float = 1e-8,
) -> np.ndarray:
    """
    Compute NPG over a sequence of model losses against a single fixed baseline.

    FORMAL_CORE §10

    Parameters
    ----------
    model_losses  : array of per-step losses
    baseline_loss : fixed baseline (computed before the run)
    epsilon       : numerical stability

    Returns
    -------
    np.ndarray — NPG at each step
    """
    return (baseline_loss - model_losses) / (baseline_loss + epsilon)


# =============================================================================
# EXPECTED FREE ENERGY  (FORMAL_CORE §8)
# =============================================================================

def expected_free_energy_gaussian(
    pred_mean: np.ndarray,
    pred_var: np.ndarray,
    preferred_mean: np.ndarray,
) -> float:
    """
    Expected Free Energy for a Gaussian outcome model.

    G(π) = Risk + Ambiguity
         = 0.5 * ||μ_pred - μ_pref||²  +  0.5 * Σ_j ln(2πe σ²_j)

    FORMAL_CORE §8

    Parameters
    ----------
    pred_mean      : predicted outcome mean under policy π
    pred_var       : predicted outcome variance (diagonal)
    preferred_mean : preferred outcome mean (goal)

    Returns
    -------
    float — Expected Free Energy
    """
    risk = 0.5 * float(np.sum((pred_mean - preferred_mean) ** 2))
    ambiguity = 0.5 * float(np.sum(np.log(2 * np.pi * np.e * pred_var)))
    return risk + ambiguity


# =============================================================================
# CONSISTENCY PENALTY  (FORMAL_CORE §12)
# =============================================================================

def consistency_penalty(beliefs: list) -> float:
    """
    Cross-agent consistency penalty C({Q_i}).

    C = (1/m²) Σ_{i,j} KL(Q_i || Q_j)

    For Gaussian beliefs parameterized as (mean, std):

    FORMAL_CORE §12, FORMULA_131YM §2

    Parameters
    ----------
    beliefs : list of (mean, std) tuples — one per agent

    Returns
    -------
    float — consistency penalty, always >= 0
    """
    m = len(beliefs)
    if m < 2:
        return 0.0
    total = 0.0
    for i in range(m):
        for j in range(m):
            if i != j:
                mu_i, sig_i = beliefs[i]
                mu_j, sig_j = beliefs[j]
                total += kl_gaussian(
                    np.atleast_1d(mu_i), np.atleast_1d(sig_i),
                    np.atleast_1d(mu_j), np.atleast_1d(sig_j),
                )
    return total / (m ** 2)
