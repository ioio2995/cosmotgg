"""Model-free unit tests for cosmotgg.core.states."""

import numpy as np
import pytest

from cosmotgg.core.states import (
    conditional_expectation,
    partial_trace,
    traceless_part,
    validate_density_matrix,
)

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


@pytest.mark.parametrize(
    "dimensions",
    [(2.5, 2), ("2", 2), (True, 4)],
    ids=["float_dim", "str_dim", "bool_dim"],
)
def test_partial_trace_rejects_non_integer_dimensions_without_coercion(dimensions):
    rho_ab = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        partial_trace(rho_ab, dimensions=dimensions, keep=[0])


# ---------------------------------------------------------------------------
# Tolerance validation (fail-closed, no default)
# ---------------------------------------------------------------------------

BAD_TOLERANCES = [-1e-9, float("nan"), float("inf")]


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_validate_density_matrix_rejects_bad_hermiticity_tolerance(bad_tolerance):
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=bad_tolerance,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_validate_density_matrix_rejects_bad_trace_tolerance(bad_tolerance):
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=bad_tolerance,
            positivity_tolerance=TOL,
        )


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_validate_density_matrix_rejects_bad_positivity_tolerance(bad_tolerance):
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    with pytest.raises(ValueError):
        validate_density_matrix(
            rho,
            require_faithful=False,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=bad_tolerance,
        )


def test_validate_density_matrix_accepts_zero_tolerances_on_exact_state():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    result = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=0.0,
        trace_tolerance=0.0,
        positivity_tolerance=0.0,
    )
    assert np.allclose(result, rho)


def test_validate_density_matrix_accepts_zero_positivity_tolerance_at_exact_boundary():
    # lambda_min == 0.0 exactly: PSD check `lambda_min >= -0.0` holds exactly.
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    result = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=0.0,
        trace_tolerance=0.0,
        positivity_tolerance=0.0,
    )
    assert np.allclose(result, rho)


# ---------------------------------------------------------------------------
# conditional_expectation (model-free)
# ---------------------------------------------------------------------------


def _deterministic_operator(dim: int, *, seed_shift: float = 0.0) -> np.ndarray:
    """Deterministic non-hermitian complex `dim x dim` operator, no RNG."""
    rows = np.arange(dim).reshape(dim, 1)
    cols = np.arange(dim).reshape(1, dim)
    return (rows + 1j * cols + seed_shift) / (dim + 1.0)


def test_ce1_identity_bipartite():
    identity_ab = np.eye(4, dtype=complex)
    result = conditional_expectation(identity_ab, dimensions=(2, 2), keep=[1])
    assert np.allclose(result, np.eye(2, dtype=complex))


def test_ce2_equivalence_with_partial_trace():
    x = _deterministic_operator(6)
    result = conditional_expectation(x, dimensions=(2, 3), keep=[0])
    expected = partial_trace(x, dimensions=(2, 3), keep=[0]) / 3.0
    assert np.allclose(result, expected)


def test_ce3_generic_non_qubit_dimensions():
    x = _deterministic_operator(12)
    result = conditional_expectation(x, dimensions=(2, 3, 2), keep=[1])
    expected = partial_trace(x, dimensions=(2, 3, 2), keep=[1]) / 4.0
    assert result.shape == (3, 3)
    assert np.allclose(result, expected)


def test_ce4_keep_several_factors():
    x = _deterministic_operator(12)
    result = conditional_expectation(x, dimensions=(2, 3, 2), keep=[0, 2])
    expected = partial_trace(x, dimensions=(2, 3, 2), keep=[0, 2]) / 3.0
    assert result.shape == (4, 4)
    assert np.allclose(result, expected)


def test_ce5_keep_all_subsystems_is_identity_map():
    x = _deterministic_operator(6)
    result = conditional_expectation(x, dimensions=(2, 3), keep=[0, 1])
    assert np.allclose(result, x)


def test_ce6_normalized_trace_preservation():
    x = _deterministic_operator(12)
    dimensions = (2, 3, 2)
    keep = [0, 2]
    result = conditional_expectation(x, dimensions=dimensions, keep=keep)
    d_keep = 2 * 2
    d_total = 2 * 3 * 2
    assert np.trace(result) / d_keep == pytest.approx(np.trace(x) / d_total)


def test_ce7_bimodularity_bipartite():
    x = _deterministic_operator(4)
    b1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    b2 = np.array([[2.0, 1j], [0.0, 3.0]], dtype=complex)
    identity_a = np.eye(2, dtype=complex)

    sandwiched = np.kron(identity_a, b1) @ x @ np.kron(identity_a, b2)
    lhs = conditional_expectation(sandwiched, dimensions=(2, 2), keep=[1])
    rhs = b1 @ conditional_expectation(x, dimensions=(2, 2), keep=[1]) @ b2

    assert np.allclose(lhs, rhs)


def test_ce8_non_hermitian_input_accepted():
    x = np.array([[0.0, 1.0, 0.0, 0.0]] * 4, dtype=complex) + 1j * np.eye(4, dtype=complex)
    result = conditional_expectation(x, dimensions=(2, 2), keep=[0])
    expected = partial_trace(x, dimensions=(2, 2), keep=[0]) / 2.0
    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "dimensions,keep",
    [
        ((2, 3), [0]),  # product(dimensions) mismatch below
        ((2, 2), [2]),  # invalid keep index
        ((2, 2, 2), [0, 0]),  # duplicated keep
        ((2, 2, 2), [1, 0]),  # non-ascending keep
    ],
    ids=["dim_mismatch", "invalid_index", "duplicated_keep", "non_ascending_keep"],
)
def test_ce9_fail_closed_propagation_from_partial_trace(dimensions, keep):
    operator = np.eye(4, dtype=complex)
    with pytest.raises(ValueError):
        conditional_expectation(operator, dimensions=dimensions, keep=keep)


# ---------------------------------------------------------------------------
# traceless_part (model-free)
# ---------------------------------------------------------------------------


def test_tp1_traceless_result_has_zero_trace():
    x = _deterministic_operator(4)
    result = traceless_part(x)
    assert abs(np.trace(result)) < 1e-9


def test_tp2_traceless_part_of_scalar_multiple_of_identity_is_zero():
    c = 3.0 + 2.0j
    x = c * np.eye(5, dtype=complex)
    result = traceless_part(x)
    assert np.allclose(result, np.zeros((5, 5), dtype=complex))


def test_tp3_traceless_part_invariant_under_identity_shift():
    x = _deterministic_operator(4)
    c = -1.5 + 0.5j
    shifted = x + c * np.eye(4, dtype=complex)
    assert np.allclose(traceless_part(shifted), traceless_part(x))


def test_tp4_non_hermitian_complex_operator_accepted():
    x = np.array(
        [[1.0 + 1j, 2.0, 0.0], [0.0, -1.0j, 3.0], [1.0, 0.0, 2.0 - 1j]],
        dtype=complex,
    )
    result = traceless_part(x)
    assert abs(np.trace(result)) < 1e-9


def test_tp5_generic_non_2x2_dimension():
    x = _deterministic_operator(5)
    result = traceless_part(x)
    assert result.shape == (5, 5)
    assert abs(np.trace(result)) < 1e-9


def test_tp6_non_square_rejected():
    x = np.zeros((2, 3), dtype=complex)
    with pytest.raises(ValueError):
        traceless_part(x)


def test_tp7_zero_dimension_rejected():
    x = np.zeros((0, 0), dtype=complex)
    with pytest.raises(ValueError):
        traceless_part(x)


@pytest.mark.parametrize(
    "bad_value",
    [float("nan"), float("inf"), float("-inf")],
    ids=["nan", "inf", "neg_inf"],
)
def test_tp8_non_finite_entries_rejected(bad_value):
    x = np.eye(3, dtype=complex)
    x[0, 1] = bad_value
    with pytest.raises(ValueError):
        traceless_part(x)
