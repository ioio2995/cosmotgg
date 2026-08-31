"""Unit tests for cosmotgg.models.model1c.diagnostics.

Implementation-corroborative checks only
(`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`):
never a component of the `T5a` qualification record.
"""

import numpy as np
import pytest

from cosmotgg.models.model1c.diagnostics import (
    bell_projection_gap,
    connected_xx_correlator,
    require_faithful_state,
)
from cosmotgg.models.model1c.local_cell import SIGMA_0, SIGMA_0_NULL, sigma_0_family
from cosmotgg.models.model1c.refinement import canonical_branch_sequence

TOL = 1e-9
_LARGE_N = 60


# ---------------------------------------------------------------------------
# N1 / LOCAL-ONLY — null seed limit is I/4, C_XX -> 0 (spec §12, §13, §21)
# ---------------------------------------------------------------------------


def test_d1_null_seed_limit_is_i_over_4():
    sequence = canonical_branch_sequence(
        SIGMA_0_NULL, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    assert np.allclose(sequence[-1], np.eye(4) / 4.0, atol=1e-9)


def test_d2_local_only_null_seed_connected_correlator_vanishes():
    sequence = canonical_branch_sequence(
        SIGMA_0_NULL, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    c_xx = connected_xx_correlator(
        sequence[-1], hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert c_xx == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# RELATIONAL-LIVE — canonical seed limit has C_XX -> 1/4 exactly (spec §13,
# §21)
# ---------------------------------------------------------------------------


def test_d3_relational_live_canonical_seed_connected_correlator_is_one_quarter():
    sequence = canonical_branch_sequence(
        SIGMA_0, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    c_xx = connected_xx_correlator(
        sequence[-1], hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    assert c_xx == pytest.approx(0.25, abs=1e-9)


# ---------------------------------------------------------------------------
# N9 — anti-collapse: Bell-distinct seeds do not comparison-collapse
# (spec §15)
# ---------------------------------------------------------------------------


def test_d4_bell_projection_gap_nonzero_for_distinct_kappa():
    gap = bell_projection_gap(sigma_0_family(0.25), sigma_0_family(0.0))
    assert not np.allclose(gap, np.zeros((4, 4)), atol=TOL)


def test_d5_anti_collapse_gap_does_not_vanish_along_the_branch():
    """The two Bell-distinct branch sequences must NOT become indiscernible
    as n grows: their difference converges to the constant, nonzero
    P_BELL gap, it does not tend to zero (N9, spec §15)."""
    seq_live = canonical_branch_sequence(
        SIGMA_0, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    seq_null = canonical_branch_sequence(
        SIGMA_0_NULL, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    difference = seq_live[-1] - seq_null[-1]
    expected_gap = bell_projection_gap(SIGMA_0, SIGMA_0_NULL)
    assert not np.allclose(difference, np.zeros((4, 4)), atol=TOL)
    assert np.allclose(difference, expected_gap, atol=1e-9)


def test_d6_anti_collapse_gap_increases_relative_to_early_level():
    """At n=0 the two seeds already differ; at large n they still differ by
    the same nonzero constant gap (comparison never collapses toward zero
    as n grows)."""
    seq_live = canonical_branch_sequence(
        SIGMA_0, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    seq_null = canonical_branch_sequence(
        SIGMA_0_NULL, _LARGE_N, hermiticity_tolerance=TOL, trace_tolerance=TOL,
        positivity_tolerance=TOL,
    )
    norm_at_large_n = np.linalg.norm(seq_live[-1] - seq_null[-1])
    assert norm_at_large_n == pytest.approx(np.linalg.norm(bell_projection_gap(SIGMA_0, SIGMA_0_NULL)), abs=1e-9)
    assert norm_at_large_n > 1e-3


# ---------------------------------------------------------------------------
# Faithfulness (spec §16): faithful seed remains faithful along the branch
# ---------------------------------------------------------------------------


def test_d7_faithful_seed_remains_faithful_along_the_branch():
    sequence = canonical_branch_sequence(
        SIGMA_0, 6, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
    )
    for state in sequence:
        validated = require_faithful_state(
            state, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )
        assert np.linalg.eigvalsh(validated).min() > 0.0


def test_d8_require_faithful_state_rejects_non_faithful_state():
    non_faithful = np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex)
    with pytest.raises(ValueError):
        require_faithful_state(
            non_faithful, hermiticity_tolerance=TOL, trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


# ---------------------------------------------------------------------------
# Fail-closed on malformed input
# ---------------------------------------------------------------------------


def test_d9_connected_xx_correlator_rejects_wrong_shape():
    with pytest.raises(ValueError):
        connected_xx_correlator(
            np.eye(3, dtype=complex) / 3.0,
            hermiticity_tolerance=TOL,
            trace_tolerance=TOL,
            positivity_tolerance=TOL,
        )


def test_d10_connected_xx_correlator_rejects_invalid_density_matrix():
    bad = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)  # trace 2
    with pytest.raises(ValueError):
        connected_xx_correlator(
            bad, hermiticity_tolerance=TOL, trace_tolerance=TOL, positivity_tolerance=TOL
        )


def test_d11_bell_projection_gap_rejects_malformed_input():
    with pytest.raises(ValueError):
        bell_projection_gap(np.eye(3), SIGMA_0_NULL)
