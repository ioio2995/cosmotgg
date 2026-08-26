"""Tests for cosmotgg.models.model0a.diagnostics.

Fixture values used below (`A`, `B`, `C`, `ETA`, `S1`, `S2`, and the
finite-difference step `H`) are explicitly `NON_NORMATIVE_TEST_FIXTURE` /
`NON_NORMATIVE_TEST_NUMERICS`: purely internal-development numerical
examples. They are not `STATE_PARAMETER_VALUES` nor a
`MODULAR_PARAMETER_DOMAIN` in the scientific sense of
`docs/toy-models/toy0a/specification.md` (§12), which remain `OPEN`.
"""

import numpy as np
import pytest

from cosmotgg.core.modular import hermitian_log
from cosmotgg.core.states import partial_trace
from cosmotgg.models.model0a.diagnostics import (
    log_commutator_obstruction,
    model0a_reference_state,
    ordinary_group_defect,
)
from cosmotgg.models.model0a.states import two_qubit_fixed_marginal_correlation_state

DIMENSIONS = (2, 2)

# NON_NORMATIVE_TEST_FIXTURE: canonical N0/N1/N2 slices at fixed a, b
# (docs/toy-models/toy0a/specification.md §3.3). Not model0a scientific
# STATE_PARAMETER_VALUES.
A, B = 0.3, 0.4

# Development-only numerical tolerance for core primitive calls in these
# tests; not a model0a scientific tolerance, not a protocol tolerance.
NON_NORMATIVE_TEST_TOLERANCE = 1e-9


def _diagnostics_kwargs():
    return dict(
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        trace_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )


def _n0_state():
    return two_qubit_fixed_marginal_correlation_state(A, B, 0.0, 0.0)


def _n1_state():
    return two_qubit_fixed_marginal_correlation_state(A, B, 0.02, 0.0)


def _n2_state():
    return two_qubit_fixed_marginal_correlation_state(A, B, 0.02, 0.05)


ZERO_4X4 = np.zeros((4, 4))


# ---------------------------------------------------------------------------
# model0a_reference_state
# ---------------------------------------------------------------------------


def test_reference_state_matches_manual_assembly():
    rho_ab = _n2_state()

    sigma_ab = model0a_reference_state(rho_ab)

    rho_a = partial_trace(rho_ab, dimensions=DIMENSIONS, keep=[0])
    rho_b = partial_trace(rho_ab, dimensions=DIMENSIONS, keep=[1])
    expected = np.kron(rho_a, rho_b)

    assert np.allclose(sigma_ab, expected)


def test_reference_state_is_fixed_across_c_and_eta():
    rho_ab_1 = two_qubit_fixed_marginal_correlation_state(A, B, 0.0, 0.0)
    rho_ab_2 = two_qubit_fixed_marginal_correlation_state(A, B, 0.02, 0.05)

    sigma_1 = model0a_reference_state(rho_ab_1)
    sigma_2 = model0a_reference_state(rho_ab_2)

    assert np.allclose(sigma_1, sigma_2)


# ---------------------------------------------------------------------------
# log_commutator_obstruction — C_AB
# ---------------------------------------------------------------------------


def test_log_commutator_obstruction_vanishes_in_n0():
    c_ab = log_commutator_obstruction(_n0_state(), **_diagnostics_kwargs())
    assert np.allclose(c_ab, ZERO_4X4, atol=1e-8)


def test_log_commutator_obstruction_vanishes_in_n1():
    c_ab = log_commutator_obstruction(_n1_state(), **_diagnostics_kwargs())
    assert np.allclose(c_ab, ZERO_4X4, atol=1e-8)


def test_log_commutator_obstruction_is_nonzero_in_n2():
    c_ab = log_commutator_obstruction(_n2_state(), **_diagnostics_kwargs())
    assert not np.allclose(c_ab, ZERO_4X4, atol=1e-8)


def test_n2_reference_pair_does_not_commute_independently():
    # Independent structural witness for N2, computed without going
    # through log_commutator_obstruction: direct matrix commutator
    # [rho_ab, sigma_ab] on the raw density matrices.
    rho_ab = _n2_state()
    sigma_ab = model0a_reference_state(rho_ab)
    commutator = rho_ab @ sigma_ab - sigma_ab @ rho_ab
    assert not np.allclose(commutator, ZERO_4X4, atol=1e-8)


@pytest.mark.parametrize(
    "state_factory", [_n0_state, _n1_state, _n2_state], ids=["N0", "N1", "N2"]
)
def test_log_commutator_obstruction_matches_independent_log_route(state_factory):
    # Independent oracle: compute C_AB via hermitian_log directly (A =
    # ln(rho), B = ln(sigma)) rather than via modular_hamiltonian's
    # K = -ln(rho) route used in production.
    rho_ab = state_factory()
    sigma_ab = model0a_reference_state(rho_ab)

    log_rho = hermitian_log(
        rho_ab,
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )
    log_sigma = hermitian_log(
        sigma_ab,
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )
    expected = log_rho @ log_sigma - log_sigma @ log_rho

    c_ab = log_commutator_obstruction(rho_ab, **_diagnostics_kwargs())
    assert np.allclose(c_ab, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# ordinary_group_defect — G(s1, s2)
# ---------------------------------------------------------------------------


# NON_NORMATIVE_TEST_FIXTURE: development-only modular-parameter values,
# not a MODULAR_PARAMETER_DOMAIN.
S1, S2 = 0.3, 0.5


def test_ordinary_group_defect_vanishes_in_n0():
    g = ordinary_group_defect(_n0_state(), S1, S2, **_diagnostics_kwargs())
    assert np.allclose(g, ZERO_4X4, atol=1e-8)


def test_ordinary_group_defect_vanishes_in_n1():
    g = ordinary_group_defect(_n1_state(), S1, S2, **_diagnostics_kwargs())
    assert np.allclose(g, ZERO_4X4, atol=1e-8)


def test_ordinary_group_defect_is_not_identically_zero_in_n2():
    # Regression on this specific deterministic fixture only: G is
    # nonzero for THIS (s1, s2) pair on THIS N2 state. This is not the
    # scientific claim "G(s1, s2) != 0 for all s1, s2" (spec §9.7,
    # NOT_IDENTICALLY_ZERO), which is not tested here.
    g = ordinary_group_defect(_n2_state(), S1, S2, **_diagnostics_kwargs())
    assert not np.allclose(g, ZERO_4X4, atol=1e-8)


# ---------------------------------------------------------------------------
# Local identity: d^2 G / ds1 ds2 |_(0,0) = C_AB (spec §9.6)
# ---------------------------------------------------------------------------


def test_ordinary_group_defect_local_identity_matches_log_commutator_regression():
    """Numerical regression check of `d^2G/ds1ds2|_(0,0) = C_AB` on an N2
    fixture, via a centered finite-difference approximation.

    `FINITE_DIFFERENCE_STEP` and `REGRESSION_TOLERANCE` below are
    engineering-only `NON_NORMATIVE_TEST_NUMERICS` parameters of this
    specific numerical regression test. They are NOT a production
    tolerance of `cosmotgg.core`/`model0a`, NOT a `MODULAR_PARAMETER_DOMAIN`,
    and NOT a T1 threshold; they carry no normative status outside this
    test.
    """
    FINITE_DIFFERENCE_STEP = 1e-3
    REGRESSION_TOLERANCE = 1e-5

    rho_ab = _n2_state()
    h = FINITE_DIFFERENCE_STEP

    g_pp = ordinary_group_defect(rho_ab, h, h, **_diagnostics_kwargs())
    g_pm = ordinary_group_defect(rho_ab, h, -h, **_diagnostics_kwargs())
    g_mp = ordinary_group_defect(rho_ab, -h, h, **_diagnostics_kwargs())
    g_mm = ordinary_group_defect(rho_ab, -h, -h, **_diagnostics_kwargs())

    numerical_second_derivative = (g_pp - g_pm - g_mp + g_mm) / (4.0 * h * h)

    c_ab = log_commutator_obstruction(rho_ab, **_diagnostics_kwargs())

    assert np.allclose(
        numerical_second_derivative, c_ab, atol=REGRESSION_TOLERANCE
    )


# ---------------------------------------------------------------------------
# Fail-closed: s1 / s2 validation is not duplicated, but must still hold
# (delegated to cosmotgg.core.modular.finite_connes_cocycle)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_s",
    [1.0 + 1.0j, float("nan"), float("inf"), float("-inf"), np.array([0.1, 0.2])],
    ids=["complex", "nan", "inf", "-inf", "non-scalar"],
)
def test_ordinary_group_defect_rejects_bad_s1(bad_s):
    with pytest.raises(ValueError):
        ordinary_group_defect(_n2_state(), bad_s, S2, **_diagnostics_kwargs())


@pytest.mark.parametrize(
    "bad_s",
    [1.0 + 1.0j, float("nan"), float("inf"), float("-inf"), np.array([0.1, 0.2])],
    ids=["complex", "nan", "inf", "-inf", "non-scalar"],
)
def test_ordinary_group_defect_rejects_bad_s2(bad_s):
    with pytest.raises(ValueError):
        ordinary_group_defect(_n2_state(), S1, bad_s, **_diagnostics_kwargs())
