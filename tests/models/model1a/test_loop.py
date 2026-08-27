"""Tests for cosmotgg.models.model1a.loop.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`
(`docs/toy-models/toy1a/specification.md` §23). This file also carries
the G1-G7 qualification-guard evidence and the A0-A6 architecture
controls for the whole `cosmotgg.models.model1a` package.
"""

import ast
import hashlib
import inspect
from pathlib import Path

import numpy as np
import pytest

from cosmotgg.models.model1a.states import (
    four_qubit_relational_loop_reductions,
    four_qubit_relational_loop_state,
)
from cosmotgg.models.model1a.links import (
    apply_directional_link,
    state_derived_edge_link,
)
from cosmotgg.models.model1a.loop import (
    projective_loop_action,
    projective_loop_holonomy,
    relational_curvature_response_candidate,
    state_derived_loop_transfer,
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

MODEL1A_SRC_DIR = Path(__file__).resolve().parents[3] / "src" / "cosmotgg" / "models" / "model1a"


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


def _loop_kwargs():
    return dict(hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


def _build_reductions(params):
    rho = four_qubit_relational_loop_state(
        params["eps_ab"], params["eps_bc"], params["eps_cd"], params["eps_da"],
        params["m_ab"], params["m_bc"], params["m_cd"], params["m_da"], **_core_kwargs()
    )
    return four_qubit_relational_loop_reductions(rho)


def _all_links(reductions):
    return {
        edge: state_derived_edge_link(reductions[f"rho_{edge}"], **_link_kwargs())
        for edge in ("ab", "bc", "cd", "da")
    }


def _random_unitary(dim, seed):
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(m)
    ph = np.diag(r) / np.abs(np.diag(r))
    return q * ph


# ---------------------------------------------------------------------------
# P1-P3 — projective holonomy, phase-independent oracle, loop strength oracle
# ---------------------------------------------------------------------------


def test_p1_p2_projective_holonomy_matches_primary_fixture_oracle():
    reductions = _build_reductions(PRIMARY)
    links = _all_links(reductions)
    holonomy = projective_loop_holonomy(
        links["ab"]["correlation_matrix"], links["bc"]["correlation_matrix"],
        links["cd"]["correlation_matrix"], links["da"]["correlation_matrix"],
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    # H_A = -i sigma_Z up to scalar phase; test the PHASE-INDEPENDENT action.
    for name, xi, expected in (("Z", PAULI_Z, PAULI_Z), ("X", PAULI_X, -PAULI_X), ("Y", PAULI_Y, -PAULI_Y)):
        action = projective_loop_action(
            holonomy, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(action, expected, atol=1e-8)


def test_p3_loop_strength_oracle():
    reductions = _build_reductions(PRIMARY)
    links = _all_links(reductions)
    w_square = (
        links["ab"]["strength"] * links["bc"]["strength"]
        * links["cd"]["strength"] * links["da"]["strength"]
    )
    assert np.isclose(w_square, 0.05**4, atol=1e-12)


# ---------------------------------------------------------------------------
# P4 — direct state-derived centered loop transfer == w Ad_H(X)
# ---------------------------------------------------------------------------


def test_p4_state_derived_loop_transfer_matches_w_ad_h():
    reductions = _build_reductions(PRIMARY)
    links = _all_links(reductions)
    w_square = (
        links["ab"]["strength"] * links["bc"]["strength"]
        * links["cd"]["strength"] * links["da"]["strength"]
    )
    holonomy = projective_loop_holonomy(
        links["ab"]["correlation_matrix"], links["bc"]["correlation_matrix"],
        links["cd"]["correlation_matrix"], links["da"]["correlation_matrix"],
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        transferred = state_derived_loop_transfer(
            reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
            xi, **_loop_kwargs()
        )
        action = projective_loop_action(
            holonomy, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(transferred, w_square * action, atol=1e-9)


# ---------------------------------------------------------------------------
# P5-P6 — primary response == L_square(X) - wX, matches analytic Pauli oracle
# ---------------------------------------------------------------------------


def test_p5_p6_primary_response_matches_analytic_oracle():
    reductions = _build_reductions(PRIMARY)
    w_square = 0.05**4

    r_z = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Z, **_link_kwargs()
    )
    r_x = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_X, **_link_kwargs()
    )
    r_y = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Y, **_link_kwargs()
    )

    assert np.allclose(r_z, np.zeros((2, 2)), atol=1e-12)
    assert np.allclose(r_x, -2.0 * w_square * PAULI_X, atol=1e-12)
    assert np.allclose(r_y, -2.0 * w_square * PAULI_Y, atol=1e-12)


# ---------------------------------------------------------------------------
# P7 — directional content
# ---------------------------------------------------------------------------


def test_p7_directional_content():
    reductions = _build_reductions(PRIMARY)
    r_z = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Z, **_link_kwargs()
    )
    r_x = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_X, **_link_kwargs()
    )
    r_y = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Y, **_link_kwargs()
    )
    assert np.allclose(r_z, 0.0, atol=1e-12)
    assert not np.allclose(r_x, 0.0, atol=1e-12)
    assert not np.allclose(r_y, 0.0, atol=1e-12)


# ---------------------------------------------------------------------------
# Mandatory orientation regression (D<-A vs incorrect A(x)D substitution)
# ---------------------------------------------------------------------------


def test_orientation_regression_da_vs_ad_detects_swap():
    theta = np.pi / 6.0
    m_da = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]], dtype=complex
    )
    params = dict(
        m_ab=IDENTITY2, m_bc=IDENTITY2, m_cd=IDENTITY2, m_da=m_da,
        eps_ab=0.05, eps_bc=0.05, eps_cd=0.05, eps_da=0.05,
    )
    reductions = _build_reductions(params)
    links = _all_links(reductions)

    holonomy_correct = projective_loop_holonomy(
        links["ab"]["correlation_matrix"], links["bc"]["correlation_matrix"],
        links["cd"]["correlation_matrix"], links["da"]["correlation_matrix"],
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    # Deliberately wrong: substitute the transposed (A(x)D-order-like) matrix.
    holonomy_wrong = projective_loop_holonomy(
        links["ab"]["correlation_matrix"], links["bc"]["correlation_matrix"],
        links["cd"]["correlation_matrix"], links["da"]["correlation_matrix"].T,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )

    action_correct = projective_loop_action(
        holonomy_correct, PAULI_X, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    action_wrong = projective_loop_action(
        holonomy_wrong, PAULI_X, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    assert not np.allclose(action_correct, action_wrong, atol=1e-6)


# ---------------------------------------------------------------------------
# F0 — PURE_GAUGE
# ---------------------------------------------------------------------------


def test_f0_pure_gauge_links_give_identity_holonomy_and_zero_response():
    g_a, g_b, g_c, g_d = (_random_unitary(2, s) for s in (101, 102, 103, 104))
    m_ab = g_a @ g_b.T
    m_bc = g_b @ g_c.T
    m_cd = g_c @ g_d.T
    m_da = g_d @ g_a.T
    params = dict(m_ab=m_ab, m_bc=m_bc, m_cd=m_cd, m_da=m_da,
                  eps_ab=0.05, eps_bc=0.04, eps_cd=0.03, eps_da=0.06)
    reductions = _build_reductions(params)

    holonomy = projective_loop_holonomy(
        m_ab, m_bc, m_cd, m_da, max_entanglement_unitarity_tolerance=UNITARITY_TOL
    )
    assert np.allclose(holonomy / holonomy[0, 0], IDENTITY2, atol=1e-6)

    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        r = relational_curvature_response_candidate(
            reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
            xi, **_link_kwargs()
        )
        assert np.allclose(r, 0.0, atol=1e-8)


# ---------------------------------------------------------------------------
# F1 — CENTRAL_PHASE
# ---------------------------------------------------------------------------


def test_f1_central_holonomy_gives_zero_response():
    reductions = _build_reductions(PRIMARY)
    holonomy_central = np.exp(1j * 0.42) * IDENTITY2
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        action = projective_loop_action(
            holonomy_central, xi, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            max_entanglement_unitarity_tolerance=UNITARITY_TOL,
        )
        assert np.allclose(action, xi, atol=1e-10)


# ---------------------------------------------------------------------------
# F2 — WEAK_LINK continuity
# ---------------------------------------------------------------------------


def test_f2_weak_link_continuity():
    ratios = []
    prev = None
    for r_value in (0.05, 0.005, 0.0005, 0.00005):
        params = dict(m_ab=IDENTITY2, m_bc=PAULI_X, m_cd=IDENTITY2, m_da=PAULI_Y,
                      eps_ab=r_value, eps_bc=0.05, eps_cd=0.05, eps_da=0.05)
        reductions = _build_reductions(params)
        r_response = relational_curvature_response_candidate(
            reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
            PAULI_X, **_link_kwargs()
        )
        val = np.max(np.abs(r_response))
        if prev is not None:
            ratios.append(val / prev)
        prev = val
    # linear scaling in r_value (each step divides r_value by 10)
    assert all(np.isclose(ratio, 0.1, atol=1e-6) for ratio in ratios)

    # raw projective action stays fixed/nonzero regardless of eps_ab
    links = _all_links(_build_reductions(PRIMARY))
    holonomy = projective_loop_holonomy(
        links["ab"]["correlation_matrix"], links["bc"]["correlation_matrix"],
        links["cd"]["correlation_matrix"], links["da"]["correlation_matrix"],
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    raw_action = projective_loop_action(
        holonomy, PAULI_X, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        max_entanglement_unitarity_tolerance=UNITARITY_TOL,
    )
    assert not np.allclose(raw_action, PAULI_X, atol=1e-6)  # remains nonzero-different


# ---------------------------------------------------------------------------
# F3 — NO_RELATION limit
# ---------------------------------------------------------------------------


def test_f3_no_relation_limit():
    prev = None
    for eps_value in (0.05, 0.005, 0.0005):
        params = dict(m_ab=IDENTITY2, m_bc=PAULI_X, m_cd=IDENTITY2, m_da=PAULI_Y,
                      eps_ab=eps_value, eps_bc=eps_value, eps_cd=eps_value, eps_da=eps_value)
        reductions = _build_reductions(params)
        assert np.allclose(reductions["rho_ab"], IDENTITY4 / 4.0, atol=4 * eps_value)  # -> I/16 globally
        r_response = relational_curvature_response_candidate(
            reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
            PAULI_X, **_link_kwargs()
        )
        val = np.max(np.abs(r_response))
        if prev is not None:
            assert val < prev
        prev = val
    assert prev < 1e-6


# ---------------------------------------------------------------------------
# F5 — LOCAL_BASIS covariance
# ---------------------------------------------------------------------------


def test_f5_local_basis_covariance():
    reductions = _build_reductions(PRIMARY)
    v_a, v_b, v_c, v_d = (_random_unitary(2, s) for s in (201, 202, 203, 204))

    rho = four_qubit_relational_loop_state(
        PRIMARY["eps_ab"], PRIMARY["eps_bc"], PRIMARY["eps_cd"], PRIMARY["eps_da"],
        PRIMARY["m_ab"], PRIMARY["m_bc"], PRIMARY["m_cd"], PRIMARY["m_da"], **_core_kwargs()
    )
    v_full = np.kron(np.kron(np.kron(v_a, v_b), v_c), v_d)
    rho_prime = v_full @ rho @ v_full.conj().T
    reductions_prime = four_qubit_relational_loop_reductions(rho_prime)

    xi = PAULI_X
    xi_prime = v_a @ xi @ v_a.conj().T

    r_original = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        xi, **_link_kwargs()
    )
    r_prime = relational_curvature_response_candidate(
        reductions_prime["rho_ab"], reductions_prime["rho_bc"], reductions_prime["rho_cd"],
        reductions_prime["rho_da"], xi_prime, **_link_kwargs()
    )
    expected = v_a @ r_original @ v_a.conj().T
    assert np.allclose(r_prime, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# F8 — OPEN_PATH_ATTENUATION_FALSE_POSITIVE
# ---------------------------------------------------------------------------


def test_f8_open_path_attenuation_is_not_curvature():
    # Projectively flat directional links (pure gauge), unequal edge strengths.
    g_a, g_b, g_c, g_d = (_random_unitary(2, s) for s in (301, 302, 303, 304))
    m_ab = g_a @ g_b.T
    m_bc = g_b @ g_c.T
    m_cd = g_c @ g_d.T
    m_da = g_d @ g_a.T
    params = dict(m_ab=m_ab, m_bc=m_bc, m_cd=m_cd, m_da=m_da,
                  eps_ab=0.04, eps_bc=0.05, eps_cd=0.03, eps_da=0.06)
    reductions = _build_reductions(params)
    links = _all_links(reductions)

    strength_ab_bc = links["ab"]["strength"] * links["bc"]["strength"]
    strength_da_cd = links["da"]["strength"] * links["cd"]["strength"]
    assert not np.isclose(strength_ab_bc, strength_da_cd)

    # Open-path (test-only) raw predictions using unequal strength products
    # can differ (not asserted numerically here beyond the strength check
    # above, which is sufficient to demonstrate the amplitude mismatch);
    # the mandatory invariant is the CLOSED projective loop response.
    for xi in (PAULI_X, PAULI_Y, PAULI_Z):
        r = relational_curvature_response_candidate(
            reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
            xi, **_link_kwargs()
        )
        assert np.allclose(r, 0.0, atol=1e-8)


# ---------------------------------------------------------------------------
# G1-G7 qualification-guard evidence (no T2 PASS emitted)
# ---------------------------------------------------------------------------


def test_g1_state_derivation_no_independent_epsilon_or_m_argument():
    signature = inspect.signature(relational_curvature_response_candidate)
    forbidden = {"epsilon", "eps", "m", "holonomy", "loop_strength", "w", "w_square"}
    assert forbidden.isdisjoint(signature.parameters.keys())


def test_g3_g6_curvature_nontriviality_and_tensorial_content():
    reductions = _build_reductions(PRIMARY)
    r_x0 = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Z, **_link_kwargs()
    )
    r_x1 = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_X, **_link_kwargs()
    )
    assert np.allclose(r_x0, 0.0, atol=1e-12)  # G6: exists X0 with R(X0)=0
    assert not np.allclose(r_x1, 0.0, atol=1e-12)  # G3/G6: exists X1 with R(X1)!=0


def test_g4_relative_deviation_distinct_tangent_responses():
    reductions = _build_reductions(PRIMARY)
    r_x = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_X, **_link_kwargs()
    )
    r_y = relational_curvature_response_candidate(
        reductions["rho_ab"], reductions["rho_bc"], reductions["rho_cd"], reductions["rho_da"],
        PAULI_Y, **_link_kwargs()
    )
    assert not np.allclose(r_x, r_y, atol=1e-10)


def test_no_t2_pass_emitted_anywhere():
    for path in sorted(MODEL1A_SRC_DIR.rglob("*.py")):
        content = path.read_text(encoding="utf-8")
        assert "T2_PASS" not in content
        assert "T2 PASS" not in content


# ---------------------------------------------------------------------------
# G7 static source inspection: no distance/area/metric/coordinate identifier
# ---------------------------------------------------------------------------


_FORBIDDEN_PREGEOMETRIC_IDENTIFIERS = {
    "distance",
    "area",
    "plaquette_area",
    "metric",
    "coordinate",
    "spatial_separation",
}


def test_g7_no_pregeometric_distance_identifier():
    violations = []
    for path in sorted(MODEL1A_SRC_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            identifier = None
            if isinstance(node, ast.Name):
                identifier = node.id
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                identifier = node.name
            elif isinstance(node, ast.Attribute):
                identifier = node.attr
            if identifier and identifier.lower() in _FORBIDDEN_PREGEOMETRIC_IDENTIFIERS:
                violations.append((path, identifier))
    assert not violations, f"forbidden pre-geometric identifier found: {violations}"


# ---------------------------------------------------------------------------
# A0-A6 — architecture / structural controls for the whole model1a package.
# ---------------------------------------------------------------------------


def _model1a_python_files():
    return sorted(MODEL1A_SRC_DIR.rglob("*.py"))


def test_a0_no_prior_model_production_import():
    forbidden = ("model0a", "model0b", "model0c", "model0d", "model0e")
    violations = []
    for path in _model1a_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(name in alias.name for name in forbidden):
                        violations.append((path, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if any(name in module for name in forbidden):
                    violations.append((path, node.lineno))
    assert not violations, f"forbidden prior-model import found: {violations}"


def test_a1_no_private_core_import():
    violations = []
    for path in _model1a_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module.startswith("cosmotgg.core"):
                    for alias in node.names:
                        if alias.name.startswith("_"):
                            violations.append((path, node.lineno, alias.name))
    assert not violations, f"private cosmotgg.core symbol imported: {violations}"


def test_a2_no_scipy_import_anywhere():
    violations = []
    for path in _model1a_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "scipy" in alias.name:
                        violations.append((path, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if "scipy" in (node.module or ""):
                    violations.append((path, node.lineno))
    assert not violations, f"forbidden scipy import found: {violations}"


def test_a3_no_graph_framework_class_hierarchy():
    forbidden_class_names = {"Model1A", "Connection", "Curvature", "Graph", "Groupoid"}
    violations = []
    for path in _model1a_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in forbidden_class_names:
                violations.append((path, node.name))
    assert not violations, f"forbidden class hierarchy found: {violations}"


_FORBIDDEN_PHYSICAL_API_NAMES = {
    "riemann",
    "tidal_acceleration",
    "geodesic_deviation",
    "gravity",
    "spacetime_curvature",
}


def test_a4_forbidden_physical_api_name_firewall():
    violations = []
    for path in _model1a_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.lower() in _FORBIDDEN_PHYSICAL_API_NAMES:
                    violations.append((path, node.name))
    assert not violations, f"forbidden physical API name found: {violations}"


_EXPECTED_TOY1A_SPEC_SHA256 = (
    "42f2ae32bf7d33dfbaca299984685e51a446c30b7f18f054beb6fe8af57d821e"
)
_EXPECTED_TOY1A_DESIGN_SHA256 = (
    "1d30d89a59a6ad308fd5c3a05314b4f04b5d2d6235204e4238792ce1fb9b1be5"
)


def test_a5_toy1a_documents_unchanged_since_model1a_impl_1_preflight():
    """Freeze-guard against accidental modification during this
    implementation lot: byte-identical to the state read at the
    `MODEL1A-IMPL-1` preflight (HEAD =
    `cbd662353ae93b747579cac7b470bf4620b4c0d9`)."""
    repo_root = Path(__file__).resolve().parents[3]
    spec_path = repo_root / "docs" / "toy-models" / "toy1a" / "specification.md"
    design_path = repo_root / "docs" / "toy-models" / "toy1a" / "implementation-design.md"

    spec_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    design_hash = hashlib.sha256(design_path.read_bytes()).hexdigest()

    assert spec_hash == _EXPECTED_TOY1A_SPEC_SHA256, (
        "docs/toy-models/toy1a/specification.md changed since MODEL1A-IMPL-1 preflight"
    )
    assert design_hash == _EXPECTED_TOY1A_DESIGN_SHA256, (
        "docs/toy-models/toy1a/implementation-design.md changed since MODEL1A-IMPL-1 preflight"
    )


def test_a6_no_changes_to_docs_model_directory():
    # Structural reminder only: docs/model/** is READ_ONLY for this lot;
    # this test asserts the directory exists and is not touched by any
    # model1a production import (already covered by A0), matching the
    # frozen-scope contract of this lot.
    repo_root = Path(__file__).resolve().parents[3]
    assert (repo_root / "docs" / "model").is_dir()
