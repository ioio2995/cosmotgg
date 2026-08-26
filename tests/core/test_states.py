"""Model-free unit tests for cosmotgg.core.states."""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace, validate_density_matrix

TOL = 1e-9


# ---------------------------------------------------------------------------
# validate_density_matrix
# ---------------------------------------------------------------------------


def test_valid_mixed_state_is_accepted():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    result = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    assert np.allclose(result, rho)


def test_pure_state_psd_accepted_when_faithfulness_not_required():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    result = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    assert np.allclose(result, rho)


def test_pure_state_rejected_when_faithfulness_required():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=True,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_wrong_ndim_rejected():
    rho = np.array([1.0, 0.0, 0.0])
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_non_square_shape_rejected():
    rho = np.zeros((2, 3), dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_non_hermitian_rejected():
    rho = np.array([[0.7, 0.2], [0.0, 0.3]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_wrong_trace_rejected():
    rho = np.array([[0.7, 0.0], [0.0, 0.4]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_negative_eigenvalue_outside_tolerance_rejected():
    rho = np.array([[1.1, 0.0], [0.0, -0.1]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_faithfulness_threshold_boundary():
    positivity_tolerance = 1e-6

    lam_at_boundary = positivity_tolerance
    rho_at_boundary = np.array(
        [[1.0 - lam_at_boundary, 0.0], [0.0, lam_at_boundary]], dtype=complex
    )
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho_at_boundary,
            require_faithful=True,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=positivity_tolerance,
        )

    lam_above_boundary = positivity_tolerance * 10.0
    rho_above_boundary = np.array(
        [[1.0 - lam_above_boundary, 0.0], [0.0, lam_above_boundary]], dtype=complex
    )
    result = validate_density_matrix(
        rho_above_boundary,
        require_faithful=True,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=positivity_tolerance,
    )
    assert np.allclose(result, rho_above_boundary)


# ---------------------------------------------------------------------------
# partial_trace
# ---------------------------------------------------------------------------


def test_partial_trace_of_product_state():
    rho_a = np.array([[0.6, 0.0], [0.0, 0.4]], dtype=complex)
    rho_b = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    rho_ab = np.kron(rho_a, rho_b)

    reduced_a = partial_trace(rho_ab, dimensions=(2, 2), keep=[0])
    reduced_b = partial_trace(rho_ab, dimensions=(2, 2), keep=[1])

    assert np.allclose(reduced_a, rho_a)
    assert np.allclose(reduced_b, rho_b)


def test_partial_trace_of_bell_state():
    bell = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_ab = np.outer(bell, bell.conj())

    reduced_a = partial_trace(rho_ab, dimensions=(2, 2), keep=[0])
    expected = np.eye(2, dtype=complex) / 2.0

    assert np.allclose(reduced_a, expected)


def test_partial_trace_invalid_dimensions_rejected():
    rho_ab = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        partial_trace(rho_ab, dimensions=(2, 3), keep=[0])


def test_partial_trace_invalid_keep_index_rejected():
    rho_ab = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        partial_trace(rho_ab, dimensions=(2, 2), keep=[2])


def test_partial_trace_duplicated_keep_rejected():
    rho_ab = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        partial_trace(rho_ab, dimensions=(2, 2), keep=[0, 0])


def test_partial_trace_non_ascending_keep_rejected():
    rho_abc = np.eye(8, dtype=complex) / 8.0
    with pytest.raises(ValueError):
        partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[1, 0])
