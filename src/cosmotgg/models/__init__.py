"""`cosmotgg.models` — toy-model packages (assemblage, consumers of `core`).

Each `cosmotgg.models.modelXX` package holds the configuration, assembly,
and scientific choices specific to a given toy model of CosmoTGG: named
states, protocol parameters, and any oracle/acceptance composition
proper to that model. A model package consumes `cosmotgg.core`; it never
redefines a generic primitive already available there.

See `docs/governance/software-architecture-governance.md` for the
architecture distinguishing `core` (generic, model-independent
primitives) from `models/modelXX` (model-specific assembly).
"""
