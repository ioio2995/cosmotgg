"""Model-free unit tests for cosmotgg.core.modular."""

import numpy as np
import pytest

from cosmotgg.core.modular import hermitian_log, modular_flow, modular_hamiltonian

TOL = 1e-9


def test_modular_hamiltonian_of_diagonal_state():
    eigvals = np.array([0.7, 0.3])
    rho = np.diag(eigvals).astype(complex)

    k = modular_hamiltonian(
        rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    expected = np.diag(-np.log(eigvals)).astype(complex)
    assert np.allclose(k, expected)


def test_modular_hamiltonian_rejects_non_faithful_state():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        modular_hamiltonian(
            rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_hermitian_log_on_known_positive_definite_matrix():
    eigvals = np.array([2.0, 8.0])
    matrix = np.diag(eigvals).astype(complex)

    log_matrix = hermitian_log(matrix, hermiticity_tolerance=TOL, positivity_tolerance=TOL)
    expected = np.diag(np.log(eigvals)).astype(complex)
    assert np.allclose(log_matrix, expected)


def test_modular_flow_at_s_zero_is_identity_action():
    k = np.diag([1.0, 2.0]).astype(complex)
    o = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    result = modular_flow(o, k, 0.0, hermiticity_tolerance=TOL)
    assert np.allclose(result, o)


def test_modular_flow_sign_convention():
    # K = diag(k1, k2), O = E_{01} (row 0, column 1, purely off-diagonal).
    # Frozen convention: O(s) = exp(+iKs) O exp(-iKs).
    # For this K and O, entry (0,1) of the result is exp(i k1 s) exp(-i k2 s).
    k1, k2 = 1.0, 3.0
    k = np.diag([k1, k2]).astype(complex)
    o = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    s = 0.5

    result = modular_flow(o, k, s, hermiticity_tolerance=TOL)

    expected_entry = np.exp(1j * k1 * s) * np.exp(-1j * k2 * s)
    expected = np.array([[0.0, expected_entry], [0.0, 0.0]], dtype=complex)
    assert np.allclose(result, expected)

    # The inverted sign convention must NOT match the implemented result.
    inverted_entry = np.exp(-1j * k1 * s) * np.exp(1j * k2 * s)
    inverted = np.array([[0.0, inverted_entry], [0.0, 0.0]], dtype=complex)
    assert not np.allclose(result, inverted)


BAD_TOLERANCES = [-1e-9, float("nan"), float("inf")]


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_hermitian_log_rejects_bad_hermiticity_tolerance(bad_tolerance):
    matrix = np.diag([2.0, 8.0]).astype(complex)
    with pytest.raises(ValueError):
        hermitian_log(matrix, hermiticity_tolerance=bad_tolerance, positivity_tolerance=TOL)


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_hermitian_log_rejects_bad_positivity_tolerance(bad_tolerance):
    matrix = np.diag([2.0, 8.0]).astype(complex)
    with pytest.raises(ValueError):
        hermitian_log(matrix, hermiticity_tolerance=TOL, positivity_tolerance=bad_tolerance)


def test_hermitian_log_accepts_zero_tolerances_on_exact_matrix():
    eigvals = np.array([2.0, 8.0])
    matrix = np.diag(eigvals).astype(complex)

    log_matrix = hermitian_log(matrix, hermiticity_tolerance=0.0, positivity_tolerance=0.0)
    expected = np.diag(np.log(eigvals)).astype(complex)
    assert np.allclose(log_matrix, expected)


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_modular_hamiltonian_rejects_bad_trace_tolerance(bad_tolerance):
    rho = np.diag([0.7, 0.3]).astype(complex)
    with pytest.raises(ValueError):
        modular_hamiltonian(
            rho,
            hermiticity_tolerance=TOL,
            trace_tolerance=bad_tolerance,
            positivity_tolerance=TOL,
        )


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_modular_flow_rejects_bad_hermiticity_tolerance(bad_tolerance):
    k = np.diag([1.0, 2.0]).astype(complex)
    o = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        modular_flow(o, k, 0.5, hermiticity_tolerance=bad_tolerance)


def test_modular_flow_group_property():
    k = np.diag([1.0, 3.0]).astype(complex)
    o = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    s1, s2 = 0.3, 0.7

    stepwise = modular_flow(
        modular_flow(o, k, s1, hermiticity_tolerance=TOL), k, s2, hermiticity_tolerance=TOL
    )
    combined = modular_flow(o, k, s1 + s2, hermiticity_tolerance=TOL)

    assert np.allclose(stepwise, combined, atol=1e-8)
