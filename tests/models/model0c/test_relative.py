"""Tests for cosmotgg.models.model0c.relative.

Fixture values used below (`alpha`, `gamma`, `lambda_`, `mu`) are
explicitly `NON_NORMATIVE_TEST_FIXTURE`: purely internal-development
numerical examples. They are not
`ALPHA_VALUE`/`GAMMA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` in the scientific
sense of `docs/toy-models/toy0c/specification.md` (§23), which remain
`OPEN`.

The analytic oracles for `chi_A`, `chi_C` (`_chi_a_scalar_oracle`,
`_chi_c_scalar_oracle`) and `N` (`-2*a*c*Z_B` when `chi_A = a*X_B`,
`chi_C = c*Y_B`) below reproduce the closed-form formulas of
`docs/toy-models/toy0c/specification.md` §11–§13, independently of the
modular-mechanism production path in `cosmotgg.models.model0c.relative`
(`partial_trace` + `modular_hamiltonian` + `conditional_expectation` +
`traceless_part`). They are ORACLES, used only in this test module,
never reused as a production shortcut.
"""

import math

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model0c.relative import (
    overlap_projected_noncollinearity_operator,
    overlap_relative_modular_derivation,
    overlap_relative_modular_generator,
    overlap_relative_modular_projections,
)
from cosmotgg.models.model0c.states import three_qubit_noncollinear_overlap_relation_state

DIMENSIONS_ABC = (2, 2, 2)

# Development-only numerical tolerance for core primitive calls in these
# tests; not a model0c scientific tolerance, not a protocol tolerance.
NON_NORMATIVE_TEST_TOLERANCE = 1e-9

IDENTITY2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
ZERO_2X2 = np.zeros((2, 2), dtype=complex)

# NON_NORMATIVE_TEST_FIXTURE (docs/toy-models/toy0c/specification.md §8 of
# the mandate / implementation-design.md §11).
MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU = 0.20, 0.15, 0.20, 0.10

C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU = 0.20, 0.15, 0.0, 0.0
C1_ALPHA, C1_GAMMA, C1_LAMBDA, C1_MU = 0.0, 0.15, 0.20, 0.10
C2_ALPHA, C2_GAMMA, C2_LAMBDA, C2_MU = 0.20, 0.0, 0.20, 0.10
C3_ALPHA, C3_GAMMA, C3_LAMBDA, C3_MU = MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU
C4_ALPHA, C4_GAMMA, C4_LAMBDA, C4_MU = 0.0, 0.15, 0.20, 0.10


def _generator_kwargs():
    return dict(
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        trace_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )


def _state(alpha, gamma, lam, mu):
    return three_qubit_noncollinear_overlap_relation_state(alpha, gamma, lam, mu)


def _projections(alpha, gamma, lam, mu):
    rho_abc = _state(alpha, gamma, lam, mu)
    return overlap_relative_modular_projections(rho_abc, **_generator_kwargs())


def _chi_a_scalar_oracle(alpha, lam):
    """Independent oracle: `chi_A = a * X_B`, `a` per spec §11."""
    if lam == 0.0:
        return 0.0
    abs_lam = abs(lam)
    g_plus = math.atanh(abs_lam / (1.0 + alpha)) / abs_lam
    g_minus = math.atanh(abs_lam / (1.0 - alpha)) / abs_lam
    return -(lam / 2.0) * (g_plus - g_minus)


def _chi_c_scalar_oracle(gamma, mu):
    """Independent oracle: `chi_C = c * Y_B`, `c` per spec §11."""
    if mu == 0.0:
        return 0.0
    abs_mu = abs(mu)
    g_plus = math.atanh(abs_mu / (1.0 + gamma)) / abs_mu
    g_minus = math.atanh(abs_mu / (1.0 - gamma)) / abs_mu
    return -(mu / 2.0) * (g_plus - g_minus)


# ---------------------------------------------------------------------------
# REL1/REL2 — production chi_A/chi_C match the independent analytic oracle
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "alpha, gamma, lam, mu",
    [
        (MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU),
        (C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU),  # lambda = mu = 0 branch
    ],
    ids=["main", "zero_branch"],
)
def test_rel1_chi_a_matches_independent_analytic_oracle(alpha, gamma, lam, mu):
    chi_a, _ = _projections(alpha, gamma, lam, mu)
    a_scalar = _chi_a_scalar_oracle(alpha, lam)
    expected = a_scalar * PAULI_X
    assert np.allclose(chi_a, expected, atol=1e-8)


@pytest.mark.parametrize(
    "alpha, gamma, lam, mu",
    [
        (MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU),
        (C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU),  # lambda = mu = 0 branch
    ],
    ids=["main", "zero_branch"],
)
def test_rel2_chi_c_matches_independent_analytic_oracle(alpha, gamma, lam, mu):
    _, chi_c = _projections(alpha, gamma, lam, mu)
    c_scalar = _chi_c_scalar_oracle(gamma, mu)
    expected = c_scalar * PAULI_Y
    assert np.allclose(chi_c, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# REL3/REL4 — chi_A, chi_C hermitian and traceless
# ---------------------------------------------------------------------------


def test_rel3_chi_a_is_hermitian_and_traceless():
    chi_a, _ = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    assert np.allclose(chi_a, chi_a.conj().T, atol=1e-8)
    assert abs(np.trace(chi_a)) < 1e-8


def test_rel4_chi_c_is_hermitian_and_traceless():
    _, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    assert np.allclose(chi_c, chi_c.conj().T, atol=1e-8)
    assert abs(np.trace(chi_c)) < 1e-8


# ---------------------------------------------------------------------------
# REL5 — fixture C3: chi_A != 0, chi_C != 0
# ---------------------------------------------------------------------------


def test_rel5_c3_chi_a_and_chi_c_are_nonzero():
    chi_a, chi_c = _projections(C3_ALPHA, C3_GAMMA, C3_LAMBDA, C3_MU)
    assert not np.allclose(chi_a, ZERO_2X2, atol=1e-8)
    assert not np.allclose(chi_c, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL6 — axes in the canonical basis: chi_A ~ a X_B, chi_C ~ c Y_B, without
# parasitic components. Bounded to the declared canonical family, not a
# basis-invariant claim.
# ---------------------------------------------------------------------------


def test_rel6_axes_are_x_b_and_y_b_without_parasitic_components():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)

    # Pauli basis coefficients: coeff_P(M) = Tr(P @ M) / 2 for P in {I, X, Y, Z}.
    for label, pauli in [("I", IDENTITY2), ("X", PAULI_X), ("Y", PAULI_Y), ("Z", PAULI_Z)]:
        coeff_a = np.trace(pauli @ chi_a) / 2.0
        coeff_c = np.trace(pauli @ chi_c) / 2.0
        if label == "X":
            assert abs(coeff_a) > 1e-6  # the expected nonzero axis of chi_A
        else:
            assert abs(coeff_a) < 1e-8
        if label == "Y":
            assert abs(coeff_c) > 1e-6  # the expected nonzero axis of chi_C
        else:
            assert abs(coeff_c) < 1e-8


# ---------------------------------------------------------------------------
# REL7/REL8/REL9 — Delta = -chi_A + chi_C, hermitian, traceless
# ---------------------------------------------------------------------------


def test_rel7_delta_equals_minus_chi_a_plus_chi_c():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    assert np.allclose(delta, -chi_a + chi_c)


def test_rel8_delta_is_hermitian():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    assert np.allclose(delta, delta.conj().T, atol=1e-8)


def test_rel9_delta_is_traceless():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    assert abs(np.trace(delta)) < 1e-8


# ---------------------------------------------------------------------------
# REL10 — N = i[chi_A, chi_C] against the independent oracle -2*a*c*Z_B
# ---------------------------------------------------------------------------


def test_rel10_n_matches_independent_analytic_oracle():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)

    a_scalar = _chi_a_scalar_oracle(MAIN_ALPHA, MAIN_LAMBDA)
    c_scalar = _chi_c_scalar_oracle(MAIN_GAMMA, MAIN_MU)
    expected = -2.0 * a_scalar * c_scalar * PAULI_Z

    assert np.allclose(n, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# REL11/REL12 — N hermitian, Tr(N) ~= 0
# ---------------------------------------------------------------------------


def test_rel11_n_is_hermitian():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)
    assert np.allclose(n, n.conj().T, atol=1e-8)


def test_rel12_n_is_traceless():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)
    assert abs(np.trace(n)) < 1e-8


# ---------------------------------------------------------------------------
# REL13 — C3: alpha*gamma*lambda*mu != 0 => N != 0
# ---------------------------------------------------------------------------


def test_rel13_c3_n_is_nonzero():
    assert C3_ALPHA * C3_GAMMA * C3_LAMBDA * C3_MU != 0.0  # precondition
    chi_a, chi_c = _projections(C3_ALPHA, C3_GAMMA, C3_LAMBDA, C3_MU)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)
    assert not np.allclose(n, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# REL14 — analytic nonnullity condition of N across several deterministic
# fixtures: N != 0 iff alpha*gamma*lambda*mu != 0. Test-only assessment, not
# a production classifier.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "alpha, gamma, lam, mu",
    [
        (MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU),  # all nonzero
        (C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU),  # lambda = mu = 0
        (C1_ALPHA, C1_GAMMA, C1_LAMBDA, C1_MU),  # alpha = 0
        (C2_ALPHA, C2_GAMMA, C2_LAMBDA, C2_MU),  # gamma = 0
        (0.20, 0.15, 0.20, 0.0),  # mu = 0
        (-0.10, 0.20, 0.15, -0.05),  # all nonzero, mixed signs
    ],
    ids=["main", "C0_lambda_mu_zero", "C1_alpha_zero", "C2_gamma_zero", "mu_zero", "mixed_signs"],
)
def test_rel14_nonnullity_condition_across_deterministic_fixtures(alpha, gamma, lam, mu):
    chi_a, chi_c = _projections(alpha, gamma, lam, mu)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)
    is_nonzero = not np.allclose(n, ZERO_2X2, atol=1e-8)
    expected_nonzero = (alpha * gamma * lam * mu) != 0.0
    assert is_nonzero == expected_nonzero


# ---------------------------------------------------------------------------
# C0 — C0_NO_AB_BC_OVERLAP_RELATIONS: lambda = mu = 0
# ---------------------------------------------------------------------------


def test_c0_no_overlap_relations_product_states():
    rho_abc = _state(C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU)

    rho_ab = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0, 1])
    rho_a = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0])
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    assert np.allclose(rho_ab, np.kron(rho_a, rho_b), atol=1e-8)

    rho_bc = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1, 2])
    rho_c = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[2])
    assert np.allclose(rho_bc, np.kron(rho_b, rho_c), atol=1e-8)


def test_c0_no_overlap_relations_generators_vanish():
    chi_a, chi_c = _projections(C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)

    assert np.allclose(chi_a, ZERO_2X2, atol=1e-8)
    assert np.allclose(chi_c, ZERO_2X2, atol=1e-8)
    assert np.allclose(delta, ZERO_2X2, atol=1e-8)
    assert np.allclose(n, ZERO_2X2, atol=1e-8)


def test_c0_global_state_is_not_a_product_when_alpha_gamma_nonzero():
    assert C0_ALPHA * C0_GAMMA != 0.0  # precondition
    rho_abc = _state(C0_ALPHA, C0_GAMMA, C0_LAMBDA, C0_MU)

    rho_a = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0])
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    rho_c = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[2])
    product = np.kron(rho_a, np.kron(rho_b, rho_c))

    assert not np.allclose(rho_abc, product, atol=1e-8)


# ---------------------------------------------------------------------------
# C1 — C1_CORRELATED_BUT_ZERO_PROJECTED_A: alpha = 0, lambda != 0
# ---------------------------------------------------------------------------


def test_c1_correlated_ab_but_zero_projected_a():
    assert C1_ALPHA == 0.0 and C1_LAMBDA != 0.0  # precondition
    rho_abc = _state(C1_ALPHA, C1_GAMMA, C1_LAMBDA, C1_MU)
    rho_ab = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0, 1])
    rho_a = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[0])
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    assert not np.allclose(rho_ab, np.kron(rho_a, rho_b), atol=1e-8)

    chi_a, _ = _projections(C1_ALPHA, C1_GAMMA, C1_LAMBDA, C1_MU)
    assert np.allclose(chi_a, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# C2 — C2_CORRELATED_BUT_ZERO_PROJECTED_C: gamma = 0, mu != 0
# ---------------------------------------------------------------------------


def test_c2_correlated_bc_but_zero_projected_c():
    assert C2_GAMMA == 0.0 and C2_MU != 0.0  # precondition
    rho_abc = _state(C2_ALPHA, C2_GAMMA, C2_LAMBDA, C2_MU)
    rho_bc = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1, 2])
    rho_b = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[1])
    rho_c = partial_trace(rho_abc, dimensions=DIMENSIONS_ABC, keep=[2])
    assert not np.allclose(rho_bc, np.kron(rho_b, rho_c), atol=1e-8)

    _, chi_c = _projections(C2_ALPHA, C2_GAMMA, C2_LAMBDA, C2_MU)
    assert np.allclose(chi_c, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# C3 — C3_NONCOLLINEAR: alpha*gamma*lambda*mu != 0
# ---------------------------------------------------------------------------


def test_c3_noncollinear_generators_and_commutator_nonzero():
    assert C3_ALPHA * C3_GAMMA * C3_LAMBDA * C3_MU != 0.0  # precondition
    chi_a, chi_c = _projections(C3_ALPHA, C3_GAMMA, C3_LAMBDA, C3_MU)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)

    assert not np.allclose(chi_a, ZERO_2X2, atol=1e-8)
    assert not np.allclose(chi_c, ZERO_2X2, atol=1e-8)
    assert not np.allclose(n, ZERO_2X2, atol=1e-8)

    commutator = chi_a @ chi_c - chi_c @ chi_a
    assert not np.allclose(commutator, ZERO_2X2, atol=1e-8)


# ---------------------------------------------------------------------------
# C4 — C4_DELTA_NONZERO_BUT_N_ZERO: alpha = 0, lambda != 0, gamma*mu != 0
# ---------------------------------------------------------------------------


def test_c4_delta_nonzero_but_n_zero():
    assert C4_ALPHA == 0.0
    assert C4_LAMBDA != 0.0
    assert C4_GAMMA * C4_MU != 0.0  # precondition

    chi_a, chi_c = _projections(C4_ALPHA, C4_GAMMA, C4_LAMBDA, C4_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)

    assert np.allclose(chi_a, ZERO_2X2, atol=1e-8)
    assert not np.allclose(chi_c, ZERO_2X2, atol=1e-8)
    assert not np.allclose(delta, ZERO_2X2, atol=1e-8)
    assert np.allclose(n, ZERO_2X2, atol=1e-8)
    # DELTA_NONZERO_IS_NOT_SUFFICIENT_FOR_NONCOLLINEARITY (structural
    # conclusion only, not a production classifier).


# ---------------------------------------------------------------------------
# LOCAL_PRODUCT_UNITARY_COVARIANCE — chi_A/chi_C/Delta/N covariant under
# rho' = (U_A (x) U_B (x) U_C) rho (U_A (x) U_B (x) U_C)^dagger.
#
# Scope note (do not generalize): this covers ONLY local product unitaries
# U_A (x) U_B (x) U_C, preserving the A|B|C tensor factorization itself.
# It says nothing about an arbitrary global/entangling unitary or a
# refactorization; those are explicitly NOT tested here
# (docs/toy-models/toy0c/specification.md §19).
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


def test_local_product_unitary_covariance_of_chi_and_delta_and_n():
    rho_abc = _state(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    chi_a, chi_c = overlap_relative_modular_projections(rho_abc, **_generator_kwargs())
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    n = overlap_projected_noncollinearity_operator(chi_a, chi_c)

    rho_abc_transformed = U_ABC @ rho_abc @ U_ABC.conj().T
    chi_a_transformed, chi_c_transformed = overlap_relative_modular_projections(
        rho_abc_transformed, **_generator_kwargs()
    )
    delta_transformed = overlap_relative_modular_generator(chi_a_transformed, chi_c_transformed)
    n_transformed = overlap_projected_noncollinearity_operator(
        chi_a_transformed, chi_c_transformed
    )

    assert np.allclose(chi_a_transformed, U_B @ chi_a @ U_B.conj().T, atol=1e-8)
    assert np.allclose(chi_c_transformed, U_B @ chi_c @ U_B.conj().T, atol=1e-8)
    assert np.allclose(delta_transformed, U_B @ delta @ U_B.conj().T, atol=1e-8)
    assert np.allclose(n_transformed, U_B @ n @ U_B.conj().T, atol=1e-8)


# ---------------------------------------------------------------------------
# Derivation — D(O) = -i[Delta, O] on X_B, Y_B, Z_B, against an independent
# identity built from the analytic scalar oracles and known Pauli
# commutation relations (not by re-deriving the production formula).
# ---------------------------------------------------------------------------


def _delta_scalars(alpha, gamma, lam, mu):
    a_scalar = _chi_a_scalar_oracle(alpha, lam)
    c_scalar = _chi_c_scalar_oracle(gamma, mu)
    return a_scalar, c_scalar


def test_derivation_of_x_matches_independent_pauli_identity():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)

    _, c_scalar = _delta_scalars(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    # Delta = -a X + c Y (p=-a, q=c); D(X) = -i[pX+qY, X] = -2*q*Z = -2*c*Z.
    result = overlap_relative_modular_derivation(delta, PAULI_X)
    expected = -2.0 * c_scalar * PAULI_Z
    assert np.allclose(result, expected, atol=1e-8)


def test_derivation_of_y_matches_independent_pauli_identity():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)

    a_scalar, _ = _delta_scalars(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    # D(Y) = -i[pX+qY, Y] = 2*p*Z = 2*(-a)*Z = -2*a*Z.
    result = overlap_relative_modular_derivation(delta, PAULI_Y)
    expected = -2.0 * a_scalar * PAULI_Z
    assert np.allclose(result, expected, atol=1e-8)


def test_derivation_of_z_matches_independent_pauli_identity():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)

    a_scalar, c_scalar = _delta_scalars(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    # D(Z) = -i[pX+qY, Z] = -2*p*Y + 2*q*X = 2*a*Y + 2*c*X.
    result = overlap_relative_modular_derivation(delta, PAULI_Z)
    expected = 2.0 * a_scalar * PAULI_Y + 2.0 * c_scalar * PAULI_X
    assert np.allclose(result, expected, atol=1e-8)


def test_derivation_does_not_require_hermitian_observable():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    non_hermitian_observable = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    result = overlap_relative_modular_derivation(delta, non_hermitian_observable)
    expected = -1j * (delta @ non_hermitian_observable - non_hermitian_observable @ delta)
    assert np.allclose(result, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# Fail-closed: overlap_relative_modular_projections
# ---------------------------------------------------------------------------


def test_projections_rejects_non_8x8_shape():
    rho_4x4 = np.eye(4, dtype=complex) / 4.0
    with pytest.raises(ValueError):
        overlap_relative_modular_projections(rho_4x4, **_generator_kwargs())


def test_projections_rejects_non_hermitian_input():
    rho_abc = _state(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    broken = rho_abc.copy()
    broken[0, 1] += 0.5  # break hermiticity without fixing broken[1, 0]
    with pytest.raises(ValueError):
        overlap_relative_modular_projections(broken, **_generator_kwargs())


def test_projections_rejects_wrong_trace():
    rho_abc = _state(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    broken = rho_abc * 2.0  # trace = 2, still hermitian and PSD
    with pytest.raises(ValueError):
        overlap_relative_modular_projections(broken, **_generator_kwargs())


def test_projections_rejects_non_positive_semidefinite_input():
    rho_abc = _state(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    eigvals, eigvecs = np.linalg.eigh(rho_abc)
    eigvals[0] = -abs(eigvals[0]) - 0.5  # force a strictly negative eigenvalue
    broken = (eigvecs * eigvals) @ eigvecs.conj().T
    broken = broken / np.trace(broken)  # restore unit trace, keep non-PSD
    with pytest.raises(ValueError):
        overlap_relative_modular_projections(broken, **_generator_kwargs())


def test_projections_rejects_non_faithful_input():
    eigvals = np.array([0.0, 0.0, 0.0, 0.25, 0.25, 0.25, 0.25, 0.0])
    non_faithful = np.diag(eigvals).astype(complex)
    with pytest.raises(ValueError):
        overlap_relative_modular_projections(non_faithful, **_generator_kwargs())


# ---------------------------------------------------------------------------
# Fail-closed: overlap_relative_modular_generator /
# overlap_projected_noncollinearity_operator
# ---------------------------------------------------------------------------


def test_generator_rejects_non_square_chi():
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(np.zeros((2, 3), dtype=complex), PAULI_Y)


def test_generator_rejects_wrong_dimension_chi():
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(np.eye(3, dtype=complex), PAULI_Y)


@pytest.mark.parametrize(
    "bad_entry", [float("nan"), float("inf"), float("-inf")], ids=["nan", "inf", "-inf"]
)
def test_generator_rejects_non_finite_chi(bad_entry):
    bad_chi = np.array([[bad_entry, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        overlap_relative_modular_generator(bad_chi, PAULI_Y)


def test_noncollinearity_operator_rejects_non_square_chi():
    with pytest.raises(ValueError):
        overlap_projected_noncollinearity_operator(np.zeros((2, 3), dtype=complex), PAULI_Y)


def test_noncollinearity_operator_rejects_wrong_dimension_chi():
    with pytest.raises(ValueError):
        overlap_projected_noncollinearity_operator(np.eye(3, dtype=complex), PAULI_Y)


@pytest.mark.parametrize(
    "bad_entry", [float("nan"), float("inf"), float("-inf")], ids=["nan", "inf", "-inf"]
)
def test_noncollinearity_operator_rejects_non_finite_chi(bad_entry):
    bad_chi = np.array([[bad_entry, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        overlap_projected_noncollinearity_operator(bad_chi, PAULI_Y)


# ---------------------------------------------------------------------------
# Fail-closed: overlap_relative_modular_derivation
# ---------------------------------------------------------------------------


def test_derivation_rejects_non_square_delta():
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(np.zeros((2, 3), dtype=complex), PAULI_X)


def test_derivation_rejects_wrong_dimension_observable():
    chi_a, chi_c = _projections(MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU)
    delta = overlap_relative_modular_generator(chi_a, chi_c)
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(delta, np.eye(3, dtype=complex))


@pytest.mark.parametrize(
    "bad_entry", [float("nan"), float("inf"), float("-inf")], ids=["nan", "inf", "-inf"]
)
def test_derivation_rejects_non_finite_delta(bad_entry):
    delta_b = np.array([[bad_entry, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        overlap_relative_modular_derivation(delta_b, PAULI_X)
