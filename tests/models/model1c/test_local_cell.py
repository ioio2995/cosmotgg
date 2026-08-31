"""Unit tests for cosmotgg.models.model1c.local_cell.

Implementation-corroborative checks only
(`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`):
never a component of the `T5a` qualification record.
"""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model1c.local_cell import (
    ALPHA,
    SIGMA_0,
    SIGMA_0_NULL,
    controlled_bell_unitary,
    local_refinement_cell,
    phi,
    sigma_0_family,
)
from cosmotgg.models.model1c.oracle import phi_closed_form

TOL = 1e-9


def _random_density_matrix(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    h = a + a.conj().T
    eigvals, eigvecs = np.linalg.eigh(h)
    weights = (eigvals - eigvals.min()) + 1.0
    weights = weights / weights.sum()
    return (eigvecs * weights) @ eigvecs.conj().T


_SAMPLE_STATES = [SIGMA_0, SIGMA_0_NULL, np.eye(4, dtype=complex) / 4.0, _random_density_matrix(7)]


# ---------------------------------------------------------------------------
# U^dagger U = I (spec §6)
# ---------------------------------------------------------------------------


def test_lc1_controlled_unitary_is_unitary():
    u = controlled_bell_unitary()
    assert np.allclose(u.conj().T @ u, np.eye(16), atol=TOL)
    assert np.allclose(u @ u.conj().T, np.eye(16), atol=TOL)


def test_lc2_controlled_unitary_is_deterministic_constant():
    """N6 support: U carries no per-call/per-level free parameter."""
    assert np.array_equal(controlled_bell_unitary(), controlled_bell_unitary())


# ---------------------------------------------------------------------------
# local_refinement_cell — CPTP (trace-preserving, positivity-preserving)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rho", _SAMPLE_STATES)
def test_lc3_local_refinement_cell_preserves_trace(rho):
    joint = local_refinement_cell(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert joint.shape == (16, 16)
    assert np.trace(joint).real == pytest.approx(1.0, abs=1e-10)


@pytest.mark.parametrize("rho", _SAMPLE_STATES)
def test_lc4_local_refinement_cell_preserves_positivity(rho):
    joint = local_refinement_cell(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    eigvals = np.linalg.eigvalsh(joint)
    assert eigvals.min() >= -1e-10


# ---------------------------------------------------------------------------
# phi (production, local_refinement_cell -> partial_trace) == phi_closed_form
# (independent oracle) — mandate: PHI production must equal the closed-form
# oracle exactly (spec §7).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rho", _SAMPLE_STATES)
def test_lc5_phi_matches_closed_form_oracle(rho):
    produced = phi(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    expected = phi_closed_form(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.allclose(produced, expected, atol=1e-10)


def test_lc6_phi_is_derived_via_partial_trace_of_local_refinement_cell():
    """PHI_PRODUCTION_PATH = local_refinement_cell -> partial_trace: phi(rho)
    must equal an independent manual partial trace of local_refinement_cell's
    own output (rather than being computed by any shortcut)."""
    rho = SIGMA_0
    joint = local_refinement_cell(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    manual = partial_trace(joint, dimensions=(4, 4), keep=(0,))
    produced = phi(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    assert np.array_equal(manual, produced)


# ---------------------------------------------------------------------------
# Faithfulness preserved for a faithful seed (spec §16)
# ---------------------------------------------------------------------------


def test_lc7_local_refinement_cell_preserves_faithfulness():
    joint = local_refinement_cell(
        SIGMA_0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    eigvals = np.linalg.eigvalsh(joint)
    assert eigvals.min() > 0.0


def test_lc8_phi_preserves_faithfulness():
    result = phi(SIGMA_0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    eigvals = np.linalg.eigvalsh(result)
    assert eigvals.min() > 0.0


# ---------------------------------------------------------------------------
# Pre-registered seeds (spec §11)
# ---------------------------------------------------------------------------


def test_lc9_sigma_0_family_reproduces_canonical_and_null_seeds():
    assert np.array_equal(sigma_0_family(0.25), SIGMA_0)
    assert np.array_equal(sigma_0_family(0.0), SIGMA_0_NULL)


def test_lc10_sigma_0_is_faithful():
    eigvals = np.linalg.eigvalsh(SIGMA_0)
    assert eigvals.min() > 0.0
    assert np.trace(SIGMA_0).real == pytest.approx(1.0, abs=TOL)


def test_lc11_sigma_0_null_has_unit_trace_and_is_positive():
    eigvals = np.linalg.eigvalsh(SIGMA_0_NULL)
    assert eigvals.min() >= -TOL
    assert np.trace(SIGMA_0_NULL).real == pytest.approx(1.0, abs=TOL)


def test_lc12_alpha_is_the_fixed_diagonal():
    assert np.allclose(ALPHA, np.diag([5.0 / 8.0, 1.0 / 8.0, 1.0 / 8.0, 1.0 / 8.0]))
    assert np.trace(ALPHA).real == pytest.approx(1.0, abs=TOL)


# ---------------------------------------------------------------------------
# Fail-closed on invalid input (no clipping, no pseudo-inverse, no silent
# regularization)
# ---------------------------------------------------------------------------


def test_lc13_local_refinement_cell_rejects_non_hermitian():
    bad = np.array(
        [[1.0, 0.5, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
        dtype=complex,
    )
    with pytest.raises(ValueError):
        local_refinement_cell(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_lc14_local_refinement_cell_rejects_wrong_trace():
    bad = np.diag([0.5, 0.5, 0.5, 0.5]).astype(complex)
    with pytest.raises(ValueError):
        local_refinement_cell(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_lc15_local_refinement_cell_rejects_non_positive_semidefinite():
    bad = np.diag([1.5, -0.5, 0.0, 0.0]).astype(complex)
    with pytest.raises(ValueError):
        local_refinement_cell(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_lc16_local_refinement_cell_rejects_wrong_dimensions():
    bad = np.eye(3, dtype=complex) / 3.0
    with pytest.raises(ValueError):
        local_refinement_cell(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_lc17_sigma_0_family_rejects_non_scalar_kappa():
    with pytest.raises(ValueError):
        sigma_0_family(np.array([0.1, 0.2]))


def test_lc18_sigma_0_family_rejects_bool_kappa():
    with pytest.raises(ValueError):
        sigma_0_family(True)
