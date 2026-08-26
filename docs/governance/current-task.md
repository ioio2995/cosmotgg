# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11 et porte le statut opérationnel courant du projet CosmoTGG.

---

## Git

```text
REPOSITORY    = ioio2995/cosmotgg
REMOTE        = https://github.com/ioio2995/cosmotgg.git
ACTIVE_BRANCH = master
BASE_COMMIT   = dd3b89f7a5f056089a266beca0dd57f08c70ece3
```

Ce document sera mis à jour à chaque jalon.

---

## État global

```text
PROJECT_STATUS = ACTIVE_RESEARCH
CURRENT_LOT    = MODEL0A-SPEC-1
PHASE          = MODEL0A_SPECIFICATION_PROPOSED_PENDING_REVIEW
```

La gouvernance transverse (`collaboration-governance.md`, `documentation-governance.md`, `software-architecture-governance.md`) et les contrats des rôles spécialisés (`docs/governance/agents/`) sont en place. Le lot `T1-CORE-FOUNDATION-0A` (fondation `core` préalable au test de réfutabilité T1) a été implémenté et la gouvernance des notebooks Jupyter d'exécution des toy models a été intégrée (§ci-dessous). Une première spécification scientifique `PROPOSED` de `model0a` (`docs/toy-models/toy0a/specification.md`) a été créée par le lot `MODEL0A-SPEC-1` ; aucune implémentation, aucun plan de validation et aucun notebook ne sont encore engagés.

---

## Hypothèse fondatrice

```text
HYPOTHESIS_SOURCE       = docs/model/hypothesis.md
HYPOTHESIS_STATUS       = FROZEN (v0.2)
HYPOTHESIS_TITLE        = Temps, Géométrie et Gravitation depuis une structure quantique relationnelle
HYPOTHESIS_ANNEX_SOURCE = docs/model/hypothesis-annex-a.md
HYPOTHESIS_ANNEX_STATUS = FROZEN (synchronisée avec hypothesis.md v0.2)
```

Première source scientifique du projet. Elle pose la question de recherche et l'hypothèse centrale de CosmoTGG (temps et géométrie comme deux manifestations d'une même structure quantique relationnelle, gravitation recherchée ensuite comme propriété collective), distingue explicitement `[KNOWN]`, `[DERIVED]`, `[HYPOTHESIS]` et `[OPEN]`, et définit sept tests de réfutabilité (T1–T7, §15 du document). Statut `FROZEN` (v0.2) : gel documentaire du document scientifique comme point de départ du programme, après seconde contre-expertise physic PASS et arbitrage ChatGPT. Ce gel ne signifie pas `COSMOTGG_HYPOTHESIS = TRUE` : les GAP-1 à GAP-6 restent explicitement `OPEN`.

`docs/model/hypothesis-annex-a.md` (Annexe A) est la mémoire de traçabilité conceptuelle associée : elle cartographie les idées et résultats de la littérature rencontrés pendant la construction de l'hypothèse (échelles de Planck, tenseur énergie-impulsion, Tolman–Ehrenfest, gravité stochastique, TGFT, gravité induite de Sakharov, équilibre d'intrication de Jacobson, courbure de Berry modulaire, etc.), y compris les pistes explicitement `[ARCHIVED]` ou `[REJECTED]` (ex. facteur temporel unique expliquant toute la gravitation, \(\alpha_G\) comme quantum minimal de géométrie), et liste des questions encore `[OPEN]` (§A.24). Elle ne redéfinit aucun objet normatif de `hypothesis.md`.

```text
FIRST_PHYSIC_REVIEW        = REVISION_REQUIRED
CHATGPT_ARBITRATION        = INTEGRATED
SECOND_PHYSIC_REVIEW       = PASS
FREEZE_DECISION            = AUTHORIZED
FOUNDING_HYPOTHESIS_FREEZE = FROZEN
```

La première contre-expertise scientifique (`physic`) a retourné `SCIENTIFIC_REVIEW = BLOCKED` / `RECOMMENDATION = REVISION_REQUIRED`. ChatGPT a ensuite arbitré scientifiquement les points bloquants (décisions D1 à D11 du lot `FOUNDING-HYPOTHESIS-CORR-1`), intégrées documentairement dans `hypothesis.md` (passage v0.1 → v0.2) et son Annexe A. Une seconde contre-expertise `physic`, bornée à la v0.2, a retourné `SECOND_SCIENTIFIC_REVIEW = PASS` / `BLOCKING = NONE` / `RECOMMENDATION = VALIDATED_FOR_FREEZE`. ChatGPT a arbitré `CHATGPT_SCIENTIFIC_ARBITRATION = PASS` / `FOUNDING_HYPOTHESIS_V02 = VALIDATED_FOR_FREEZE`. Lionel ORCIL a autorisé le gel documentaire de l'hypothèse fondatrice v0.2.

```text
SCIENTIFIC_CONTENT_HEAD = 589b0727ad880670435bfbb50a268d7472e5410f
```

Le contenu scientifique de référence gelé est celui validé au commit ci-dessus ; le présent lot ne modifie que les métadonnées de statut documentaire.

---

## Workflow Claude Code courant

La gouvernance de collaboration impose un préflight explicite et un profil d'exécution déclaré pour chaque mandat.

Profils disponibles (cf. `docs/governance/collaboration-governance.md` §12) :

```text
DOCUMENTATION                    = CLAUDE_SONNET_5 / AUTO
REVIEW_OR_ENGINEERING            = CLAUDE_SONNET_5 / AUTO
SCIENTIFIC_ESCALATION            = CLAUDE_OPUS_5 / AUTO
SCIENTIFIC_HARD_BLOCKING         = CLAUDE_OPUS_5 / HIGH
```

Principe :

```text
VERSIONED_PRODUCTION_MODEL = CLAUDE_SONNET_5
HAIKU_FOR_VERSIONED_PRODUCTION = NOT_USED
MODEL_ESCALATION_ABOVE_SONNET = EXPLICIT
```

Chaque mandat déclare aussi :

```text
REPOSITORY
REMOTE
BRANCH
EXPECTED_HEAD
EXPECTED_WORKTREE
```

Autre principe :

```text
ONE_TASK = ONE_BOUNDED_SCOPE
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_GLOBAL_AUDIT_BY_DEFAULT
```

Une objection est classée :

```text
BLOCKING
NON_BLOCKING_BACKLOG
REJECTED
```

Une objection `BLOCKING` peut arrêter le lot. Un élément `NON_BLOCKING_BACKLOG` ne rouvre pas le périmètre courant.

---

## Rôles spécialisés disponibles

```text
docs   = AVAILABLE / DOCS_PROTOCOL_V1          / docs/governance/agents/docs-governance.md
code   = AVAILABLE / CODE_PROTOCOL_V1          / docs/governance/agents/code-governance.md
physic = AVAILABLE / PHYSIC_REVIEW_PROTOCOL_V1 / docs/governance/agents/physic-governance.md
```

Aucun lot n'a encore été confié à un rôle spécialisé.

---

## Lot courant

```text
CURRENT_LOT = MODEL0A-SPEC-1
PHASE       = MODEL0A_SPECIFICATION_PROPOSED_PENDING_REVIEW
```

Le rôle `docs` a créé la première spécification scientifique `PROPOSED` de `model0a` (`docs/toy-models/toy0a/specification.md`), sur décisions déjà arbitrées par ChatGPT (revue physique bornée). Les deux lots précédents ont été menés à terme : l'implémentation bornée du socle `core` (`T1-CORE-FOUNDATION-0A`) et l'intégration de la gouvernance des notebooks Jupyter d'exécution des toy models (`NOTEBOOK-GOVERNANCE-1`). Le lot antérieur à ces deux-là (rôle `docs`) avait effectué le gel documentaire (`VALIDATED_FOR_FREEZE` → `FROZEN`) de `docs/model/hypothesis.md` et `docs/model/hypothesis-annex-a.md` (v0.2), suite à la seconde contre-expertise `physic` PASS et à l'arbitrage scientifique de ChatGPT.

```text
MODEL0A_T1_BOUNDARY_REVIEW   = PASS_WITH_CHATGPT_CORRECTIONS
MODEL0A_CARRIER_CANDIDATE    = FINITE_CONNES_COCYCLE
MODEL0A_T1_STATUS            = OPEN_NOT_EXECUTED
MODEL0A_SPECIFICATION_STATUS = PROPOSED
```

```text
T1_CORE_FOUNDATION_AUDIT = PASS
```

Arbitrage ChatGPT sur la classification architecture/core :

```text
R_AB_CODE_CLASSIFICATION     = NO_PROJECT_SPECIFIC_PRIMITIVE_YET
CORE_GENERIC_OPERATOR        = log(rho) - log(sigma)
CORE_GENERIC_OPERATOR_STATUS = established
```

Sens normatif : le `core` peut fournir la primitive mathématique générique `log(rho) - log(sigma)` ; la notation `R_AB` reste définie par `docs/model/hypothesis.md` ; aucun module `core` *project-defined* spécifique à `R_AB` n'est créé dans ce lot ; un consommateur peut obtenir `R_AB` en évaluant la primitive générique avec `rho = rho_AB` et `sigma = rho_A tensor rho_B`.

```text
CORE_API_GENERALITY_DECISION = entropy primitives must not be artificially restricted to faithful states when their established mathematical definition supports positive-semidefinite states.
```

`modular_hamiltonian` reste restreint au domaine *faithful* requis par `docs/model/hypothesis.md` v0.2.

```text
T1_CORE_FOUNDATION_IMPLEMENTATION = PASS

CORE_FOUNDATION_HEAD     = 4c4fbf650b3e099c738b90ed9ac3d72952e29bed
CORE_FOUNDATION_TESTS    = 75 PASS
CORE_FOUNDATION_BLOCKING = NONE
```

Ce `PASS` est un `ENGINEERING_PASS` (tests unitaires et invariants d'architecture verts sur le socle `core` générique) et non une `SCIENTIFIC_CONFIRMATION` : aucun résultat scientifique n'est validé par ce lot.

```text
NOTEBOOK_GOVERNANCE = INTEGRATED

NOTEBOOK_ROLE                          = EXECUTABLE_SCIENTIFIC_REPORT
NOTEBOOK_NORMATIVE_SOURCE              = NO
NOTEBOOK_CODE_LIBRARY                  = NO
NOTEBOOK_CAN_CONTAIN_COMMITTED_RESULTS = YES_WITH_PROVENANCE_AND_AUTHORIZED_EXECUTION
NOTEBOOK_CONFIRMATORY_FIREWALL         = SAME_AS_OTHER_CONFIRMATORY_EXECUTION
JUPYTER_RUNTIME_DEPENDENCY             = NOT_ADDED_YET
```

La gouvernance normative applicable aux notebooks Jupyter d'exécution des toy models est intégrée dans `docs/governance/software-architecture-governance.md` §23 et `docs/governance/documentation-governance.md` §2–§4. Aucun notebook, aucun dossier `experiments/` et aucune dépendance Jupyter ne sont créés par ce lot.

---

## Mémoire de session

```text
BRANCHE                     = master
LOT_COURANT                 = MODEL0A-SPEC-1
DERNIER_JALON_VALIDE        = spécification scientifique PROPOSED de model0a créée (docs/toy-models/toy0a/specification.md)
DOCUMENTS_APPLICABLES       = docs/governance/*, docs/model/hypothesis.md, docs/model/hypothesis-annex-a.md, docs/toy-models/toy0a/specification.md
TRAVAIL_REALISE             = rédaction v0.1 ; première revue physic ; corrections v0.2 ; seconde revue physic PASS ; arbitrage ChatGPT PASS ; gel documentaire v0.2 ; audit architectural T1-CORE-FOUNDATION-0A PASS ; arbitrage architecture/core effectué ; implémentation socle core ; correctif fail-closed ; gouvernance Jupyter ; spécification scientifique PROPOSED de model0a (toy0a)
TRAVAIL_NON_REALISE         = revue physic bornée de specification.md ; implémentation model0a ; plan de validation toy0a ; notebook toy0a ; ajout dépendance Jupyter ; définition opérationnelle de T1 ; exécution T1
PROCHAINE_ACTION_AUTORISEE  = revue physic bornée de specification.md après revue du commit distant par ChatGPT
QUESTIONS_OUVERTES          = T4_OPERATIONAL_CRITERION, DIMENSIONAL_CALIBRATION, TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE
BACKLOG_NON_BLOQUANT        = K_ADDITIVE_CONSTANT_CONVENTION_FOR_R_AB, T1_NONTRIVIALITY_CRITERION, RELATIONAL_CLOCK_BOUNDARY_WORDING, JUPYTER_RUNTIME_DEPENDENCY (état technique non ajouté, cf. §23.14 software-architecture-governance.md)
```
