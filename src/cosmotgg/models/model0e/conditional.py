"""toy0e physical conditional states, correlation map, fixed law, reference change.

Normative source: `docs/toy-models/toy0e/specification.md` §19-§32.

This module assembles the actual physical conditional states of a
qutrit subsystem given a reference reading
(`physical_conditional_states_from_reference`, §19) and their probe
statistics (`conditional_reference_statistics`, §20); the anti-linear
correlation map `M_AB` derived from the unique maximal eigenvector of
`rho_AB` (`correlation_matrix_from_rho_ab`, §21), together with its
strictly distinct vector map (`vector_correlation_map_ab`) and operator
transfer map (`operator_correlation_transfer_ab`); the derived fixed
`Z3` relational law `V_A` and its application
(`derived_fixed_law_unitary`, `apply_fixed_z3_relational_law`, §22);
and the reference-change overlap/affine label map
(`reference_change_overlap_matrix`,
`cosmotgg.models.model0e.reference.extract_affine_z3_reference_map`
companion, §29-§30).

`rho_A|k` are `ACTUAL_PHYSICAL_CONDITIONAL_STATES_OF_A` (§19): not
auxiliary reconstructed states. `J_AB` (vector map) and `Jop_AB`
(operator map) are strictly distinct (§21): any operator (e.g. a
projector `E_k^B`) transferred from `B` to `A` in this module uses
`operator_correlation_transfer_ab`, never `vector_correlation_map_ab`.

This module never names anything `time_evolution`, `clock`,
`physical_change`, or `relational_time`; it does not import
`cosmotgg.models.model0c` or any other prior model.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import validate_density_matrix

_IDENTITY3 = np.eye(3, dtype=complex)


def _validate_tolerance(value, *, name: str) -> float:
    """Validate a real, finite, non-negative numeric scalar tolerance.

    Private and local to this module (no private `cosmotgg.core`
    symbol is imported).
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


def physical_conditional_states_from_reference(
    rho_ab,
    reference_pvm_b,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Actual physical conditional states of `A` given a `B` reading (spec §19).

    `rho_ab` must have shape `(9, 9)` and be a faithful density matrix
    (validated via `cosmotgg.core.states.validate_density_matrix`).
    `reference_pvm_b` must contain exactly three `(3, 3)` effects
    `E_0, E_1, E_2` (a resolution of identity is not itself re-checked
    here; it is a property of `derived_z3_relational_reference`).

    For each `k`:

        unnormalized = Tr_B[(I_A (x) E_k) rho_ab]   (explicit contraction)
        p_k          = Tr(unnormalized)
        rho_A|k      = unnormalized / p_k

    computed via an explicit tensor contraction of `rho_ab` (reshaped
    to its `(3, 3, 3, 3)` `A, B` block form) against `E_k`; this is NOT
    the canonical closed-form oracle `(1-eta)/3 I + eta E_k^T` of the
    specification, which is reserved for independent testing. `p_k`
    must be finite, have vanishing imaginary part within
    `hermiticity_tolerance`, and be strictly positive; otherwise this
    function fails closed with `ValueError`. Each `rho_A|k` is itself
    validated as a faithful density matrix.

    `rho_A|k` are `ACTUAL_PHYSICAL_CONDITIONAL_STATES_OF_A`, not
    auxiliary reconstructed states.
    """
    rho_ab_arr = np.asarray(rho_ab)
    if rho_ab_arr.ndim != 2 or rho_ab_arr.shape != (9, 9):
        raise ValueError(f"rho_ab must have shape (9, 9), got shape={rho_ab_arr.shape}")
    if len(reference_pvm_b) != 3:
        raise ValueError(f"reference_pvm_b must contain exactly three effects, got {len(reference_pvm_b)}")
    effects = []
    for index, effect in enumerate(reference_pvm_b):
        eff_arr = np.asarray(effect)
        if eff_arr.ndim != 2 or eff_arr.shape != (3, 3):
            raise ValueError(f"reference_pvm_b[{index}] must have shape (3, 3), got shape={eff_arr.shape}")
        effects.append(eff_arr.astype(complex, copy=False))

    hermiticity_tol = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")

    validated_rho_ab = validate_density_matrix(
        rho_ab_arr,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    tensor = validated_rho_ab.reshape(3, 3, 3, 3)

    probabilities = np.empty(3, dtype=float)
    states = []
    for k, effect in enumerate(effects):
        unnormalized = np.einsum("apqb,bp->aq", tensor, effect)
        trace_value = np.trace(unnormalized)
        if not np.isfinite(trace_value):
            raise ValueError(f"p_B({k}) is not finite: got {trace_value}")
        if abs(trace_value.imag) > hermiticity_tol:
            raise ValueError(
                f"p_B({k}) has non-negligible imaginary part within hermiticity_tolerance="
                f"{hermiticity_tol}: got {trace_value}"
            )
        p_k = trace_value.real
        if not (p_k > 0.0):
            raise ValueError(f"p_B({k}) must be strictly positive, got {p_k}")

        rho_a_given_k = unnormalized / p_k
        rho_a_given_k = validate_density_matrix(
            rho_a_given_k,
            require_faithful=True,
            hermiticity_tolerance=hermiticity_tolerance,
            trace_tolerance=trace_tolerance,
            positivity_tolerance=positivity_tolerance,
        )
        probabilities[k] = p_k
        states.append(rho_a_given_k)

    return probabilities, tuple(states)


def conditional_reference_statistics(conditional_states, probe_pvm_a) -> np.ndarray:
    """Physical probe statistics `p(k, j) = Tr[M_j rho_A|k]` (spec §20).

    `conditional_states` must contain exactly three `(3, 3)` states;
    `probe_pvm_a` must contain exactly three `(3, 3)` effects. Returns
    a real `(3, 3)` array; no normalization repair is performed.
    """
    if len(conditional_states) != 3:
        raise ValueError(f"conditional_states must contain exactly three states, got {len(conditional_states)}")
    if len(probe_pvm_a) != 3:
        raise ValueError(f"probe_pvm_a must contain exactly three effects, got {len(probe_pvm_a)}")

    states = []
    for index, state in enumerate(conditional_states):
        arr = np.asarray(state)
        if arr.ndim != 2 or arr.shape != (3, 3):
            raise ValueError(f"conditional_states[{index}] must have shape (3, 3), got shape={arr.shape}")
        states.append(arr.astype(complex, copy=False))

    effects = []
    for index, effect in enumerate(probe_pvm_a):
        arr = np.asarray(effect)
        if arr.ndim != 2 or arr.shape != (3, 3):
            raise ValueError(f"probe_pvm_a[{index}] must have shape (3, 3), got shape={arr.shape}")
        effects.append(arr.astype(complex, copy=False))

    result = np.empty((3, 3), dtype=float)
    for k, state in enumerate(states):
        for j, effect in enumerate(effects):
            result[k, j] = np.trace(effect @ state).real
    return result


def correlation_matrix_from_rho_ab(
    rho_ab,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
    spectral_tolerance: float,
    unitarity_tolerance: float,
) -> np.ndarray:
    """Anti-linear correlation matrix `M_AB` from `rho_AB`'s top eigenvector (spec §21).

    `rho_ab` must have shape `(9, 9)` and be a faithful density matrix.
    Its unique maximal eigenvalue must be separated from the
    second-largest by strictly more than `spectral_tolerance`
    (`ValueError` otherwise). The corresponding eigenvector is reshaped
    to a `(3, 3)` matrix (fixed `A, B` tensor convention) and scaled by
    `sqrt(3)`: `M_AB = sqrt(3) * Psi_matrix`. `M_AB` must be unitary
    (both `M_AB^dagger M_AB` and `M_AB M_AB^dagger` within
    `unitarity_tolerance` of the identity); otherwise `ValueError`. No
    attempt is made to fix the residual global phase of the eigenvector.
    """
    validated_rho_ab = validate_density_matrix(
        rho_ab,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if validated_rho_ab.shape != (9, 9):
        raise ValueError(f"rho_ab must have shape (9, 9), got shape={validated_rho_ab.shape}")

    spectral_tol = _validate_tolerance(spectral_tolerance, name="spectral_tolerance")
    unitarity_tol = _validate_tolerance(unitarity_tolerance, name="unitarity_tolerance")

    eigvals, eigvecs = np.linalg.eigh(validated_rho_ab)
    gap = eigvals[-1] - eigvals[-2]
    if not (gap > spectral_tol):
        raise ValueError(
            "rho_ab does not have a unique maximal eigenvalue within "
            f"spectral_tolerance={spectral_tol}: eigenvalues={eigvals}"
        )

    psi = eigvecs[:, -1]
    psi_matrix = psi.reshape(3, 3)
    m_ab = np.sqrt(3.0) * psi_matrix

    identity3 = _IDENTITY3
    dev_left = np.max(np.abs(m_ab.conj().T @ m_ab - identity3))
    dev_right = np.max(np.abs(m_ab @ m_ab.conj().T - identity3))
    if dev_left > unitarity_tol or dev_right > unitarity_tol:
        raise ValueError(
            f"correlation matrix M_AB is not unitary within unitarity_tolerance={unitarity_tol}: "
            f"max|M^dagger M - I|={dev_left}, max|M M^dagger - I|={dev_right}"
        )
    return m_ab


def vector_correlation_map_ab(vector_b, correlation_matrix) -> np.ndarray:
    """Anti-linear vector correlation map `J_AB(b) = M_AB @ b.conj()` (spec §21).

    `vector_b` must have shape `(3,)`; `correlation_matrix` must have
    shape `(3, 3)`. This is a map on VECTORS of `H_B`, never exposed as
    a "time reversal" operation. Never call this function on an
    operator: use `operator_correlation_transfer_ab` instead.
    """
    vector = np.asarray(vector_b)
    if vector.ndim != 1 or vector.shape != (3,):
        raise ValueError(f"vector_b must have shape (3,), got shape={vector.shape}")
    matrix = np.asarray(correlation_matrix)
    if matrix.ndim != 2 or matrix.shape != (3, 3):
        raise ValueError(f"correlation_matrix must have shape (3, 3), got shape={matrix.shape}")
    return matrix @ vector.conj()


def operator_correlation_transfer_ab(operator_b, correlation_matrix) -> np.ndarray:
    """Operator correlation transfer `Jop_AB(X) = M_AB @ X.conj() @ M_AB^dagger` (spec §21).

    `operator_b` must have shape `(3, 3)`; `correlation_matrix` must
    have shape `(3, 3)`. Any operator (e.g. a rank-1 projector `E`)
    transferred from `B` to `A` in this module uses this function,
    never `vector_correlation_map_ab` directly.
    """
    operator = np.asarray(operator_b)
    if operator.ndim != 2 or operator.shape != (3, 3):
        raise ValueError(f"operator_b must have shape (3, 3), got shape={operator.shape}")
    matrix = np.asarray(correlation_matrix)
    if matrix.ndim != 2 or matrix.shape != (3, 3):
        raise ValueError(f"correlation_matrix must have shape (3, 3), got shape={matrix.shape}")
    return matrix @ operator.conj() @ matrix.conj().T


def derived_fixed_law_unitary(
    rho_ab,
    cycle_unitary_b,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
    spectral_tolerance: float,
    unitarity_tolerance: float,
) -> np.ndarray:
    """Derived fixed `Z3` relational law `V_A = M_AB U_B^* M_AB^dagger` (spec §22).

    `V_A` is derived from `rho_ab` and `cycle_unitary_b` (`U_B`) via
    `correlation_matrix_from_rho_ab`; it is never hard-coded as
    `U_B.conj()`, `U_B.T`, or any other canonical-basis shortcut. `V_A`
    must be unitary within `unitarity_tolerance` (`ValueError`
    otherwise). No target state is supplied to this function.
    """
    m_ab = correlation_matrix_from_rho_ab(
        rho_ab,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
        spectral_tolerance=spectral_tolerance,
        unitarity_tolerance=unitarity_tolerance,
    )
    u_b = np.asarray(cycle_unitary_b)
    if u_b.ndim != 2 or u_b.shape != (3, 3):
        raise ValueError(f"cycle_unitary_b must have shape (3, 3), got shape={u_b.shape}")

    v_a = m_ab @ u_b.conj() @ m_ab.conj().T

    unitarity_tol = _validate_tolerance(unitarity_tolerance, name="unitarity_tolerance")
    identity3 = _IDENTITY3
    dev_left = np.max(np.abs(v_a.conj().T @ v_a - identity3))
    dev_right = np.max(np.abs(v_a @ v_a.conj().T - identity3))
    if dev_left > unitarity_tol or dev_right > unitarity_tol:
        raise ValueError(
            f"derived fixed-law V_A is not unitary within unitarity_tolerance={unitarity_tol}: "
            f"max|V^dagger V - I|={dev_left}, max|V V^dagger - I|={dev_right}"
        )
    return v_a


def apply_fixed_z3_relational_law(
    state_a,
    fixed_law_unitary_a,
    *,
    k_source: int,
    k_target: int,
) -> np.ndarray:
    """Apply the fixed law: `Lambda_(k_target<-k_source)(state_a)` (spec §22-§23).

    `k_source`, `k_target` must each be an `int` (not `bool`) in
    `{0, 1, 2}`. `delta_k = (k_target - k_source) mod 3`; returns
    `V_A^delta_k @ state_a @ (V_A^delta_k)^dagger`. This function
    accepts no independently supplied target state
    (`NUMBER_OF_INDEPENDENT_TARGET_STATE_INPUTS = ZERO`, spec §22).
    """
    for name, value in (("k_source", k_source), ("k_target", k_target)):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
            raise ValueError(f"{name} must be an int, not bool: got {value!r}")
        if int(value) not in (0, 1, 2):
            raise ValueError(f"{name} must be in {{0, 1, 2}}, got {value!r}")

    state = np.asarray(state_a)
    if state.ndim != 2 or state.shape != (3, 3):
        raise ValueError(f"state_a must have shape (3, 3), got shape={state.shape}")
    v_a = np.asarray(fixed_law_unitary_a)
    if v_a.ndim != 2 or v_a.shape != (3, 3):
        raise ValueError(f"fixed_law_unitary_a must have shape (3, 3), got shape={v_a.shape}")

    delta_k = (int(k_target) - int(k_source)) % 3
    v_power = np.linalg.matrix_power(v_a, delta_k)
    return v_power @ state @ v_power.conj().T


def reference_change_overlap_matrix(
    reference_pvm_a,
    reference_pvm_b,
    correlation_matrix_ab,
) -> np.ndarray:
    """Reference-change overlap matrix `Tr[E_j^A Jop_AB(E_k^B)]` (spec §29).

    `reference_pvm_a`, `reference_pvm_b` must each contain exactly
    three `(3, 3)` effects; `correlation_matrix_ab` must have shape
    `(3, 3)`. Returns a real `(3, 3)` array `overlap[j, k]`; values are
    never silently rounded to `0`/`1`.
    """
    if len(reference_pvm_a) != 3:
        raise ValueError(f"reference_pvm_a must contain exactly three effects, got {len(reference_pvm_a)}")
    if len(reference_pvm_b) != 3:
        raise ValueError(f"reference_pvm_b must contain exactly three effects, got {len(reference_pvm_b)}")

    overlap = np.empty((3, 3), dtype=float)
    for j in range(3):
        e_j_a = np.asarray(reference_pvm_a[j])
        for k in range(3):
            e_k_b = np.asarray(reference_pvm_b[k])
            transferred = operator_correlation_transfer_ab(e_k_b, correlation_matrix_ab)
            overlap[j, k] = np.trace(e_j_a @ transferred).real
    return overlap


def extract_affine_z3_reference_map(overlap_matrix, *, overlap_tolerance: float) -> tuple[int, int]:
    """Extract the affine `Z3` reference-change map `pi(k) = offset + orientation*k mod 3` (spec §29-§30).

    `overlap_matrix` must have shape `(3, 3)` and finite entries. The
    six candidate affine maps (`offset` in `{0, 1, 2}`, `orientation`
    in `{-1, +1}`; for `Z3` these already enumerate all six
    permutations of three elements, no Hungarian-algorithm dependency
    needed) are each compared, entrywise, to `overlap_matrix` within
    `overlap_tolerance`. Exactly one candidate must match; otherwise
    (`0` or more than `1` matches) this function fails closed with
    `ValueError`.

    Returns `(offset, orientation)`.
    """
    tol = _validate_tolerance(overlap_tolerance, name="overlap_tolerance")
    arr = np.asarray(overlap_matrix)
    if arr.ndim != 2 or arr.shape != (3, 3):
        raise ValueError(f"overlap_matrix must have shape (3, 3), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("overlap_matrix must contain only finite values")

    matches = []
    for offset in (0, 1, 2):
        for orientation in (-1, 1):
            candidate = np.zeros((3, 3))
            for k in range(3):
                j = (offset + orientation * k) % 3
                candidate[j, k] = 1.0
            if np.max(np.abs(arr - candidate)) <= tol:
                matches.append((offset, orientation))

    if len(matches) != 1:
        raise ValueError(
            "overlap_matrix does not match a unique affine Z3 relabeling within "
            f"overlap_tolerance={tol}: found {len(matches)} candidate(s)"
        )
    return matches[0]
