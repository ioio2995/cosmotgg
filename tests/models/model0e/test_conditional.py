"""Tests for cosmotgg.models.model0e.conditional.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`
(`docs/toy-models/toy0e/specification.md` §34). `F0` below is a
`TEST_ONLY_OFF_CONTRACT_NEGATIVE_CONTROL` (spec §33): it constructs
`rho_AB(eta=0) = I_AB/9` directly, not through the production state
constructor.

This file also carries the architecture/structural controls A0-A5 for
the whole `cosmotgg.models.model0e` package (no prior-model import, no
private-core import, no `scipy`, no time/clock-implying identifier, no
target-state parameter on the fixed-law application, and a frozen-hash
guard on the two `toy0e` normative documents).
"""

import ast
import hashlib
import inspect
from pathlib import Path

import numpy as np
import pytest

from cosmotgg.models.model0e.states import (
    four_partite_discrete_multimodular_reductions,
    four_partite_discrete_multimodular_reference_state,
)
from cosmotgg.models.model0e.reference import (
    derived_z3_relational_reference,
    projected_modular_context_pair,
    relabel_z3_reference_pvm,
)
from cosmotgg.models.model0e.conditional import (
    apply_fixed_z3_relational_law,
    conditional_reference_statistics,
    correlation_matrix_from_rho_ab,
    derived_fixed_law_unitary,
    extract_affine_z3_reference_map,
    operator_correlation_transfer_ab,
    physical_conditional_states_from_reference,
    reference_change_overlap_matrix,
    vector_correlation_map_ab,
)

TOL = 1e-9
SPECTRAL_TOL = 1e-9
EQUAL_MODULUS_TOL = 1e-6
UNITARITY_TOL = 1e-8

IDENTITY2 = np.eye(2, dtype=complex)
IDENTITY3 = np.eye(3, dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

MAIN = dict(eta=0.02, gamma=0.10, mu_a=0.10, mu_b=0.10, delta=0.20, nu_a=0.05, nu_b=0.05)
ASYM = dict(eta=0.02, gamma=0.10, mu_a=0.08, mu_b=0.12, delta=0.20, nu_a=0.04, nu_b=0.06)

MODEL0E_SRC_DIR = Path(__file__).resolve().parents[3] / "src" / "cosmotgg" / "models" / "model0e"


def _core_kwargs():
    return dict(hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


def _corr_kwargs():
    return dict(
        hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL,
        spectral_tolerance=SPECTRAL_TOL, unitarity_tolerance=UNITARITY_TOL,
    )


def _setup(params):
    rho = four_partite_discrete_multimodular_reference_state(
        params["eta"], params["gamma"], params["mu_a"], params["mu_b"],
        params["delta"], params["nu_a"], params["nu_b"], **_core_kwargs()
    )
    reductions = four_partite_discrete_multimodular_reductions(rho)

    h_q_b, h_n_b = projected_modular_context_pair(reductions["rho_bc"], reductions["rho_bd"], **_core_kwargs())
    ref_b = derived_z3_relational_reference(
        h_q_b, h_n_b, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
        equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )
    h_q_a, h_n_a = projected_modular_context_pair(reductions["rho_ac"], reductions["rho_ad"], **_core_kwargs())
    ref_a = derived_z3_relational_reference(
        h_q_a, h_n_a, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
        equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )
    return {"rho": rho, "reductions": reductions, "ref_a": ref_a, "ref_b": ref_b}


# ---------------------------------------------------------------------------
# C1/C2 — physical conditional states, oracle
# ---------------------------------------------------------------------------


def test_c1_physical_conditional_states_match_analytic_oracle():
    ctx = _setup(MAIN)
    probs, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    assert np.allclose(probs, 1.0 / 3.0, atol=1e-10)
    eta = MAIN["eta"]
    for k in range(3):
        expected = (1 - eta) / 3.0 * IDENTITY3 + eta * ctx["ref_b"]["pvm"][k].T
        assert np.allclose(states[k], expected, atol=1e-9)
        assert np.isclose(np.trace(states[k]), 1.0, atol=1e-10)
        assert np.all(np.linalg.eigvalsh(states[k]) > 0.0)


def test_c2_conditional_states_are_distinct_physical_carriers():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    assert not np.allclose(states[0], states[1], atol=1e-8)
    assert not np.allclose(states[1], states[2], atol=1e-8)
    assert not np.allclose(states[0], states[2], atol=1e-8)


# ---------------------------------------------------------------------------
# C3/C4 — observable nontriviality
# ---------------------------------------------------------------------------


def test_c3_c4_probe_statistics_differ_across_readings():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    stats = conditional_reference_statistics(states, ctx["ref_a"]["pvm"])
    assert np.allclose(stats.sum(axis=1), 1.0, atol=1e-8)
    for k1 in range(3):
        for k2 in range(3):
            if k1 != k2:
                assert not np.allclose(stats[k1], stats[k2], atol=1e-8)


# ---------------------------------------------------------------------------
# F0 — absence of physical change content (TEST_ONLY_OFF_CONTRACT)
# ---------------------------------------------------------------------------


def test_f0_zero_eta_makes_c3_fail():
    ctx = _setup(MAIN)  # valid contexts/reference (independent of eta)
    rho_ab_off_contract = np.eye(9, dtype=complex) / 9.0

    _, states = physical_conditional_states_from_reference(
        rho_ab_off_contract, ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    for state in states:
        assert np.allclose(state, IDENTITY3 / 3.0, atol=1e-10)

    stats = conditional_reference_statistics(states, ctx["ref_a"]["pvm"])
    for k1 in range(3):
        for k2 in range(3):
            assert np.allclose(stats[k1], stats[k2], atol=1e-10)  # C3 fails: no distinguishing observable


# ---------------------------------------------------------------------------
# COR1-COR3 — correlation map
# ---------------------------------------------------------------------------


def test_cor1_correlation_matrix_is_unitary():
    ctx = _setup(MAIN)
    m_ab = correlation_matrix_from_rho_ab(ctx["reductions"]["rho_ab"], **_corr_kwargs())
    assert np.allclose(m_ab.conj().T @ m_ab, IDENTITY3, atol=1e-8)
    assert np.allclose(m_ab @ m_ab.conj().T, IDENTITY3, atol=1e-8)


def test_cor2_operator_transfer_matches_rank_one_vector_identity():
    ctx = _setup(MAIN)
    m_ab = correlation_matrix_from_rho_ab(ctx["reductions"]["rho_ab"], **_corr_kwargs())

    rng = np.random.default_rng(123)
    b_vec = rng.normal(size=3) + 1j * rng.normal(size=3)
    b_vec = b_vec / np.linalg.norm(b_vec)

    j_b = vector_correlation_map_ab(b_vec, m_ab)
    effect = np.outer(b_vec, b_vec.conj())
    transferred = operator_correlation_transfer_ab(effect, m_ab)
    expected = np.outer(j_b, j_b.conj())
    assert np.allclose(transferred, expected, atol=1e-10)


def test_cor3_global_phase_of_m_ab_does_not_affect_jop_or_v_action():
    ctx = _setup(MAIN)
    m_ab = correlation_matrix_from_rho_ab(ctx["reductions"]["rho_ab"], **_corr_kwargs())
    phase = np.exp(1j * 0.837)
    m_ab_phased = phase * m_ab

    effect = ctx["ref_b"]["pvm"][0]
    transferred = operator_correlation_transfer_ab(effect, m_ab)
    transferred_phased = operator_correlation_transfer_ab(effect, m_ab_phased)
    assert np.allclose(transferred, transferred_phased, atol=1e-10)

    u_b = ctx["ref_b"]["cycle_unitary"]
    v_a = m_ab @ u_b.conj() @ m_ab.conj().T
    v_a_phased = m_ab_phased @ u_b.conj() @ m_ab_phased.conj().T
    assert np.allclose(v_a, v_a_phased, atol=1e-10)


# ---------------------------------------------------------------------------
# LAW1-LAW4 — derived fixed law
# ---------------------------------------------------------------------------


def test_law1_v_a_matches_canonical_basis_oracle_for_symmetric_seed():
    """`Q_A=Q_B`, `N_A=N_B` (spec §6) => `M_AB=I` for the declared family,
    so the canonical-basis oracle `V_A = U_B^*` (spec §22) must hold
    exactly, even though production derives `V_A` generically via
    `M_AB`, never by hard-coding this oracle."""
    ctx = _setup(MAIN)
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    expected = ctx["ref_b"]["cycle_unitary"].conj()
    assert np.allclose(v_a, expected, atol=1e-8)


def test_law2_v_a_cubed_is_identity_up_to_phase():
    ctx = _setup(MAIN)
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    cubed = np.linalg.matrix_power(v_a, 3)
    phase = cubed[0, 0] / abs(cubed[0, 0])
    assert np.allclose(cubed, phase * IDENTITY3, atol=1e-8)
    # conjugation action (Lambda) is exactly identity regardless of phase.
    probe = np.array([[0.6, 0.1 - 0.05j, 0.0], [0.1 + 0.05j, 0.3, 0.02], [0.0, 0.02, 0.1]], dtype=complex)
    assert np.allclose(cubed @ probe @ cubed.conj().T, probe, atol=1e-8)


def test_law3_conditional_states_lie_on_one_fixed_orbit():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    for k in range(3):
        lhs = states[(k + 1) % 3]
        rhs = v_a @ states[k] @ v_a.conj().T
        assert np.allclose(lhs, rhs, atol=1e-8)


def test_law4_apply_fixed_law_predicts_k1_and_k2_from_k0_without_target():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())

    predicted_1 = apply_fixed_z3_relational_law(states[0], v_a, k_source=0, k_target=1)
    predicted_2 = apply_fixed_z3_relational_law(states[0], v_a, k_source=0, k_target=2)
    assert np.allclose(predicted_1, states[1], atol=1e-8)
    assert np.allclose(predicted_2, states[2], atol=1e-8)


@pytest.mark.parametrize("bad_k", [True, 3, -1, 1.5], ids=["bool", "out-of-range", "negative", "float"])
def test_apply_fixed_law_rejects_bad_k(bad_k):
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    with pytest.raises(ValueError):
        apply_fixed_z3_relational_law(states[0], v_a, k_source=bad_k, k_target=1)
    with pytest.raises(ValueError):
        apply_fixed_z3_relational_law(states[0], v_a, k_source=0, k_target=bad_k)


# ---------------------------------------------------------------------------
# C4C — two-reading probability consistency
# ---------------------------------------------------------------------------


def test_c4c_law_predicted_matches_direct_for_all_ordered_pairs():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    probe_pvm = tuple(np.outer(IDENTITY3[:, j], IDENTITY3[:, j].conj()) for j in range(3))

    def _probe_probabilities(state):
        return np.array([np.trace(effect @ state).real for effect in probe_pvm])

    for k1 in range(3):
        for k2 in range(3):
            if k1 == k2:
                continue
            predicted_state = apply_fixed_z3_relational_law(states[k1], v_a, k_source=k1, k_target=k2)
            p_direct = _probe_probabilities(states[k2])
            p_law = _probe_probabilities(predicted_state)
            assert np.allclose(p_direct, p_law, atol=1e-8)
            assert np.all(p_direct >= -1e-10)
            assert np.isclose(p_direct.sum(), 1.0, atol=1e-8)


# ---------------------------------------------------------------------------
# C5 — physical admissibility (Lambda is structurally unitary/CPTP)
# ---------------------------------------------------------------------------


def test_c5_lambda_preserves_trace_hermiticity_and_positivity():
    ctx = _setup(MAIN)
    _, states = physical_conditional_states_from_reference(
        ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"], **_core_kwargs()
    )
    v_a = derived_fixed_law_unitary(ctx["reductions"]["rho_ab"], ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())
    for k in range(3):
        out = apply_fixed_z3_relational_law(states[0], v_a, k_source=0, k_target=k)
        assert np.isclose(np.trace(out), 1.0, atol=1e-9)
        assert np.allclose(out, out.conj().T, atol=1e-9)
        assert np.all(np.linalg.eigvalsh(out) > -1e-9)


# ---------------------------------------------------------------------------
# C6 — reparametrization firewall: no s/t/tau/time parameter anywhere.
# ---------------------------------------------------------------------------


def test_c6_no_real_flow_parameter_in_any_public_signature():
    import cosmotgg.models.model0e.states as states_mod
    import cosmotgg.models.model0e.reference as reference_mod
    import cosmotgg.models.model0e.conditional as conditional_mod

    forbidden_names = {"s", "t", "tau", "time"}
    for module in (states_mod, reference_mod, conditional_mod):
        for name in dir(module):
            if name.startswith("_"):
                continue
            obj = getattr(module, name)
            if not inspect.isfunction(obj):
                continue
            signature = inspect.signature(obj)
            assert forbidden_names.isdisjoint(signature.parameters.keys()), (
                f"{module.__name__}.{name} exposes a forbidden flow parameter"
            )


# ---------------------------------------------------------------------------
# C7 — reference nonprivilege
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("params", [MAIN, ASYM], ids=["symmetric", "amplitude-asymmetric"])
def test_c7_reference_nonprivilege(params):
    ctx = _setup(params)
    rho_ab = ctx["reductions"]["rho_ab"]
    pvm_a = ctx["ref_a"]["pvm"]
    pvm_b = ctx["ref_b"]["pvm"]

    # (1)/(2) independently derived from BC/BD and AC/AD respectively: ctx already does this.
    # (3) relation derived from rho_AB.
    m_ab = correlation_matrix_from_rho_ab(rho_ab, **_corr_kwargs())
    overlap = reference_change_overlap_matrix(pvm_a, pvm_b, m_ab)
    offset, orientation = extract_affine_z3_reference_map(overlap, overlap_tolerance=1e-6)
    assert offset in (0, 1, 2)
    assert orientation in (-1, 1)

    # (4) joint physical probabilities, common under both conditioning directions.
    tensor = rho_ab.reshape(3, 3, 3, 3)
    joint = np.empty((3, 3), dtype=float)
    for j in range(3):
        for k in range(3):
            op = np.kron(pvm_a[j], pvm_b[k])
            joint[j, k] = np.trace(op @ rho_ab).real
    assert np.isclose(joint.sum(), 1.0, atol=1e-8)
    assert np.allclose(joint.sum(axis=1), 1.0 / 3.0, atol=1e-8)
    assert np.allclose(joint.sum(axis=0), 1.0 / 3.0, atol=1e-8)

    # (5) reciprocal conditionals normalized.
    p_k_given_j = joint / joint.sum(axis=1, keepdims=True)
    p_j_given_k = joint / joint.sum(axis=0, keepdims=True)
    assert np.allclose(p_k_given_j.sum(axis=1), 1.0, atol=1e-8)
    assert np.allclose(p_j_given_k.sum(axis=0), 1.0, atol=1e-8)

    # (6) only the affine Z3 relabeling ambiguity: the overlap matrix
    # itself IS (within tolerance) exactly the candidate affine permutation matrix.
    candidate = np.zeros((3, 3))
    for k in range(3):
        j = (offset + orientation * k) % 3
        candidate[j, k] = 1.0
    assert np.max(np.abs(overlap - candidate)) <= 1e-6


# ---------------------------------------------------------------------------
# F4 — three arbitrary conditional states, no common derived orbit.
# ---------------------------------------------------------------------------


def test_f4_arbitrary_conditional_states_generically_reject_common_orbit():
    def random_density_matrix(d, seed):
        rng = np.random.default_rng(seed)
        m = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        h = m @ m.conj().T
        return h / np.trace(h).real

    sigma0 = random_density_matrix(3, 501)
    sigma1 = random_density_matrix(3, 502)
    sigma2 = random_density_matrix(3, 503)

    spectrum0 = np.sort(np.linalg.eigvalsh(sigma0))
    spectrum1 = np.sort(np.linalg.eigvalsh(sigma1))
    spectrum2 = np.sort(np.linalg.eigvalsh(sigma2))

    # A necessary condition for sigma1 = V sigma0 V^dagger (any unitary V) is
    # identical spectra; this generically fails for independent random states,
    # demonstrating FIXED_LAW_OVERDETERMINATION = FAIL for arbitrary targets.
    assert not np.allclose(spectrum0, spectrum1, atol=1e-6)
    assert not np.allclose(spectrum1, spectrum2, atol=1e-6)


# ---------------------------------------------------------------------------
# F5 — perturbation breaking AB isotropic covariance.
# ---------------------------------------------------------------------------


def test_f5_trace_zero_perturbation_breaks_fixed_law():
    ctx = _setup(MAIN)
    rho_ab = ctx["reductions"]["rho_ab"]

    perturbation = np.zeros((9, 9), dtype=complex)
    perturbation[0, 1] = 0.01
    perturbation[1, 0] = 0.01
    assert np.isclose(np.trace(perturbation), 0.0, atol=1e-12)

    rho_ab_perturbed = rho_ab + perturbation
    assert np.isclose(np.trace(rho_ab_perturbed), 1.0, atol=1e-10)
    assert np.allclose(rho_ab_perturbed, rho_ab_perturbed.conj().T, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(rho_ab_perturbed) > 0.0)  # remains a valid density matrix

    with pytest.raises(ValueError):
        derived_fixed_law_unitary(rho_ab_perturbed, ctx["ref_b"]["cycle_unitary"], **_corr_kwargs())


# ---------------------------------------------------------------------------
# Malformed input rejection (conditional.py)
# ---------------------------------------------------------------------------


def test_physical_conditional_states_rejects_wrong_shape():
    ctx = _setup(MAIN)
    with pytest.raises(ValueError):
        physical_conditional_states_from_reference(np.eye(6, dtype=complex), ctx["ref_b"]["pvm"], **_core_kwargs())


def test_physical_conditional_states_rejects_wrong_pvm_length():
    ctx = _setup(MAIN)
    with pytest.raises(ValueError):
        physical_conditional_states_from_reference(
            ctx["reductions"]["rho_ab"], ctx["ref_b"]["pvm"][:2], **_core_kwargs()
        )


def test_correlation_matrix_rejects_degenerate_top_eigenvalue():
    with pytest.raises(ValueError):
        correlation_matrix_from_rho_ab(np.eye(9, dtype=complex) / 9.0, **_corr_kwargs())


def test_vector_and_operator_maps_reject_wrong_shape():
    m = np.eye(3, dtype=complex)
    with pytest.raises(ValueError):
        vector_correlation_map_ab(np.zeros(4, dtype=complex), m)
    with pytest.raises(ValueError):
        operator_correlation_transfer_ab(np.zeros((2, 2), dtype=complex), m)


def test_extract_affine_map_rejects_non_permutation_overlap():
    bad_overlap = np.full((3, 3), 1.0 / 3.0)
    with pytest.raises(ValueError):
        extract_affine_z3_reference_map(bad_overlap, overlap_tolerance=1e-6)


# ---------------------------------------------------------------------------
# A0-A5 — architecture / structural controls for the whole model0e package.
# ---------------------------------------------------------------------------


def _model0e_python_files():
    return sorted(MODEL0E_SRC_DIR.rglob("*.py"))


def test_a0_no_prior_model_production_import():
    forbidden = ("model0a", "model0b", "model0c", "model0d")
    violations = []
    for path in _model0e_python_files():
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
    for path in _model0e_python_files():
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
    for path in _model0e_python_files():
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


_FORBIDDEN_TIME_IDENTIFIERS = {
    "clock",
    "time",
    "physical_time",
    "proper_time",
    "time_evolution",
    "physical_change",
    "relational_time",
}


def test_a3_no_time_or_clock_implying_identifier():
    violations = []
    for path in _model0e_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if node.name in ("Clock", "Time"):
                    violations.append((path, node.lineno, node.name))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.lower() in _FORBIDDEN_TIME_IDENTIFIERS:
                    violations.append((path, node.lineno, node.name))
            elif isinstance(node, ast.Name):
                if node.id.lower() in _FORBIDDEN_TIME_IDENTIFIERS:
                    violations.append((path, node.lineno, node.id))
    assert not violations, f"forbidden time/clock-implying identifier found: {violations}"


def test_a4_apply_fixed_law_signature_has_no_target_state():
    signature = inspect.signature(apply_fixed_z3_relational_law)
    assert set(signature.parameters.keys()) == {
        "state_a",
        "fixed_law_unitary_a",
        "k_source",
        "k_target",
    }


_EXPECTED_TOY0E_SPEC_SHA256 = (
    "5f334e2590977e54af6a364e35272f0207e792a81df048b483fd614672f7eaba"
)
_EXPECTED_TOY0E_DESIGN_SHA256 = (
    "72ce816b866fd18baa09c63c30189d540de1c3fc863073886f2b2b603c056aaf"
)


def test_a5_toy0e_documents_unchanged_since_model0e_design_accepted_head():
    repo_root = Path(__file__).resolve().parents[3]
    spec_path = repo_root / "docs" / "toy-models" / "toy0e" / "specification.md"
    design_path = repo_root / "docs" / "toy-models" / "toy0e" / "implementation-design.md"

    spec_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    design_hash = hashlib.sha256(design_path.read_bytes()).hexdigest()

    assert spec_hash == _EXPECTED_TOY0E_SPEC_SHA256, (
        "docs/toy-models/toy0e/specification.md changed since "
        "MODEL0E_DESIGN_ACCEPTED_HEAD=4b839571f3d800f351f933735ecd68f3722a1391"
    )
    assert design_hash == _EXPECTED_TOY0E_DESIGN_SHA256, (
        "docs/toy-models/toy0e/implementation-design.md changed since "
        "MODEL0E_DESIGN_ACCEPTED_HEAD=4b839571f3d800f351f933735ecd68f3722a1391"
    )


def test_structural_conditional_module_has_no_scipy_or_private_core_import():
    path = MODEL0E_SRC_DIR / "conditional.py"
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
