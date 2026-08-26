"""`cosmotgg.core` — reusable, model-independent scientific/numeric primitives.

This package holds only briques that are intrinsically generic in the sense
of `docs/governance/software-architecture-governance.md`: their definition
and behaviour can be formulated without reference to the assemblage of any
particular CosmoTGG toy model. It must never import `cosmotgg.models`.

Submodules:

- `cosmotgg.core.states` — finite-dimensional quantum state primitives
  (density matrix validation, partial trace).
- `cosmotgg.core.information` — quantum information primitives (von Neumann
  entropy, Umegaki relative entropy, mutual information, generic
  log-density difference).
- `cosmotgg.core.modular` — modular theory primitives (hermitian matrix
  logarithm, modular Hamiltonian `K = -log(rho)`, modular flow, finite
  Connes cocycle).
"""

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}
