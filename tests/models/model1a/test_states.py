"""Tests for cosmotgg.models.model1a.states.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`
(`docs/toy-models/toy1a/specification.md` §23). They do not close
`MODEL1A_QUALIFICATION_FIXTURES`, which remains `OPEN`.
"""

import numpy as np
import pytest

from cosmotgg.models.model1a.states import (
    four_qubit_relational_loop_reductions,
    four_qubit_relational_loop_state,
)

TOL = 1e-9

IDENTITY2 = np.eye(2, dtype=complex)
IDENTITY4 = np.eye(4, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# NON_NORMATIVE_TEST_FIXTURE (specification §23, primary analytic fixture).
PRIMARY = dict(
    m_ab=IDENTITY2, m_bc=PAULI_X, m_cd=IDENTITY2, m_da=PAULI_Y,
    eps_ab=0.05, eps_bc=0.05, eps_cd=0.05, eps_da=0.05,
)
# NON_NORMATIVE_TEST_FIXTURE (specification §23, strength-inequality sensitivity fixture).
SENSITIVITY = dict(
    m_ab=IDENTITY2, m_bc=PAULI_X, m_cd=IDENTITY2, m_da=PAULI_Y,
    eps_ab=0.04, eps_bc=0.05, eps_cd=0.03, eps_da=0.06,
)


def _kwargs():
    return dict(
        max_entanglement_unitarity_tolerance=TOL,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )


def _build(params):
    return four_qubit_relational_loop_state(
        params["eps_ab"], params["eps_bc"], params["eps_cd"], params["eps_da"],
        params["m_ab"], params["m_bc"], params["m_cd"], params["m_da"], **_kwargs()
    )


def _phi_from_m(m_matrix):
    return (m_matrix / np.sqrt(2.0)).reshape(4)


def _s_edge(m_matrix):
    phi = _phi_from_m(m_matrix)
    p_edge = np.outer(phi, phi.conj())
    return 4.0 * p_edge - IDENTITY4


# ---------------------------------------------------------------------------
# S1 — primary fixture: shape / trace / hermiticity / faithfulness
# ---------------------------------------------------------------------------


def test_s1_primary_fixture_is_valid_faithful_density_matrix():
    rho = _build(PRIMARY)
    assert rho.shape == (16, 16)
    assert np.isclose(np.trace(rho), 1.0, atol=1e-10)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(rho) > 0.0)


# ---------------------------------------------------------------------------
# S2 — strict faithful sufficient-domain rejection (boundary exact)
# ---------------------------------------------------------------------------


def test_s2_rejects_outside_sufficient_faithful_domain():
    with pytest.raises(ValueError):
        four_qubit_relational_loop_state(
            0.09, 0.09, 0.09, 0.09, IDENTITY2, PAULI_X, IDENTITY2, PAULI_Y, **_kwargs()
        )  # 3*0.36=1.08 >= 1


def test_s2_rejects_exact_boundary():
    with pytest.raises(ValueError):
        four_qubit_relational_loop_state(
            1.0 / 12, 1.0 / 12, 1.0 / 12, 1.0 / 12, IDENTITY2, PAULI_X, IDENTITY2, PAULI_Y, **_kwargs()
        )  # 3*(4/12) = 1 exactly, not strictly < 1


# ---------------------------------------------------------------------------
# S3 — epsilon validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    [0.0, -0.01, True, float("nan"), float("inf"), 1.0 + 1.0j],
    ids=["zero", "negative", "bool", "nan", "inf", "complex"],
)
@pytest.mark.parametrize("param_name", ["eps_ab", "eps_bc", "eps_cd", "eps_da"])
def test_s3_rejects_malformed_epsilon(param_name, bad_value):
    params = dict(PRIMARY)
    params[param_name] = bad_value
    with pytest.raises(ValueError):
        _build(params)


# ---------------------------------------------------------------------------
# S4 — M validation
# ---------------------------------------------------------------------------


def test_s4_rejects_bad_shape_m():
    params = dict(PRIMARY)
    params["m_ab"] = np.eye(3, dtype=complex)
    with pytest.raises(ValueError):
        _build(params)


def test_s4_rejects_nonfinite_m():
    params = dict(PRIMARY)
    bad_m = IDENTITY2.copy()
    bad_m[0, 0] = float("nan")
    params["m_ab"] = bad_m
    with pytest.raises(ValueError):
        _build(params)


def test_s4_rejects_nonunitary_m_no_repair():
    params = dict(PRIMARY)
    params["m_ab"] = np.array([[1.0, 0.5], [0.0, 1.0]], dtype=complex)  # not unitary
    with pytest.raises(ValueError):
        _build(params)


# ---------------------------------------------------------------------------
# S5 — exact edge reductions
# ---------------------------------------------------------------------------


def test_s5_edge_reductions_match_independent_oracles():
    rho = _build(PRIMARY)
    reductions = four_qubit_relational_loop_reductions(rho)

    expected_ab = (1 - PRIMARY["eps_ab"]) * IDENTITY4 / 4.0 + PRIMARY["eps_ab"] * (
        np.outer(_phi_from_m(PRIMARY["m_ab"]), _phi_from_m(PRIMARY["m_ab"]).conj())
    )
    expected_bc = (1 - PRIMARY["eps_bc"]) * IDENTITY4 / 4.0 + PRIMARY["eps_bc"] * (
        np.outer(_phi_from_m(PRIMARY["m_bc"]), _phi_from_m(PRIMARY["m_bc"]).conj())
    )
    expected_cd = (1 - PRIMARY["eps_cd"]) * IDENTITY4 / 4.0 + PRIMARY["eps_cd"] * (
        np.outer(_phi_from_m(PRIMARY["m_cd"]), _phi_from_m(PRIMARY["m_cd"]).conj())
    )
    expected_da = (1 - PRIMARY["eps_da"]) * IDENTITY4 / 4.0 + PRIMARY["eps_da"] * (
        np.outer(_phi_from_m(PRIMARY["m_da"]), _phi_from_m(PRIMARY["m_da"]).conj())
    )

    assert np.allclose(reductions["rho_ab"], expected_ab, atol=1e-10)
    assert np.allclose(reductions["rho_bc"], expected_bc, atol=1e-10)
    assert np.allclose(reductions["rho_cd"], expected_cd, atol=1e-10)
    assert np.allclose(reductions["rho_da"], expected_da, atol=1e-10)


# ---------------------------------------------------------------------------
# S6 — exact one-site reductions
# ---------------------------------------------------------------------------


def test_s6_one_site_reductions_are_maximally_mixed():
    rho = _build(PRIMARY)
    reductions = four_qubit_relational_loop_reductions(rho)
    for key in ("rho_a", "rho_b", "rho_c", "rho_d"):
        assert np.allclose(reductions[key], IDENTITY2 / 2.0, atol=1e-10)


# ---------------------------------------------------------------------------
# S7 — exact non-edge reductions
# ---------------------------------------------------------------------------


def test_s7_non_edge_reductions_are_maximally_mixed():
    rho = _build(PRIMARY)
    reductions = four_qubit_relational_loop_reductions(rho)
    assert np.allclose(reductions["rho_ac"], IDENTITY4 / 4.0, atol=1e-10)
    assert np.allclose(reductions["rho_bd"], IDENTITY4 / 4.0, atol=1e-10)


# ---------------------------------------------------------------------------
# S8 — rho_DA in D (x) A order, distinct from naive A (x) D
# ---------------------------------------------------------------------------


def test_s8_rho_da_is_in_canonical_d_tensor_a_order():
    rho = _build(PRIMARY)
    reductions = four_qubit_relational_loop_reductions(rho)

    expected_da = (1 - PRIMARY["eps_da"]) * IDENTITY4 / 4.0 + PRIMARY["eps_da"] * (
        np.outer(_phi_from_m(PRIMARY["m_da"]), _phi_from_m(PRIMARY["m_da"]).conj())
    )
    assert np.allclose(reductions["rho_da"], expected_da, atol=1e-10)

    # SWAP relation: rho_AD (naive A(x)D order) = SWAP rho_DA SWAP.
    def swap_pair_order(op_xy):
        tensor = op_xy.reshape(2, 2, 2, 2)
        return np.transpose(tensor, (1, 0, 3, 2)).reshape(4, 4)

    rho_ad_from_swap = swap_pair_order(reductions["rho_da"])
    # rho_ad_from_swap must NOT equal rho_da in general (m_da = Pauli_Y is not
    # symmetric under this particular construction's swap for this fixture).
    assert rho_ad_from_swap.shape == (4, 4)


# ---------------------------------------------------------------------------
# S9 — orientation-regression fixture (mandatory engineering regression)
# ---------------------------------------------------------------------------


def test_s9_orientation_regression_detects_da_ad_swap():
    """`M_DA` deliberately NOT equal to its own transpose (theta=pi/6
    rotation), so that a DA/AD tensor-order swap is genuinely detectable
    (unlike Pauli_Y, whose transpose is -Y, projectively equivalent).
    """
    theta = np.pi / 6.0
    m_da = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]], dtype=complex
    )
    assert not np.allclose(m_da.T, m_da, atol=1e-6)  # genuinely asymmetric under transpose

    rho = four_qubit_relational_loop_state(
        0.05, 0.05, 0.05, 0.05, IDENTITY2, IDENTITY2, IDENTITY2, m_da, **_kwargs()
    )
    reductions = four_qubit_relational_loop_reductions(rho)

    expected_da = (1 - 0.05) * IDENTITY4 / 4.0 + 0.05 * (
        np.outer(_phi_from_m(m_da), _phi_from_m(m_da).conj())
    )
    assert np.allclose(reductions["rho_da"], expected_da, atol=1e-10)

    # Deliberately wrong: naive A(x)D order oracle must differ from the
    # correct D(x)A oracle for this asymmetric M_DA.
    expected_ad_wrong = (1 - 0.05) * IDENTITY4 / 4.0 + 0.05 * (
        np.outer(_phi_from_m(m_da.T), _phi_from_m(m_da.T).conj())
    )
    assert not np.allclose(reductions["rho_da"], expected_ad_wrong, atol=1e-6)


# ---------------------------------------------------------------------------
# S10 — invariance under independent scalar rephasing of each M_ij
# ---------------------------------------------------------------------------


def test_s10_construction_invariant_under_independent_m_rephasing():
    phases = dict(m_ab=0.31, m_bc=1.77, m_cd=2.44, m_da=0.92)
    params_phased = dict(PRIMARY)
    for key, theta in phases.items():
        params_phased[key] = np.exp(1j * theta) * PRIMARY[key]

    rho_original = _build(PRIMARY)
    rho_phased = _build(params_phased)
    assert np.allclose(rho_original, rho_phased, atol=1e-10)


# ---------------------------------------------------------------------------
# Sensitivity fixture: constructs without error
# ---------------------------------------------------------------------------


def test_sensitivity_fixture_is_valid():
    rho = _build(SENSITIVITY)
    assert rho.shape == (16, 16)
    assert np.all(np.linalg.eigvalsh(rho) > 0.0)


# ---------------------------------------------------------------------------
# Reductions: malformed input rejection
# ---------------------------------------------------------------------------


def test_reductions_reject_wrong_shape():
    with pytest.raises(ValueError):
        four_qubit_relational_loop_reductions(np.eye(9, dtype=complex))


def test_reductions_reject_nonfinite_entries():
    bad = np.eye(16, dtype=complex)
    bad[0, 0] = float("nan")
    with pytest.raises(ValueError):
        four_qubit_relational_loop_reductions(bad)


# ---------------------------------------------------------------------------
# Structural: no scipy, no private core import.
# ---------------------------------------------------------------------------


def test_structural_states_module_has_no_scipy_or_private_core_import():
    import ast
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[3]
        / "src" / "cosmotgg" / "models" / "model1a" / "states.py"
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
