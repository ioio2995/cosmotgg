"""Unit tests for cosmotgg.models.model1c.oracle.

Implementation-corroborative checks only
(`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`):
never a component of the `T5a` qualification record.
"""

import numpy as np
import pytest

from cosmotgg.models.model1c.algebra import p_bell
from cosmotgg.models.model1c.local_cell import SIGMA_0, SIGMA_0_NULL
from cosmotgg.models.model1c.oracle import phi_closed_form, phi_pow_closed_form

TOL = 1e-9


def test_o1_phi_closed_form_matches_manual_formula():
    """phi_closed_form(rho) must be exactly 1/2 rho + 1/2 p_bell(rho) (spec §7),
    independent of local_cell's production path."""
    rho = SIGMA_0
    produced = phi_closed_form(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    manual = 0.5 * rho + 0.5 * p_bell(rho)
    assert np.array_equal(produced, manual)


def test_o2_phi_pow_closed_form_n0_is_identity():
    for rho in (SIGMA_0, SIGMA_0_NULL):
        result = phi_pow_closed_form(
            rho, 0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
        assert np.allclose(result, rho, atol=1e-12)


def test_o3_phi_pow_closed_form_matches_iterated_phi_closed_form():
    """Independent consistency check: phi_pow_closed_form(rho, n) must equal
    n repeated applications of phi_closed_form (both from oracle.py, this
    does not exercise local_cell.phi)."""
    rho = SIGMA_0
    for n in range(5):
        iterated = rho
        for _ in range(n):
            iterated = phi_closed_form(
                iterated, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
            )
        closed = phi_pow_closed_form(
            rho, n, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
        assert np.allclose(iterated, closed, atol=1e-9)


def test_o4_phi_pow_closed_form_converges_to_p_bell():
    rho = SIGMA_0
    limit = phi_pow_closed_form(
        rho, 200, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.allclose(limit, p_bell(rho), atol=1e-12)


def test_o5_phi_closed_form_rejects_wrong_shape():
    with pytest.raises(ValueError):
        phi_closed_form(
            np.eye(3, dtype=complex) / 3.0,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_o6_phi_pow_closed_form_rejects_negative_n():
    with pytest.raises(ValueError):
        phi_pow_closed_form(
            SIGMA_0, -1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_o7_phi_pow_closed_form_rejects_non_integer_n():
    with pytest.raises(ValueError):
        phi_pow_closed_form(
            SIGMA_0, 1.5, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_o8_phi_pow_closed_form_rejects_bool_n():
    with pytest.raises(ValueError):
        phi_pow_closed_form(
            SIGMA_0, True, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_o9_phi_closed_form_rejects_invalid_density_matrix():
    bad = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)  # trace 2
    with pytest.raises(ValueError):
        phi_closed_form(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
