"""model1b fixed fine site labeling and decimation hierarchy.

Normative source: `docs/toy-models/toy1b/specification.md` §5-§6, §15.

This module declares the single canonical fine site labeling and order
`(A, X, Y, B, C, P, Q, D)` (eight qubit factors, `Gamma_2`), the cumulative
eliminated-site sets `E_2 = empty`, `E_1 = {P, Q}`, `E_0 = {P, Q, X, Y}`
(spec §6), and the three decimation reductions `rho_1 = Tr_{P,Q}(rho_2)`,
`rho_0 = Tr_{X,Y}(rho_1)`, and the direct control `rho_0_direct =
Tr_{P,Q,X,Y}(rho_2)`, delegated entirely to
`cosmotgg.core.states.partial_trace` (no duplicated trace logic, no
independently constructed coarse state).

`STATE_FLOW_PATH_INDEPENDENCE = SATISFIED_BY_CONSTRUCTION` (spec §15): the
agreement between `reduce_to_level_0(reduce_to_level_1(rho_2))` and
`reduce_to_level_0_direct(rho_2)` is an algebraic consequence of partial
trace composition, not independent evidence of emergent geometry
(`PARTIAL_TRACE_ASSOCIATIVITY != EMERGENT_GEOMETRY_EVIDENCE`).

This module builds no Hamiltonian, no Gibbs state
(`cosmotgg.models.model1b.states`), no modular datum
(`cosmotgg.models.model1b.modular_support`), no directional/loop diagnostic
(`cosmotgg.models.model1b.directional`).
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import partial_trace

FINE_SITE_ORDER = ("A", "X", "Y", "B", "C", "P", "Q", "D")
FINE_DIMENSIONS = (2,) * len(FINE_SITE_ORDER)

LEVEL_1_SITES = ("A", "X", "Y", "B", "C", "D")
LEVEL_0_SITES = ("A", "B", "C", "D")

LEVEL_1_DIMENSIONS = (2,) * len(LEVEL_1_SITES)
LEVEL_0_DIMENSIONS = (2,) * len(LEVEL_0_SITES)

# Cumulative eliminated-site sets (spec §6). Declared before any reduction,
# relative to the single fixed fine labeling `FINE_SITE_ORDER` above.
E_2 = frozenset()
E_1 = frozenset({"P", "Q"})
E_0 = frozenset({"P", "Q", "X", "Y"})


def _keep_indices(source_order, target_sites) -> list[int]:
    """Deterministic, ascending `keep` indices of `target_sites` within
    `source_order` (required by `partial_trace`'s no-implicit-permutation
    contract)."""
    index_of = {label: i for i, label in enumerate(source_order)}
    missing = [label for label in target_sites if label not in index_of]
    if missing:
        raise ValueError(f"unknown site label(s) {missing}, not in {source_order}")
    return sorted(index_of[label] for label in target_sites)


def _validate_state_shape(rho, expected_dim: int, *, name: str) -> np.ndarray:
    arr = np.asarray(rho)
    if arr.ndim != 2 or arr.shape != (expected_dim, expected_dim):
        raise ValueError(
            f"{name} must have shape ({expected_dim}, {expected_dim}), got shape={arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr.astype(complex, copy=False)


def reduce_to_level_1(rho_2) -> np.ndarray:
    """`rho_1 = Tr_{P,Q}(rho_2)`, surviving sites `(A, X, Y, B, C, D)` (spec §6).

    `rho_2` must have shape `(256, 256)` (eight declared fine qubit factors);
    otherwise this function fails closed with `ValueError`.
    """
    arr = _validate_state_shape(rho_2, 2 ** len(FINE_SITE_ORDER), name="rho_2")
    keep = _keep_indices(FINE_SITE_ORDER, LEVEL_1_SITES)
    return partial_trace(arr, dimensions=FINE_DIMENSIONS, keep=keep)


def reduce_to_level_0(rho_1) -> np.ndarray:
    """`rho_0 = Tr_{X,Y}(rho_1)`, surviving sites `(A, B, C, D)` (spec §6).

    `rho_1` must have shape `(64, 64)` (the six sites of `LEVEL_1_SITES`);
    otherwise this function fails closed with `ValueError`.
    """
    arr = _validate_state_shape(rho_1, 2 ** len(LEVEL_1_SITES), name="rho_1")
    keep = _keep_indices(LEVEL_1_SITES, LEVEL_0_SITES)
    return partial_trace(arr, dimensions=LEVEL_1_DIMENSIONS, keep=keep)


def reduce_to_level_0_direct(rho_2) -> np.ndarray:
    """`rho_0_direct = Tr_{P,Q,X,Y}(rho_2)`, direct control (spec §6, §15).

    Same primitive (`cosmotgg.core.states.partial_trace`) as
    `reduce_to_level_1`/`reduce_to_level_0`, applied directly from `rho_2` to
    the level-0 sites in a single step, without composing the two sequential
    reductions: this is the independent-path control required by `T5F11`/
    `T5F3` (spec §15), classified `SATISFIED_BY_CONSTRUCTION`
    (`PARTIAL_TRACE_ASSOCIATIVITY != EMERGENT_GEOMETRY_EVIDENCE`).
    """
    arr = _validate_state_shape(rho_2, 2 ** len(FINE_SITE_ORDER), name="rho_2")
    keep = _keep_indices(FINE_SITE_ORDER, LEVEL_0_SITES)
    return partial_trace(arr, dimensions=FINE_DIMENSIONS, keep=keep)
