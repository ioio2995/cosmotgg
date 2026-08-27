"""Tests for cosmotgg.models.model0e.reference.

Fixture values below are explicitly `NON_NORMATIVE_TEST_FIXTURE`
(`docs/toy-models/toy0e/specification.md` §34). Independent analytic
oracles (`_delta_q_oracle`, `_h_n_oracle`) reproduce the closed-form
formulas of `docs/toy-models/toy0e/specification.md` §11-§12
independently of the modular-mechanism production path in
`cosmotgg.models.model0e.reference` (`modular_hamiltonian` +
`conditional_expectation` + `traceless_part`).

F1/F2 below are `TEST_ONLY_OFF_CONTRACT_NEGATIVE_CONTROLS` (spec §33):
they construct the off-contract `(6, 6)` reduction directly in this
test file and feed it to the production functions
`projected_modular_context_pair`/`derived_z3_relational_reference`
(which have no `mu_X`/`nu_X` domain restriction of their own); they do
NOT go through, and do not test, the production state constructor's
branch-domain rejection (covered separately by `test_states.py`
S3/`CONTRACT_REJECTION`).
"""

import math

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

TOL = 1e-9
SPECTRAL_TOL = 1e-9
EQUAL_MODULUS_TOL = 1e-6

IDENTITY2 = np.eye(2, dtype=complex)
IDENTITY3 = np.eye(3, dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

MAIN = dict(eta=0.02, gamma=0.10, mu_a=0.10, mu_b=0.10, delta=0.20, nu_a=0.05, nu_b=0.05)
ASYM = dict(eta=0.02, gamma=0.10, mu_a=0.08, mu_b=0.12, delta=0.20, nu_a=0.04, nu_b=0.06)


def _core_kwargs():
    return dict(hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


def _oracle_q():
    q0 = np.ones(3, dtype=complex) / np.sqrt(3.0)
    return np.outer(q0, q0.conj()) - IDENTITY3 / 3.0


def _oracle_n():
    return np.diag([-1.0, 0.0, 1.0]).astype(complex)


def _delta_q_oracle(gamma, mu_x):
    return 0.5 * math.log(
        (1.0 - (gamma - mu_x / 3.0) ** 2) / (1.0 - (gamma + 2.0 * mu_x / 3.0) ** 2)
    )


def _h_n_oracle(n, delta, nu_x):
    a = delta + nu_x * n
    return math.log(6.0) - 0.5 * math.log(1.0 - a**2)


def _reductions(params):
    rho = four_partite_discrete_multimodular_reference_state(
        params["eta"], params["gamma"], params["mu_a"], params["mu_b"],
        params["delta"], params["nu_a"], params["nu_b"], **_core_kwargs()
    )
    return four_partite_discrete_multimodular_reductions(rho)


def _context_pair(params, side):
    reductions = _reductions(params)
    rho_xc = reductions[f"rho_{side}c"]
    rho_xd = reductions[f"rho_{side}d"]
    return projected_modular_context_pair(rho_xc, rho_xd, **_core_kwargs())


def _reference(params, side):
    h_q, h_n = _context_pair(params, side)
    return h_q, h_n, derived_z3_relational_reference(
        h_q, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
        equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )


# ---------------------------------------------------------------------------
# R1 — exact Q analytic oracle
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("params, side, mu_key", [
    (MAIN, "a", "mu_a"), (MAIN, "b", "mu_b"), (ASYM, "a", "mu_a"), (ASYM, "b", "mu_b"),
])
def test_r1_h_q_matches_analytic_oracle(params, side, mu_key):
    h_q, _ = _context_pair(params, side)
    delta_q = _delta_q_oracle(params["gamma"], params[mu_key])
    expected = delta_q * _oracle_q()
    assert np.allclose(h_q, expected, atol=1e-9)
    assert delta_q > 0.0


# ---------------------------------------------------------------------------
# R2 — unique maximum Q eigenprojector == |q0><q0|
# ---------------------------------------------------------------------------


def test_r2_seed_projector_matches_q0_projector():
    _, _, ref = _reference(MAIN, "b")
    q0 = np.ones(3, dtype=complex) / np.sqrt(3.0)
    expected = np.outer(q0, q0.conj())
    assert np.allclose(ref["seed_projector"], expected, atol=1e-8)


# ---------------------------------------------------------------------------
# R3 — exact N eigenvalue-function oracle and strict ordering
# ---------------------------------------------------------------------------


def test_r3_h_n_ordering_and_oracle():
    params = MAIN
    h_val_minus = _h_n_oracle(-1, params["delta"], params["nu_b"])
    h_val_zero = _h_n_oracle(0, params["delta"], params["nu_b"])
    h_val_plus = _h_n_oracle(+1, params["delta"], params["nu_b"])
    assert h_val_minus < h_val_zero < h_val_plus

    _, _, ref = _reference(params, "b")
    mean = (h_val_minus + h_val_zero + h_val_plus) / 3.0
    expected_eigvals = np.array([h_val_minus - mean, h_val_zero - mean, h_val_plus - mean])
    assert np.allclose(ref["ordered_eigenvalues"], expected_eigvals, atol=1e-9)


# ---------------------------------------------------------------------------
# R4 — common commutant dimension 1 (test-only linear algebra)
# ---------------------------------------------------------------------------


def _commutant_dimension(mats, d=3, tol=1e-8):
    identity = np.eye(d, dtype=complex)
    rows = [np.kron(h, identity) - np.kron(identity, h.T) for h in mats]
    stacked = np.vstack(rows)
    singular_values = np.linalg.svd(stacked, compute_uv=False)
    return int(np.sum(singular_values < tol))


def test_r4_common_commutant_is_trivial():
    h_q, h_n = _context_pair(MAIN, "b")
    assert _commutant_dimension([h_q, h_n]) == 1


# ---------------------------------------------------------------------------
# R5 — extracted ordered projectors match the computational basis
# ---------------------------------------------------------------------------


def test_r5_ordered_projectors_match_computational_basis():
    _, _, ref = _reference(MAIN, "b")
    identity3 = IDENTITY3
    for n, projector in enumerate(ref["ordered_projectors"]):
        expected = np.outer(identity3[:, n], identity3[:, n].conj())
        assert np.allclose(projector, expected, atol=1e-8)


# ---------------------------------------------------------------------------
# R6 — equal-modulus gate passes on the declared family (implicit: no raise)
# ---------------------------------------------------------------------------


def test_r6_equal_modulus_gate_passes_on_declared_family():
    for params in (MAIN, ASYM):
        for side in ("a", "b"):
            _reference(params, side)  # must not raise


# ---------------------------------------------------------------------------
# R7-R10 — PVM orthogonality, resolution of identity, cyclic covariance, U^3=I
# ---------------------------------------------------------------------------


def test_r7_r10_pvm_exact_properties():
    _, _, ref = _reference(MAIN, "b")
    pvm = ref["pvm"]
    identity3 = IDENTITY3
    u = ref["cycle_unitary"]

    for j in range(3):
        for k in range(3):
            expected = pvm[k] if j == k else np.zeros((3, 3), dtype=complex)
            assert np.allclose(pvm[j] @ pvm[k], expected, atol=1e-8)

    assert np.allclose(sum(pvm), identity3, atol=1e-8)

    for k in range(3):
        assert np.allclose(pvm[(k + 1) % 3], u @ pvm[k] @ u.conj().T, atol=1e-8)

    assert np.allclose(np.linalg.matrix_power(u, 3), identity3, atol=1e-8)


# ---------------------------------------------------------------------------
# R11 — local basis covariance modulo affine Z3 gauge
# ---------------------------------------------------------------------------


def _random_unitary(d, seed):
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(m)
    phases = np.diag(r) / np.abs(np.diag(r))
    return q * phases


def test_r11_local_basis_covariance_modulo_affine_gauge():
    params = MAIN
    reductions = _reductions(params)
    q = _oracle_q()
    n = _oracle_n()
    gamma, mu_b, delta, nu_b = params["gamma"], params["mu_b"], params["delta"], params["nu_b"]

    v_b = _random_unitary(3, 7)
    v_c = _random_unitary(2, 8)
    v_d = _random_unitary(2, 9)

    q_prime = v_b @ q @ v_b.conj().T
    n_prime = v_b @ n @ v_b.conj().T
    z_c_prime = v_c @ PAULI_Z @ v_c.conj().T
    z_d_prime = v_d @ PAULI_Z @ v_d.conj().T

    rho_bc_prime = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + gamma * np.kron(IDENTITY3, z_c_prime)
        + mu_b * np.kron(q_prime, z_c_prime)
    )
    rho_bd_prime = (1.0 / 6.0) * (
        np.kron(IDENTITY3, IDENTITY2) + delta * np.kron(IDENTITY3, z_d_prime)
        + nu_b * np.kron(n_prime, z_d_prime)
    )

    h_q_prime, h_n_prime = projected_modular_context_pair(rho_bc_prime, rho_bd_prime, **_core_kwargs())
    ref_prime = derived_z3_relational_reference(
        h_q_prime, h_n_prime, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
        equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )

    _, _, ref = _reference(params, "b")
    expected_pvm = [v_b @ e @ v_b.conj().T for e in ref["pvm"]]

    found = False
    for offset in (0, 1, 2):
        for orientation in (-1, 1):
            relabeled = relabel_z3_reference_pvm(ref_prime["pvm"], offset=offset, orientation=orientation)
            if all(np.allclose(relabeled[k], expected_pvm[k], atol=1e-6) for k in range(3)):
                found = True
                break
        if found:
            break
    assert found, "no affine Z3 relabeling reconciles the transformed PVM with V_B pvm V_B^dagger"


# ---------------------------------------------------------------------------
# R12 — amplitude asymmetry
# ---------------------------------------------------------------------------


def test_r12_amplitude_asymmetry_differs_but_pvm_compatible():
    delta_q_a = _delta_q_oracle(ASYM["gamma"], ASYM["mu_a"])
    delta_q_b = _delta_q_oracle(ASYM["gamma"], ASYM["mu_b"])
    assert not np.isclose(delta_q_a, delta_q_b)

    _, h_n_a = _context_pair(ASYM, "a")
    _, h_n_b = _context_pair(ASYM, "b")
    assert not np.allclose(np.linalg.eigvalsh(h_n_a), np.linalg.eigvalsh(h_n_b))

    # both sides still yield a valid derived reference (PVM structure compatible).
    _reference(ASYM, "a")
    _reference(ASYM, "b")


# ---------------------------------------------------------------------------
# R13 — weighted-projection sensitivity
# ---------------------------------------------------------------------------


def test_r13_weighted_projection_preserves_projectors_not_amplitudes():
    """The weighted rule (spec §32) may permute WHICH Z3 label (0,1,2) is
    assigned to which computational-basis projector relative to the
    tracial rule (both are valid Z3 labelings; spec §17 explicitly
    anticipates this residual affine ambiguity). What must be preserved
    is the underlying SET of three orthogonal rank-1 projectors (i.e.
    `H_N`'s eigenbasis and `H_Q`'s extremal eigenvector), not a specific
    numeric order; amplitudes are allowed, and expected, to differ.
    """
    from cosmotgg.core.modular import modular_hamiltonian
    from cosmotgg.core.states import traceless_part

    reductions = _reductions(MAIN)
    rho_bc = reductions["rho_bc"]
    rho_bd = reductions["rho_bd"]
    k_bc = modular_hamiltonian(rho_bc, **_core_kwargs())
    k_bd = modular_hamiltonian(rho_bd, **_core_kwargs())

    rho_c_marginal = np.trace(rho_bc.reshape(3, 2, 3, 2), axis1=0, axis2=2)
    rho_d_marginal = np.trace(rho_bd.reshape(3, 2, 3, 2), axis1=0, axis2=2)

    # E_weighted[i,j] = sum_{a,b} K_tensor[i,a,j,b] * rho_C[b,a]
    # (weight by the marginal of the traced-out factor C/D, spec §32).
    weighted_e_q = np.einsum(
        "iajb,ba->ij", k_bc.reshape(3, 2, 3, 2), rho_c_marginal
    )
    weighted_e_n = np.einsum(
        "iajb,ba->ij", k_bd.reshape(3, 2, 3, 2), rho_d_marginal
    )
    h_q_weighted = traceless_part(weighted_e_q)
    h_n_weighted = traceless_part(weighted_e_n)

    ref_weighted = derived_z3_relational_reference(
        h_q_weighted, h_n_weighted, hermiticity_tolerance=TOL,
        spectral_tolerance=SPECTRAL_TOL, equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )
    h_q_tracial, h_n_tracial = _context_pair(MAIN, "b")
    ref_tracial = derived_z3_relational_reference(
        h_q_tracial, h_n_tracial, hermiticity_tolerance=TOL,
        spectral_tolerance=SPECTRAL_TOL, equal_modulus_tolerance=EQUAL_MODULUS_TOL,
    )

    # Same set of three orthogonal projectors, modulo affine Z3 relabeling.
    found = False
    for offset in (0, 1, 2):
        for orientation in (-1, 1):
            relabeled = relabel_z3_reference_pvm(ref_weighted["pvm"], offset=offset, orientation=orientation)
            if all(np.allclose(relabeled[k], ref_tracial["pvm"][k], atol=1e-6) for k in range(3)):
                found = True
                break
        if found:
            break
    assert found, "weighted PVM is not the tracial PVM up to an affine Z3 relabeling"

    # Same eigenbasis (projector SET), but amplitudes (the operators
    # themselves) differ: ROBUST_MODULAR_AMPLITUDE = NO.
    assert not np.allclose(h_q_weighted, h_q_tracial, atol=1e-8)
    assert not np.allclose(h_n_weighted, h_n_tracial, atol=1e-8)


# ---------------------------------------------------------------------------
# F1 — absence of Q-branch context (TEST_ONLY_OFF_CONTRACT)
# ---------------------------------------------------------------------------


def test_f1_missing_q_context_fails_reference_extraction():
    gamma = MAIN["gamma"]
    rho_xc_off_contract = (1.0 / 6.0) * (np.kron(IDENTITY3, IDENTITY2) + gamma * np.kron(IDENTITY3, PAULI_Z))
    reductions = _reductions(MAIN)
    rho_xd_valid = reductions["rho_bd"]

    h_q, h_n = projected_modular_context_pair(rho_xc_off_contract, rho_xd_valid, **_core_kwargs())
    assert np.allclose(h_q, np.zeros((3, 3)), atol=1e-10)

    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


# ---------------------------------------------------------------------------
# F2 — absence of N-branch context (TEST_ONLY_OFF_CONTRACT)
# ---------------------------------------------------------------------------


def test_f2_missing_n_context_fails_reference_extraction():
    delta = MAIN["delta"]
    rho_xd_off_contract = (1.0 / 6.0) * (np.kron(IDENTITY3, IDENTITY2) + delta * np.kron(IDENTITY3, PAULI_Z))
    reductions = _reductions(MAIN)
    rho_xc_valid = reductions["rho_bc"]

    h_q, h_n = projected_modular_context_pair(rho_xc_valid, rho_xd_off_contract, **_core_kwargs())
    assert np.allclose(h_n, np.zeros((3, 3)), atol=1e-10)

    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


# ---------------------------------------------------------------------------
# F3 — unequal-modulus seed (test-only)
# ---------------------------------------------------------------------------


def test_f3_unequal_modulus_seed_fails_equal_modulus_gate():
    _, h_n = _context_pair(MAIN, "b")
    # h_q_bad: unique maximal eigenvector is a computational basis vector
    # (not the equal-modulus q0), so the equal-modulus gate must fail.
    h_q_bad = np.diag([1.0, 0.0, -1.0]).astype(complex)

    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q_bad, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


# ---------------------------------------------------------------------------
# F6 — affine Z3 relabeling
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("offset,orientation", [(0, 1), (1, 1), (2, 1), (0, -1), (1, -1), (2, -1)])
def test_f6_relabel_is_a_deterministic_bijection(offset, orientation):
    _, _, ref = _reference(MAIN, "b")
    pvm = ref["pvm"]
    relabeled = relabel_z3_reference_pvm(pvm, offset=offset, orientation=orientation)
    assert len(relabeled) == 3
    # every original element appears exactly once among the relabeled tuple.
    for original in pvm:
        assert any(np.allclose(original, candidate, atol=1e-12) for candidate in relabeled)


def test_f6_relabel_rejects_bool_and_out_of_range():
    _, _, ref = _reference(MAIN, "b")
    pvm = ref["pvm"]
    with pytest.raises(ValueError):
        relabel_z3_reference_pvm(pvm, offset=True, orientation=1)
    with pytest.raises(ValueError):
        relabel_z3_reference_pvm(pvm, offset=3, orientation=1)
    with pytest.raises(ValueError):
        relabel_z3_reference_pvm(pvm, offset=0, orientation=2)
    with pytest.raises(ValueError):
        relabel_z3_reference_pvm(pvm, offset=0, orientation=True)
    with pytest.raises(ValueError):
        relabel_z3_reference_pvm((pvm[0], pvm[1]), offset=0, orientation=1)


# ---------------------------------------------------------------------------
# Malformed input rejection
# ---------------------------------------------------------------------------


def test_projected_modular_context_pair_rejects_wrong_shape():
    with pytest.raises(ValueError):
        projected_modular_context_pair(np.eye(5, dtype=complex), np.eye(6, dtype=complex), **_core_kwargs())
    with pytest.raises(ValueError):
        projected_modular_context_pair(np.eye(6, dtype=complex), np.eye(5, dtype=complex), **_core_kwargs())


def test_derived_z3_relational_reference_rejects_degenerate_h_n():
    h_q, _ = _context_pair(MAIN, "b")
    h_n_degenerate = np.zeros((3, 3), dtype=complex)
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n_degenerate, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


def test_derived_z3_relational_reference_rejects_degenerate_h_q_maximum():
    _, h_n = _context_pair(MAIN, "b")
    h_q_degenerate = np.zeros((3, 3), dtype=complex)
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q_degenerate, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


def test_derived_z3_relational_reference_rejects_bad_shape():
    h_q, h_n = _context_pair(MAIN, "b")
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q[:2, :2], h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


def test_derived_z3_relational_reference_rejects_nonfinite():
    h_q, h_n = _context_pair(MAIN, "b")
    h_q_bad = h_q.copy()
    h_q_bad[0, 0] = float("nan")
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q_bad, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )


@pytest.mark.parametrize("bad_tolerance", [-1e-9, float("nan"), float("inf")], ids=["negative", "nan", "inf"])
def test_derived_z3_relational_reference_rejects_bad_tolerances(bad_tolerance):
    h_q, h_n = _context_pair(MAIN, "b")
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n, hermiticity_tolerance=bad_tolerance, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n, hermiticity_tolerance=TOL, spectral_tolerance=bad_tolerance,
            equal_modulus_tolerance=EQUAL_MODULUS_TOL,
        )
    with pytest.raises(ValueError):
        derived_z3_relational_reference(
            h_q, h_n, hermiticity_tolerance=TOL, spectral_tolerance=SPECTRAL_TOL,
            equal_modulus_tolerance=bad_tolerance,
        )


# ---------------------------------------------------------------------------
# Structural: no scipy, no private core import in this module's source.
# ---------------------------------------------------------------------------


def test_structural_reference_module_has_no_scipy_or_private_core_import():
    import ast
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[3]
        / "src" / "cosmotgg" / "models" / "model0e" / "reference.py"
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
