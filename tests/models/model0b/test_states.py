"""Tests for cosmotgg.models.model0b.states.

Fixture values used below (`beta`, `lambda_`, `mu`) are explicitly
`NON_NORMATIVE_TEST_FIXTURE`: purely internal-development numerical
examples, chosen strictly inside (or, for the negative controls,
strictly outside/on the boundary of) the analytic domain of
`docs/toy-models/toy0b/specification.md` §6. They are not
`BETA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` in the scientific sense of the
specification (§23), which remain `OPEN`.
"""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model0b.states import three_qubit_overlapping_pauli_relation_state

DIMENSIONS_ABC = (2, 2, 2)
DIMENSIONS_PAIR = (2, 2)

# NON_NORMATIVE_TEST_FIXTURE: interior admissible point used across
# several tests below. Not a model0b canonical/scientific parameter
# value.
BETA, LAMBDA, MU = 0.2, 0.3, 0.1

IDENTITY2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _oracle_state(beta, lam, mu):
    """Independent oracle for `rho_ABC(beta, lam, mu)` (spec §5).

    Built by direct enumeration of the computational basis `|abc>`
    (`a, b, c in {0, 1}`, index `4a + 2b + c`) and the explicit action
    of `Z_B`, `X_A X_B`, `Y_B Y_C` on each basis state, WITHOUT using
    `numpy.kron` on Pauli matrices: a computational path independent of
    the production construction in
    `cosmotgg.models.model0b.states.three_qubit_overlapping_pauli_relation_state`.

    `Z|b> = (-1)**b |b>`; `X` flips a bit; `Y|b> = 1j*(-1)**b |1-b>`
    (`Y|0>=1j|1>`, `Y|1>=-1j|0>`), so
    `(Y_B Y_C)|b,c> = -(-1)**(b+c) |1-b,1-c>`.
    """
    dim = 8
    rho = np.zeros((dim, dim), dtype=complex)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                i = 4 * a + 2 * b + c
                rho[i, i] += (1.0 + beta * (-1) ** b) / 8.0

                j_lambda = 4 * (1 - a) + 2 * (1 - b) + c
                rho[i, j_lambda] += lam / 8.0

                j_mu = 4 * a + 2 * (1 - b) + (1 - c)
                rho[i, j_mu] += -mu * (-1) ** (b + c) / 8.0
    return rho


# ---------------------------------------------------------------------------
# S1 — exact matrix against an independently constructed oracle
# ---------------------------------------------------------------------------


def test_s1_state_matches_independent_oracle():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    expected = _oracle_state(BETA, LAMBDA, MU)
    assert np.allclose(rho, expected)


# ---------------------------------------------------------------------------
# S2 — shape
# ---------------------------------------------------------------------------


def test_s2_state_shape_is_8x8():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    assert rho.shape == (8, 8)


# ---------------------------------------------------------------------------
# S3 — hermiticity (exact / numerical machine precision)
# ---------------------------------------------------------------------------


def test_s3_state_is_hermitian():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    assert np.allclose(rho, rho.conj().T, atol=1e-12)


# ---------------------------------------------------------------------------
# S4 — trace == 1
# ---------------------------------------------------------------------------


def test_s4_state_trace_is_one():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    assert np.isclose(np.trace(rho), 1.0)


# ---------------------------------------------------------------------------
# S5 — faithfulness of an interior fixture, checked directly via eigvalsh
# ---------------------------------------------------------------------------


def test_s5_state_interior_fixture_has_strictly_positive_spectrum():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > 0.0)


# ---------------------------------------------------------------------------
# S6 — analytic spectrum: (1+r)/8 x4, (1-r)/8 x4
# ---------------------------------------------------------------------------


def test_s6_state_spectrum_matches_analytic_formula():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    eigvals = np.sort(np.linalg.eigvalsh(rho))

    r = np.sqrt(BETA**2 + LAMBDA**2 + MU**2)
    expected = np.sort(np.array([(1.0 - r) / 8.0] * 4 + [(1.0 + r) / 8.0] * 4))

    assert np.allclose(eigvals, expected, atol=1e-12)


# ---------------------------------------------------------------------------
# S7 — reduced states against the analytic formulas of specification.md §7
# ---------------------------------------------------------------------------


def test_s7_reduced_state_rho_ab_matches_analytic_formula():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    rho_ab = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[0, 1])

    x_a_x_b = np.kron(PAULI_X, PAULI_X)
    z_b = np.kron(IDENTITY2, PAULI_Z)
    expected = (np.eye(4, dtype=complex) + BETA * z_b + LAMBDA * x_a_x_b) / 4.0

    assert np.allclose(rho_ab, expected, atol=1e-12)


def test_s7_reduced_state_rho_bc_matches_analytic_formula():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    rho_bc = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1, 2])

    z_b = np.kron(PAULI_Z, IDENTITY2)
    pauli_y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    y_b_y_c = np.kron(pauli_y, pauli_y)
    expected = (np.eye(4, dtype=complex) + BETA * z_b + MU * y_b_y_c) / 4.0

    assert np.allclose(rho_bc, expected, atol=1e-12)


def test_s7_reduced_state_rho_b_matches_analytic_formula():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    rho_b = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[1])

    expected = (IDENTITY2 + BETA * PAULI_Z) / 2.0

    assert np.allclose(rho_b, expected, atol=1e-12)


def test_s7_reduced_state_rho_a_is_maximally_mixed():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[0])
    assert np.allclose(rho_a, IDENTITY2 / 2.0, atol=1e-12)


def test_s7_reduced_state_rho_c_is_maximally_mixed():
    rho = three_qubit_overlapping_pauli_relation_state(BETA, LAMBDA, MU)
    rho_c = partial_trace(rho, dimensions=DIMENSIONS_ABC, keep=[2])
    assert np.allclose(rho_c, IDENTITY2 / 2.0, atol=1e-12)


# ---------------------------------------------------------------------------
# S8 — rejection at radius == 1 (boundary, no tolerance)
# ---------------------------------------------------------------------------


def test_s8_state_rejects_radius_equal_to_one():
    # 0.6**2 + 0.8**2 + 0.0**2 == 1.0 exactly.
    with pytest.raises(ValueError):
        three_qubit_overlapping_pauli_relation_state(0.6, 0.8, 0.0)


# ---------------------------------------------------------------------------
# S9 — rejection at radius > 1
# ---------------------------------------------------------------------------


def test_s9_state_rejects_radius_greater_than_one():
    with pytest.raises(ValueError):
        three_qubit_overlapping_pauli_relation_state(1.1, 0.0, 0.0)


# ---------------------------------------------------------------------------
# S10 — fail-closed input types (parametrized across beta, lambda_, mu)
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


@pytest.mark.parametrize("param_index", [0, 1, 2], ids=["beta", "lambda_", "mu"])
@pytest.mark.parametrize("bad_value", BAD_PARAMETER_VALUES, ids=BAD_PARAMETER_IDS)
def test_s10_state_rejects_bad_parameter_types(param_index, bad_value):
    args = [BETA, LAMBDA, MU]
    args[param_index] = bad_value
    with pytest.raises(ValueError):
        three_qubit_overlapping_pauli_relation_state(*args)


# ---------------------------------------------------------------------------
# S11 — no silent repair of an out-of-domain parameter
# ---------------------------------------------------------------------------


def test_s11_state_out_of_domain_parameter_raises_without_returning_corrected_state():
    # Grossly outside the admissible domain: must raise, never return a
    # silently corrected/clipped/renormalized state.
    with pytest.raises(ValueError):
        three_qubit_overlapping_pauli_relation_state(5.0, 5.0, 5.0)
