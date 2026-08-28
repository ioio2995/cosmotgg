"""model1b directional polar factor, active-cycle loop object, and diagnostics.

Normative source: `docs/toy-models/toy1b/specification.md` §12-§14, §18, §20.

This module implements the fail-closed right-polar directional factor
`DIRECTIONAL_FACTOR(J) = O` on `J in GL(3, R)` (`directional_factor`, spec
§12), the route `Z2` directional typing (`det(O) = -1` expected for every
active relational edge; `det(O) = +1` on an otherwise-invertible `J` fails
closed as `TYPE_MISMATCH_FAIL_CLOSED`, spec §12), the active-cycle loop
object `Q_n` (`active_cycle_loop_object`/`active_cycle_loop_object_from_
blocks`, spec §13), the gauge-invariant diagnostics `d_flat(Q_n)`,
`chi_n = (Tr(Q_n) - 1) / 2`, `Delta_chi(n, m)` (spec §14), and the tree
relative-direction diagnostic `D_tree = O_path^T O_coarse` (spec §18).

Two directional domain failures are distinct and never confused (spec §12):

    SINGULAR_DIRECTIONAL_FACTOR    (J singular: no pseudo-inverse, no
                                     epsilon repair)
    Z2_DIRECTIONAL_TYPE_MISMATCH   (J invertible but det(O) = +1: no sign
                                     repair, no orientation fitting)

Both propagate, when resolving an active-cycle loop object, into a single
generic `LOOP_DIAGNOSTIC = UNDEFINED_DIRECTIONAL_DOMAIN` result with an
explicit, preserved `LOOP_UNDEFINED_REASON` (spec §13-§14): no `d_flat`,
`chi`, or `Delta_chi` is ever constructed in that case.

This module imports no `model0a`-`model0e`/`model1a` production API.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

REASON_SINGULAR_DIRECTIONAL_FACTOR = "SINGULAR_DIRECTIONAL_FACTOR"
REASON_Z2_DIRECTIONAL_TYPE_MISMATCH = "Z2_DIRECTIONAL_TYPE_MISMATCH"


class DirectionalFactorUndefinedError(ValueError):
    """`DIRECTIONAL_FACTOR = UNDEFINED` (spec §12, §19): `J` is exactly singular.

    Carries the exact, externally inspectable `reason` (always
    `REASON_SINGULAR_DIRECTIONAL_FACTOR`), preserved distinctly from
    `DirectionalTypeMismatchError`.
    """

    def __init__(self, reason: str, *, message: str):
        super().__init__(message)
        self.reason = reason


class DirectionalTypeMismatchError(ValueError):
    """`DIRECTIONAL_RELATIONAL_TYPE = TYPE_MISMATCH_FAIL_CLOSED` (spec §12):
    `J` is invertible but its polar orthogonal factor has `det(O) = +1`
    instead of the expected `det(O) = -1` for the declared odd-`Z2`
    relational route.

    Carries the exact, externally inspectable `reason` (always
    `REASON_Z2_DIRECTIONAL_TYPE_MISMATCH`), never confused with
    `DirectionalFactorUndefinedError`.
    """

    def __init__(self, reason: str, *, message: str):
        super().__init__(message)
        self.reason = reason


class LoopDiagnosticUndefinedError(ValueError):
    """`LOOP_DIAGNOSTIC = UNDEFINED_DIRECTIONAL_DOMAIN` (spec §13-§14).

    Carries the exact, preserved `reason` of whichever edge factor failed
    (`REASON_SINGULAR_DIRECTIONAL_FACTOR` |
    `REASON_Z2_DIRECTIONAL_TYPE_MISMATCH`), never confused between causes.
    """

    def __init__(self, reason: str, *, message: str):
        super().__init__(message)
        self.reason = reason


def _validate_real_3x3(matrix, *, name: str) -> np.ndarray:
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape != (3, 3):
        raise ValueError(f"{name} must have shape (3, 3), got shape={arr.shape}")
    if np.iscomplexobj(arr) and np.max(np.abs(arr.imag)) > 0.0:
        raise ValueError(f"{name} must be real, got a nonzero imaginary part")
    arr = np.asarray(arr, dtype=float)
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def directional_conditioning(j_matrix) -> np.ndarray:
    """Singular values of `j_matrix` (spec §12): numerical conditioning,
    reported strictly separately from mathematical existence of
    `DIRECTIONAL_FACTOR`. Diagnostic only; no verdict, no threshold."""
    arr = _validate_real_3x3(j_matrix, name="j_matrix")
    return np.linalg.svd(arr, compute_uv=False)


def directional_factor(j_matrix) -> np.ndarray:
    """Right-polar directional factor `O` of a real, invertible `(3, 3)` `J`
    (spec §12): `J = O S`, `S = sqrt(J^T J) > 0`, `O = J (J^T J)^(-1/2)`,
    `O in O(3)`, computed via `numpy.linalg.svd` (`J = W diag(s) V^T`,
    `O = W V^T`).

    Domain: `J in GL(3, R)` (exact nonzero determinant; no rank-tolerance
    threshold). If `J` is exactly singular (`det(J) == 0.0`), fails closed
    with `DirectionalFactorUndefinedError` (reason
    `SINGULAR_DIRECTIONAL_FACTOR`) — no pseudo-inverse, no epsilon repair,
    no arbitrary orientation.

    Route `Z2` directional typing (spec §12): every active relational edge
    of this route is required to satisfy `det(O) = -1`
    (`ACTIVE_RELATIONAL_EDGE_DIRECTIONAL_TYPE = O_MINUS_3`), checked by
    SIGN only (never by closeness to `-1`). If `J` is otherwise invertible
    but `det(O) = +1`, fails closed with `DirectionalTypeMismatchError`
    (reason `Z2_DIRECTIONAL_TYPE_MISMATCH`) — no hidden sign flip, no
    single-axis sign repair, no post-hoc orientation fitting.
    """
    arr = _validate_real_3x3(j_matrix, name="j_matrix")

    if np.linalg.det(arr) == 0.0:
        raise DirectionalFactorUndefinedError(
            REASON_SINGULAR_DIRECTIONAL_FACTOR,
            message=f"j_matrix is exactly singular (det(J)=0): {arr!r}",
        )

    w_matrix, _singular_values, vh_matrix = np.linalg.svd(arr)
    o_matrix = w_matrix @ vh_matrix

    det_o = np.linalg.det(o_matrix)
    if not (det_o < 0.0):
        raise DirectionalTypeMismatchError(
            REASON_Z2_DIRECTIONAL_TYPE_MISMATCH,
            message=(
                f"directional factor has det(O)={det_o}, expected det(O) < 0 "
                "(route Z2 typing O_MINUS_3, spec §12)"
            ),
        )
    return o_matrix


def active_cycle_loop_object(directional_factors: Sequence[np.ndarray]) -> np.ndarray:
    """`Q_n = O_{v0<-v1} O_{v1<-v2} ... O_{v(m-1)<-v0}` (spec §13).

    `directional_factors` must already be a sequence of well-defined
    `(3, 3)` real orthogonal matrices, given in the declared active-cycle
    order; this function performs no domain resolution itself (see
    `active_cycle_loop_object_from_blocks` for the `J`-block-driven,
    exception-preserving variant).
    """
    factors = list(directional_factors)
    if len(factors) == 0:
        raise ValueError("directional_factors must be a non-empty sequence")
    result = np.eye(3)
    for o_matrix in factors:
        result = result @ _validate_real_3x3(o_matrix, name="directional factor")
    return result


def active_cycle_loop_object_from_blocks(j_matrices: Sequence[np.ndarray]) -> np.ndarray:
    """`Q_n` resolved directly from the ordered active-cycle `J` blocks (spec §13).

    Resolves `directional_factor` for each `J` block in order. On the
    first undefined or type-mismatched edge, raises
    `LoopDiagnosticUndefinedError` with the exact preserved `reason`
    (`SINGULAR_DIRECTIONAL_FACTOR` | `Z2_DIRECTIONAL_TYPE_MISMATCH`, spec
    §13-§14) — `LOOP_DIAGNOSTIC = UNDEFINED_DIRECTIONAL_DOMAIN`; no
    `d_flat`/`chi`/`Delta_chi` may be produced in that case.
    """
    factors = []
    for j_matrix in j_matrices:
        try:
            factors.append(directional_factor(j_matrix))
        except (DirectionalFactorUndefinedError, DirectionalTypeMismatchError) as exc:
            raise LoopDiagnosticUndefinedError(
                exc.reason,
                message=f"active-cycle loop object undefined ({exc.reason}): {exc}",
            ) from exc
    return active_cycle_loop_object(factors)


def flatness_diagnostic(q_matrix) -> float:
    """`d_flat(Q) = ||Q - I_3||_F / sqrt(8)` (spec §14): gauge-invariant
    projective-flatness scalar, invariant under `Q -> R_A Q R_A^T`. No
    numerical `PASS` tolerance is fixed by this function."""
    arr = _validate_real_3x3(q_matrix, name="q_matrix")
    return float(np.linalg.norm(arr - np.eye(3)) / np.sqrt(8.0))


def conjugacy_class_scalar(q_matrix) -> float:
    """`chi(Q) = (Tr(Q) - 1) / 2` (spec §14): for `Q in SO(3)`, `chi =
    cos(phi)`, gauge invariant under `Q -> R_A Q R_A^T`. Only defined on
    the `SO(3)` domain established by `active_cycle_loop_object_from_
    blocks` (spec §13); callers must not evaluate this on an
    `UNDEFINED_DIRECTIONAL_DOMAIN` result."""
    arr = _validate_real_3x3(q_matrix, name="q_matrix")
    return float((np.trace(arr) - 1.0) / 2.0)


def finite_scale_running(chi_n: float, chi_m: float) -> float:
    """`Delta_chi(n, m) = |chi_n - chi_m|` (spec §14): derived structural
    diagnostic only. `Delta_chi != CURVATURE`, `Delta_chi != CONTINUUM`,
    `Delta_chi != PHYSICAL_FORCE`."""
    return abs(float(chi_n) - float(chi_m))


def tree_relative_direction(o_path, o_coarse) -> np.ndarray:
    """`D_tree = O_path^T O_coarse` (spec §18): tree relative-direction
    diagnostic, transforms by conjugation at one endpoint. Tree
    directional agreement requires `D_tree = I` via a gauge-invariant
    verdict (not decided by this mathematical primitive alone). This
    function does not select any future confirmatory tree topology or
    fixture value."""
    path_arr = _validate_real_3x3(o_path, name="o_path")
    coarse_arr = _validate_real_3x3(o_coarse, name="o_coarse")
    return path_arr.T @ coarse_arr
