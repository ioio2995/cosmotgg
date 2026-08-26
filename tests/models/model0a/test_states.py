"""Tests for cosmotgg.models.model0a.states.

Fixture values used below (`a`, `b`, `c`, `eta`) are explicitly
`NON_NORMATIVE_TEST_FIXTURE`: purely internal-development numerical
examples, chosen strictly inside the analytic domain of
`docs/toy-models/toy0a/specification.md` §3.2. They are not
`STATE_PARAMETER_VALUES` in the scientific sense of the specification
(§15), which remain `OPEN`.
"""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace, validate_density_matrix
from cosmotgg.models.model0a.states import two_qubit_fixed_marginal_correlation_state

DIMENSIONS = (2, 2)

# NON_NORMATIVE_TEST_FIXTURE: interior admissible point used across several
# tests below. Not a model0a canonical/scientific parameter value.
A, B, C, ETA = 0.3, 0.4, 0.02, 0.05


# ---------------------------------------------------------------------------
# S1 — shape / trace / hermiticity
# ---------------------------------------------------------------------------


def test_state_shape_trace_hermiticity():
    rho = two_qubit_fixed_marginal_correlation_state(A, B, C, ETA)
    assert rho.shape == (4, 4)
    assert np.isclose(np.trace(rho), 1.0)
    assert np.allclose(rho, rho.conj().T)


# ---------------------------------------------------------------------------
# S2 — marginals match the analytic formula
# ---------------------------------------------------------------------------


def test_state_marginals_match_analytic_formula():
    rho = two_qubit_fixed_marginal_correlation_state(A, B, C, ETA)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS, keep=[0])
    rho_b = partial_trace(rho, dimensions=DIMENSIONS, keep=[1])
    assert np.allclose(rho_a, np.diag([A, 1.0 - A]))
    assert np.allclose(rho_b, np.diag([B, 1.0 - B]))


# ---------------------------------------------------------------------------
# S3 — marginals (and sigma_AB) are fixed across c, eta at fixed a, b
# ---------------------------------------------------------------------------


def test_state_marginals_are_fixed_across_c_and_eta():
    rho_1 = two_qubit_fixed_marginal_correlation_state(A, B, 0.0, 0.0)
    rho_2 = two_qubit_fixed_marginal_correlation_state(A, B, C, ETA)

    rho_a_1 = partial_trace(rho_1, dimensions=DIMENSIONS, keep=[0])
    rho_b_1 = partial_trace(rho_1, dimensions=DIMENSIONS, keep=[1])
    rho_a_2 = partial_trace(rho_2, dimensions=DIMENSIONS, keep=[0])
    rho_b_2 = partial_trace(rho_2, dimensions=DIMENSIONS, keep=[1])

    assert np.allclose(rho_a_1, rho_a_2)
    assert np.allclose(rho_b_1, rho_b_2)
    assert np.allclose(np.kron(rho_a_1, rho_b_1), np.kron(rho_a_2, rho_b_2))


# ---------------------------------------------------------------------------
# S4 — N0 canonical slice: product state
# ---------------------------------------------------------------------------


def test_state_n0_slice_equals_product_of_marginals():
    rho = two_qubit_fixed_marginal_correlation_state(A, B, 0.0, 0.0)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS, keep=[0])
    rho_b = partial_trace(rho, dimensions=DIMENSIONS, keep=[1])
    sigma = np.kron(rho_a, rho_b)
    assert np.allclose(rho, sigma)


# ---------------------------------------------------------------------------
# S5 — N1 canonical slice: correlated, commuting
# ---------------------------------------------------------------------------


def test_state_n1_slice_is_correlated_and_commutes():
    rho = two_qubit_fixed_marginal_correlation_state(A, B, C, 0.0)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS, keep=[0])
    rho_b = partial_trace(rho, dimensions=DIMENSIONS, keep=[1])
    sigma = np.kron(rho_a, rho_b)

    assert not np.allclose(rho, sigma)
    # Commutation only (no T1 verdict is emitted here).
    assert np.allclose(rho @ sigma, sigma @ rho)


# ---------------------------------------------------------------------------
# S6 — N2 canonical slice: non-commuting, analytic commutator entry
# ---------------------------------------------------------------------------


def test_state_n2_slice_does_not_commute_and_matches_commutator_formula():
    # a + b = 0.7 != 1, required for the N2 canonical slice (spec §3.3).
    rho = two_qubit_fixed_marginal_correlation_state(A, B, C, ETA)
    rho_a = partial_trace(rho, dimensions=DIMENSIONS, keep=[0])
    rho_b = partial_trace(rho, dimensions=DIMENSIONS, keep=[1])
    sigma = np.kron(rho_a, rho_b)

    commutator = rho @ sigma - sigma @ rho
    assert not np.allclose(commutator, np.zeros((4, 4)))

    expected_entry = ETA * (1.0 - A - B)
    assert np.isclose(commutator[0, 3], expected_entry)
    assert np.isclose(commutator[3, 0], -expected_entry)


# ---------------------------------------------------------------------------
# S7 — faithfulness of an interior fixture
# ---------------------------------------------------------------------------


def test_state_interior_fixture_is_faithful():
    rho = two_qubit_fixed_marginal_correlation_state(A, B, C, ETA)

    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > 0.0)

    # Complementary check via the core validation primitive, with an
    # explicit NON_NORMATIVE_TEST_TOLERANCE: a development-only numerical
    # tolerance, not a model0a scientific value nor a protocol tolerance.
    NON_NORMATIVE_TEST_TOLERANCE = 1e-9
    validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        trace_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
        positivity_tolerance=NON_NORMATIVE_TEST_TOLERANCE,
    )


# ---------------------------------------------------------------------------
# S8 — bounds on a, b
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_a", [0.0, 1.0, -0.1, 1.1], ids=["=0", "=1", "<0", ">1"])
def test_state_rejects_a_out_of_bounds(bad_a):
    with pytest.raises(ValueError):
        two_qubit_fixed_marginal_correlation_state(bad_a, B, 0.0, 0.0)


@pytest.mark.parametrize("bad_b", [0.0, 1.0, -0.1, 1.1], ids=["=0", "=1", "<0", ">1"])
def test_state_rejects_b_out_of_bounds(bad_b):
    with pytest.raises(ValueError):
        two_qubit_fixed_marginal_correlation_state(A, bad_b, 0.0, 0.0)


# ---------------------------------------------------------------------------
# S9 — bounds on c (excluded boundaries)
# ---------------------------------------------------------------------------


def test_state_rejects_c_at_or_beyond_bounds():
    lower_c = -min(A * B, (1.0 - A) * (1.0 - B))
    upper_c = min(A * (1.0 - B), (1.0 - A) * B)

    for bad_c in (lower_c, lower_c - 0.01, upper_c, upper_c + 0.01):
        with pytest.raises(ValueError):
            two_qubit_fixed_marginal_correlation_state(A, B, bad_c, 0.0)


# ---------------------------------------------------------------------------
# S10 — bound on eta (excluded boundary)
# ---------------------------------------------------------------------------


def test_state_rejects_eta_at_or_beyond_bound():
    block_product = (A * B + C) * ((1.0 - A) * (1.0 - B) + C)
    boundary = np.sqrt(block_product)

    for bad_eta in (boundary, -boundary):
        with pytest.raises(ValueError):
            two_qubit_fixed_marginal_correlation_state(A, B, C, bad_eta)

    # A strictly interior value must be accepted.
    two_qubit_fixed_marginal_correlation_state(A, B, C, 0.9 * boundary)


# ---------------------------------------------------------------------------
# S11 — fail-closed input types (parametrized across a, b, c, eta)
# ---------------------------------------------------------------------------


BAD_PARAMETER_VALUES = [
    True,
    1.0 + 1.0j,
    float("nan"),
    float("inf"),
    float("-inf"),
    np.array([0.1, 0.2]),
]
BAD_PARAMETER_IDS = ["bool", "complex", "nan", "inf", "-inf", "non-scalar"]


@pytest.mark.parametrize("param_index", [0, 1, 2, 3], ids=["a", "b", "c", "eta"])
@pytest.mark.parametrize("bad_value", BAD_PARAMETER_VALUES, ids=BAD_PARAMETER_IDS)
def test_state_rejects_bad_parameter_types(param_index, bad_value):
    args = [A, B, C, ETA]
    args[param_index] = bad_value
    with pytest.raises(ValueError):
        two_qubit_fixed_marginal_correlation_state(*args)


# ---------------------------------------------------------------------------
# S12 — no silent normalization/repair of an out-of-domain parameter
# ---------------------------------------------------------------------------


def test_state_out_of_domain_parameter_raises_without_returning_corrected_state():
    # c grossly outside the admissible domain: must raise, never return a
    # silently corrected/clipped state.
    with pytest.raises(ValueError):
        two_qubit_fixed_marginal_correlation_state(A, B, 10.0, 0.0)
