"""Tests for cosmotgg.models.model0b.relative.

Fixture values used below (`beta`, `lambda_`, `mu`) are explicitly
`NON_NORMATIVE_TEST_FIXTURE`: purely internal-development numerical
examples. They are not `BETA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` in the
scientific sense of `docs/toy-models/toy0b/specification.md` (§23),
which remain `OPEN`.

REL1 below also serves as the conditional-expectation-normalization
regression required by
`docs/toy-models/toy0b/implementation-design.md`: the production
construction of `overlap_relative_modular_generator` divides the
partial trace of each modular Hamiltonian by `d_A = d_C = 2` (§9 of the
specification); REL1 compares that production output against the
independent closed-form oracle of §14, so an implementation that
silently dropped this `/2` normalization would produce a `Delta_B`
scaled incorrectly and fail REL1.
"""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model0b.relative import (
    overlap_relative_modular_derivation,
    overlap_relative_modular_generator,
)
from cosmotgg.models.model0b.states import three_qubit_overlapping_pauli_relation_state

DIMENSIONS_ABC = (2, 2, 2)

# Development-only numerical tolerance for core primitive calls in these
# tests; not a model0b scientific tolerance, not a protocol tolerance.
NON_NORMATIVE_TEST_TOLERANCE = 1e-9

IDENTITY2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
ZERO_2X2 = np.zeros((2, 2), dtype=complex)

# NON_NORMATIVE_TEST_FIXTURE (docs/toy-models/toy0b/specification.md §16).
GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU = 0.2, 0.3, 0.1
R0_BETA, R0_LAMBDA, R0_MU = 0.2, 0.0, 0.0
R1_BETA, R1_LAMBDA, R1_MU = 0.2, 0.3, -0.3
R2_BETA, R2_LAMBDA, R2_MU = 0.2, 0.3, 0.1
R3_BETA, R3_LAMBDA, R3_MU = 0.0, 0.3, 0.1


def _generator_kwargs():
    return dict(
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        trace_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )


def _state(beta, lam, mu):
    return three_qubit_overlapping_pauli_relation_state(beta, lam, mu)


def _delta(beta, lam, mu):
    return overlap_relative_modular_generator(_state(beta, lam, mu), **_generator_kwargs())


def _f(r):
    """Independent oracle helper `f(r) = atanh(r)/r`, `f(0) = 1` (spec §14)."""
    if r == 0.0:
        return 1.0
    return np.arctanh(r) / r


def _expected_delta_scalar(beta, lam, mu):
    """Independent oracle `delta = beta * [f(r_AB) - f(r_BC)]` (spec §14)."""
    r_ab = np.hypot(beta, lam)
    r_bc = np.hypot(beta, mu)
    return beta * (_f(r_ab) - _f(r_bc))


# ---------------------------------------------------------------------------
# REL1 — modular construction matches the independent closed-form oracle
# ---------------------------------------------------------------------------


def test_rel1_delta_matches_independent_analytic_oracle():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    expected_scalar = _expected_delta_scalar(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    expected = expected_scalar * PAULI_Z
    assert np.allclose(delta_b, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# REL2 — Delta is hermitian
# ---------------------------------------------------------------------------


def test_rel2_delta_is_hermitian():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    assert np.allclose(delta_b, delta_b.conj().T, atol=1e-8)


# ---------------------------------------------------------------------------
# REL3 — Tr(Delta) ~= 0
# ---------------------------------------------------------------------------


def test_rel3_delta_is_traceless():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    assert abs(np.trace(delta_b)) < 1e-8


# ---------------------------------------------------------------------------
# REL4-REL6 — derivation identities D(X_B), D(Y_B), D(Z_B) (spec §14)
# ---------------------------------------------------------------------------


def test_rel4_derivation_of_x_equals_two_delta_y():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    delta_scalar = _expected_delta_scalar(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)

    result = overlap_relative_modular_derivation(delta_b, PAULI_X)
    expected = 2.0 * delta_scalar * PAULI_Y
    assert np.allclose(result, expected, atol=1e-8)


def test_rel5_derivation_of_y_equals_minus_two_delta_x():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    delta_scalar = _expected_delta_scalar(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)

    result = overlap_relative_modular_derivation(delta_b, PAULI_Y)
    expected = -2.0 * delta_scalar * PAULI_X
    assert np.allclose(result, expected, atol=1e-8)


def test_rel6_derivation_of_z_is_zero():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)

    result = overlap_relative_modular_derivation(delta_b, PAULI_Z)
    assert np.allclose(result, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL7 — R0_PRODUCT: lambda = mu = 0 => Delta ~= 0
# ---------------------------------------------------------------------------


def test_rel7_r0_product_delta_vanishes():
    delta_b = _delta(R0_BETA, R0_LAMBDA, R0_MU)
    assert np.allclose(delta_b, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL8 — R1_EQUAL_RELATIONS: |lambda| = |mu| != 0 => Delta ~= 0, while the
# two relations are individually nontrivial (Delta = 0 DOES NOT IMPLY
# NO_RELATION, spec §16).
# ---------------------------------------------------------------------------


def test_rel8_r1_equal_relations_delta_vanishes():
    delta_b = _delta(R1_BETA, R1_LAMBDA, R1_MU)
    assert np.allclose(delta_b, ZERO_2X2, atol=1e-8)


def test_rel8_r1_relations_are_individually_nontrivial():
    rho_abc = _state(R1_BETA, R1_LAMBDA, R1_MU)

    rho_ab = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0, 1])
    rho_a = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0])
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    assert not np.allclose(rho_ab, np.kron(rho_a, rho_b), atol=1e-8)

    rho_bc = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1, 2])
    rho_c = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[2])
    assert not np.allclose(rho_bc, np.kron(rho_b, rho_c), atol=1e-8)


# ---------------------------------------------------------------------------
# REL9 — R2_ASYMMETRIC_RELATIONS: beta != 0, lambda**2 != mu**2 => Delta != 0
# ---------------------------------------------------------------------------


def test_rel9_r2_asymmetric_relations_delta_is_nonzero():
    delta_b = _delta(R2_BETA, R2_LAMBDA, R2_MU)
    assert not np.allclose(delta_b, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL10 — R3_MAXIMALLY_MIXED_OVERLAP: beta = 0 => rho_B ~= I/2, Delta ~= 0,
# despite lambda**2 != mu**2.
# ---------------------------------------------------------------------------


def test_rel10_r3_maximally_mixed_overlap_rho_b_is_maximally_mixed():
    rho_abc = _state(R3_BETA, R3_LAMBDA, R3_MU)
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    assert np.allclose(rho_b, IDENTITY2 / 2.0, atol=1e-12)


def test_rel10_r3_maximally_mixed_overlap_delta_vanishes():
    assert R3_LAMBDA**2 != R3_MU**2  # precondition making the control meaningful
    delta_b = _delta(R3_BETA, R3_LAMBDA, R3_MU)
    assert np.allclose(delta_b, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL11 — non-nullity condition across several deterministic fixtures
# (spec §15: Delta != 0 iff beta != 0 and lambda**2 != mu**2). Test-only
# assessment, not a production classifier.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "beta, lam, mu, expect_nonzero",
    [
        (R0_BETA, R0_LAMBDA, R0_MU, False),  # lambda = mu = 0
        (R1_BETA, R1_LAMBDA, R1_MU, False),  # |lambda| = |mu| != 0
        (R2_BETA, R2_LAMBDA, R2_MU, True),  # beta != 0, lambda**2 != mu**2
        (R3_BETA, R3_LAMBDA, R3_MU, False),  # beta = 0
        (0.15, 0.25, -0.05, True),  # beta != 0, lambda**2 != mu**2
    ],
    ids=["R0", "R1", "R2", "R3", "extra_asymmetric"],
)
def test_rel11_nonnullity_condition_across_deterministic_fixtures(
    beta, lam, mu, expect_nonzero
):
    delta_b = _delta(beta, lam, mu)
    is_nonzero = not np.allclose(delta_b, ZERO_2X2, atol=1e-8)
    assert is_nonzero == expect_nonzero


# ---------------------------------------------------------------------------
# LOCAL_PRODUCT_UNITARY_COVARIANCE — Delta(rho') ~= U_B Delta(rho) U_B^dagger
# under rho' = (U_A (x) U_B (x) U_C) rho (U_A (x) U_B (x) U_C)^dagger.
#
# Scope note (do not generalize): this covers ONLY local product
# unitaries U_A (x) U_B (x) U_C, preserving the A|B|C tensor
# factorization itself. It says nothing about an arbitrary
# global/entangling unitary or a refactorization; those are explicitly
# NOT tested here (docs/toy-models/toy0b/specification.md §21).
# ---------------------------------------------------------------------------

# NON_NORMATIVE_TEST_FIXTURE: deterministic, explicitly unitary 2x2
# matrices with no privileged physical status, used only to leave the
# canonical computational basis for this covariance check.
_SQRT2 = np.sqrt(2.0)
U_A = (1.0 / _SQRT2) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
U_B = (1.0 / _SQRT2) * np.array([[1.0, 1.0j], [1.0j, 1.0]], dtype=complex)
U_C = np.array([[1.0, 0.0], [0.0, 1.0j]], dtype=complex)
U_ABC = np.kron(U_A, np.kron(U_B, U_C))


def test_local_product_unitary_fixtures_are_actually_unitary():
    assert np.allclose(U_A.conj().T @ U_A, IDENTITY2, atol=1e-10)
    assert np.allclose(U_B.conj().T @ U_B, IDENTITY2, atol=1e-10)
    assert np.allclose(U_C.conj().T @ U_C, IDENTITY2, atol=1e-10)
    assert np.allclose(U_ABC.conj().T @ U_ABC, np.eye(8, dtype=complex), atol=1e-10)


def test_local_product_unitary_covariance_of_delta():
    rho_abc = _state(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    delta_b = overlap_relative_modular_generator(rho_abc, **_generator_kwargs())

    rho_abc_transformed = U_ABC @ rho_abc @ U_ABC.conj().T
    delta_b_transformed = overlap_relative_modular_generator(
        rho_abc_transformed, **_generator_kwargs()
    )

    expected = U_B @ delta_b @ U_B.conj().T
    assert np.allclose(delta_b_transformed, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# Fail-closed: overlap_relative_modular_generator
# ---------------------------------------------------------------------------


def test_generator_rejects_non_8x8_shape():
    rho_4x4 = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(rho_4x4, **_generator_kwargs())


def test_generator_rejects_non_hermitian_input():
    rho_abc = _state(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    broken = rho_abc.copy()
    broken[0, 1] += 0.5  # break hermiticity without fixing broken[1, 0]
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(broken, **_generator_kwargs())


def test_generator_rejects_wrong_trace():
    rho_abc = _state(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    broken = rho_abc * 2.0  # trace = 2, still hermitian and PSD
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(broken, **_generator_kwargs())


def test_generator_rejects_non_positive_semidefinite_input():
    rho_abc = _state(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    eigvals, eigvecs = np.linalg.eigh(rho_abc)
    eigvals[0] = -abs(eigvals[0]) - 0.5  # force a strictly negative eigenvalue
    broken = (eigvecs * eigvals) @ eigvecs.conj().T
    broken = broken / np.trace(broken)  # restore unit trace, keep non-PSD
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(broken, **_generator_kwargs())


def test_generator_rejects_non_faithful_input():
    eigvals = np.array([0.0, 0.0, 0.0, 0.25, 0.25, 0.25, 0.25, 0.0])
    non_faithful = np.diag(eigvals).astype(complex)
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(non_faithful, **_generator_kwargs())


# ---------------------------------------------------------------------------
# Fail-closed: overlap_relative_modular_derivation
# ---------------------------------------------------------------------------


def test_derivation_rejects_non_square_delta():
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(np.zeros((2, 3), dtype=complex), PAULI_X)


def test_derivation_rejects_wrong_dimension_observable():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(delta_b, np.eye(3, dtype=complex))


@pytest.mark.parametrize(
    "bad_entry", [float("nan"), float("inf"), float("-inf")], ids=["nan", "inf", "-inf"]
)
def test_derivation_rejects_non_finite_delta(bad_entry):
    delta_b = np.array([[bad_entry, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(delta_b, PAULI_X)


def test_derivation_does_not_require_hermitian_observable():
    delta_b = _delta(GENERIC_BETA, GENERIC_LAMBDA, GENERIC_MU)
    non_hermitian_observable = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    result = overlap_relative_modular_derivation(delta_b, non_hermitian_observable)
    expected = -1j * (delta_b @ non_hermitian_observable - non_hermitian_observable @ delta_b)
    assert np.allclose(result, expected, atol=1e-8)
