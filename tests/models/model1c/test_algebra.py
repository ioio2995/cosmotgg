"""Unit tests for cosmotgg.models.model1c.algebra.

Implementation-corroborative checks only
(`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`):
never a component of the `T5a` qualification record.
"""

import numpy as np
import pytest

from cosmotgg.models.model1c.algebra import (
    BELL_PROJECTORS,
    G_BELL,
    G_BELL_LABELS,
    PAULI_STACK,
    p_bell,
    p_bell_via_projectors,
)

TOL = 1e-9


def _random_hermitian(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    return a + a.conj().T


# ---------------------------------------------------------------------------
# G_BELL = {II, XX, ZZ, YY} — unitary, hermitian, involutive (spec §5)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("label", G_BELL_LABELS)
def test_a1_generator_unitary_hermitian_involutive(label):
    g = G_BELL[label]
    assert np.allclose(g @ g.conj().T, np.eye(4), atol=TOL)
    assert np.allclose(g, g.conj().T, atol=TOL)
    assert np.allclose(g @ g, np.eye(4), atol=TOL)


def test_a2_pauli_stack_identity_first():
    assert np.allclose(PAULI_STACK[0], np.eye(2))


# ---------------------------------------------------------------------------
# Bell projectors Pi_k — sum to I, pairwise orthogonal (spec §5)
# ---------------------------------------------------------------------------


def test_a3_bell_projectors_sum_to_identity():
    total = sum(BELL_PROJECTORS)
    assert np.allclose(total, np.eye(4), atol=TOL)


def test_a4_bell_projectors_pairwise_orthogonal():
    for i, pi_i in enumerate(BELL_PROJECTORS):
        for j, pi_j in enumerate(BELL_PROJECTORS):
            if i != j:
                assert np.allclose(pi_i @ pi_j, np.zeros((4, 4)), atol=TOL)


def test_a5_bell_projectors_rank_one_idempotent():
    for pi in BELL_PROJECTORS:
        assert np.allclose(pi @ pi, pi, atol=TOL)
        assert np.trace(pi).real == pytest.approx(1.0, abs=TOL)


# ---------------------------------------------------------------------------
# p_bell — equivalence with p_bell_via_projectors, idempotence (spec §5, §7)
# ---------------------------------------------------------------------------


def test_a6_p_bell_matches_projector_form_generic_hermitian():
    rho = _random_hermitian(0)
    assert np.allclose(p_bell(rho), p_bell_via_projectors(rho), atol=1e-10)


def test_a7_p_bell_idempotent():
    rho = _random_hermitian(1)
    once = p_bell(rho)
    twice = p_bell(once)
    assert np.allclose(once, twice, atol=1e-10)


def test_a8_p_bell_fixes_generators():
    for label in G_BELL_LABELS:
        g = G_BELL[label]
        assert np.allclose(p_bell(g), g, atol=TOL)


def test_a9_p_bell_annihilates_local_xi():
    xi = np.kron(PAULI_STACK[1], PAULI_STACK[0])
    assert np.allclose(p_bell(xi), np.zeros((4, 4)), atol=TOL)


# ---------------------------------------------------------------------------
# Fail-closed on malformed input
# ---------------------------------------------------------------------------


def test_a10_p_bell_rejects_wrong_shape():
    with pytest.raises(ValueError):
        p_bell(np.eye(3))


def test_a11_p_bell_rejects_non_finite():
    bad = np.eye(4, dtype=complex)
    bad[0, 0] = np.nan
    with pytest.raises(ValueError):
        p_bell(bad)
