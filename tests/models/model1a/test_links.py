"""Tests for cosmotgg.models.model1a.links.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`. F6/F7
below are off-contract negative controls built directly in this test
file (not through `four_qubit_relational_loop_state`), consistent with
`docs/toy-models/toy1a/specification.md` §26.
"""

import numpy as np
import pytest

from cosmotgg.models.model1a.states import (
    four_qubit_relational_loop_reductions,
    four_qubit_relational_loop_state,
)
from cosmotgg.models.model1a.links import (
    apply_directional_link,
    reverse_correlation_matrix,
    state_derived_centered_edge_transfer,
    state_derived_edge_link,
)

TOL = 1e-9
EDGE_SPECTRAL_TOL = 1e-9
UNITARITY_TOL = 1e-8

IDENTITY2 = np.eye(2, dtype=complex)
IDENTITY4 = np.eye(4, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

PRIMARY = dict(
    m_ab=IDENTITY2, m_bc=PAULI_X, m_cd=IDENTITY2, m_da=PAULI_Y,
    eps_ab=0.05, eps_bc=0.05, eps_cd=0.05, eps_da=0.05,
)


def _core_kwargs():
    return dict(
        max_entanglement_unitarity_tolerance=TOL,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )


def _link_kwargs():
    return dict(
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=TOL,
        edge_spectral_tolerance=EDGE_SPECTRAL_TOL,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )


def _reductions(params):
    rho = four_qubit_relational_loop_state(
        params["eps_ab"], params["eps_bc"], params["eps_cd"], params["eps_da"],
        params["m_ab"], params["m_bc"], params["m_cd"], params["m_da"], **_core_kwargs()
    )
    return four_qubit_relational_loop_reductions(rho)


# ---------------------------------------------------------------------------
# L1 — modular minimum projector == state maximum projector
# ---------------------------------------------------------------------------


def test_l1_modular_minimum_matches_state_maximum():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_ab"], **_link_kwargs())
    w, v = np.linalg.eigh(reductions["rho_ab"])
    expected_projector = np.outer(v[:, -1], v[:, -1].conj())
    assert np.allclose(link["modular_ground_projector"], expected_projector, atol=1e-8)


# ---------------------------------------------------------------------------
# L2 — lambda_plus / lambda_minus oracle
# ---------------------------------------------------------------------------


def test_l2_spectrum_matches_analytic_oracle():
    eps = PRIMARY["eps_ab"]
    reductions = _reductions(PRIMARY)
    eigvals = np.linalg.eigvalsh(reductions["rho_ab"])
    expected_plus = (1 + 3 * eps) / 4.0
    expected_minus = (1 - eps) / 4.0
    assert np.isclose(eigvals[-1], expected_plus, atol=1e-10)
    assert np.allclose(eigvals[:3], expected_minus, atol=1e-10)


# ---------------------------------------------------------------------------
# L3 — extracted strength == epsilon oracle
# ---------------------------------------------------------------------------


def test_l3_strength_matches_epsilon_oracle():
    reductions = _reductions(PRIMARY)
    for key, eps in (("rho_ab", PRIMARY["eps_ab"]), ("rho_bc", PRIMARY["eps_bc"]),
                     ("rho_cd", PRIMARY["eps_cd"]), ("rho_da", PRIMARY["eps_da"])):
        link = state_derived_edge_link(reductions[key], **_link_kwargs())
        assert np.isclose(link["strength"], eps, atol=1e-9)


# ---------------------------------------------------------------------------
# L4 — extracted M reconstructs the extremal projector
# ---------------------------------------------------------------------------


def test_l4_extracted_m_reconstructs_extremal_projector():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_matrix = link["correlation_matrix"]
    phi_from_m = (m_matrix / np.sqrt(2.0)).reshape(4)
    reconstructed_projector = np.outer(phi_from_m, phi_from_m.conj())
    assert np.allclose(reconstructed_projector, link["modular_ground_projector"], atol=1e-8)


# ---------------------------------------------------------------------------
# L5 — extracted M unitary
# ---------------------------------------------------------------------------


def test_l5_extracted_m_is_unitary():
    reductions = _reductions(PRIMARY)
    for key in ("rho_ab", "rho_bc", "rho_cd", "rho_da"):
        link = state_derived_edge_link(reductions[key], **_link_kwargs())
        m_matrix = link["correlation_matrix"]
        assert np.allclose(m_matrix.conj().T @ m_matrix, IDENTITY2, atol=1e-8)


# ---------------------------------------------------------------------------
# L6 — directional action preserves hermiticity / tracelessness / HS norm
# ---------------------------------------------------------------------------


def test_l6_directional_action_preserves_structure():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_matrix = link["correlation_matrix"]
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        out = apply_directional_link(
            m_matrix, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(out, out.conj().T, atol=1e-10)
        assert np.isclose(np.trace(out), 0.0, atol=1e-10)
        hs_norm_in = np.sqrt(np.trace(xi.conj().T @ xi).real)
        hs_norm_out = np.sqrt(np.trace(out.conj().T @ out).real)
        assert np.isclose(hs_norm_in, hs_norm_out, atol=1e-10)


# ---------------------------------------------------------------------------
# L7 — explicit transpose convention (discriminated via Pauli_Y)
# ---------------------------------------------------------------------------


def test_l7_transpose_convention_is_explicit_not_conjugate():
    """For ANY hermitian tangent X, `X.conj() == X.T` identically (that IS
    hermiticity: `X^dagger = X` <=> `X.conj().T = X` <=> `X.conj() = X.T`).
    So `M @ X.T @ M^dagger` and `M @ X.conj() @ M^dagger` can never be
    discriminated by any hermitian `X`/unitary `M` choice — the mandate's
    warning is precisely that this numerical coincidence must not be
    mistaken for "the transpose doesn't matter". What DOES need to be
    verified explicitly is that the transpose is actually applied at all
    (as opposed to an implementation bug that silently drops it): for
    `Pauli_Y`, `Y.T = -Y != Y`, so `M @ Y.T @ M^dagger` and a (deliberately
    wrong) `M @ Y @ M^dagger` (no transpose) are genuinely different.
    """
    m_complex = np.diag([1.0, 1j]).astype(complex)  # unitary, complex, non-real

    out = apply_directional_link(
        m_complex, PAULI_Y, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    expected_correct = m_complex @ PAULI_Y.T @ m_complex.conj().T
    expected_conjugate_equivalent = m_complex @ PAULI_Y.conj() @ m_complex.conj().T
    expected_missing_transpose = m_complex @ PAULI_Y @ m_complex.conj().T  # deliberately WRONG

    assert np.allclose(out, expected_correct, atol=1e-12)
    # X.conj() == X.T identically for hermitian X: this is expected, not a
    # discriminator (recorded explicitly, not silently assumed elsewhere).
    assert np.allclose(expected_correct, expected_conjugate_equivalent, atol=1e-12)
    # The genuine discriminator: omitting the transpose entirely changes
    # the result for Y (Y.T = -Y != Y).
    assert not np.allclose(out, expected_missing_transpose, atol=1e-6)


# ---------------------------------------------------------------------------
# L8 — reverse M_ji = M_ij^T
# ---------------------------------------------------------------------------


def test_l8_reverse_link_is_transpose():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_bc = link["correlation_matrix"]
    m_cb = reverse_correlation_matrix(m_bc, max_entanglement_unitarity_tolerance=UNITARITY_TOL)
    assert np.allclose(m_cb, m_bc.T, atol=1e-12)


# ---------------------------------------------------------------------------
# L9 — U_reverse o U_forward = identity
# ---------------------------------------------------------------------------


def test_l9_reverse_composition_is_identity():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_bc = link["correlation_matrix"]
    m_cb = reverse_correlation_matrix(m_bc, max_entanglement_unitarity_tolerance=UNITARITY_TOL)
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        forward = apply_directional_link(
            m_bc, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        back = apply_directional_link(
            m_cb, forward, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(back, xi, atol=1e-8)


# ---------------------------------------------------------------------------
# L10 — centered edge transfer == strength * directional action
# ---------------------------------------------------------------------------


def test_l10_centered_transfer_equals_strength_times_action():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_bc = link["correlation_matrix"]
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        transferred = state_derived_centered_edge_transfer(
            reductions["rho_bc"], xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )
        action = apply_directional_link(
            m_bc, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(transferred, link["strength"] * action, atol=1e-9)


# ---------------------------------------------------------------------------
# F4 — arbitrary rephasing leaves projective/directional action unchanged
# ---------------------------------------------------------------------------


def test_f4_rephasing_leaves_directional_action_unchanged():
    reductions = _reductions(PRIMARY)
    link = state_derived_edge_link(reductions["rho_bc"], **_link_kwargs())
    m_bc = link["correlation_matrix"]
    m_bc_phased = np.exp(1j * 0.77) * m_bc
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        out1 = apply_directional_link(
            m_bc, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        out2 = apply_directional_link(
            m_bc_phased, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(out1, out2, atol=1e-10)


# ---------------------------------------------------------------------------
# F6 — nonmaximally-entangled top eigenvector (TEST_ONLY_OFF_CONTRACT)
# ---------------------------------------------------------------------------


def test_f6_nonmaximally_entangled_seed_fails_unitary_gate():
    product_vec = np.zeros(4, dtype=complex)
    product_vec[0] = 1.0  # |00>
    p_bad = np.outer(product_vec, product_vec.conj())
    eps_bad = 0.3
    rho_bad = (1 - eps_bad) * IDENTITY4 / 4.0 + eps_bad * p_bad
    with pytest.raises(ValueError):
        state_derived_edge_link(rho_bad, **_link_kwargs())


# ---------------------------------------------------------------------------
# F7 — degenerate top eigenspace (TEST_ONLY_OFF_CONTRACT, eps=0)
# ---------------------------------------------------------------------------


def test_f7_degenerate_edge_state_fails_extraction():
    rho_deg = IDENTITY4 / 4.0
    with pytest.raises(ValueError):
        state_derived_edge_link(rho_deg, **_link_kwargs())


# ---------------------------------------------------------------------------
# Additional malformed declared-family control: unique top but lower three
# eigenvalues NOT mutually degenerate.
# ---------------------------------------------------------------------------


def test_rejects_unique_top_with_nondegenerate_lower_spectrum():
    rho_bad = np.diag([0.1, 0.2, 0.3, 0.4]).astype(complex)
    with pytest.raises(ValueError):
        state_derived_edge_link(rho_bad, **_link_kwargs())


# ---------------------------------------------------------------------------
# Malformed input rejection (shape, unitarity, hermiticity, tracelessness)
# ---------------------------------------------------------------------------


def test_state_derived_edge_link_rejects_wrong_shape():
    with pytest.raises(ValueError):
        state_derived_edge_link(np.eye(3, dtype=complex), **_link_kwargs())


def test_apply_directional_link_rejects_nonunitary_m():
    bad_m = np.array([[1.0, 0.5], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        apply_directional_link(
            bad_m, PAULI_X, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )


def test_apply_directional_link_rejects_nonhermitian_tangent():
    with pytest.raises(ValueError):
        apply_directional_link(
            IDENTITY2, np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex),
            hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )


def test_apply_directional_link_rejects_nontraceless_tangent():
    with pytest.raises(ValueError):
        apply_directional_link(
            IDENTITY2, np.diag([1.0, 1.0]).astype(complex),
            hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )


def test_reverse_correlation_matrix_rejects_nonunitary():
    bad_m = np.array([[1.0, 0.5], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        reverse_correlation_matrix(bad_m, max_entanglement_unitarity_tolerance=UNITARITY_TOL)


def test_state_derived_centered_edge_transfer_rejects_wrong_shape():
    with pytest.raises(ValueError):
        state_derived_centered_edge_transfer(
            np.eye(3, dtype=complex), PAULI_X, hermiticity_tolerance=TOL,
            trace_tolerance=TOL, positivity_tolerance=TOL,
        )


# ---------------------------------------------------------------------------
# Structural: no scipy, no private core import.
# ---------------------------------------------------------------------------


def test_structural_links_module_has_no_scipy_or_private_core_import():
    import ast
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[3]
        / "src" / "cosmotgg" / "models" / "model1a" / "links.py"
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
