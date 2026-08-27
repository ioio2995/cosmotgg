"""Tests for cosmotgg.models.model0e.states.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`
(`docs/toy-models/toy0e/specification.md` §34): purely
internal-development numerical examples. They do not close
`MODEL0E_QUALIFICATION_FIXTURES`, which remains `OPEN`.

Independent analytic oracles (`_phi3_oracle`, reduction oracles below)
reproduce the closed-form formulas of `docs/toy-models/toy0e/
specification.md` §6-§9 directly, without importing any private
constant of `cosmotgg.models.model0e.states`.
"""

import numpy as np
import pytest

from cosmotgg.models.model0e.states import (
    four_partite_discrete_multimodular_reductions,
    four_partite_discrete_multimodular_reference_state,
)

TOL = 1e-9

IDENTITY2 = np.eye(2, dtype=complex)
IDENTITY3 = np.eye(3, dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# NON_NORMATIVE_TEST_FIXTURE (specification §34, primary symmetric fixture).
MAIN = dict(eta=0.02, gamma=0.10, mu_a=0.10, mu_b=0.10, delta=0.20, nu_a=0.05, nu_b=0.05)
# NON_NORMATIVE_TEST_FIXTURE (specification §34, amplitude-asymmetric fixture).
ASYM = dict(eta=0.02, gamma=0.10, mu_a=0.08, mu_b=0.12, delta=0.20, nu_a=0.04, nu_b=0.06)


def _kwargs():
    return dict(hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


def _oracle_q():
    q0 = np.ones(3, dtype=complex) / np.sqrt(3.0)
    return np.outer(q0, q0.conj()) - IDENTITY3 / 3.0


def _oracle_n():
    return np.diag([-1.0, 0.0, 1.0]).astype(complex)


def _oracle_phi3():
    phi3 = np.zeros(9, dtype=complex)
    for i in range(3):
        phi3[i * 3 + i] = 1.0 / np.sqrt(3.0)
    return phi3


def _build(params):
    return four_partite_discrete_multimodular_reference_state(
        params["eta"], params["gamma"], params["mu_a"], params["mu_b"],
        params["delta"], params["nu_a"], params["nu_b"], **_kwargs()
    )


# ---------------------------------------------------------------------------
# S1 — shape / trace / hermiticity / faithfulness
# ---------------------------------------------------------------------------


def test_s1_state_is_valid_faithful_density_matrix():
    rho = _build(MAIN)
    assert rho.shape == (36, 36)
    assert np.isclose(np.trace(rho), 1.0, atol=1e-10)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(rho) > 0.0)


# ---------------------------------------------------------------------------
# S2 — sufficient faithful-domain strict rejection
# ---------------------------------------------------------------------------


def test_s2_rejects_outside_sufficient_faithful_domain():
    # 8*eta alone exceeds 1: bound violated even though branch conditions hold.
    with pytest.raises(ValueError):
        four_partite_discrete_multimodular_reference_state(
            0.20, 0.10, 0.10, 0.10, 0.20, 0.05, 0.05, **_kwargs()
        )


# ---------------------------------------------------------------------------
# S3 — branch-condition rejection (exact, no tolerance)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "override",
    [
        dict(eta=0.0),
        dict(eta=-0.01),
        dict(gamma=-0.01),
        dict(mu_a=0.0),
        dict(mu_a=-0.01),
        dict(mu_b=0.0),
        dict(mu_b=-0.01),
        dict(delta=0.0),
        dict(delta=-0.01),
        dict(nu_a=0.0),
        dict(nu_a=-0.01),
        dict(nu_a=0.20),  # nu_a == delta, must be strictly less
        dict(nu_a=0.25),  # nu_a > delta
        dict(nu_b=0.0),
        dict(nu_b=-0.01),
        dict(nu_b=0.20),
        dict(nu_b=0.25),
    ],
    ids=[
        "eta=0", "eta<0", "gamma<0", "mu_a=0", "mu_a<0", "mu_b=0", "mu_b<0",
        "delta=0", "delta<0", "nu_a=0", "nu_a<0", "nu_a=delta", "nu_a>delta",
        "nu_b=0", "nu_b<0", "nu_b=delta", "nu_b>delta",
    ],
)
def test_s3_rejects_branch_condition_violations(override):
    params = dict(MAIN)
    params.update(override)
    with pytest.raises(ValueError):
        _build(params)


# ---------------------------------------------------------------------------
# S4 — exact rho_AB oracle
# ---------------------------------------------------------------------------


def test_s4_rho_ab_matches_independent_oracle():
    rho = _build(MAIN)
    reductions = four_partite_discrete_multimodular_reductions(rho)
    phi3 = _oracle_phi3()
    p_phi = np.outer(phi3, phi3.conj())
    expected = (1 - MAIN["eta"]) / 9.0 * np.eye(9, dtype=complex) + MAIN["eta"] * p_phi
    assert np.allclose(reductions["rho_ab"], expected, atol=1e-10)


# ---------------------------------------------------------------------------
# S5 — rho_A = rho_B = I/3
# ---------------------------------------------------------------------------


def test_s5_marginals_are_maximally_mixed():
    rho = _build(MAIN)
    reductions = four_partite_discrete_multimodular_reductions(rho)
    assert np.allclose(reductions["rho_a"], IDENTITY3 / 3.0, atol=1e-10)
    assert np.allclose(reductions["rho_b"], IDENTITY3 / 3.0, atol=1e-10)


# ---------------------------------------------------------------------------
# S6 — exact rho_AC / rho_AD / rho_BC / rho_BD oracles
# ---------------------------------------------------------------------------


def test_s6_context_reductions_match_independent_oracles():
    rho = _build(MAIN)
    reductions = four_partite_discrete_multimodular_reductions(rho)
    q = _oracle_q()
    n = _oracle_n()

    expected_ac = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + MAIN["gamma"] * np.kron(IDENTITY3, PAULI_Z)
        + MAIN["mu_a"] * np.kron(q, PAULI_Z)
    )
    expected_ad = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + MAIN["delta"] * np.kron(IDENTITY3, PAULI_Z)
        + MAIN["nu_a"] * np.kron(n, PAULI_Z)
    )
    expected_bc = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + MAIN["gamma"] * np.kron(IDENTITY3, PAULI_Z)
        + MAIN["mu_b"] * np.kron(q, PAULI_Z)
    )
    expected_bd = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + MAIN["delta"] * np.kron(IDENTITY3, PAULI_Z)
        + MAIN["nu_b"] * np.kron(n, PAULI_Z)
    )

    assert np.allclose(reductions["rho_ac"], expected_ac, atol=1e-10)
    assert np.allclose(reductions["rho_ad"], expected_ad, atol=1e-10)
    assert np.allclose(reductions["rho_bc"], expected_bc, atol=1e-10)
    assert np.allclose(reductions["rho_bd"], expected_bd, atol=1e-10)


# ---------------------------------------------------------------------------
# S7 — amplitude-asymmetric family valid
# ---------------------------------------------------------------------------


def test_s7_amplitude_asymmetric_family_is_valid():
    rho = _build(ASYM)
    assert rho.shape == (36, 36)
    assert np.isclose(np.trace(rho), 1.0, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(rho) > 0.0)


# ---------------------------------------------------------------------------
# S8 — malformed / nonfinite / bool parameter rejection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    [float("nan"), float("inf"), float("-inf"), 1.0 + 1.0j, True, np.array([0.1, 0.2]), "0.1"],
    ids=["nan", "inf", "-inf", "complex", "bool", "non-scalar", "str"],
)
@pytest.mark.parametrize(
    "param_name", ["eta", "gamma", "mu_a", "mu_b", "delta", "nu_a", "nu_b"]
)
def test_s8_rejects_malformed_parameters(param_name, bad_value):
    params = dict(MAIN)
    params[param_name] = bad_value
    with pytest.raises(ValueError):
        _build(params)


# ---------------------------------------------------------------------------
# Reductions: malformed input rejection
# ---------------------------------------------------------------------------


def test_reductions_reject_wrong_shape():
    with pytest.raises(ValueError):
        four_partite_discrete_multimodular_reductions(np.eye(9, dtype=complex))


def test_reductions_reject_nonfinite_entries():
    bad = np.eye(36, dtype=complex)
    bad[0, 0] = float("nan")
    with pytest.raises(ValueError):
        four_partite_discrete_multimodular_reductions(bad)


# ---------------------------------------------------------------------------
# Structural: no scipy, no private core import, in this module's source.
# ---------------------------------------------------------------------------


def test_structural_states_module_has_no_scipy_or_private_core_import():
    import ast
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[3]
        / "src" / "cosmotgg" / "models" / "model0e" / "states.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "scipy" not in alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            assert "scipy" not in module
            if module.startswith("cosmotgg.core"):
                for alias in node.names:
                    assert not alias.name.startswith("_"), (
                        f"private core symbol imported: {module}.{alias.name}"
                    )
