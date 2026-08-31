"""Unit tests for cosmotgg.models.model1c.refinement.

Implementation-corroborative checks only
(`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`):
never a component of the `T5a` qualification record.
"""

import numpy as np
import pytest

from cosmotgg.core.states import partial_trace
from cosmotgg.models.model1c.local_cell import (
    SIGMA_0,
    SIGMA_0_NULL,
    local_refinement_cell,
    phi,
)
from cosmotgg.models.model1c.oracle import phi_pow_closed_form
from cosmotgg.models.model1c.refinement import canonical_branch_sequence, global_refinement

TOL = 1e-9


# ---------------------------------------------------------------------------
# canonical_branch_sequence — length, first entry, equals phi_pow_closed_form
# (mandate: canonical_branch_sequence = phi_pow_closed_form)
# ---------------------------------------------------------------------------


def test_r1_sequence_length_and_first_entry():
    n_max = 4
    sequence = canonical_branch_sequence(
        SIGMA_0, n_max, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert len(sequence) == n_max + 1
    assert np.array_equal(sequence[0], SIGMA_0)


@pytest.mark.parametrize("seed", [SIGMA_0, SIGMA_0_NULL])
def test_r2_sequence_matches_phi_pow_closed_form_at_every_level(seed):
    n_max = 6
    sequence = canonical_branch_sequence(
        seed, n_max, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    for n, value in enumerate(sequence):
        expected = phi_pow_closed_form(
            seed, n, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
        assert np.allclose(value, expected, atol=1e-9)


def test_r3_sequence_step_is_exactly_phi():
    n_max = 3
    sequence = canonical_branch_sequence(
        SIGMA_0, n_max, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    for n in range(n_max):
        stepped = phi(
            sequence[n], hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
        assert np.array_equal(stepped, sequence[n + 1])


# ---------------------------------------------------------------------------
# N3 — relabeling invariance: python int vs numpy integer give the same
# result (verdict independent of index labeling, spec §17)
# ---------------------------------------------------------------------------


def test_r4_relabeling_invariance_int_vs_numpy_integer():
    a = canonical_branch_sequence(
        SIGMA_0, 5, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    b = canonical_branch_sequence(
        SIGMA_0, np.int64(5), hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    for va, vb in zip(a, b):
        assert np.array_equal(va, vb)


# ---------------------------------------------------------------------------
# Structural closure corroboration (spec §10, T5A-C3): global_refinement
# reduced to the canonical branch cell matches canonical_branch_sequence /
# local_cell.phi, INCLUDING on an explicitly correlated global state.
# ---------------------------------------------------------------------------


def test_r5_closure_corroboration_n0_to_1():
    rho1 = global_refinement(
        SIGMA_0, 0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert rho1.shape == (16, 16)
    extracted = partial_trace(rho1, dimensions=(4, 4), keep=(0,))
    expected = phi(SIGMA_0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL)
    assert np.allclose(extracted, expected, atol=1e-10)

    sequence = canonical_branch_sequence(
        SIGMA_0, 1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.allclose(extracted, sequence[1], atol=1e-10)


def test_r6_closure_corroboration_n1_to_2_on_correlated_global_state():
    """Closure lemma corroboration on an EXPLICITLY inter-cell-correlated
    global state (mandate item 6: 'closure on explicitly correlated global
    state'). `rho_level1 = R_cell(SIGMA_0)` is a genuinely correlated
    two-cell state (U entangles system and ancilla): it is verified below
    to NOT be a product state before being used as `global_refinement`'s
    input, ruling out the forbidden 'local marginal -> independent
    refinement -> retensoring' shortcut trivially satisfying the identity."""
    rho_level1 = local_refinement_cell(
        SIGMA_0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    i_system = partial_trace(rho_level1, dimensions=(4, 4), keep=(0,))
    i_ancilla = partial_trace(rho_level1, dimensions=(4, 4), keep=(1,))
    product_state = np.kron(i_system, i_ancilla)
    assert not np.allclose(rho_level1, product_state, atol=1e-6), (
        "fixture must be genuinely correlated for this corroboration to be meaningful"
    )

    rho2 = global_refinement(
        rho_level1, 1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert rho2.shape == (256, 256)

    extracted = partial_trace(rho2, dimensions=(4, 4, 4, 4), keep=(0,))
    expected = phi(
        i_system, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.allclose(extracted, expected, atol=1e-9)


def test_r7_global_refinement_preserves_trace_and_positivity():
    rho2 = global_refinement(
        SIGMA_0, 0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.trace(rho2).real == pytest.approx(1.0, abs=1e-10)
    assert np.linalg.eigvalsh(rho2).min() >= -1e-10


# ---------------------------------------------------------------------------
# N6 — no per-level free parameter: U/alpha embedded by global_refinement
# are exactly controlled_bell_unitary()'s fixed constant, for every n.
# ---------------------------------------------------------------------------


def test_r8_global_refinement_at_n0_matches_local_refinement_cell_exactly():
    """N6 support: global_refinement(rho, 0) must be bit-identical to
    local_refinement_cell(rho) (same fixed U/alpha, no per-level parameter
    or retuning introduced by the multi-cell code path)."""
    rho2_global = global_refinement(
        SIGMA_0, 0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    rho2_local = local_refinement_cell(
        SIGMA_0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert np.allclose(rho2_global, rho2_local, atol=1e-10)


# ---------------------------------------------------------------------------
# Fail-closed on invalid input
# ---------------------------------------------------------------------------


def test_r9_canonical_branch_sequence_rejects_negative_n_max():
    with pytest.raises(ValueError):
        canonical_branch_sequence(
            SIGMA_0, -1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_r10_canonical_branch_sequence_rejects_invalid_seed():
    bad = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    with pytest.raises(ValueError):
        canonical_branch_sequence(
            bad, 2, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_r11_global_refinement_rejects_wrong_dimension_for_level():
    bad = np.eye(4, dtype=complex) / 4.0  # dim 4, but n=1 expects dim 16
    with pytest.raises(ValueError):
        global_refinement(
            bad, 1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_r12_global_refinement_rejects_negative_n():
    with pytest.raises(ValueError):
        global_refinement(
            SIGMA_0, -1, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_r13_global_refinement_rejects_invalid_density_matrix():
    bad = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)  # trace 2, dim matches n=0
    with pytest.raises(ValueError):
        global_refinement(
            bad, 0, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
