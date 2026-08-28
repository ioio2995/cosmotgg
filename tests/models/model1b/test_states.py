"""Unit tests for cosmotgg.models.model1b.states."""

import math
import pathlib

import numpy as np
import pytest

from cosmotgg.core.states import embed_operator
from cosmotgg.models.model1b.hierarchy import FINE_DIMENSIONS, FINE_SITE_ORDER
from cosmotgg.models.model1b.states import (
    FINE_EDGES,
    fine_relational_gibbs_state,
    fine_relational_hamiltonian,
)

TOL = 1e-9
_SITE_POSITIONS = {label: i for i, label in enumerate(FINE_SITE_ORDER)}


def _unitary_from_angle(theta: float, nx: float, ny: float, nz: float) -> np.ndarray:
    """Deterministic fixed SU(2) element `cos(theta/2) I - i sin(theta/2) sigma_n`."""
    n = np.array([nx, ny, nz], dtype=float)
    n = n / np.linalg.norm(n)
    identity2 = np.eye(2, dtype=complex)
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    sigma_n = n[0] * sx + n[1] * sy + n[2] * sz
    return math.cos(theta / 2.0) * identity2 - 1j * math.sin(theta / 2.0) * sigma_n


def _oracle_s_edge(m_matrix: np.ndarray) -> np.ndarray:
    """Independent oracle for `S_e(M) = 4 |phi><phi| - I`, written fresh here
    (not imported from production `_s_edge`)."""
    phi = (m_matrix / math.sqrt(2.0)).reshape(4)
    p_edge = np.outer(phi, phi.conj())
    return 4.0 * p_edge - np.eye(4, dtype=complex)


def _generic_fixture():
    """A fixed, generic, nonzero, distinct-parameter fixture over all eight
    fine edges (finite theta_e, distinct M_e), declared once and reused."""
    thetas = {edge: 0.1 + 0.02 * i for i, edge in enumerate(FINE_EDGES)}
    correlation_matrices = {
        edge: _unitary_from_angle(0.3 + 0.1 * i, 1.0, (i % 3) + 1.0, 2.0)
        for i, edge in enumerate(FINE_EDGES)
    }
    return thetas, correlation_matrices


def _identity_fixture():
    thetas = {edge: 0.2 for edge in FINE_EDGES}
    correlation_matrices = {edge: np.eye(2, dtype=complex) for edge in FINE_EDGES}
    return thetas, correlation_matrices


# ---------------------------------------------------------------------------
# S1 — canonical fine ordering / declared edges
# ---------------------------------------------------------------------------


def test_s1_fine_edges_declared_exactly():
    assert FINE_EDGES == ("AX", "XY", "YB", "BC", "CP", "PQ", "QD", "DA")


# ---------------------------------------------------------------------------
# S2 — all eight declared edge embeddings, each checked independently
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("active_edge", FINE_EDGES)
def test_s2_single_edge_hamiltonian_matches_independent_embed_oracle(active_edge):
    thetas = {edge: (1.0 if edge == active_edge else 0.0) for edge in FINE_EDGES}
    correlation_matrices = {edge: np.eye(2, dtype=complex) for edge in FINE_EDGES}
    correlation_matrices[active_edge] = _unitary_from_angle(0.77, 0.0, 1.0, 1.0)

    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )

    site_1, site_2 = active_edge[0], active_edge[1]
    positions = (_SITE_POSITIONS[site_1], _SITE_POSITIONS[site_2])
    s_e = _oracle_s_edge(correlation_matrices[active_edge])
    expected = embed_operator(s_e, dimensions=FINE_DIMENSIONS, positions=positions)

    assert np.allclose(h_rel, expected)


# ---------------------------------------------------------------------------
# S3 — DA orientation/order specifically
# ---------------------------------------------------------------------------


def test_s3_da_edge_uses_positions_d_then_a_not_a_then_d():
    """The DA edge must embed with positions=(D, A), matching S_DA(M_DA)'s
    own factor order; using (A, D) instead would silently reorder it."""
    thetas = {edge: (1.0 if edge == "DA" else 0.0) for edge in FINE_EDGES}
    correlation_matrices = {edge: np.eye(2, dtype=complex) for edge in FINE_EDGES}
    m_da = _unitary_from_angle(1.1, 1.0, 1.0, 1.0)  # nonzero sigma_y component: M != M^T
    correlation_matrices["DA"] = m_da

    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )

    s_da = _oracle_s_edge(m_da)
    pos_d, pos_a = _SITE_POSITIONS["D"], _SITE_POSITIONS["A"]
    expected_da_order = embed_operator(s_da, dimensions=FINE_DIMENSIONS, positions=(pos_d, pos_a))
    wrong_ad_order = embed_operator(s_da, dimensions=FINE_DIMENSIONS, positions=(pos_a, pos_d))

    assert np.allclose(h_rel, expected_da_order)
    assert not np.allclose(h_rel, wrong_ad_order)


# ---------------------------------------------------------------------------
# S4 — Hermiticity / faithfulness of H_rel and rho_2
# ---------------------------------------------------------------------------


def test_s4_h_rel_is_hermitian():
    thetas, correlation_matrices = _generic_fixture()
    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )
    assert np.allclose(h_rel, h_rel.conj().T, atol=1e-10)


def test_s5_rho_2_hermitian_trace_one_positive_definite():
    thetas, correlation_matrices = _generic_fixture()
    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )
    rho_2 = fine_relational_gibbs_state(
        h_rel, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=1e-12
    )
    assert np.allclose(rho_2, rho_2.conj().T, atol=1e-10)
    assert np.trace(rho_2) == pytest.approx(1.0, abs=1e-10)
    eigvals = np.linalg.eigvalsh(rho_2)
    assert np.all(eigvals > 0.0)


# ---------------------------------------------------------------------------
# S6 — zero-relation domain: theta=0 -> I/256 exactly up to floating arithmetic
# ---------------------------------------------------------------------------


def test_s6_zero_theta_gives_maximally_mixed_state():
    thetas = {edge: 0.0 for edge in FINE_EDGES}
    correlation_matrices = {edge: np.eye(2, dtype=complex) for edge in FINE_EDGES}
    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )
    assert np.allclose(h_rel, np.zeros((256, 256), dtype=complex), atol=0.0)

    rho_2 = fine_relational_gibbs_state(
        h_rel, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=1e-12
    )
    assert np.allclose(rho_2, np.eye(256, dtype=complex) / 256.0, atol=1e-12)


# ---------------------------------------------------------------------------
# S7 — common scalar spectral-shift invariance under normalization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("shift", [0.0, 1.7, -3.4, 100.0])
def test_s7_common_spectral_shift_invariance(shift):
    thetas, correlation_matrices = _generic_fixture()
    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )
    identity = np.eye(256, dtype=complex)

    rho_unshifted = fine_relational_gibbs_state(
        h_rel, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=1e-12
    )
    rho_shifted = fine_relational_gibbs_state(
        h_rel + shift * identity,
        hermiticity_tolerance=TOL,
        trace_tolerance=TOL,
        positivity_tolerance=1e-12,
    )
    assert np.allclose(rho_unshifted, rho_shifted, atol=1e-10)


# ---------------------------------------------------------------------------
# S8 — fail-closed domain: malformed/non-unitary M, missing/unknown edge data
# ---------------------------------------------------------------------------


def test_s8_malformed_m_shape_rejected():
    thetas, correlation_matrices = _generic_fixture()
    correlation_matrices["AX"] = np.eye(3, dtype=complex)
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s9_non_unitary_m_rejected():
    thetas, correlation_matrices = _generic_fixture()
    correlation_matrices["BC"] = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s10_missing_edge_in_thetas_rejected():
    thetas, correlation_matrices = _generic_fixture()
    del thetas["DA"]
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s11_unknown_edge_in_thetas_rejected():
    thetas, correlation_matrices = _generic_fixture()
    thetas["ZZ"] = 0.5
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s12_missing_edge_in_correlation_matrices_rejected():
    thetas, correlation_matrices = _generic_fixture()
    del correlation_matrices["XY"]
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s13_theta_bool_rejected():
    thetas, correlation_matrices = _generic_fixture()
    thetas["AX"] = True
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s14_theta_nan_rejected():
    thetas, correlation_matrices = _generic_fixture()
    thetas["AX"] = float("nan")
    with pytest.raises(ValueError):
        fine_relational_hamiltonian(
            thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
        )


def test_s15_h_rel_wrong_shape_rejected_by_gibbs_state():
    with pytest.raises(ValueError):
        fine_relational_gibbs_state(
            np.eye(64, dtype=complex),
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=1e-12,
        )


def test_s16_non_hermitian_h_rel_rejected_by_gibbs_state():
    h_rel = np.zeros((256, 256), dtype=complex)
    h_rel[0, 1] = 1.0  # breaks hermiticity
    with pytest.raises(ValueError):
        fine_relational_gibbs_state(
            h_rel, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=1e-12
        )


# ---------------------------------------------------------------------------
# Structural control: MODEL1B_PRODUCTION_IMPORTS_PRIOR_MODELS = NO
# ---------------------------------------------------------------------------


def test_structural_model1b_imports_no_prior_models_production_code():
    """AST-based structural control (not a docstring substring search: the
    package docstrings legitimately *mention* the excluded prior models in
    prose)."""
    import ast

    import cosmotgg.models.model1b as model1b_package

    package_dir = pathlib.Path(model1b_package.__file__).parent
    forbidden_modules = {"model0a", "model0b", "model0c", "model0d", "model0e", "model1a"}
    for py_file in sorted(package_dir.glob("*.py")):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    parts = alias.name.split(".")
                    assert not (forbidden_modules & set(parts)), (
                        f"{py_file} imports forbidden prior-model module {alias.name!r}"
                    )
            elif isinstance(node, ast.ImportFrom) and node.module:
                parts = node.module.split(".")
                assert not (forbidden_modules & set(parts)), (
                    f"{py_file} imports from forbidden prior-model module {node.module!r}"
                )


def test_identity_fixture_is_consistent_and_faithful():
    """Sanity check on the shared trivial-correlation fixture used elsewhere."""
    thetas, correlation_matrices = _identity_fixture()
    h_rel = fine_relational_hamiltonian(
        thetas, correlation_matrices, max_entanglement_unitarity_tolerance=TOL
    )
    rho_2 = fine_relational_gibbs_state(
        h_rel, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=1e-12
    )
    assert np.trace(rho_2) == pytest.approx(1.0, abs=1e-10)
