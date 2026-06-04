"""
UAF v2.0 — Tests for src/uaf/metrics.py

Run: python -m pytest tests/ -v
  or: python tests/test_metrics.py

All tests correspond to definitions in FORMAL_CORE.md.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from uaf.metrics import (
    surprise,
    gaussian_surprise,
    free_energy_gaussian,
    kl_gaussian,
    precision_weighted_error,
    npg,
    npg_fixed_baseline,
    expected_free_energy_gaussian,
    consistency_penalty,
)


# =============================================================================
# surprise
# =============================================================================

def test_surprise_zero_log_likelihood():
    """Surprise = 0 when log P(o|Q) = 0 (i.e. P = 1)."""
    assert surprise(0.0) == 0.0


def test_surprise_negative_log():
    """Typical log-likelihood is negative; surprise should be positive."""
    assert surprise(-2.3) == pytest.approx(2.3)


def test_surprise_large():
    assert surprise(-100.0) == pytest.approx(100.0)


# =============================================================================
# gaussian_surprise
# =============================================================================

def test_gaussian_surprise_perfect():
    """If obs == mean, surprise = 0."""
    obs = np.array([1.0, 2.0, 3.0])
    assert gaussian_surprise(obs, obs, np.ones(3)) == pytest.approx(0.0)


def test_gaussian_surprise_unit_error():
    """One unit error along one dim with precision 1 → surprise = 0.5."""
    obs  = np.array([1.0])
    mean = np.array([0.0])
    prec = np.array([1.0])
    assert gaussian_surprise(obs, mean, prec) == pytest.approx(0.5)


def test_gaussian_surprise_scaling():
    """Higher precision = higher surprise for same error."""
    obs  = np.array([1.0])
    mean = np.array([0.0])
    s1 = gaussian_surprise(obs, mean, np.array([1.0]))
    s2 = gaussian_surprise(obs, mean, np.array([4.0]))
    assert s2 == pytest.approx(4 * s1)


# =============================================================================
# free_energy_gaussian
# =============================================================================

def test_fe_at_prior_with_perfect_observation():
    """F = 0 when belief = prior and obs = belief."""
    mu = np.array([0.5, -0.5])
    assert free_energy_gaussian(mu, mu, mu, np.ones(2)) == pytest.approx(0.0)


def test_fe_decomposes_inaccuracy_plus_kl():
    """F = inaccuracy + KL, both >= 0."""
    obs   = np.array([1.0, 0.0])
    mean  = np.array([0.0, 0.0])
    prior = np.array([0.0, 0.0])
    prec  = np.array([2.0, 2.0])
    fe = free_energy_gaussian(obs, mean, prior, prec)
    assert fe >= 0.0


# =============================================================================
# kl_gaussian
# =============================================================================

def test_kl_identical_distributions():
    """KL(Q||Q) = 0."""
    mu  = np.array([1.0, -1.0])
    sig = np.array([0.5, 2.0])
    assert kl_gaussian(mu, sig, mu, sig) == pytest.approx(0.0, abs=1e-10)


def test_kl_non_negative():
    """KL divergence is always >= 0."""
    mu_q  = np.array([1.0, 2.0])
    sig_q = np.array([1.0, 0.5])
    mu_p  = np.array([0.0, 1.0])
    sig_p = np.array([2.0, 1.0])
    assert kl_gaussian(mu_q, sig_q, mu_p, sig_p) >= 0.0


def test_kl_asymmetry():
    """KL(Q||P) ≠ KL(P||Q) in general."""
    mu_q, sig_q = np.array([1.0]), np.array([0.5])
    mu_p, sig_p = np.array([0.0]), np.array([2.0])
    kl1 = kl_gaussian(mu_q, sig_q, mu_p, sig_p)
    kl2 = kl_gaussian(mu_p, sig_p, mu_q, sig_q)
    assert kl1 != pytest.approx(kl2)


# =============================================================================
# precision_weighted_error  (v2.0 core fix)
# =============================================================================

def test_precision_weighted_error_unit():
    """With precision=1, weighted error equals raw error."""
    obs  = np.array([3.0, -1.0])
    mean = np.array([1.0,  1.0])
    prec = np.ones(2)
    result = precision_weighted_error(obs, mean, prec)
    np.testing.assert_allclose(result, obs - mean)


def test_precision_weighted_error_scaling():
    """Doubling precision doubles the weighted error."""
    obs  = np.array([2.0])
    mean = np.array([0.0])
    e1 = precision_weighted_error(obs, mean, np.array([1.0]))
    e2 = precision_weighted_error(obs, mean, np.array([2.0]))
    np.testing.assert_allclose(e2, 2 * e1)


def test_precision_weighted_error_not_raw():
    """Weighted error differs from raw error when precision != 1."""
    obs  = np.array([1.0])
    mean = np.array([0.0])
    prec = np.array([3.0])
    weighted = precision_weighted_error(obs, mean, prec)
    raw = obs - mean
    assert not np.allclose(weighted, raw)


# =============================================================================
# NPG — fixed baseline  (v2.0 requirement)
# =============================================================================

def test_npg_zero_when_equal():
    """NPG = 0 when model loss equals baseline."""
    assert npg(1.0, 1.0) == pytest.approx(0.0, abs=1e-6)


def test_npg_positive_when_model_better():
    """NPG > 0 when model has lower loss than baseline."""
    assert npg(0.5, 1.0) > 0.0


def test_npg_negative_when_model_worse():
    """NPG < 0 when model has higher loss than baseline."""
    assert npg(2.0, 1.0) < 0.0


def test_npg_approaches_one():
    """NPG → 1 when model loss → 0."""
    val = npg(1e-9, 1.0)
    assert val == pytest.approx(1.0, abs=1e-6)


def test_npg_fixed_baseline_shape():
    """npg_fixed_baseline returns array of same shape as input."""
    losses = np.array([1.2, 0.8, 0.5, 0.3])
    result = npg_fixed_baseline(losses, baseline_loss=1.0)
    assert result.shape == losses.shape


def test_npg_fixed_baseline_values():
    """Verify npg_fixed_baseline is monotonically increasing as loss decreases."""
    losses = np.array([0.9, 0.7, 0.5, 0.3])
    result = npg_fixed_baseline(losses, baseline_loss=1.0)
    assert np.all(np.diff(result) > 0)


# =============================================================================
# expected_free_energy_gaussian
# =============================================================================

def test_efe_at_goal():
    """Risk = 0 when predicted mean equals preferred mean."""
    pref = np.array([0.0, 0.0])
    efe  = expected_free_energy_gaussian(pref, np.ones(2), pref)
    ambiguity_only = 0.5 * float(np.sum(np.log(2 * np.pi * np.e * np.ones(2))))
    assert efe == pytest.approx(ambiguity_only, rel=1e-6)


def test_efe_increases_with_distance():
    """EFE increases as predicted mean moves away from preferred."""
    pref = np.zeros(2)
    var  = np.ones(2)
    e1 = expected_free_energy_gaussian(np.array([0.5, 0.5]), var, pref)
    e2 = expected_free_energy_gaussian(np.array([2.0, 2.0]), var, pref)
    assert e2 > e1


def test_efe_increases_with_variance():
    """EFE increases with higher variance (more ambiguity)."""
    pred = np.zeros(2)
    pref = np.zeros(2)
    e1 = expected_free_energy_gaussian(pred, np.ones(2) * 0.5, pref)
    e2 = expected_free_energy_gaussian(pred, np.ones(2) * 2.0, pref)
    assert e2 > e1


# =============================================================================
# consistency_penalty
# =============================================================================

def test_consistency_penalty_identical():
    """C = 0 when all agents have identical beliefs."""
    b = (np.array([1.0, 0.0]), np.array([1.0, 1.0]))
    beliefs = [b, b, b]
    assert consistency_penalty(beliefs) == pytest.approx(0.0, abs=1e-8)


def test_consistency_penalty_increases_with_divergence():
    """C increases when agents disagree more."""
    b1 = (np.array([0.0]), np.array([1.0]))
    b2_close = (np.array([0.1]), np.array([1.0]))
    b2_far   = (np.array([5.0]), np.array([1.0]))
    c_close = consistency_penalty([b1, b2_close])
    c_far   = consistency_penalty([b1, b2_far])
    assert c_far > c_close


def test_consistency_penalty_single_agent():
    """C = 0 with only one agent."""
    b = (np.array([1.0]), np.array([1.0]))
    assert consistency_penalty([b]) == 0.0


# =============================================================================

if __name__ == "__main__":
    # Run without pytest
    import traceback
    tests = [
        test_surprise_zero_log_likelihood,
        test_surprise_negative_log,
        test_gaussian_surprise_perfect,
        test_gaussian_surprise_unit_error,
        test_gaussian_surprise_scaling,
        test_fe_at_prior_with_perfect_observation,
        test_fe_decomposes_inaccuracy_plus_kl,
        test_kl_identical_distributions,
        test_kl_non_negative,
        test_kl_asymmetry,
        test_precision_weighted_error_unit,
        test_precision_weighted_error_scaling,
        test_precision_weighted_error_not_raw,
        test_npg_zero_when_equal,
        test_npg_positive_when_model_better,
        test_npg_negative_when_model_worse,
        test_npg_approaches_one,
        test_npg_fixed_baseline_shape,
        test_npg_fixed_baseline_values,
        test_efe_at_goal,
        test_efe_increases_with_distance,
        test_efe_increases_with_variance,
        test_consistency_penalty_identical,
        test_consistency_penalty_increases_with_divergence,
        test_consistency_penalty_single_agent,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} tests passed.")
