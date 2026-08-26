"""Model-free unit tests for cosmotgg.core.information."""

import numpy as np
import pytest

from cosmotgg.core.information import (
    log_density_difference,
    mutual_information,
    relative_entropy,
    von_neumann_entropy,
)

TOL = 1e-9


def _entropy_kwargs():
    return dict(
        hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )


def _relative_entropy_kwargs():
    return dict(
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
        support_tolerance=TOL,
    )


# ---------------------------------------------------------------------------
# von_neumann_entropy
# ---------------------------------------------------------------------------


def test_pure_state_entropy_is_zero():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert abs(von_neumann_entropy(rho, **_entropy_kwargs())) < 1e-8


def test_maximally_mixed_entropy_is_log_d():
    d = 4
    rho = np.eye(d, dtype=complex) / d
    s = von_neumann_entropy(rho, **_entropy_kwargs())
    assert abs(s - np.log(d)) < 1e-8


# ---------------------------------------------------------------------------
# relative_entropy
# ---------------------------------------------------------------------------


def test_relative_entropy_of_faithful_state_with_itself_is_zero():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    d = relative_entropy(rho, rho, **_relative_entropy_kwargs())
    assert abs(d) < 1e-8


def test_relative_entropy_of_non_faithful_state_with_itself_is_zero():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    d = relative_entropy(rho, rho, **_relative_entropy_kwargs())
    assert abs(d) < 1e-8


def test_relative_entropy_diagonal_known_value():
    rho = np.array([[0.8, 0.0], [0.0, 0.2]], dtype=complex)
    sigma = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    expected = 0.8 * np.log(0.8 / 0.5) + 0.2 * np.log(0.2 / 0.5)
    d = relative_entropy(rho, sigma, **_relative_entropy_kwargs())
    assert abs(d - expected) < 1e-8


def test_relative_entropy_support_violation_returns_inf():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    sigma = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    d = relative_entropy(rho, sigma, **_relative_entropy_kwargs())
    assert d == np.inf


def test_relative_entropy_matches_trace_of_log_density_difference():
    # Non-commuting rho, sigma (sigma is a rotated diagonal state).
    theta = 0.3
    c, s = np.cos(theta), np.sin(theta)
    rotation = np.array([[c, -s], [s, c]], dtype=complex)

    rho = np.array([[0.9, 0.0], [0.0, 0.1]], dtype=complex)
    sigma_diag = np.array([[0.4, 0.0], [0.0, 0.6]], dtype=complex)
    sigma = rotation @ sigma_diag @ rotation.conj().T

    diff = log_density_difference(
        rho,
        sigma,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    trace_value = np.trace(rho @ diff)

    expected = relative_entropy(rho, sigma, **_relative_entropy_kwargs())

    assert abs(trace_value.real - expected) < 1e-7
    assert abs(trace_value.imag) < 1e-8


# ---------------------------------------------------------------------------
# mutual_information
# ---------------------------------------------------------------------------


def test_mutual_information_of_product_state_is_zero():
    rho_a = np.array([[0.6, 0.0], [0.0, 0.4]], dtype=complex)
    rho_b = np.array([[0.3, 0.0], [0.0, 0.7]], dtype=complex)
    rho_ab = np.kron(rho_a, rho_b)

    i = mutual_information(rho_ab, dimensions=(2, 2), **_entropy_kwargs())
    assert abs(i) < 1e-8


def test_mutual_information_of_bell_state():
    bell = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_ab = np.outer(bell, bell.conj())

    i = mutual_information(rho_ab, dimensions=(2, 2), **_entropy_kwargs())
    assert abs(i - 2.0 * np.log(2.0)) < 1e-8


def test_mutual_information_of_classically_correlated_state():
    # rho_AB = 0.5 |00><00| + 0.5 |11><11|
    rho_ab = np.diag([0.5, 0.0, 0.0, 0.5]).astype(complex)

    i = mutual_information(rho_ab, dimensions=(2, 2), **_entropy_kwargs())
    assert abs(i - np.log(2.0)) < 1e-8


def test_mutual_information_rejects_non_integer_dimension_without_coercion():
    rho_ab = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        mutual_information(rho_ab, dimensions=(2.0, 2), **_entropy_kwargs())


# ---------------------------------------------------------------------------
# Tolerance validation (fail-closed, no default)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_tolerance", [-1e-9, float("nan"), float("inf")], ids=["negative", "nan", "inf"]
)
def test_relative_entropy_rejects_bad_support_tolerance(bad_tolerance):
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    with pytest.raises(ValueError):
        relative_entropy(
            rho,
            rho,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
            support_tolerance=bad_tolerance,
        )


def test_relative_entropy_accepts_zero_support_tolerance_when_support_matches_exactly():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    d = relative_entropy(
        rho,
        rho,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
        support_tolerance=0.0,
    )
    assert abs(d) < 1e-8
