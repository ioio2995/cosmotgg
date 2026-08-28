"""Unit tests for cosmotgg.models.model1b.hierarchy.

`STATE_COMPOSITION_CONTROL`: `PARTIAL_TRACE_ASSOCIATIVITY !=
EMERGENT_GEOMETRY_EVIDENCE` (spec §15). These tests are implementation
regression guards only, never scientific/geometric evidence.
"""

import numpy as np
import pytest

from cosmotgg.models.model1b.hierarchy import (
    E_0,
    E_1,
    E_2,
    FINE_DIMENSIONS,
    FINE_SITE_ORDER,
    LEVEL_0_SITES,
    LEVEL_1_SITES,
    reduce_to_level_0,
    reduce_to_level_0_direct,
    reduce_to_level_1,
)


def _deterministic_hermitian_density_matrix(dim: int) -> np.ndarray:
    """Deterministic faithful density matrix of shape `(dim, dim)`, no RNG."""
    rows = np.arange(dim).reshape(dim, 1)
    cols = np.arange(dim).reshape(1, dim)
    base = (rows + 1j * cols) / (dim + 1.0)
    hermitian = base + base.conj().T
    # Shift to strictly positive spectrum, then normalize to unit trace.
    eigvals, eigvecs = np.linalg.eigh(hermitian)
    shifted = eigvals - eigvals.min() + 1.0
    weights = shifted / shifted.sum()
    return (eigvecs * weights) @ eigvecs.conj().T


# ---------------------------------------------------------------------------
# Declared fixed site labeling and cumulative eliminated sets (spec §6)
# ---------------------------------------------------------------------------


def test_h1_fine_site_order_and_dimensions():
    assert FINE_SITE_ORDER == ("A", "X", "Y", "B", "C", "P", "Q", "D")
    assert FINE_DIMENSIONS == (2,) * 8


def test_h2_level_sites_declared():
    assert LEVEL_1_SITES == ("A", "X", "Y", "B", "C", "D")
    assert LEVEL_0_SITES == ("A", "B", "C", "D")


def test_h3_cumulative_eliminated_sets():
    assert E_2 == frozenset()
    assert E_1 == frozenset({"P", "Q"})
    assert E_0 == frozenset({"P", "Q", "X", "Y"})
    # E_0 superset E_1 superset E_2 (nested, coarser levels eliminate more).
    assert E_2 <= E_1 <= E_0


# ---------------------------------------------------------------------------
# Deterministic reductions via cosmotgg.core.states.partial_trace
# ---------------------------------------------------------------------------


def test_h4_reduce_to_level_1_shape_and_determinism():
    rho_2 = _deterministic_hermitian_density_matrix(256)
    rho_1_a = reduce_to_level_1(rho_2)
    rho_1_b = reduce_to_level_1(rho_2)
    assert rho_1_a.shape == (64, 64)
    assert np.allclose(rho_1_a, rho_1_b)


def test_h5_reduce_to_level_0_shape():
    rho_2 = _deterministic_hermitian_density_matrix(256)
    rho_1 = reduce_to_level_1(rho_2)
    rho_0 = reduce_to_level_0(rho_1)
    assert rho_0.shape == (16, 16)


def test_h6_reduce_to_level_0_direct_shape():
    rho_2 = _deterministic_hermitian_density_matrix(256)
    rho_0_direct = reduce_to_level_0_direct(rho_2)
    assert rho_0_direct.shape == (16, 16)


def test_h7_state_composition_control_sequential_equals_direct():
    """STATE_FLOW_PATH_INDEPENDENCE = SATISFIED_BY_CONSTRUCTION (spec §15):
    implementation regression guard only, not geometry evidence."""
    rho_2 = _deterministic_hermitian_density_matrix(256)
    rho_1 = reduce_to_level_1(rho_2)
    rho_0_sequential = reduce_to_level_0(rho_1)
    rho_0_direct = reduce_to_level_0_direct(rho_2)
    assert np.allclose(rho_0_sequential, rho_0_direct, atol=1e-10)


def test_h8_reduction_preserves_trace():
    rho_2 = _deterministic_hermitian_density_matrix(256)
    rho_1 = reduce_to_level_1(rho_2)
    rho_0 = reduce_to_level_0(rho_1)
    assert np.trace(rho_2) == pytest.approx(1.0, abs=1e-10)
    assert np.trace(rho_1) == pytest.approx(1.0, abs=1e-10)
    assert np.trace(rho_0) == pytest.approx(1.0, abs=1e-10)


# ---------------------------------------------------------------------------
# Fail-closed domain guards
# ---------------------------------------------------------------------------


def test_h9_reduce_to_level_1_rejects_wrong_shape():
    with pytest.raises(ValueError):
        reduce_to_level_1(np.eye(64, dtype=complex))


def test_h10_reduce_to_level_0_rejects_wrong_shape():
    with pytest.raises(ValueError):
        reduce_to_level_0(np.eye(256, dtype=complex))


def test_h11_reduce_to_level_0_direct_rejects_wrong_shape():
    with pytest.raises(ValueError):
        reduce_to_level_0_direct(np.eye(64, dtype=complex))


def test_h12_reduce_to_level_1_rejects_non_finite_entries():
    rho_2 = np.eye(256, dtype=complex)
    rho_2[0, 0] = float("nan")
    with pytest.raises(ValueError):
        reduce_to_level_1(rho_2)
