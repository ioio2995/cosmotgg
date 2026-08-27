"""toy0e projected modular context pair and derived Z3 relational reference.

Normative source: `docs/toy-models/toy0e/specification.md` §10, §14-§18.

This module assembles the projected modular contexts `H_Q^X`
(`PROJECTED_PHASE_FIXING_MODULAR_CONTEXT`) and `H_N^X`
(`PROJECTED_ORDERING_MODULAR_CONTEXT`) for `X` a qutrit physical
subsystem, from its two relational-context reductions
(`projected_modular_context_pair`, §10), extracts the derived discrete
`Z3` relational reference PVM from that pair
(`derived_z3_relational_reference`, §14-§15), and applies the affine
`Z3` label gauge (`relabel_z3_reference_pvm`, §17). The companion
affine reference-CHANGE map between two independently derived PVMs
(`extract_affine_z3_reference_map`) is exposed by
`cosmotgg.models.model0e.conditional`, alongside the reference-change
overlap matrix it consumes.

`H_Q^X`, `H_N^X` are purely structural names (§10): this module never
calls `Q` "the phase of time" nor `N` "a clock Hamiltonian", and never
constructs anything named `time`, `clock`, `physical_time`, or
`proper_time`.

The ordered spectral extraction of `H_N^X` (`P_0, P_1, P_2`, `R_X`,
`U_X`) and the maximal-eigenprojector selection of `H_Q^X` are
model-specific candidate-construction rules (`docs/toy-models/toy0e/
implementation-design.md` §3): they are not promoted to `cosmotgg.core`
by this module. Spectral decomposition uses `numpy.linalg.eigh`
directly (no private `cosmotgg.core` helper is imported).

This module builds no state family, no reduction, no physical
conditional state, no correlation map, no fixed law
(`cosmotgg.models.model0e.states`, `cosmotgg.models.model0e.conditional`).
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import modular_hamiltonian
from cosmotgg.core.states import conditional_expectation, traceless_part

_XC_DIMENSIONS = (3, 2)


def _validate_tolerance(value, *, name: str) -> float:
    """Validate a real, finite, non-negative numeric scalar tolerance.

    Private and local to this module (no private `cosmotgg.core`
    symbol is imported): fail-closed (raise `ValueError`) on `bool`,
    complex, `NaN`, `+/-inf`, negative, non-scalar, or non-numeric
    input.
    """
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a real numeric scalar, not bool: got {value!r}")
    arr = np.asarray(value)
    if arr.ndim != 0:
        raise ValueError(f"{name} must be a scalar, got shape={arr.shape}")
    if not np.issubdtype(arr.dtype, np.number):
        raise ValueError(
            f"{name} must be a real numeric scalar, got {type(value).__name__}: {value!r}"
        )
    if np.iscomplexobj(arr):
        raise ValueError(f"{name} must be real, not complex: got {value!r}")
    scalar = float(arr)
    if not np.isfinite(scalar):
        raise ValueError(f"{name} must be finite, got {scalar}")
    if scalar < 0.0:
        raise ValueError(f"{name} must be >= 0, got {scalar}")
    return scalar


def _validate_square_hermitian_3x3(matrix, *, hermiticity_tolerance: float, name: str) -> np.ndarray:
    tol = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape != (3, 3):
        raise ValueError(f"{name} must have shape (3, 3), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    arr = arr.astype(complex, copy=False)
    deviation = np.max(np.abs(arr - arr.conj().T))
    if deviation > tol:
        raise ValueError(
            f"{name} is not hermitian within hermiticity_tolerance={tol}: "
            f"max |{name} - {name}^dagger| = {deviation}"
        )
    return arr


def projected_modular_context_pair(
    rho_xc,
    rho_xd,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Projected modular context pair `(H_Q^X, H_N^X)` (spec §10).

    `rho_xc`, `rho_xd` must each have shape `(6, 6)` (the `X (x) C` /
    `X (x) D` relational-context reduction of `model0e/states.py`, `X`
    of local dimension 3, `C`/`D` of local dimension 2). For each:
    `K = modular_hamiltonian(rho, ...)`, then the tracial conditional
    expectation onto `X` (`conditional_expectation(K, dimensions=(3, 2),
    keep=(0,))`), then its traceless part. `H_Q^X` is derived from
    `rho_xc`, `H_N^X` from `rho_xd`; returned in this order.

    `hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`
    are explicit, keyword-only, with no default value, forwarded
    unchanged to `modular_hamiltonian`; no tolerance is invented
    locally. No canonical `Q`/`N` matrix of `model0e/states.py` is used
    anywhere in this computation.
    """
    rho_xc_arr = np.asarray(rho_xc)
    if rho_xc_arr.ndim != 2 or rho_xc_arr.shape != (6, 6):
        raise ValueError(f"rho_xc must have shape (6, 6), got shape={rho_xc_arr.shape}")
    rho_xd_arr = np.asarray(rho_xd)
    if rho_xd_arr.ndim != 2 or rho_xd_arr.shape != (6, 6):
        raise ValueError(f"rho_xd must have shape (6, 6), got shape={rho_xd_arr.shape}")

    modular_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    k_xc = modular_hamiltonian(rho_xc_arr, **modular_kwargs)
    k_xd = modular_hamiltonian(rho_xd_arr, **modular_kwargs)

    e_xc = conditional_expectation(k_xc, dimensions=_XC_DIMENSIONS, keep=[0])
    e_xd = conditional_expectation(k_xd, dimensions=_XC_DIMENSIONS, keep=[0])

    h_q = traceless_part(e_xc)
    h_n = traceless_part(e_xd)
    return h_q, h_n


def derived_z3_relational_reference(
    h_q,
    h_n,
    *,
    hermiticity_tolerance: float,
    spectral_tolerance: float,
    equal_modulus_tolerance: float,
) -> dict:
    """Derived discrete `Z3` relational reference PVM (spec §14-§15).

    `h_q`, `h_n` must each be a `(3, 3)`, finite, hermitian (within
    `hermiticity_tolerance`) array. `h_n` is diagonalized
    (`numpy.linalg.eigh`); its three eigenvalues must be pairwise
    nondegenerate, each adjacent gap strictly greater than
    `spectral_tolerance` (`REFERENCE_EXTRACTION` fails closed with
    `ValueError` otherwise, no repair). The ordered spectral projectors
    `P_0, P_1, P_2` (ascending eigenvalue) define the rankless rank
    operator `R = 0 P_0 + 1 P_1 + 2 P_2` and the cyclic unitary
    `U = exp(-2 pi i R / 3)`. Only the ORDER of `h_n`'s eigenvalues is
    used, never their numerical gaps.

    `h_q`'s unique maximal eigenvalue must be separated from the
    second-largest by strictly more than `spectral_tolerance`
    (otherwise `ValueError`); its eigenprojector is the seed `E_0`.

    Equal-modulus gate (spec §15): `E_0`, evaluated in `h_n`'s ordered
    eigenbasis, must satisfy `|Tr(P_n E_0) - 1/3| <=
    equal_modulus_tolerance` for each of the three `n`; otherwise this
    function fails closed with `ValueError` (`NO_SILENT_GRAM_SCHMIDT`,
    `NO_REPAIR`, `NO_REPLACEMENT_SEED`). The PVM `E_k = U^k E_0 U^{-k}`
    (`k=0,1,2`) is only returned once this gate passes.

    `hermiticity_tolerance`, `spectral_tolerance`,
    `equal_modulus_tolerance` are explicit, keyword-only, with no
    default value.

    Returns a `dict` with exactly the keys `ordered_eigenvalues`
    (the three ascending eigenvalues of `h_n`, informational only:
    never used to construct `R`/`U`/the PVM above), `ordered_projectors`
    (`(P_0, P_1, P_2)`), `rank_operator` (`R`), `cycle_unitary` (`U`),
    `seed_projector` (`E_0`), `pvm` (`(E_0, E_1, E_2)`). No PASS/FAIL
    score is returned: failure is exclusively signalled by `ValueError`.
    """
    h_q_arr = _validate_square_hermitian_3x3(h_q, hermiticity_tolerance=hermiticity_tolerance, name="h_q")
    h_n_arr = _validate_square_hermitian_3x3(h_n, hermiticity_tolerance=hermiticity_tolerance, name="h_n")
    spectral_tol = _validate_tolerance(spectral_tolerance, name="spectral_tolerance")
    equal_modulus_tol = _validate_tolerance(equal_modulus_tolerance, name="equal_modulus_tolerance")

    eigvals_n, eigvecs_n = np.linalg.eigh(h_n_arr)
    gap_01 = eigvals_n[1] - eigvals_n[0]
    gap_12 = eigvals_n[2] - eigvals_n[1]
    if not (gap_01 > spectral_tol and gap_12 > spectral_tol):
        raise ValueError(
            "h_n does not have three pairwise nondegenerate eigenvalues within "
            f"spectral_tolerance={spectral_tol}: eigenvalues={eigvals_n}"
        )

    p0 = np.outer(eigvecs_n[:, 0], eigvecs_n[:, 0].conj())
    p1 = np.outer(eigvecs_n[:, 1], eigvecs_n[:, 1].conj())
    p2 = np.outer(eigvecs_n[:, 2], eigvecs_n[:, 2].conj())
    ordered_projectors = (p0, p1, p2)

    rank_operator = 0.0 * p0 + 1.0 * p1 + 2.0 * p2
    omega = np.exp(-2j * np.pi / 3.0)
    cycle_unitary = p0 + omega * p1 + (omega**2) * p2

    eigvals_q, eigvecs_q = np.linalg.eigh(h_q_arr)
    top_gap = eigvals_q[2] - eigvals_q[1]
    if not (top_gap > spectral_tol):
        raise ValueError(
            "h_q does not have a unique maximal eigenvalue within "
            f"spectral_tolerance={spectral_tol}: eigenvalues={eigvals_q}"
        )
    seed_projector = np.outer(eigvecs_q[:, 2], eigvecs_q[:, 2].conj())

    for index, projector in enumerate(ordered_projectors):
        overlap = np.trace(projector @ seed_projector).real
        if abs(overlap - 1.0 / 3.0) > equal_modulus_tol:
            raise ValueError(
                "equal-modulus gate failed (spec §15): seed_projector is not "
                f"compatible with an orthogonal Z3 PVM within "
                f"equal_modulus_tolerance={equal_modulus_tol} at n={index}: "
                f"|<n|q_0>|^2={overlap}"
            )

    pvm = []
    u_power = np.eye(3, dtype=complex)
    for _ in range(3):
        pvm.append(u_power @ seed_projector @ u_power.conj().T)
        u_power = u_power @ cycle_unitary
    pvm = tuple(pvm)

    return {
        "ordered_eigenvalues": eigvals_n,
        "ordered_projectors": ordered_projectors,
        "rank_operator": rank_operator,
        "cycle_unitary": cycle_unitary,
        "seed_projector": seed_projector,
        "pvm": pvm,
    }


def relabel_z3_reference_pvm(
    pvm,
    *,
    offset: int,
    orientation: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Affine `Z3` relabeling of a derived reference PVM (spec §17).

    `pvm` must contain exactly three elements. `offset` must be an
    `int` (not `bool`) in `{0, 1, 2}`; `orientation` must be an `int`
    (not `bool`) in `{-1, +1}`. Old label `k` maps to new label
    `(offset + orientation*k) mod 3`. Returns a deterministic tuple
    ordered by the NEW labels. This relabeling carries no physical
    interpretation of `offset`/`orientation` (§17): `k -> -k` is never
    a physical time reversal, causal reversal, or arrow reversal.
    """
    if len(pvm) != 3:
        raise ValueError(f"pvm must contain exactly three elements, got {len(pvm)}")
    if isinstance(offset, bool) or not isinstance(offset, (int, np.integer)):
        raise ValueError(f"offset must be an int, not bool: got {offset!r}")
    if int(offset) not in (0, 1, 2):
        raise ValueError(f"offset must be in {{0, 1, 2}}, got {offset!r}")
    if isinstance(orientation, bool) or not isinstance(orientation, (int, np.integer)):
        raise ValueError(f"orientation must be an int, not bool: got {orientation!r}")
    if int(orientation) not in (-1, 1):
        raise ValueError(f"orientation must be in {{-1, +1}}, got {orientation!r}")

    offset_v = int(offset)
    orientation_v = int(orientation)
    relabeled = {}
    for k in range(3):
        new_label = (offset_v + orientation_v * k) % 3
        relabeled[new_label] = pvm[k]
    return tuple(relabeled[label] for label in range(3))
