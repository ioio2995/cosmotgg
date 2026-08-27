"""Tests for cosmotgg.models.model0d.transport.

Fixture values used below (`chi_x`, `chi_y`, `chi_z`, `chi_0`, and the
`model0c` upstream integration fixture `alpha=0.20, gamma=0.15,
lambda_=0.20, mu=0.10`) are explicitly `NON_NORMATIVE_TEST_FIXTURE` /
`NON_NORMATIVE_UPSTREAM_INTEGRATION_FIXTURE`: purely internal-development
numerical examples. They do not close `MODEL0D_CONTEXT_FIXTURES`
(`docs/toy-models/toy0d/specification.md` §20), which remains `OPEN`.

Tests D2, D3, D6 additionally import `cosmotgg.models.model0c` for
upstream integration only (never a production dependency of
`cosmotgg.models.model0d`, checked structurally below).
"""

import ast
import inspect
from pathlib import Path

import numpy as np
import pytest

from cosmotgg.core.modular import connes_cocycle_at_minus_i_half, modular_hamiltonian
from cosmotgg.core.states import partial_trace, traceless_part
from cosmotgg.models.model0c.relative import (
    overlap_projected_noncollinearity_operator,
    overlap_relative_modular_projections,
)
from cosmotgg.models.model0c.states import three_qubit_noncollinear_overlap_relation_state
from cosmotgg.models.model0d.transport import (
    contextual_state_from_projected_generator,
    finite_relative_contextual_state_transport_guards,
    finite_relative_contextual_state_transporter,
)

# Development-only numerical tolerance for these tests; not a model0d
# scientific tolerance, not a protocol tolerance (NUMERICAL_TOLERANCES
# remains OPEN, specification §20).
TOL = 1e-9

IDENTITY2 = np.eye(2, dtype=complex)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
ZERO_2X2 = np.zeros((2, 2), dtype=complex)

# NON_NORMATIVE_TEST_FIXTURE.
CHI_X = 0.20 * PAULI_X
CHI_Y = 0.15 * PAULI_Y
CHI_Z = 0.10 * PAULI_Z
CHI_0 = ZERO_2X2

# NON_NORMATIVE_UPSTREAM_INTEGRATION_FIXTURE (reproduces the model0c
# MAIN fixture of tests/models/model0c/test_relative.py).
MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU = 0.20, 0.15, 0.20, 0.10

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL0D_SRC_DIR = REPO_ROOT / "src" / "cosmotgg" / "models" / "model0d"


def _chi_kwargs():
    return dict(hermiticity_tolerance=TOL, positivity_tolerance=TOL)


def _cocycle_kwargs():
    return dict(hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)


def _fixed_deterministic_unitary_2x2():
    """A fixed 2x2 real-orthogonal (hence unitary) matrix, test-only."""
    theta = 0.41
    return np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]],
        dtype=complex,
    )


def _polar_decomposition(f_matrix):
    """Test-only right polar decomposition `F = U P` via SVD.

    Private helper, test-only: not production, not a new scientific
    object (mandate §16). `F = W diag(s) V^dagger` (`numpy.linalg.svd`);
    `U = W V^dagger`, `P = V diag(s) V^dagger`.
    """
    w_matrix, singular_values, vh_matrix = np.linalg.svd(f_matrix)
    u_matrix = w_matrix @ vh_matrix
    p_matrix = vh_matrix.conj().T @ np.diag(singular_values) @ vh_matrix
    return u_matrix, p_matrix


# ---------------------------------------------------------------------------
# 6. contextual_state_from_projected_generator — CS1-CS11
# ---------------------------------------------------------------------------


def test_cs1_contextual_state_is_valid_density_matrix():
    omega = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    assert omega.shape == (2, 2)
    assert np.allclose(omega, omega.conj().T, atol=1e-10)
    assert np.isclose(np.trace(omega), 1.0, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(omega) > 0.0)


def test_cs2_matches_independent_eigendecomposition_oracle():
    chi = CHI_Y + CHI_Z
    eigvals, eigvecs = np.linalg.eigh(chi)
    weights = np.exp(-eigvals)
    expected = (eigvecs * (weights / weights.sum())) @ eigvecs.conj().T

    omega = contextual_state_from_projected_generator(chi, **_chi_kwargs())
    assert np.allclose(omega, expected, atol=1e-10)


def test_cs3_zero_generator_gives_maximally_mixed_state():
    omega = contextual_state_from_projected_generator(CHI_0, **_chi_kwargs())
    assert np.allclose(omega, IDENTITY2 / 2, atol=1e-12)


def test_cs4_invariant_under_additive_scalar_shift():
    scalar = 3.7
    omega = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_shifted = contextual_state_from_projected_generator(
        CHI_X + scalar * IDENTITY2, **_chi_kwargs()
    )
    assert np.allclose(omega, omega_shifted, atol=1e-10)


def test_cs5_covariance_under_unitary_conjugation():
    u_matrix = _fixed_deterministic_unitary_2x2()
    chi = CHI_X + CHI_Y
    omega = contextual_state_from_projected_generator(chi, **_chi_kwargs())
    omega_rotated = contextual_state_from_projected_generator(
        u_matrix @ chi @ u_matrix.conj().T, **_chi_kwargs()
    )
    assert np.allclose(omega_rotated, u_matrix @ omega @ u_matrix.conj().T, atol=1e-10)


def test_cs6_accepts_generic_dimension_three():
    chi = np.diag([0.30, -0.10, 0.05]).astype(complex)
    omega = contextual_state_from_projected_generator(chi, **_chi_kwargs())
    assert omega.shape == (3, 3)
    assert np.isclose(np.trace(omega), 1.0, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(omega) > 0.0)


def test_cs7_rejects_non_hermitian_generator():
    chi = np.array([[0.2, 0.3], [0.0, -0.2]], dtype=complex)
    with pytest.raises(ValueError):
        contextual_state_from_projected_generator(chi, **_chi_kwargs())


def test_cs8_rejects_non_square_generator():
    chi = np.zeros((2, 3), dtype=complex)
    with pytest.raises(ValueError):
        contextual_state_from_projected_generator(chi, **_chi_kwargs())


@pytest.mark.parametrize(
    "bad_value", [float("nan"), float("inf"), float("-inf")], ids=["nan", "inf", "-inf"]
)
def test_cs9_rejects_non_finite_generator(bad_value):
    chi = np.array([[bad_value, 0.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(ValueError):
        contextual_state_from_projected_generator(chi, **_chi_kwargs())


def test_cs10_rejects_near_boundary_state_for_explicit_tolerance():
    # Well conditioned under a tiny, explicit tolerance.
    chi = 5.0 * PAULI_Z
    omega = contextual_state_from_projected_generator(chi, **_chi_kwargs())
    assert omega[0, 0].real < 1e-3

    # Fails closed, without repair, under a larger, still explicit tolerance.
    with pytest.raises(ValueError):
        contextual_state_from_projected_generator(
            chi, hermiticity_tolerance=TOL, positivity_tolerance=1e-3
        )


def test_cs11_tolerances_are_keyword_only_and_mandatory():
    signature = inspect.signature(contextual_state_from_projected_generator)
    for name in ("hermiticity_tolerance", "positivity_tolerance"):
        parameter = signature.parameters[name]
        assert parameter.kind == inspect.Parameter.KEYWORD_ONLY
        assert parameter.default is inspect.Parameter.empty

    with pytest.raises(TypeError):
        contextual_state_from_projected_generator(CHI_X)


# ---------------------------------------------------------------------------
# 7. finite_relative_contextual_state_transporter — FT1-FT8
# ---------------------------------------------------------------------------


def test_ft1_transporter_matches_core_half_point_primitive_directly():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    expected = connes_cocycle_at_minus_i_half(omega_target, omega_source, **_cocycle_kwargs())
    assert np.allclose(f_matrix, expected, atol=1e-12)


def test_ft2_transporter_satisfies_exact_transport_identity():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    assert np.allclose(f_matrix @ omega_source @ f_matrix.conj().T, omega_target, atol=1e-10)


def test_ft3_identity_when_source_equals_target():
    omega = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    f_matrix = finite_relative_contextual_state_transporter(omega, omega, **_cocycle_kwargs())
    assert np.allclose(f_matrix, IDENTITY2, atol=1e-10)


def test_ft4_inverse_via_direction_swap():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())

    f_source_to_target = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    f_target_to_source = finite_relative_contextual_state_transporter(
        omega_target, omega_source, **_cocycle_kwargs()
    )
    assert np.allclose(f_target_to_source @ f_source_to_target, IDENTITY2, atol=1e-10)


def test_ft5_covariance_under_unitary_conjugation():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    u_matrix = _fixed_deterministic_unitary_2x2()

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    f_rotated = finite_relative_contextual_state_transporter(
        u_matrix @ omega_source @ u_matrix.conj().T,
        u_matrix @ omega_target @ u_matrix.conj().T,
        **_cocycle_kwargs(),
    )
    assert np.allclose(f_rotated, u_matrix @ f_matrix @ u_matrix.conj().T, atol=1e-10)


def test_ft6_supports_generic_dimension_three():
    chi_source = np.diag([0.30, -0.10, 0.05]).astype(complex)
    chi_target = np.diag([-0.20, 0.15, 0.10]).astype(complex)
    omega_source = contextual_state_from_projected_generator(chi_source, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(chi_target, **_chi_kwargs())

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    assert f_matrix.shape == (3, 3)
    assert np.allclose(f_matrix @ omega_source @ f_matrix.conj().T, omega_target, atol=1e-10)


def test_ft7_rejects_nonfaithful_or_malformed_states_via_core_delegation():
    faithful_omega = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    non_faithful = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    with pytest.raises(ValueError):
        finite_relative_contextual_state_transporter(
            non_faithful, faithful_omega, **_cocycle_kwargs()
        )
    with pytest.raises(ValueError):
        finite_relative_contextual_state_transporter(
            faithful_omega, non_faithful, **_cocycle_kwargs()
        )


def test_ft8_transporter_exposes_no_flow_parameter():
    signature = inspect.signature(finite_relative_contextual_state_transporter)
    forbidden_names = {"s", "t", "tau", "time"}
    assert forbidden_names.isdisjoint(signature.parameters.keys())
    assert set(signature.parameters.keys()) == {
        "omega_source",
        "omega_target",
        "hermiticity_tolerance",
        "trace_tolerance",
        "positivity_tolerance",
    }


# ---------------------------------------------------------------------------
# 8-14. Controls D0-D6
# ---------------------------------------------------------------------------


def test_d0_identity_when_omega_source_equals_omega_target():
    omega = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    f_matrix = finite_relative_contextual_state_transporter(omega, omega, **_cocycle_kwargs())
    assert np.allclose(f_matrix, IDENTITY2, atol=1e-10)

    u_matrix, p_matrix = _polar_decomposition(f_matrix)
    assert np.allclose(u_matrix, IDENTITY2, atol=1e-10)
    assert np.allclose(p_matrix, IDENTITY2, atol=1e-10)


def test_d1_commuting_distinct_contexts():
    """FINITE_TRANSPORT_NONTRIVIAL does not imply noncommuting/orientation content."""
    omega_source = contextual_state_from_projected_generator(CHI_0, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Z, **_chi_kwargs())

    assert np.allclose(omega_source, IDENTITY2 / 2, atol=1e-12)
    assert not np.allclose(omega_target, IDENTITY2 / 2, atol=1e-6)
    assert np.allclose(omega_source @ omega_target, omega_target @ omega_source, atol=1e-10)

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    assert not np.allclose(f_matrix, IDENTITY2, atol=1e-6)
    assert np.allclose(f_matrix, f_matrix.conj().T, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(f_matrix) > 0.0)

    u_matrix, p_matrix = _polar_decomposition(f_matrix)
    assert np.allclose(u_matrix, IDENTITY2, atol=1e-8)
    assert not np.allclose(p_matrix, IDENTITY2, atol=1e-6)


def test_d2_noncommuting_contexts_pure_model0d():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    assert not np.allclose(omega_source @ omega_target, omega_target @ omega_source, atol=1e-10)

    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    assert not np.allclose(f_matrix, IDENTITY2, atol=1e-6)

    u_matrix, _ = _polar_decomposition(f_matrix)
    assert not np.allclose(u_matrix, IDENTITY2, atol=1e-6)


def test_d2_upstream_integration_consistency_with_model0c_noncollinearity():
    rho_abc = three_qubit_noncollinear_overlap_relation_state(
        MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU
    )
    chi_a, chi_c = overlap_relative_modular_projections(rho_abc, **_cocycle_kwargs())
    n_matrix = overlap_projected_noncollinearity_operator(chi_a, chi_c)
    assert not np.allclose(n_matrix, ZERO_2X2, atol=1e-8)

    omega_a = contextual_state_from_projected_generator(chi_a, **_chi_kwargs())
    omega_c = contextual_state_from_projected_generator(chi_c, **_chi_kwargs())
    f_matrix = finite_relative_contextual_state_transporter(omega_a, omega_c, **_cocycle_kwargs())

    u_matrix, _ = _polar_decomposition(f_matrix)
    assert not np.allclose(u_matrix, IDENTITY2, atol=1e-6)


def test_d3_actual_overlap_state_unchanged_negative_control():
    """TRANSPORT_IS_BETWEEN_AUXILIARY_CONTEXTUAL_STATES, NOT_SUCCESSIVE_REDUCED_STATES_OF_B.

    Mandatory negative control (spec §16, D3_ACTUAL_OVERLAP_STATE_UNCHANGED):
    the actual reduced overlap state `rho_B` is never touched by this
    transport, even though the auxiliary contextual states `omega_A`,
    `omega_C` differ and the transporter `F` is nontrivial.
    """
    rho_abc = three_qubit_noncollinear_overlap_relation_state(
        MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU
    )
    rho_b = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[1])
    assert np.allclose(rho_b, IDENTITY2 / 2, atol=1e-10)

    chi_a, chi_c = overlap_relative_modular_projections(rho_abc, **_cocycle_kwargs())
    omega_a = contextual_state_from_projected_generator(chi_a, **_chi_kwargs())
    omega_c = contextual_state_from_projected_generator(chi_c, **_chi_kwargs())
    assert not np.allclose(omega_a, omega_c, atol=1e-6)

    f_matrix = finite_relative_contextual_state_transporter(omega_a, omega_c, **_cocycle_kwargs())
    assert not np.allclose(f_matrix, IDENTITY2, atol=1e-6)

    # rho_B == I/2 is unaffected by omega_A, omega_C, or F: B does not change.
    assert np.allclose(rho_b, IDENTITY2 / 2, atol=1e-10)


def test_d4_transporter_is_not_a_cptp_channel():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    f_matrix = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **_cocycle_kwargs()
    )

    f_dagger_f = f_matrix.conj().T @ f_matrix
    assert not np.allclose(f_dagger_f, IDENTITY2, atol=1e-6)

    eigvals, eigvecs = np.linalg.eigh(f_dagger_f)
    off_one_index = int(np.argmax(np.abs(eigvals - 1.0)))
    probe_vector = eigvecs[:, off_one_index]
    sigma_probe = np.outer(probe_vector, probe_vector.conj())
    assert np.isclose(np.trace(sigma_probe).real, 1.0, atol=1e-10)

    trace_after = np.trace(f_matrix @ sigma_probe @ f_matrix.conj().T)
    assert not np.isclose(trace_after.real, 1.0, atol=1e-6)
    # NOT_CPTP_DYNAMICS.


def test_d5_composition_is_tautological_chain_rule():
    omega_a = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_c = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    omega_d = contextual_state_from_projected_generator(CHI_Z, **_chi_kwargs())

    f_ac = finite_relative_contextual_state_transporter(omega_a, omega_c, **_cocycle_kwargs())
    f_cd = finite_relative_contextual_state_transporter(omega_c, omega_d, **_cocycle_kwargs())
    f_ad = finite_relative_contextual_state_transporter(omega_a, omega_d, **_cocycle_kwargs())
    f_da = finite_relative_contextual_state_transporter(omega_d, omega_a, **_cocycle_kwargs())

    assert np.allclose(f_cd @ f_ac, f_ad, atol=1e-10)
    assert np.allclose(f_da @ f_cd @ f_ac, IDENTITY2, atol=1e-10)
    # TAUTOLOGICAL_CHAIN_RULE: no evidence for dynamics/curvature/holonomy.


def test_d6_projection_sensitivity_robust_orientation_not_robust_amplitude():
    rho_abc = three_qubit_noncollinear_overlap_relation_state(
        MAIN_ALPHA, MAIN_GAMMA, MAIN_LAMBDA, MAIN_MU
    )
    rho_ab = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[0, 1])
    rho_bc = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[1, 2])
    rho_a = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[0])
    rho_c = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[2])

    k_ab = modular_hamiltonian(rho_ab, **_cocycle_kwargs())
    k_bc = modular_hamiltonian(rho_bc, **_cocycle_kwargs())

    chi_a_tracial, chi_c_tracial = overlap_relative_modular_projections(
        rho_abc, **_cocycle_kwargs()
    )

    weighted_e_a = partial_trace(
        np.kron(rho_a, IDENTITY2) @ k_ab, dimensions=(2, 2), keep=[1]
    )
    weighted_e_c = partial_trace(
        np.kron(IDENTITY2, rho_c) @ k_bc, dimensions=(2, 2), keep=[0]
    )
    weighted_chi_a = traceless_part(weighted_e_a)
    weighted_chi_c = traceless_part(weighted_e_c)

    omega_a_tracial = contextual_state_from_projected_generator(chi_a_tracial, **_chi_kwargs())
    omega_c_tracial = contextual_state_from_projected_generator(chi_c_tracial, **_chi_kwargs())
    omega_a_weighted = contextual_state_from_projected_generator(weighted_chi_a, **_chi_kwargs())
    omega_c_weighted = contextual_state_from_projected_generator(weighted_chi_c, **_chi_kwargs())

    f_tracial = finite_relative_contextual_state_transporter(
        omega_a_tracial, omega_c_tracial, **_cocycle_kwargs()
    )
    f_weighted = finite_relative_contextual_state_transporter(
        omega_a_weighted, omega_c_weighted, **_cocycle_kwargs()
    )
    assert not np.allclose(f_weighted, f_tracial, atol=1e-6)

    u_tracial, _ = _polar_decomposition(f_tracial)
    u_weighted, _ = _polar_decomposition(f_weighted)
    assert not np.allclose(u_tracial, IDENTITY2, atol=1e-6)
    # The weighted reconstruction (§19 of the model0c specification) yields
    # a much smaller nontrivial amplitude than the tracial one (consistent
    # with ROBUST_AMPLITUDE = NO): only a tight, non-normative test
    # tolerance distinguishes it from the identity here, still far above
    # machine precision (~1e-16).
    assert not np.allclose(u_weighted, IDENTITY2, atol=1e-9, rtol=0.0)
    # ROBUST_ORIENTATION_CLASS, ROBUST_AMPLITUDE = NO: no quantitative
    # angle/amplitude comparison is made between u_tracial and u_weighted.


# ---------------------------------------------------------------------------
# 15. Numerical guards — NG1-NG5
# ---------------------------------------------------------------------------


def test_ng1_guards_return_expected_keys():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    guards = finite_relative_contextual_state_transport_guards(
        omega_source, omega_target, **_cocycle_kwargs()
    )
    expected_keys = {
        "lambda_min_source",
        "lambda_min_target",
        "sqrt_inverse_residual_source",
        "transport_residual",
        "inverse_residual",
    }
    assert expected_keys <= set(guards.keys())


def test_ng2_lambda_min_matches_eigvalsh():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    guards = finite_relative_contextual_state_transport_guards(
        omega_source, omega_target, **_cocycle_kwargs()
    )

    assert np.isclose(
        guards["lambda_min_source"], np.min(np.linalg.eigvalsh(omega_source)), atol=1e-12
    )
    assert np.isclose(
        guards["lambda_min_target"], np.min(np.linalg.eigvalsh(omega_target)), atol=1e-12
    )


def test_ng3_residuals_are_small_on_well_conditioned_fixture():
    # NON_NORMATIVE_TEST_TOLERANCE for this specific regression check only.
    residual_tolerance = 1e-8
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    guards = finite_relative_contextual_state_transport_guards(
        omega_source, omega_target, **_cocycle_kwargs()
    )

    assert guards["sqrt_inverse_residual_source"] < residual_tolerance
    assert guards["transport_residual"] < residual_tolerance
    assert guards["inverse_residual"] < residual_tolerance


def test_ng4_guards_do_not_mutate_inputs():
    omega_source = contextual_state_from_projected_generator(CHI_X, **_chi_kwargs())
    omega_target = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    omega_source_copy = omega_source.copy()
    omega_target_copy = omega_target.copy()

    finite_relative_contextual_state_transport_guards(
        omega_source, omega_target, **_cocycle_kwargs()
    )

    assert np.array_equal(omega_source, omega_source_copy)
    assert np.array_equal(omega_target, omega_target_copy)


def test_ng5_guards_fail_closed_on_non_faithful_input():
    non_faithful = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    faithful_omega = contextual_state_from_projected_generator(CHI_Y, **_chi_kwargs())
    with pytest.raises(ValueError):
        finite_relative_contextual_state_transport_guards(
            non_faithful, faithful_omega, **_cocycle_kwargs()
        )


# ---------------------------------------------------------------------------
# Structural checks: no model0c production import, no finite-flow API.
# ---------------------------------------------------------------------------


def test_structural_model0d_production_does_not_import_model0c():
    violations: list[tuple[Path, int]] = []
    for path in sorted(MODEL0D_SRC_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if any("model0c" in alias.name for alias in node.names):
                    violations.append((path, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if "model0c" in module:
                    violations.append((path, node.lineno))

    assert not violations, (
        f"forbidden model0c import found in model0d production code: {violations}"
    )


_FORBIDDEN_FLOW_IDENTIFIERS = {
    "modular_flow",
    "finite_flow",
    "evolve",
    "evolution",
    "time",
    "clock",
    "tau",
}


def test_structural_model0d_transport_exposes_no_flow_api():
    transport_path = MODEL0D_SRC_DIR / "transport.py"
    tree = ast.parse(transport_path.read_text(encoding="utf-8"), filename=str(transport_path))

    identifiers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            identifiers.add(node.id)
        elif isinstance(node, ast.FunctionDef):
            identifiers.add(node.name)
            for arg in node.args.args + node.args.kwonlyargs:
                identifiers.add(arg.arg)
        elif isinstance(node, ast.Attribute):
            identifiers.add(node.attr)

    lowered = {identifier.lower() for identifier in identifiers}
    violations = _FORBIDDEN_FLOW_IDENTIFIERS & lowered
    assert not violations, (
        f"forbidden flow-related identifier(s) found in transport.py: {violations}"
    )
