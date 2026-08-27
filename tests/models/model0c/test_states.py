"""Tests for cosmotgg.models.model0c.states.

Fixture values used below (`alpha`, `gamma`, `lambda_`, `mu`) are
explicitly `NON_NORMATIVE_TEST_FIXTURE`: purely internal-development
numerical examples, chosen strictly inside (or, for the negative
controls, strictly outside/on the boundary of) the analytic domain of
`docs/toy-models/toy0c/specification.md` §6. They are not
`ALPHA_VALUE`/`GAMMA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` in the scientific
sense of the specification (§23), which remain `OPEN`.
"""

import math

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model0c.states import three_qubit_noncollinear_overlap_relation_state

DIMENSIONS_ABC = (2, 2, 2)

# NON_NORMATIVE_TEST_FIXTURE: interior admissible point used across
# several tests below. Not a model0c canonical/scientific parameter
# value.
ALPHA, GAMMA, LAMBDA, MU = 0.20, 0.15, 0.20, 0.10

IDENTITY2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _oracle_state(alpha, gamma, lam, mu):
    """Independent oracle for `rho_ABC(alpha, gamma, lam, mu)` (spec §5).

    Built by direct enumeration of the computational basis `|abc>`
    (`a, b, c in {0, 1}`, index `4a + 2b + c`) and the explicit action
    of `X_A`, `Z_C`, `X_A X_B`, `Y_B Z_C` on each basis state, WITHOUT
    using `numpy.kron` on Pauli matrices: a computational path
    independent of the production construction in
    `cosmotgg.models.model0c.states.three_qubit_noncollinear_overlap_relation_state`.

    `X|a> = |1-a>`; `Z|c> = (-1)**c |c>`; `Y|b> = 1j*(-1)**b |1-b>`
    (`Y|0>=1j|1>`, `Y|1>=-1j|0>`).

    For a general single/two-factor Pauli-string operator `O` acting on
    basis ket `|j> = |a,b,c>`, `O|j> = coefficient * |target>`; the
    corresponding matrix element is `O[target, j] = coefficient` (row =
    target index reached by the action, column = source index `j`).
    This convention is applied explicitly below (rather than assumed
    symmetric) because the `mu` term (`Y_B Z_C`) carries a genuinely
    complex coefficient.
    """
    dim = 8
    rho = np.zeros((dim, dim), dtype=complex)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                j = 4 * a + 2 * b + c  # source index

                # I + gamma * Z_C: diagonal.
                rho[j, j] += (1.0 + gamma * (-1) ** c) / 8.0

                # alpha * X_A: flips a.
                target_alpha = 4 * (1 - a) + 2 * b + c
                rho[target_alpha, j] += alpha / 8.0

                # lambda_ * X_A X_B: flips a and b.
                target_lambda = 4 * (1 - a) + 2 * (1 - b) + c
                rho[target_lambda, j] += lam / 8.0

                # mu * Y_B Z_C: flips b, phase 1j*(-1)**(b+c), Z_C keeps c.
                target_mu = 4 * a + 2 * (1 - b) + c
                rho[target_mu, j] += mu * 1j * (-1) ** (b + c) / 8.0
    return rho


# ---------------------------------------------------------------------------
# S1 — exact matrix against an independently constructed oracle
# ---------------------------------------------------------------------------


def test_s1_state_matches_independent_oracle():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    expected = _oracle_state(ALPHA, GAMMA, LAMBDA, MU)
    assert np.allclose(rho, expected)


# ---------------------------------------------------------------------------
# S2 — shape
# ---------------------------------------------------------------------------


def test_s2_state_shape_is_8x8():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    assert rho.shape == (8, 8)


# ---------------------------------------------------------------------------
# S3 — hermiticity (exact / numerical machine precision)
# ---------------------------------------------------------------------------


def test_s3_state_is_hermitian():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    assert np.allclose(rho, rho.conj().T, atol=1e-12)


# ---------------------------------------------------------------------------
# S4 — trace == 1
# ---------------------------------------------------------------------------


def test_s4_state_trace_is_one():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    assert np.isclose(np.trace(rho), 1.0)


# ---------------------------------------------------------------------------
# S5 — faithfulness of an interior fixture, checked directly via eigvalsh
# ---------------------------------------------------------------------------


def test_s5_state_interior_fixture_has_strictly_positive_spectrum():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > 0.0)


# ---------------------------------------------------------------------------
# S6 — analytic spectrum: (1 + alpha*x + gamma*z +/- hypot(lambda, mu)) / 8
# for x, z in {-1, +1}
# ---------------------------------------------------------------------------


def test_s6_state_spectrum_matches_analytic_formula():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    eigvals = np.sort(np.linalg.eigvalsh(rho))

    radius = math.hypot(LAMBDA, MU)
    expected = []
    for x in (-1, 1):
        for z in (-1, 1):
            base = 1.0 + ALPHA * x + GAMMA * z
            expected.append((base + radius) / 8.0)
            expected.append((base - radius) / 8.0)
    expected = np.sort(np.array(expected))

    assert np.allclose(eigvals, expected, atol=1e-12)


# ---------------------------------------------------------------------------
# S7 — reduced states against the analytic formulas of specification.md §7
# ---------------------------------------------------------------------------


def test_s7_reduced_state_rho_ab_matches_analytic_formula():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_ab = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[0, 1])

    x_a = np.kron(PAULI_X, IDENTITY2)
    x_a_x_b = np.kron(PAULI_X, PAULI_X)
    expected = (np.eye(4, dtype=complex) + ALPHA * x_a + LAMBDA * x_a_x_b) / 4.0

    assert np.allclose(rho_ab, expected, atol=1e-12)


def test_s7_reduced_state_rho_bc_matches_analytic_formula():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_bc = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1, 2])

    z_c = np.kron(IDENTITY2, PAULI_Z)
    y_b_z_c = np.kron(PAULI_Y, PAULI_Z)
    expected = (np.eye(4, dtype=complex) + GAMMA * z_c + MU * y_b_z_c) / 4.0

    assert np.allclose(rho_bc, expected, atol=1e-12)


def test_s7_reduced_state_rho_b_is_maximally_mixed():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_b = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1])
    assert np.allclose(rho_b, IDENTITY2 / 2.0, atol=1e-12)


def test_s7_reduced_state_rho_a_matches_analytic_formula():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[0])
    expected = (IDENTITY2 + ALPHA * PAULI_X) / 2.0
    assert np.allclose(rho_a, expected, atol=1e-12)


def test_s7_reduced_state_rho_c_matches_analytic_formula():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_c = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[2])
    expected = (IDENTITY2 + GAMMA * PAULI_Z) / 2.0
    assert np.allclose(rho_c, expected, atol=1e-12)


# ---------------------------------------------------------------------------
# S8 — rho_B == I/2 (already covered above); kept as an explicit,
# separately named assertion for direct traceability to spec §7.
# ---------------------------------------------------------------------------


def test_s8_rho_b_equals_identity_over_two():
    rho = three_qubit_noncollinear_overlap_relation_state(ALPHA, GAMMA, LAMBDA, MU)
    rho_b = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1])
    assert np.allclose(rho_b, IDENTITY2 / 2.0, atol=1e-12)


# ---------------------------------------------------------------------------
# S9 — executability corollary: rho_AB, rho_BC faithful on several valid
# fixtures (spec §6: |alpha|+|lambda|<1, |gamma|+|mu|<1 are implied by the
# full domain, hence automatic).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "alpha, gamma, lam, mu",
    [
        (ALPHA, GAMMA, LAMBDA, MU),
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.3, 0.1, 0.05),
        (-0.2, -0.3, 0.25, -0.15),
    ],
    ids=["main", "origin", "generic", "mixed_signs"],
)
def test_s9_reduced_pair_states_are_faithful(alpha, gamma, lam, mu):
    rho = three_qubit_noncollinear_overlap_relation_state(alpha, gamma, lam, mu)
    rho_ab = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[0, 1])
    rho_bc = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1, 2])

    assert np.all(np.linalg.eigvalsh(rho_ab) > 0.0)
    assert np.all(np.linalg.eigvalsh(rho_bc) > 0.0)


# ---------------------------------------------------------------------------
# S10 — rejection at the exact boundary (no tolerance)
# ---------------------------------------------------------------------------


def test_s10_state_rejects_exact_boundary():
    # abs(1.0) + abs(0.0) + hypot(0.0, 0.0) == 1.0 exactly, no rounding.
    with pytest.raises(ValueError):
        three_qubit_noncollinear_overlap_relation_state(1.0, 0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# S11 — rejection strictly outside the domain
# ---------------------------------------------------------------------------


def test_s11_state_rejects_outside_domain():
    with pytest.raises(ValueError):
        three_qubit_noncollinear_overlap_relation_state(1.5, 0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# S12 — fail-closed input types (parametrized across alpha, gamma, lambda_, mu)
# ---------------------------------------------------------------------------


BAD_PARAMETER_VALUES = [
    True,
    1.0 + 1.0j,
    float("nan"),
    float("inf"),
    float("-inf"),
    np.array([0.1, 0.2]),
    "0.2",
]
BAD_PARAMETER_IDS = ["bool", "complex", "nan", "inf", "-inf", "non-scalar", "non-numeric"]


@pytest.mark.parametrize(
    "param_index", [0, 1, 2, 3], ids=["alpha", "gamma", "lambda_", "mu"]
)
@pytest.mark.parametrize("bad_value", BAD_PARAMETER_VALUES, ids=BAD_PARAMETER_IDS)
def test_s12_state_rejects_bad_parameter_types(param_index, bad_value):
    args = [ALPHA, GAMMA, LAMBDA, MU]
    args[param_index] = bad_value
    with pytest.raises(ValueError):
        three_qubit_noncollinear_overlap_relation_state(*args)


# ---------------------------------------------------------------------------
# S13 — no silent repair of an out-of-domain parameter
# ---------------------------------------------------------------------------


def test_s13_state_out_of_domain_parameter_raises_without_returning_corrected_state():
    # Grossly outside the admissible domain: must raise, never return a
    # silently corrected/clipped/renormalized state.
    with pytest.raises(ValueError):
        three_qubit_noncollinear_overlap_relation_state(5.0, 5.0, 5.0, 5.0)
