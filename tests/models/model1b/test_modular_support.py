"""Unit tests for cosmotgg.models.model1b.modular_support."""

import math

import numpy as np
import pytest

from cosmotgg.core.states import embed_operator
from cosmotgg.models.model1b.modular_support import (
    PAULI_STACK,
    global_two_body_block,
    modular_datum,
    modular_pauli_coefficients,
    reconstruct_from_pauli_coefficients,
    support_weight_norms,
    support_weights,
)

TOL = 1e-9

_SIGMA_X = PAULI_STACK[1]
_SIGMA_Y = PAULI_STACK[2]
_SIGMA_Z = PAULI_STACK[3]
_IDENTITY2 = PAULI_STACK[0]


def _deterministic_hermitian(dim: int, *, seed_shift: float = 0.0) -> np.ndarray:
    rows = np.arange(dim).reshape(dim, 1)
    cols = np.arange(dim).reshape(1, dim)
    base = (rows + 1j * cols + seed_shift) / (dim + 1.0)
    return base + base.conj().T


def _deterministic_faithful_density_matrix(dim: int) -> np.ndarray:
    hermitian = _deterministic_hermitian(dim)
    eigvals, eigvecs = np.linalg.eigh(hermitian)
    shifted = eigvals - eigvals.min() + 1.0
    weights = shifted / shifted.sum()
    return (eigvecs * weights) @ eigvecs.conj().T


# ---------------------------------------------------------------------------
# modular_datum — delegates entirely to core.modular.modular_hamiltonian
# ---------------------------------------------------------------------------


def test_md1_modular_datum_diagonal_oracle():
    rho = np.diag([0.7, 0.3]).astype(complex)
    k = modular_datum(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    expected = np.diag(-np.log([0.7, 0.3])).astype(complex)
    assert np.allclose(k, expected)


def test_md2_modular_datum_rejects_non_faithful_state():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        modular_datum(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


# ---------------------------------------------------------------------------
# modular_pauli_coefficients — N=1, N=2 known strings, normalization
# ---------------------------------------------------------------------------


def test_pc1_n1_exact_basis_operators():
    for index, sigma in enumerate(PAULI_STACK):
        coeff = modular_pauli_coefficients(sigma, 1)
        expected = np.zeros(4, dtype=complex)
        expected[index] = 1.0
        assert np.allclose(coeff, expected, atol=1e-10)


def test_pc2_n1_coefficient_normalization_independent_oracle():
    k = np.array([[1.0, 0.3 - 0.2j], [0.3 + 0.2j, -0.5]], dtype=complex)
    coeff = modular_pauli_coefficients(k, 1)
    oracle = np.array(
        [
            np.trace(k @ _IDENTITY2) / 2.0,
            np.trace(k @ _SIGMA_X) / 2.0,
            np.trace(k @ _SIGMA_Y) / 2.0,
            np.trace(k @ _SIGMA_Z) / 2.0,
        ]
    )
    assert np.allclose(coeff, oracle, atol=1e-10)


def test_pc3_n2_known_pauli_string_x_tensor_z():
    k = np.kron(_SIGMA_X, _SIGMA_Z)
    coeff = modular_pauli_coefficients(k, 2)
    expected = np.zeros((4, 4), dtype=complex)
    expected[1, 3] = 1.0  # (X, Z) -> index (1, 3)
    assert np.allclose(coeff, expected, atol=1e-10)


def test_pc4_identity_only_gives_weight_zero_only():
    k = np.eye(16, dtype=complex)  # N=4
    coeff = modular_pauli_coefficients(k, 4)
    expected = np.zeros((4,) * 4, dtype=complex)
    expected[0, 0, 0, 0] = 1.0
    assert np.allclose(coeff, expected, atol=1e-10)

    norms = support_weight_norms(coeff)
    assert norms[0] == pytest.approx(1.0, abs=1e-10)
    for w in range(1, 5):
        assert norms[w] == pytest.approx(0.0, abs=1e-10)


def test_pc5_known_three_body_string_correct_weight():
    # K = X (x) I (x) Y (x) Z, N=4: nonzero at (1, 0, 2, 3), weight = 3.
    k = np.kron(np.kron(_SIGMA_X, _IDENTITY2), np.kron(_SIGMA_Y, _SIGMA_Z))
    coeff = modular_pauli_coefficients(k, 4)
    weight = support_weights(coeff)
    assert coeff[1, 0, 2, 3] == pytest.approx(1.0, abs=1e-10)
    assert weight[1, 0, 2, 3] == 3

    norms = support_weight_norms(coeff)
    assert norms[3] == pytest.approx(1.0, abs=1e-10)
    for w in (0, 1, 2, 4):
        assert norms[w] == pytest.approx(0.0, abs=1e-10)


def test_pc6_known_four_body_string_correct_weight():
    k = np.kron(np.kron(_SIGMA_X, _SIGMA_Y), np.kron(_SIGMA_Z, _SIGMA_X))
    coeff = modular_pauli_coefficients(k, 4)
    weight = support_weights(coeff)
    assert coeff[1, 2, 3, 1] == pytest.approx(1.0, abs=1e-10)
    assert weight[1, 2, 3, 1] == 4


# ---------------------------------------------------------------------------
# reconstruction — full-support reconstruction (T5F5 support)
# ---------------------------------------------------------------------------


def test_pc7_reconstruction_recovers_generic_hermitian_n3():
    k = _deterministic_hermitian(8)
    coeff = modular_pauli_coefficients(k, 3)
    reconstructed = reconstruct_from_pauli_coefficients(coeff)
    assert np.allclose(reconstructed, k, atol=1e-10)


def test_pc8_reconstruction_recovers_generic_hermitian_from_real_modular_datum():
    rho = _deterministic_faithful_density_matrix(8)  # N=3
    k = modular_datum(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    coeff = modular_pauli_coefficients(k, 3)
    reconstructed = reconstruct_from_pauli_coefficients(coeff)
    assert np.allclose(reconstructed, k, atol=1e-9)


def test_pc9_n8_smoke_control_no_wall_clock_threshold():
    """N=8 control: must complete and reconstruct exactly, without ever
    materializing 4**8 dense 256x256 Pauli matrices. Not confirmatory T5
    evidence."""
    rho = _deterministic_faithful_density_matrix(256)  # N=8
    k = modular_datum(rho, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    coeff = modular_pauli_coefficients(k, 8)
    assert coeff.shape == (4,) * 8
    reconstructed = reconstruct_from_pauli_coefficients(coeff)
    assert np.allclose(reconstructed, k, atol=1e-8)

    norms = support_weight_norms(coeff)
    assert set(norms.keys()) == set(range(9))
    total_energy = sum(v**2 for v in norms.values())
    # Tr[K^2] = 2^N * sum_s |c_s|^2 (Tr[P_s P_s'] = 2^N delta_ss'), so the
    # weight-graded norms must reconstruct Tr[K^2] / 2^N exactly.
    k_hilbert_schmidt_norm_squared = float(np.real(np.trace(k @ k.conj().T)))
    assert total_energy == pytest.approx(k_hilbert_schmidt_norm_squared / 256.0, rel=1e-6)


# ---------------------------------------------------------------------------
# global_two_body_block — independent trace oracle, orientation, covariance
# ---------------------------------------------------------------------------


def test_jb1_independent_trace_oracle():
    k = _deterministic_hermitian(16)  # N=4
    j_block = global_two_body_block(k, 4, 0, 2)

    dims = (2, 2, 2, 2)
    oracle = np.zeros((3, 3))
    for a in range(1, 4):
        for b in range(1, 4):
            op = embed_operator(np.kron(PAULI_STACK[a], PAULI_STACK[b]), dimensions=dims, positions=(0, 2))
            oracle[a - 1, b - 1] = -np.real(np.trace(k @ op)) / 16.0

    assert np.allclose(j_block, oracle, atol=1e-10)
    assert j_block.dtype == np.float64


def test_jb2_orientation_i_then_j_transpose_identity():
    """Since site i and site j factors commute (different sites), `sigma_a^i
    sigma_b^j == sigma_b^j sigma_a^i` as operators, so exactly
    `J_{i<-j}[a, b] == J_{j<-i}[b, a]`, i.e. `J_{i<-j} == J_{j<-i}^T`. This
    exact algebraic identity is the correct oracle for "rows=site i,
    columns=site j" ordering (not an inequality: swapping the declared
    (i, j) argument order transposes the returned block, it does not
    silently change which physical quantity is computed)."""
    k = _deterministic_hermitian(16)
    j_forward = global_two_body_block(k, 4, 0, 1)
    j_reverse = global_two_body_block(k, 4, 1, 0)
    assert np.allclose(j_forward, j_reverse.T, atol=1e-10)


def test_jb3_same_site_pair_rejected():
    k = np.eye(16, dtype=complex)
    with pytest.raises(ValueError):
        global_two_body_block(k, 4, 1, 1)


def test_jb4_invalid_site_position_rejected():
    k = np.eye(16, dtype=complex)
    with pytest.raises(ValueError):
        global_two_body_block(k, 4, 0, 9)


def _adjoint_so3_from_su2(u_matrix: np.ndarray) -> np.ndarray:
    """R[a,b] such that U sigma_b U^dagger = sum_a R[a,b] sigma_a (adjoint rep)."""
    r_matrix = np.zeros((3, 3))
    for a in range(1, 4):
        for b in range(1, 4):
            transformed = u_matrix @ PAULI_STACK[b] @ u_matrix.conj().T
            r_matrix[a - 1, b - 1] = np.real(np.trace(PAULI_STACK[a] @ transformed)) / 2.0
    return r_matrix


def test_jb5_local_frame_covariance_j_transforms_as_r_i_j_r_j_transpose():
    k = _deterministic_hermitian(16)  # N=4
    site_i, site_j = 0, 2

    theta_i, theta_j = 0.6, 1.3
    u_i = math.cos(theta_i / 2.0) * _IDENTITY2 - 1j * math.sin(theta_i / 2.0) * _SIGMA_X
    u_j = math.cos(theta_j / 2.0) * _IDENTITY2 - 1j * math.sin(theta_j / 2.0) * _SIGMA_Z

    dims = (2, 2, 2, 2)
    u_full = (
        embed_operator(u_i, dimensions=dims, positions=(site_i,))
        @ embed_operator(u_j, dimensions=dims, positions=(site_j,))
    )
    k_prime = u_full @ k @ u_full.conj().T

    j_original = global_two_body_block(k, 4, site_i, site_j)
    j_prime = global_two_body_block(k_prime, 4, site_i, site_j)

    r_i = _adjoint_so3_from_su2(u_i)
    r_j = _adjoint_so3_from_su2(u_j)
    expected = r_i @ j_original @ r_j.T

    assert np.allclose(j_prime, expected, atol=1e-9)
