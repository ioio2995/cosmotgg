"""Model-free unit tests for cosmotgg.core.modular."""

import numpy as np
import pytest

from cosmotgg.core.information import log_density_difference
from cosmotgg.core.modular import (
    finite_connes_cocycle,
    hermitian_log,
    modular_flow,
    modular_hamiltonian,
)

TOL = 1e-9


def _cocycle_kwargs():
    return dict(
        hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )


def _noncommuting_faithful_pair():
    """A fixed, small, faithful pair `(rho, sigma)` with `[rho, sigma] != 0`.

    Used as a shared fixture across several `finite_connes_cocycle` tests
    (unitarity, intertwining, cocycle identity, chain rule, inverse,
    tangent regression). Not a model0a canonical state: purely a test-only
    numerical example.
    """
    rho = np.array([[0.5, 0.3], [0.3, 0.5]], dtype=complex)
    sigma = np.array([[0.6, 0.1 - 0.1j], [0.1 + 0.1j, 0.4]], dtype=complex)
    return rho, sigma


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


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C1: s = 0
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_at_s_zero_is_identity():
    rho, sigma = _noncommuting_faithful_pair()
    result = finite_connes_cocycle(rho, sigma, 0.0, **_cocycle_kwargs())
    assert np.allclose(result, np.eye(2))


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C2: unitarity
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_is_unitary_for_noncommuting_pair():
    rho, sigma = _noncommuting_faithful_pair()
    s = 0.4
    v_s = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())
    assert np.allclose(v_s @ v_s.conj().T, np.eye(2), atol=1e-10)
    assert np.allclose(v_s.conj().T @ v_s, np.eye(2), atol=1e-10)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C3: sign convention (explicit diagonal phases)
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_sign_convention_on_diagonal_pair():
    rho = np.diag([0.7, 0.3]).astype(complex)
    sigma = np.diag([0.4, 0.6]).astype(complex)
    s = 0.5

    result = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())

    # v_s = rho^(-is) sigma^(+is): for diagonal rho, sigma, entry k is
    # rho_k^(-is) * sigma_k^(+is) = exp(is (ln sigma_k - ln rho_k)).
    rho_eigvals = np.array([0.7, 0.3])
    sigma_eigvals = np.array([0.4, 0.6])
    expected_diag = np.exp(1j * s * (np.log(sigma_eigvals) - np.log(rho_eigvals)))
    expected = np.diag(expected_diag)
    assert np.allclose(result, expected)

    # The inverted sign convention (rho^(+is) sigma^(-is)) must NOT match.
    inverted_diag = np.exp(-1j * s * (np.log(sigma_eigvals) - np.log(rho_eigvals)))
    inverted = np.diag(inverted_diag)
    assert not np.allclose(result, inverted)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C4: intertwining
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_intertwining():
    rho, sigma = _noncommuting_faithful_pair()
    s = 0.4
    o = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    k_rho = modular_hamiltonian(rho, **_cocycle_kwargs())
    k_sigma = modular_hamiltonian(sigma, **_cocycle_kwargs())
    v_s = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())

    lhs = (
        v_s
        @ modular_flow(o, k_sigma, s, hermiticity_tolerance=TOL)
        @ v_s.conj().T
    )
    rhs = modular_flow(o, k_rho, s, hermiticity_tolerance=TOL)

    assert np.allclose(lhs, rhs, atol=1e-10)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C5: cocycle identity
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_cocycle_identity():
    rho, sigma = _noncommuting_faithful_pair()
    s, s_prime = 0.4, 0.7

    k_sigma = modular_hamiltonian(sigma, **_cocycle_kwargs())
    v_s = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())
    v_s_prime = finite_connes_cocycle(rho, sigma, s_prime, **_cocycle_kwargs())
    v_combined = finite_connes_cocycle(rho, sigma, s + s_prime, **_cocycle_kwargs())

    flowed_v_s_prime = modular_flow(v_s_prime, k_sigma, s, hermiticity_tolerance=TOL)
    rhs = v_s @ flowed_v_s_prime

    assert np.allclose(v_combined, rhs, atol=1e-10)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C6: chain rule
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_chain_rule():
    rho, sigma = _noncommuting_faithful_pair()
    omega = np.array(
        [[0.55, -0.05 + 0.15j], [-0.05 - 0.15j, 0.45]], dtype=complex
    )
    s = 0.4

    v_rho_sigma = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())
    v_sigma_omega = finite_connes_cocycle(sigma, omega, s, **_cocycle_kwargs())
    v_rho_omega = finite_connes_cocycle(rho, omega, s, **_cocycle_kwargs())

    assert np.allclose(v_rho_sigma @ v_sigma_omega, v_rho_omega, atol=1e-10)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C7: inverse / reference swap
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_inverse_reference_swap():
    rho, sigma = _noncommuting_faithful_pair()
    s = 0.4

    v_rho_sigma = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())
    v_sigma_rho = finite_connes_cocycle(sigma, rho, s, **_cocycle_kwargs())

    assert np.allclose(v_sigma_rho, v_rho_sigma.conj().T, atol=1e-10)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C8: commuting case, closed form
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_matches_closed_form_when_commuting():
    rho = np.diag([0.7, 0.3]).astype(complex)
    sigma = np.diag([0.4, 0.6]).astype(complex)
    s = 0.6
    assert np.allclose(rho @ sigma, sigma @ rho)

    result = finite_connes_cocycle(rho, sigma, s, **_cocycle_kwargs())

    r_ab = log_density_difference(rho, sigma, **_cocycle_kwargs())
    # rho and sigma commute (both diagonal), so r_ab = log(rho) - log(sigma)
    # is diagonal too. Build exp(-i s r_ab) directly from its diagonal
    # entries with plain numpy, independently of finite_connes_cocycle's
    # and modular_flow's internal spectral machinery.
    diag_r_ab = np.diagonal(r_ab)
    expected = np.diag(np.exp(-1j * s * diag_r_ab))

    assert np.allclose(result, expected)


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C9: tangent at s = 0 (engineering regression only)
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_tangent_at_zero_matches_generator_regression():
    """Numerical regression check of `dv_s/ds|_0 = -i (log(rho) - log(sigma))`.

    `FINITE_DIFFERENCE_STEP` and `REGRESSION_TOLERANCE` below are
    engineering-only parameters of this specific numerical regression test.
    They are NOT a production tolerance of `cosmotgg.core`, NOT a model0a
    scientific acceptance criterion, and NOT a T1 threshold; they carry no
    normative status outside this test.
    """
    FINITE_DIFFERENCE_STEP = 1e-4
    REGRESSION_TOLERANCE = 1e-6

    rho, sigma = _noncommuting_faithful_pair()

    plus = finite_connes_cocycle(rho, sigma, FINITE_DIFFERENCE_STEP, **_cocycle_kwargs())
    minus = finite_connes_cocycle(rho, sigma, -FINITE_DIFFERENCE_STEP, **_cocycle_kwargs())
    numerical_derivative = (plus - minus) / (2 * FINITE_DIFFERENCE_STEP)

    r_ab = log_density_difference(rho, sigma, **_cocycle_kwargs())
    analytic_derivative = -1j * r_ab

    assert np.allclose(
        numerical_derivative, analytic_derivative, atol=REGRESSION_TOLERANCE
    )


# ---------------------------------------------------------------------------
# finite_connes_cocycle — C10: fail-closed input validation
# ---------------------------------------------------------------------------


def test_finite_connes_cocycle_rejects_non_faithful_rho():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    sigma = np.diag([0.5, 0.5]).astype(complex)
    with pytest.raises(ValueError):
        finite_connes_cocycle(rho, sigma, 0.3, **_cocycle_kwargs())


def test_finite_connes_cocycle_rejects_non_faithful_sigma():
    rho = np.diag([0.5, 0.5]).astype(complex)
    sigma = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        finite_connes_cocycle(rho, sigma, 0.3, **_cocycle_kwargs())


def test_finite_connes_cocycle_rejects_incompatible_dimensions():
    rho = np.diag([0.6, 0.4]).astype(complex)
    sigma = np.diag([0.5, 0.3, 0.2]).astype(complex)
    with pytest.raises(ValueError):
        finite_connes_cocycle(rho, sigma, 0.3, **_cocycle_kwargs())


@pytest.mark.parametrize(
    "bad_s",
    [1.0 + 1.0j, float("nan"), float("inf"), float("-inf"), np.array([0.1, 0.2])],
    ids=["complex", "nan", "inf", "-inf", "non-scalar"],
)
def test_finite_connes_cocycle_rejects_bad_s(bad_s):
    rho, sigma = _noncommuting_faithful_pair()
    with pytest.raises(ValueError):
        finite_connes_cocycle(rho, sigma, bad_s, **_cocycle_kwargs())


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_finite_connes_cocycle_rejects_bad_hermiticity_tolerance(bad_tolerance):
    rho, sigma = _noncommuting_faithful_pair()
    with pytest.raises(ValueError):
        finite_connes_cocycle(
            rho,
            sigma,
            0.3,
            hermiticity_tolerance=bad_tolerance,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_finite_connes_cocycle_rejects_bad_trace_tolerance(bad_tolerance):
    rho, sigma = _noncommuting_faithful_pair()
    with pytest.raises(ValueError):
        finite_connes_cocycle(
            rho,
            sigma,
            0.3,
            hermiticity_tolerance=TOL,
            trace_tolerance=bad_tolerance,
            positivity_tolerance=TOL,
        )


@pytest.mark.parametrize("bad_tolerance", BAD_TOLERANCES, ids=["negative", "nan", "inf"])
def test_finite_connes_cocycle_rejects_bad_positivity_tolerance(bad_tolerance):
    rho, sigma = _noncommuting_faithful_pair()
    with pytest.raises(ValueError):
        finite_connes_cocycle(
            rho,
            sigma,
            0.3,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=bad_tolerance,
        )
