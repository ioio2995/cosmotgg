"""Unit tests for cosmotgg.models.model1b.directional."""

import numpy as np
import pytest

from cosmotgg.models.model1b.directional import (
    REASON_SINGULAR_DIRECTIONAL_FACTOR,
    REASON_Z2_DIRECTIONAL_TYPE_MISMATCH,
    DirectionalFactorUndefinedError,
    DirectionalTypeMismatchError,
    LoopDiagnosticUndefinedError,
    active_cycle_loop_object,
    active_cycle_loop_object_from_blocks,
    conjugacy_class_scalar,
    directional_conditioning,
    directional_factor,
    finite_scale_running,
    flatness_diagnostic,
    tree_relative_direction,
)

_IDENTITY3 = np.eye(3)


def _rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    """Deterministic fixed SO(3) rotation via Rodrigues' formula (test-only,
    generic linear algebra, independent of the production polar machinery)."""
    axis = axis / np.linalg.norm(axis)
    kx, ky, kz = axis
    k_matrix = np.array([[0.0, -kz, ky], [kz, 0.0, -kx], [-ky, kx, 0.0]])
    return (
        np.eye(3)
        + np.sin(angle) * k_matrix
        + (1.0 - np.cos(angle)) * (k_matrix @ k_matrix)
    )


def _householder_reflection(v: np.ndarray) -> np.ndarray:
    v = v / np.linalg.norm(v)
    return np.eye(3) - 2.0 * np.outer(v, v)


# ---------------------------------------------------------------------------
# directional_factor — exact O_MINUS_3 domain, singular/near-singular, typing
# ---------------------------------------------------------------------------


def test_df1_full_rank_o_minus_3_matches_independent_svd_oracle():
    j_matrix = np.diag([2.0, 3.0, -1.0])
    result = directional_factor(j_matrix)

    w_matrix, _singular_values, vh_matrix = np.linalg.svd(j_matrix)
    expected = w_matrix @ vh_matrix
    assert np.allclose(result, expected, atol=1e-10)
    assert np.linalg.det(result) == pytest.approx(-1.0, abs=1e-10)


def test_df2_exact_singular_j_undefined_with_reason():
    j_matrix = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
    with pytest.raises(DirectionalFactorUndefinedError) as excinfo:
        directional_factor(j_matrix)
    assert excinfo.value.reason == REASON_SINGULAR_DIRECTIONAL_FACTOR


def test_df3_near_singular_nonzero_j_remains_defined_with_poor_conditioning():
    j_matrix = np.diag([1.0, 1.0, -1e-8])  # det = -1e-8, nonzero exactly
    assert np.linalg.det(j_matrix) != 0.0

    result = directional_factor(j_matrix)  # must NOT raise
    assert np.linalg.det(result) == pytest.approx(-1.0, abs=1e-10)

    singular_values = directional_conditioning(j_matrix)
    assert singular_values.min() == pytest.approx(1e-8, rel=1e-6)
    assert singular_values.max() == pytest.approx(1.0, abs=1e-10)


def test_df4_det_o_plus_one_type_mismatch():
    j_matrix = np.diag([1.0, -1.0, -1.0])  # det = +1, well conditioned
    with pytest.raises(DirectionalTypeMismatchError) as excinfo:
        directional_factor(j_matrix)
    assert excinfo.value.reason == REASON_Z2_DIRECTIONAL_TYPE_MISMATCH


def test_df5_no_hidden_sign_repair_on_type_mismatch():
    """A det(O)=+1 case must fail closed, never silently flip a sign to
    force det(O)=-1."""
    j_matrix = np.diag([1.0, -1.0, -1.0])
    with pytest.raises(ValueError):
        directional_factor(j_matrix)
    # The exception carries the exact mismatch reason, not a repaired matrix.


def test_df6_covariance_o_prime_equals_r_i_o_r_j_transpose():
    j_matrix = np.array([[0.9, 0.1, 0.0], [-0.2, 1.1, 0.3], [0.05, -0.1, -0.8]])
    o_matrix = directional_factor(j_matrix)

    r_i = _rotation_matrix(np.array([1.0, 0.0, 0.0]), 0.7)
    r_j = _rotation_matrix(np.array([0.0, 1.0, 1.0]), 1.1)

    j_prime = r_i @ j_matrix @ r_j.T
    o_prime = directional_factor(j_prime)

    expected = r_i @ o_matrix @ r_j.T
    assert np.allclose(o_prime, expected, atol=1e-9)
    assert np.linalg.det(o_prime) == pytest.approx(np.linalg.det(o_matrix), abs=1e-10)


def test_df7_malformed_shape_rejected():
    with pytest.raises(ValueError):
        directional_factor(np.eye(2))


def test_df8_nonreal_input_rejected():
    j_matrix = np.eye(3, dtype=complex)
    j_matrix[0, 1] = 1.0j
    with pytest.raises(ValueError):
        directional_factor(j_matrix)


# ---------------------------------------------------------------------------
# active_cycle_loop_object — ordered composition, flat/nontrivial loops
# ---------------------------------------------------------------------------


def test_lo1_ordered_composition_matches_manual_product():
    o_ab = _householder_reflection(np.array([1.0, 0.3, 0.0]))
    o_bc = _householder_reflection(np.array([0.0, 1.0, 0.2]))
    o_cd = _householder_reflection(np.array([0.2, 0.0, 1.0]))
    o_da = _householder_reflection(np.array([1.0, 1.0, 1.0]))

    result = active_cycle_loop_object([o_ab, o_bc, o_cd, o_da])
    expected = o_ab @ o_bc @ o_cd @ o_da
    assert np.allclose(result, expected)


def test_lo2_identity_flat_loop():
    reflection = np.diag([1.0, 1.0, -1.0])  # reflection^2 = I, so ^4 = I
    q_matrix = active_cycle_loop_object([reflection] * 4)
    assert np.allclose(q_matrix, _IDENTITY3, atol=1e-12)
    assert flatness_diagnostic(q_matrix) == pytest.approx(0.0, abs=1e-12)
    assert conjugacy_class_scalar(q_matrix) == pytest.approx(1.0, abs=1e-12)


def test_lo3_nontrivial_so3_loop():
    o_ab = np.diag([1.0, 1.0, -1.0])
    o_bc = np.diag([1.0, -1.0, 1.0])
    o_cd = np.diag([-1.0, 1.0, 1.0])
    o_da = _householder_reflection(np.array([1.0, 1.0, 0.3]))

    q_matrix = active_cycle_loop_object([o_ab, o_bc, o_cd, o_da])
    assert np.linalg.det(q_matrix) == pytest.approx(1.0, abs=1e-10)  # domain consequence
    assert not np.allclose(q_matrix, _IDENTITY3, atol=1e-6)
    assert flatness_diagnostic(q_matrix) > 0.0


def test_lo4_empty_sequence_rejected():
    with pytest.raises(ValueError):
        active_cycle_loop_object([])


# ---------------------------------------------------------------------------
# base-point covariance Q' = R_A Q R_A^T (telescoping through R_B, R_C, R_D)
# ---------------------------------------------------------------------------


def test_lo5_base_point_covariance_via_telescoping_edge_covariance():
    o_ab = np.diag([1.0, 1.0, -1.0])
    o_bc = np.diag([1.0, -1.0, 1.0])
    o_cd = np.diag([-1.0, 1.0, 1.0])
    o_da = _householder_reflection(np.array([1.0, 1.0, 0.3]))
    q_matrix = active_cycle_loop_object([o_ab, o_bc, o_cd, o_da])

    r_a = _rotation_matrix(np.array([1.0, 0.0, 0.0]), 0.4)
    r_b = _rotation_matrix(np.array([0.0, 1.0, 0.0]), 0.9)
    r_c = _rotation_matrix(np.array([0.0, 0.0, 1.0]), 1.3)
    r_d = _rotation_matrix(np.array([1.0, 1.0, 1.0]), 0.6)

    o_ab_prime = r_a @ o_ab @ r_b.T
    o_bc_prime = r_b @ o_bc @ r_c.T
    o_cd_prime = r_c @ o_cd @ r_d.T
    o_da_prime = r_d @ o_da @ r_a.T

    q_prime = active_cycle_loop_object([o_ab_prime, o_bc_prime, o_cd_prime, o_da_prime])
    expected = r_a @ q_matrix @ r_a.T

    assert np.allclose(q_prime, expected, atol=1e-9)
    assert flatness_diagnostic(q_prime) == pytest.approx(flatness_diagnostic(q_matrix), abs=1e-9)
    assert conjugacy_class_scalar(q_prime) == pytest.approx(
        conjugacy_class_scalar(q_matrix), abs=1e-9
    )


# ---------------------------------------------------------------------------
# active_cycle_loop_object_from_blocks — undefined-domain propagation
# ---------------------------------------------------------------------------


def _well_defined_j_block():
    return np.diag([2.0, 3.0, -1.0])  # det(O) = -1, well-defined


def test_lo6_singular_edge_loop_undefined_reason_preserved():
    j_ok = _well_defined_j_block()
    j_singular = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
    with pytest.raises(LoopDiagnosticUndefinedError) as excinfo:
        active_cycle_loop_object_from_blocks([j_ok, j_ok, j_singular, j_ok])
    assert excinfo.value.reason == REASON_SINGULAR_DIRECTIONAL_FACTOR


def test_lo7_type_mismatch_edge_loop_undefined_reason_preserved():
    j_ok = _well_defined_j_block()
    j_mismatch = np.diag([1.0, -1.0, -1.0])  # det(O) = +1
    with pytest.raises(LoopDiagnosticUndefinedError) as excinfo:
        active_cycle_loop_object_from_blocks([j_ok, j_mismatch, j_ok, j_ok])
    assert excinfo.value.reason == REASON_Z2_DIRECTIONAL_TYPE_MISMATCH


def test_lo8_reasons_never_confused():
    assert REASON_SINGULAR_DIRECTIONAL_FACTOR != REASON_Z2_DIRECTIONAL_TYPE_MISMATCH


def test_lo9_well_defined_blocks_produce_so3_loop():
    j_ok = _well_defined_j_block()
    q_matrix = active_cycle_loop_object_from_blocks([j_ok, j_ok, j_ok, j_ok])
    assert np.linalg.det(q_matrix) == pytest.approx(1.0, abs=1e-10)


# ---------------------------------------------------------------------------
# finite_scale_running
# ---------------------------------------------------------------------------


def test_fsr1_delta_chi_symmetric_nonnegative():
    assert finite_scale_running(0.3, 0.8) == pytest.approx(0.5, abs=1e-12)
    assert finite_scale_running(0.8, 0.3) == pytest.approx(0.5, abs=1e-12)
    assert finite_scale_running(0.5, 0.5) == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------------------
# tree_relative_direction — D_tree = O_path^T O_coarse
# ---------------------------------------------------------------------------


def test_td1_exact_identity_agreement():
    o_matrix = directional_factor(np.diag([2.0, 3.0, -1.0]))
    d_tree = tree_relative_direction(o_matrix, o_matrix)
    assert np.allclose(d_tree, _IDENTITY3, atol=1e-10)


def test_td2_deliberately_differing_paths():
    o_path = directional_factor(np.diag([2.0, 3.0, -1.0]))  # sign pattern (+, +, -)
    o_coarse = directional_factor(np.diag([-1.0, 3.0, 2.0]))  # sign pattern (-, +, +)
    d_tree = tree_relative_direction(o_path, o_coarse)
    assert not np.allclose(d_tree, _IDENTITY3, atol=1e-6)


def test_td3_conjugation_covariance_at_shared_endpoint():
    o_path = directional_factor(np.diag([2.0, 3.0, -1.0]))
    o_coarse = directional_factor(np.diag([-1.0, 2.0, 4.0]))
    d_tree = tree_relative_direction(o_path, o_coarse)

    r_a = _rotation_matrix(np.array([1.0, 0.0, 0.0]), 0.4)
    r_d = _rotation_matrix(np.array([0.0, 0.0, 1.0]), 1.2)

    o_path_prime = r_a @ o_path @ r_d.T
    o_coarse_prime = r_a @ o_coarse @ r_d.T
    d_tree_prime = tree_relative_direction(o_path_prime, o_coarse_prime)

    expected = r_d @ d_tree @ r_d.T
    assert np.allclose(d_tree_prime, expected, atol=1e-9)


def test_td4_path_order_matters():
    m1 = _householder_reflection(np.array([1.0, 0.2, 0.0]))
    m2 = _householder_reflection(np.array([0.0, 1.0, 0.3]))

    o_path_forward = m1 @ m2
    o_path_backward = m2 @ m1
    o_coarse = _well_defined_j_block()  # any fixed reference orthogonal-ish matrix
    o_coarse = directional_factor(o_coarse)

    d_forward = tree_relative_direction(o_path_forward, o_coarse)
    d_backward = tree_relative_direction(o_path_backward, o_coarse)
    assert not np.allclose(d_forward, d_backward, atol=1e-6)


def test_td5_malformed_shape_rejected():
    with pytest.raises(ValueError):
        tree_relative_direction(np.eye(2), np.eye(3))
