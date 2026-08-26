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
CURRENT_LOT    = NONE
PHASE          = MODEL0C_CORE_PROMOTION_PENDING_CHATGPT_REVIEW
```

La gouvernance transverse (`collaboration-governance.md`, `documentation-governance.md`, `software-architecture-governance.md`) et les contrats des rôles spécialisés (`docs/governance/agents/`) sont en place. Le lot `T1-CORE-FOUNDATION-0A` (fondation `core` préalable au test de réfutabilité T1) a été implémenté et la gouvernance des notebooks Jupyter d'exécution des toy models a été intégrée (§ci-dessous). Une première spécification scientifique `PROPOSED` de `model0a` (`docs/toy-models/toy0a/specification.md`) a été créée par le lot `MODEL0A-SPEC-1` puis revue par ChatGPT (`MODEL0A_CHATGPT_SPEC_REVIEW = PASS`) et acceptée par Lionel ORCIL comme base de conception (`MODEL0A_SPECIFICATION_STATUS = ACCEPTED_AS_DESIGN_BASIS`). Le lot `MODEL0A-DESIGN-1` a fermé `LOCAL_DIMENSION` et `STATE_FAMILY` par décision ChatGPT et créé le design d'implémentation minimal (`docs/toy-models/toy0a/implementation-design.md`). La famille d'états a ensuite été implémentée (`MODEL0A_STATE_HEAD = d6b80f51d4f7262307ad38722219025390221684`, `MODEL0A_STATE_IMPL_1 = ACCEPTED`). Le lot `MODEL0A-DIAGNOSTICS-DESIGN-1` a intégré la structure analytique de qualification du cocycle (§9 de `specification.md`) et étendu `implementation-design.md` avec le module `diagnostics.py` ; ces diagnostics (`model0a_reference_state`, `log_commutator_obstruction`, `ordinary_group_defect`) ont ensuite été implémentés et testés par le lot `MODEL0A-DIAGNOSTICS-IMPL-1` ; aucun plan de validation et aucun notebook ne sont encore engagés.

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

## Règle active — gel documentaire pendant l'implémentation et canal `current-task.md`

Intégrée par le lot `GOV-IMPLEMENTATION-NARRATIVE-1` :

```text
TOY_IMPLEMENTATION_DOCUMENT_FREEZE = ENABLED
DOCUMENT_REOPEN_CONDITION          = FUNDAMENTAL_BLOCKING_ONLY

CURRENT_TASK_ROLE                           = SHARED_OPERATIONAL_COMMUNICATION_CHANNEL
CURRENT_TASK_EXCLUDED_FROM_DOCUMENT_FREEZE  = TRUE
CURRENT_TASK_WRITABLE_DURING_IMPLEMENTATION = TRUE
CURRENT_TASK_IMPLICIT_WRITE_AUTHORIZATION   = TRUE
```

À partir du premier lot d'implémentation de code d'un toy, `specification.md` et `implementation-design.md` de ce toy sont `READ_ONLY_DURING_IMPLEMENTATION` et ne sont réouverts que pour un blocage fondamental démontré, avec arbitrage ChatGPT/Lionel puis mandat documentaire borné (`docs/governance/documentation-governance.md` §11.1–§11.2). Le récit scientifique courant de l'expérience est porté par le notebook du toy (`docs/governance/documentation-governance.md` §11.3), pas par une succession de micro-lots documentaires (`docs/governance/collaboration-governance.md` §14.4).

`docs/governance/current-task.md` reste modifiable par `docs`, `code` et `physic` pendant leurs lots respectifs, y compris lorsqu'il n'est pas listé explicitement parmi les fichiers autorisés du mandat, mais uniquement pour l'enregistrement factuel prévu par `docs/governance/collaboration-governance.md` §14.1–§14.3 : cela ne crée pas de lot `docs`, ne change pas la science gelée, ne change pas la gouvernance, et n'autorise pas seul le lot suivant.

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
CURRENT_LOT = NONE
PHASE       = MODEL0B_DESIGN_PENDING_CHATGPT_REVIEW
```

Le rôle `docs` a créé la première spécification scientifique `PROPOSED` de `model0a` (`docs/toy-models/toy0a/specification.md`), sur décisions déjà arbitrées par ChatGPT (revue physique bornée). Les deux lots précédents ont été menés à terme : l'implémentation bornée du socle `core` (`T1-CORE-FOUNDATION-0A`) et l'intégration de la gouvernance des notebooks Jupyter d'exécution des toy models (`NOTEBOOK-GOVERNANCE-1`). Le lot antérieur à ces deux-là (rôle `docs`) avait effectué le gel documentaire (`VALIDATED_FOR_FREEZE` → `FROZEN`) de `docs/model/hypothesis.md` et `docs/model/hypothesis-annex-a.md` (v0.2), suite à la seconde contre-expertise `physic` PASS et à l'arbitrage scientifique de ChatGPT.

```text
MODEL0A_T1_BOUNDARY_REVIEW   = PASS_WITH_CHATGPT_CORRECTIONS
MODEL0A_CARRIER_CANDIDATE    = FINITE_CONNES_COCYCLE
MODEL0A_T1_STATUS            = OPEN_NOT_EXECUTED
MODEL0A_CHATGPT_SPEC_REVIEW  = PASS
MODEL0A_SPECIFICATION_STATUS = ACCEPTED_AS_DESIGN_BASIS
MODEL0A_SPECIFICATION_FREEZE = NOT_YET_REQUIRED
```

Décision de Lionel ORCIL et arbitrage ChatGPT sur le workflow de conception : les revues `physic` / Opus ne sont pas requises à chaque étape de conception d'un toy. Opus reste réservé aux décisions ou blocages scientifiques structurels nécessitant une escalade explicite (cf. `docs/governance/collaboration-governance.md` §12.3–§12.4). Pour `model0a`, la revue ChatGPT du commit `6673a5fa80e21689a0e50a91fed8290abe0473d3` est suffisante pour poursuivre la conception avec Sonnet/`code`.

```text
PHYSIC_ESCALATION  = NOT_REQUIRED_FOR_CURRENT_MODEL0A_DESIGN
OPUS_USAGE_POLICY  = STRUCTURAL_SCIENTIFIC_ESCALATION_ONLY
```

Le lot `MODEL0A-DESIGN-1` (rôle `docs`) a intégré la fermeture par ChatGPT de `LOCAL_DIMENSION` et `STATE_FAMILY` dans `docs/toy-models/toy0a/specification.md` (§2–§3) et créé `docs/toy-models/toy0a/implementation-design.md` (`PROPOSED_IMPLEMENTATION_DESIGN`).

```text
MODEL0A_LOCAL_DIMENSION       = (2, 2)
MODEL0A_STATE_FAMILY          = TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY
MODEL0A_IMPLEMENTATION_DESIGN = PROPOSED

STATE_PARAMETER_VALUES        = OPEN
NUMERICAL_TOLERANCES          = OPEN
MODEL0A_ACCEPTANCE_CRITERION  = OPEN

OPUS_ESCALATION = NOT_REQUIRED
```

Le lot `MODEL0A-DIAGNOSTICS-DESIGN-1` (rôle `docs`) a intégré la structure analytique de qualification du cocycle retenue par ChatGPT (`docs/toy-models/toy0a/specification.md` §9) et étendu `docs/toy-models/toy0a/implementation-design.md` avec le futur module `diagnostics.py`, sans code.

```text
MODEL0A_STATE_IMPLEMENTATION = PASS
MODEL0A_STATE_HEAD           = d6b80f51d4f7262307ad38722219025390221684

MODEL0A_DIAGNOSTIC_STRUCTURE = LOG_COMMUTATOR_PLUS_ORDINARY_GROUP_DEFECT
MODEL0A_DIAGNOSTICS_DESIGN   = PROPOSED
```

Le lot `MODEL0A-DIAGNOSTICS-IMPL-1` (rôle `code`) a implémenté ces diagnostics (`src/cosmotgg/models/model0a/diagnostics.py`) et leurs tests (`tests/models/model0a/test_diagnostics.py`), sans modifier `specification.md` ni `implementation-design.md` (`READ_ONLY_DURING_IMPLEMENTATION`).

```text
MODEL0A_DIAGNOSTICS_IMPLEMENTATION = PASS
MODEL0A_DIAGNOSTICS_HEAD           = 49b629a2ba5de5d50bcc488b7400dbc90425a178
MODEL0A_DIAGNOSTICS                = LOG_COMMUTATOR_PLUS_ORDINARY_GROUP_DEFECT
MODEL0A_DIAGNOSTICS_TESTS          = 166 PASS (143 baseline + 23 nouveaux)

MODEL0A_DIAGNOSTICS_REVIEW         = ACCEPTED
MODEL0A_DIAGNOSTICS_ACCEPTED_HEAD  = 49b629a2ba5de5d50bcc488b7400dbc90425a178

JUPYTER_RUNTIME_HEAD               = 2de8c4703a2f2d9941885da1cdf8232c070adb6d
```

Application immédiate à `model0a` de la règle de gel documentaire ci-dessus (`GOV-IMPLEMENTATION-NARRATIVE-1`) : l'implémentation de `model0a` a déjà commencé (`MODEL0A_STATE_HEAD`).

```text
MODEL0A_SPECIFICATION            = READ_ONLY_DURING_IMPLEMENTATION
MODEL0A_IMPLEMENTATION_DESIGN    = READ_ONLY_DURING_IMPLEMENTATION
MODEL0A_NORMAL_DOCS_LOTS         = DISABLED_DURING_IMPLEMENTATION
MODEL0A_EXPERIMENTAL_NARRATIVE_TARGET = experiments/toy0a/toy0a.ipynb
MODEL0A_DOCUMENT_REOPEN_CONDITION = FUNDAMENTAL_BLOCKING_ONLY
```

Le lot `MODEL0A-NOTEBOOK-QUALIFICATION-1-R1` (rôle `code`) a créé et exécuté le premier récit scientifique exécutable de `toy0a` :

```text
MODEL0A_NOTEBOOK                 = experiments/toy0a/toy0a.ipynb
MODEL0A_NOTEBOOK_SOURCE_HEAD     = 2f052e849162628629a7118b7509c16a5bd1bf38
MODEL0A_NOTEBOOK_EXECUTION_CLASS = QUALIFICATION_NONCONFIRMATORY
MODEL0A_NOTEBOOK_STATUS          = IMPLEMENTED_EXECUTED_PENDING_CHATGPT_REVIEW

MODEL0A_NOTEBOOK_REVIEW          = ACCEPTED
MODEL0A_NOTEBOOK_ACCEPTED_HEAD   = 78539a7a82ec5a49b2382c7dd181dbca86d39d88
```

Exécution top-to-bottom dans un kernel Python neuf (`nbclient`), sans état caché, sorties conservées telles qu'issues de cette exécution. Aucun paramètre `OPEN` n'est fermé par ce notebook.

Le lot `MODEL0A-LOCAL-UNITARY-COVARIANCE-1` (rôle `code`) a qualifié la covariance des diagnostics structurels sous changement de bases locales `U = U_A ⊗ U_B` (référence, information mutuelle, `R_AB`, cocycle, `C_AB`, `G`, classification N0/N1/N2), étendu `experiments/toy0a/toy0a.ipynb` (§15) et réexécuté l'ensemble du notebook top-to-bottom dans un kernel neuf, sans modifier `src/` :

```text
MODEL0A_LOCAL_UNITARY_COVARIANCE       = PASS_QUALIFICATION
MODEL0A_LOCAL_UNITARY_COVARIANCE_CLASS = LOCAL_PRODUCT_UNITARY_ONLY

MODEL0A_LOCAL_UNITARY_COVARIANCE_REVIEW          = ACCEPTED
MODEL0A_LOCAL_UNITARY_COVARIANCE_ACCEPTED_HEAD   = d967fc9918aebe9a55133c727fa507f0bb6e8196
```

Portée explicitement bornée : ce contrôle couvre uniquement `U_A ⊗ U_B` (changement de base local préservant la décomposition `A|B`), pas un unitaire global/entanglant arbitraire ni un changement de factorisation tensorielle.

Le lot `MODEL0A-NEGATIVE-CONTROLS-1` (rôle `code`) a ajouté trois contrôles négatifs (`tests/models/model0a/test_diagnostics.py`, §16 du notebook) protégeant contre trois faux positifs d'interprétation, corrigé l'hygiène d'un helper de la §15 (`apply_local_unitary` retiré, expression inline), et réexécuté l'ensemble du notebook top-to-bottom dans un kernel neuf, sans modifier `src/` :

```text
MODEL0A_NEGATIVE_CONTROLS                    = PASS_QUALIFICATION
MODEL0A_NEGATIVE_CONTROL_OFF_DIAGONAL        = PASS
MODEL0A_NEGATIVE_CONTROL_MUTUAL_INFORMATION  = PASS
MODEL0A_NEGATIVE_CONTROL_G_ACCIDENTAL_ZERO   = PASS
MODEL0A_NOTEBOOK_HELPER_HYGIENE              = PASS
```

ChatGPT a rendu la décision finale de clôture de la qualification `NONCONFIRMATORY` de `model0a` (lot `MODEL0A-QUALIFICATION-CLOSURE-1`, rôle `code`), enregistrée dans `experiments/toy0a/toy0a.ipynb` §17 :

```text
MODEL0A_FINAL_QUALIFICATION_REVIEW = PASS
MODEL0A_QUALIFICATION_STATUS       = COMPLETE_ACCEPTED_NONCONFIRMATORY
MODEL0A_QUALIFICATION_HEAD         = 2f052e849162628629a7118b7509c16a5bd1bf38
MODEL0A_RESTRICTED_CLAIM           = PASS_QUALIFICATION
MODEL0A_PHASE                      = CLOSED_AT_QUALIFICATION_LEVEL

T1                           = OPEN_NOT_EXECUTED
RELATIONAL_TIME_ESTABLISHED  = NO
CONFIRMATORY_PROTOCOL        = NOT_DEFINED
OPUS_ESCALATION               = NOT_REQUIRED
```

Restent explicitement `OPEN` (non fermés par cette clôture de qualification) : `STATE_PARAMETER_VALUES`, `MODULAR_PARAMETER_DOMAIN`, `NUMERICAL_TOLERANCES`, `T1_NONTRIVIALITY_CRITERION`, `MODEL0A_ACCEPTANCE_CRITERION`.

```text
NEXT_SCIENTIFIC_TARGET = T1_RELATIVE_CHANGE_CONSTRUCTION
NEXT_MODEL              = model0b
NEXT_TOY                 = toy0b
```

Ceci ne change aucun contenu scientifique de `docs/toy-models/toy0a/specification.md` ou `docs/toy-models/toy0a/implementation-design.md`.

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
JUPYTER_RUNTIME_DEPENDENCY             = ADDED
```

La gouvernance normative applicable aux notebooks Jupyter d'exécution des toy models est intégrée dans `docs/governance/software-architecture-governance.md` §23 et `docs/governance/documentation-governance.md` §2–§4.

Le lot `MODEL0A-NOTEBOOK-QUALIFICATION-1` (rôle `code`) a retourné `CODE_IMPLEMENTATION = BLOCKED` / `JUPYTER_RUNTIME_MISSING = CONFIRMED` (aucun runtime Jupyter exécutable dans l'environnement de travail) sans modifier aucun fichier. Le lot correctif `JUPYTER-RUNTIME-1` (rôle `code`) a ajouté l'extra optionnel minimal `notebook` à `pyproject.toml` et installé/vérifié le runtime dans l'environnement de travail :

```text
JUPYTER_RUNTIME_EXTRA      = notebook
JUPYTER_RUNTIME_COMPONENTS = nbformat==5.10.4, nbclient==0.11.0, ipykernel==7.3.0
JUPYTER_CLI_REQUIRED       = NO
NBCONVERT_REQUIRED         = NO
JUPYTER_RUNTIME_SMOKE_TEST = PASS
```

Ces dépendances sont des dépendances optionnelles d'exécution scientifique (`[project.optional-dependencies].notebook`), non des dépendances obligatoires de `cosmotgg.core`/`cosmotgg.models`. Aucun notebook et aucun dossier `experiments/` ne sont créés par ce lot.

Le lot `MODEL0B-DESIGN-1` (rôle `docs`) a créé, en un seul lot pré-implémentation, la spécification scientifique proposée et la conception d'implémentation de `model0b` (`docs/toy-models/toy0b/specification.md`, `docs/toy-models/toy0b/implementation-design.md`), transformant l'arbitrage scientifique de ChatGPT — appuyé par la contre-expertise `MODEL0B-OVERLAP-PROJECTION-REVIEW-1` — en contrat explicite :

```text
MODEL0B_OVERLAP_PROJECTION_REVIEW    = ACCEPTED
MODEL0B_CANDIDATE_DISPOSITION        = ADMISSIBLE_FOR_NONCONFIRMATORY_QUALIFICATION

MODEL0B_SPECIFICATION_STATUS         = PROPOSED_PENDING_CHATGPT_REVIEW
MODEL0B_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

MODEL0B_CLASS = T1_RELATIVE_MODULAR_GENERATOR_QUALIFICATION_NONCONFIRMATORY

COSMOTGG_TEST_TARGET             = T1_RELATIONAL_FLOW
MODEL0B_IS_T1_CONFIRMATORY_TEST  = NO
MODEL0B_PROVES_T1                = NO
MODEL0B_PROVES_RELATIONAL_TIME   = NO

T1_STATUS = OPEN_NOT_EXECUTED
```

`model0b` compare deux structures modulaires chevauchantes (\(\rho_{AB}\), \(\rho_{BC}\), sur le sous-système commun \(B\) de \(\mathcal H_A\otimes\mathcal H_B\otimes\mathcal H_C\)) et définit un générateur/dérivation algébrique relatif candidat, `OVERLAP_RELATIVE_MODULAR_GENERATOR`/`OVERLAP_RELATIVE_MODULAR_DERIVATION`, sans construire de flot fini paramétré (`FINITE_FLOW_PARAMETER_PROBLEM = OPEN`) et sans établir de changement physique relationnel, de temps relationnel, ni T1. Aucun code, aucun notebook, aucune exécution confirmatoire n'est produit par ce lot.

Le lot `MODEL0B-IMPL-1` (rôle `code`) a implémenté le socle complet de `model0b` sur la base de ce contrat, sans modifier `docs/toy-models/toy0b/specification.md` ni `docs/toy-models/toy0b/implementation-design.md` (`READ_ONLY_DURING_IMPLEMENTATION`) : la famille d'états `three_qubit_overlapping_pauli_relation_state(beta, lambda_, mu)` (`src/cosmotgg/models/model0b/states.py`, domaine analytique exact `beta**2+lambda**2+mu**2<1` fail-closed, sans tolérance) ; le générateur relatif `overlap_relative_modular_generator` et la dérivation `overlap_relative_modular_derivation` (`src/cosmotgg/models/model0b/relative.py`), construits par le mécanisme modulaire réel (`partial_trace` + `modular_hamiltonian` + conditional expectation traciale normalisée + réduction sans trace `tl_B` privée model-specific), pas par raccourci de la formule analytique fermée du §14 (utilisée uniquement comme oracle de test indépendant, `tests/models/model0b/test_relative.py`) ; les contrôles structurels R0–R3 et la condition exacte de non-nullité (§15–§16 de la spécification) ; la covariance locale `U_A ⊗ U_B ⊗ U_C` bornée à `LOCAL_PRODUCT_UNITARY_COVARIANCE` ; et la régression de la normalisation `1/2` de la conditional expectation (REL1 échoue si elle est omise, vérifié explicitement). Aucun flot fini paramétré n'est exposé (`FINITE_FLOW_PARAMETER_PROBLEM` reste `OPEN`).

```text
MODEL0B_DESIGN_REVIEW        = ACCEPTED
MODEL0B_DESIGN_ACCEPTED_HEAD = 139f05261a095473bab301fc7b48eb81e3ee392d

MODEL0B_SPECIFICATION         = READ_ONLY_DURING_IMPLEMENTATION
MODEL0B_IMPLEMENTATION_DESIGN = READ_ONLY_DURING_IMPLEMENTATION

MODEL0B_IMPLEMENTATION       = PASS
MODEL0B_IMPLEMENTATION_HEAD  = 383026bffad655aa4a60b63c514ae8f807b7f13f
MODEL0B_IMPLEMENTATION_CLASS = NONCONFIRMATORY_QUALIFICATION_INFRASTRUCTURE

T1_STATUS = OPEN_NOT_EXECUTED
```

Ce `PASS` est un `ENGINEERING_PASS` (270 tests verts : 205 baseline + 65 nouveaux) et non une confirmation scientifique : aucun paramètre `OPEN` n'est fermé par ce lot (`BETA_VALUE`, `LAMBDA_VALUE`, `MU_VALUE`, `NUMERICAL_TOLERANCES`, `MODEL0B_ACCEPTANCE_CRITERION`, `T1_NONTRIVIALITY_CRITERION` restent `OPEN`), `T1` reste `OPEN_NOT_EXECUTED`, et `RELATIONAL_TIME`/`RELATIONAL_PHYSICAL_CHANGE` restent `NOT_ESTABLISHED`.

Le lot `MODEL0B-NOTEBOOK-QUALIFICATION-1` (rôle `code`) a créé et exécuté le premier récit scientifique exécutable de `toy0b`, `experiments/toy0b/toy0b.ipynb` (20 sections narratives + provenance), sans modifier `docs/toy-models/toy0b/specification.md` ni `docs/toy-models/toy0b/implementation-design.md` (`READ_ONLY_DURING_IMPLEMENTATION`) et sans modifier `src/` ni `tests/` : famille d'états et états réduits (§3–§4) ; structures modulaires `K_AB`/`K_BC` et conditional expectation traciale sur le chevauchement `B` (§5–§6) ; générateur `Delta_B` via `overlap_relative_modular_generator` (source canonique, pas la formule analytique en production) et confirmation contre l'oracle analytique indépendant du §14 de la spécification, résidu machine (§7–§8) ; dérivation `overlap_relative_modular_derivation` sur `X_B`/`Y_B`/`Z_B` (§9) ; contrôles structurels `R0`–`R3` et condition de non-nullité, avec vérification indépendante de la non-trivialité de `rho_AB`/`rho_BC` en `R1` (§10–§14) ; covariance locale `U_A ⊗ U_B ⊗ U_C` (§15) ; limitation de colinéarité affichée explicitement, non masquée (§16) ; progrès par rapport à `toy0a` (absence de paramètre modulaire partagé dans la définition de `Delta_B`) et rappel explicite que `FINITE_FLOW_PARAMETER_PROBLEM` reste `OPEN` sans construire ni exécuter d'exponentielle matricielle (§17–§18). Exécution top-to-bottom dans un kernel Python neuf (`nbclient`), sans état caché, sorties conservées telles qu'issues de cette exécution. Aucun paramètre `OPEN` n'est fermé par ce notebook ; `T1` reste `OPEN_NOT_EXECUTED`.

```text
MODEL0B_IMPLEMENTATION_REVIEW        = ACCEPTED
MODEL0B_IMPLEMENTATION_ACCEPTED_HEAD = 383026bffad655aa4a60b63c514ae8f807b7f13f

MODEL0B_NOTEBOOK                 = experiments/toy0b/toy0b.ipynb
MODEL0B_NOTEBOOK_SOURCE_HEAD     = 383026bffad655aa4a60b63c514ae8f807b7f13f
MODEL0B_NOTEBOOK_EXECUTION_CLASS = QUALIFICATION_NONCONFIRMATORY
MODEL0B_NOTEBOOK_STATUS          = IMPLEMENTED_EXECUTED_PENDING_CHATGPT_REVIEW

T1_STATUS = OPEN_NOT_EXECUTED
```

ChatGPT a rendu la décision finale de clôture de la qualification `NONCONFIRMATORY` de `model0b` (lot `MODEL0B-QUALIFICATION-CLOSURE-1`, rôle `code`), enregistrée dans `experiments/toy0b/toy0b.ipynb` §21 : générateur relatif `Delta_B` et dérivation algébrique `D` qualifiés comme candidats, sans paramètre modulaire partagé dans leur définition (`SHARED_PARAMETER_FALSE_POSITIVE = AVOIDED_AT_DELTA_LEVEL_ONLY`), mais avec deux limitations explicites : dans la famille d'états déclarée, `Delta_B` reste colinéaire au générateur modulaire local de `B` (`OVERLAP_DERIVATION_COLLINEAR_WITH_LOCAL_MODULAR_GENERATOR = TRUE_FOR_DECLARED_STATE_FAMILY`) et aucun paramètre intrinsèque de flot fini n'est produit (`FINITE_FLOW_PARAMETER_PROBLEM = OPEN`) :

```text
MODEL0B_NOTEBOOK_REVIEW        = ACCEPTED
MODEL0B_NOTEBOOK_ACCEPTED_HEAD = e18189e90cd9851a16e94f954abccaaad2294d3c

MODEL0B_QUALIFICATION_STATUS = COMPLETE_ACCEPTED_NONCONFIRMATORY
MODEL0B_QUALIFICATION_HEAD   = e18189e90cd9851a16e94f954abccaaad2294d3c
MODEL0B_PHASE                = CLOSED_AT_QUALIFICATION_LEVEL

RELATIVE_ALGEBRAIC_GENERATOR  = QUALIFIED_CANDIDATE
RELATIVE_ALGEBRAIC_DERIVATION = QUALIFIED_CANDIDATE

RELATIONAL_PHYSICAL_CHANGE = NOT_ESTABLISHED
RELATIONAL_TIME            = NOT_ESTABLISHED
T1                          = OPEN_NOT_EXECUTED
```

Restent explicitement `OPEN` (non fermés par cette clôture de qualification) : `BETA_VALUE`, `LAMBDA_VALUE`, `MU_VALUE`, `NUMERICAL_TOLERANCES`, `MODEL0B_ACCEPTANCE_CRITERION`, `T1_NONTRIVIALITY_CRITERION`, `FINITE_FLOW_PARAMETER_PROBLEM`, `ALGEBRAIC_GENERALIZATION_OF_DELTA`, `TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE`.

```text
NEXT_SCIENTIFIC_TARGET = NONCOLLINEAR_OVERLAP_RELATIVE_GENERATOR
NEXT_MODEL              = model0c
NEXT_TOY                 = toy0c
```

Ceci ne change aucun contenu scientifique de `docs/toy-models/toy0b/specification.md` ou `docs/toy-models/toy0b/implementation-design.md`.

Le lot `MODEL0C-DESIGN-1` (rôle `docs`) a créé, en un seul lot pré-implémentation, la spécification scientifique proposée et la conception d'implémentation de `model0c` (`docs/toy-models/toy0c/specification.md`, `docs/toy-models/toy0c/implementation-design.md`), transformant en contrat explicite la revue scientifique `MODEL0C-NONCOLLINEAR-CANDIDATE-REVIEW` :

```text
MODEL0C_NONCOLLINEAR_CANDIDATE_REVIEW = ACCEPTED_WITH_LOCAL_CORRECTION
MODEL0C_CANDIDATE_DISPOSITION         = ADMISSIBLE_FOR_NONCONFIRMATORY_QUALIFICATION

MODEL0C_SPECIFICATION_STATUS         = PROPOSED_PENDING_CHATGPT_REVIEW
MODEL0C_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

MODEL0C_CLASS = T1_NONCOLLINEAR_RELATIVE_MODULAR_GENERATOR_QUALIFICATION_NONCONFIRMATORY

COSMOTGG_TEST_TARGET             = T1_RELATIONAL_FLOW
MODEL0C_IS_T1_CONFIRMATORY_TEST  = NO
MODEL0C_PROVES_RELATIONAL_TIME   = NO

T1_STATUS = OPEN_NOT_EXECUTED
```

`model0c` teste si deux relations modulaires chevauchantes (\(\rho_{AB}\), \(\rho_{BC}\), sur le sous-système commun \(B\) de \(\mathcal H_A\otimes\mathcal H_B\otimes\mathcal H_C\), famille `THREE_QUBIT_NONCOLLINEAR_OVERLAP_RELATION_FAMILY`) peuvent produire sur \(B\) deux directions opératorielles non colinéaires : les générateurs projetés \(\chi_A \propto X_B\), \(\chi_C \propto Y_B\) et le diagnostic \(N=i[\chi_A,\chi_C]\), non nul exactement lorsque \(\alpha\gamma\lambda\mu\neq0\) (`STRUCTURAL_ANALYTIC`, `NONCOLLINEARITY_COMMUTATOR_EQUIVALENCE = QUBIT_OVERLAP_ONLY`, non généralisé à \(d_B>2\)). La limitation de colinéarité de `model0b` est levée dans cette famille candidate (`MODEL0B_COLLINEARITY_LIMIT = REMOVED_IN_MODEL0C_CANDIDATE`), sans affecter `docs/toy-models/toy0b/specification.md` ni `docs/toy-models/toy0b/implementation-design.md` :

```text
MODEL0B_R3_INTERPRETATION_SCOPE = MODEL0B_DECLARED_STATE_FAMILY_ONLY
```

Limites déclarées explicitement : `N=0` peut signifier des contributions colinéaires ou l'une des deux nulle, et la famille `model0c` ne réalise pas le cas `chi_A≠0, chi_C≠0, chi_A ∥ chi_C` ; `ROBUST_AMPLITUDE = NO` (seuls les axes \(X_B\)/\(Y_B\) sont robustes sous projection \(B\)-bimodulaire arbitraire, pas l'amplitude) ; `FINITE_FLOW_PARAMETER_PROBLEM = OPEN` ; `MODEL0C_SUCCESS != T1`. Aucun code, aucun notebook, aucune exécution T1 n'est produit par ce lot.

L'audit architectural obligatoire (`docs/toy-models/toy0c/implementation-design.md` §4) a conclu :

```text
CORE_PROMOTION_NEEDED = YES
CORE_PROMOTION_TARGET = cosmotgg.core.states.conditional_expectation, cosmotgg.core.states.traceless_part
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
```

sur la base d'un second modèle concret (`model0c`, après `model0b`) réutilisant identiquement la conditional expectation traciale normalisée et la réduction sans trace, sans exécuter cette promotion ni modifier aucun code dans ce lot.

```text
MODEL0C_DESIGN_REVIEW          = ACCEPTED
MODEL0C_DESIGN_ACCEPTED_HEAD   = cf18c9197e115583bfd15a0dd9b853b3ea9f7381
```

Le lot `CORE-OVERLAP-ALGEBRA-1` (rôle `code`) a exécuté cette promotion : `conditional_expectation` et `traceless_part` sont ajoutées à `cosmotgg.core.states` (module-independent, `SCIENTIFIC_METADATA.status = established` déjà porté par le module), testées par 22 tests model-free (`tests/core/test_states.py`, CE1–CE9 et TP1–TP8 : identité bipartite, équivalence exacte avec `partial_trace`, dimensions non qubit `(2,3,2)`, `keep` multi-facteurs, `keep = all`, préservation de la trace normalisée, bimodularité `E[(I⊗B1) X (I⊗B2)] = B1 E(X) B2`, entrée non hermitienne, propagation fail-closed des erreurs de `partial_trace`, dimension générique, rejets non-square/dimension-zéro/NaN/inf). `src/cosmotgg/models/model0b/relative.py` a été refactoré pour consommer ces deux primitives promues (suppression de la primitive privée `_traceless`, remplacement de `partial_trace(K)/2` par `conditional_expectation(...)`), sans changement de mécanisme scientifique, de signature publique, ni de comportement numérique (`Delta_B = -tl(E_A) + tl(E_C)` inchangé). Aucun fichier `model0c` n'est créé.

```text
CORE_OVERLAP_ALGEBRA_PROMOTION = PASS
CORE_PROMOTED_PRIMITIVES       = conditional_expectation, traceless_part

MODEL0B_CORE_REFACTOR = PASS_NO_SCIENTIFIC_CHANGE

T1_STATUS = OPEN_NOT_EXECUTED

CURRENT_LOT                = NONE
PHASE                      = MODEL0C_CORE_PROMOTION_PENDING_CHATGPT_REVIEW
PROCHAINE_ACTION_AUTORISEE = remote core promotion review by ChatGPT
```

---

## Mémoire de session

```text
BRANCHE                     = master
LOT_COURANT                 = NONE
DERNIER_JALON_VALIDE        = promotion vers core de conditional_expectation et traceless_part (cosmotgg.core.states), 22 tests model-free ajoutés (tests/core/test_states.py), refactor de src/cosmotgg/models/model0b/relative.py pour consommer ces primitives (suppression de _traceless, remplacement de partial_trace(K)/2 par conditional_expectation), sans changement scientifique ni d'API publique model0b, aucun fichier model0c créé, lot CORE-OVERLAP-ALGEBRA-1
DOCUMENTS_APPLICABLES       = docs/governance/*, docs/model/hypothesis.md, docs/model/hypothesis-annex-a.md, docs/toy-models/toy0a/specification.md, docs/toy-models/toy0a/implementation-design.md, docs/toy-models/toy0b/specification.md, docs/toy-models/toy0b/implementation-design.md, docs/toy-models/toy0c/specification.md, docs/toy-models/toy0c/implementation-design.md
TRAVAIL_REALISE             = rédaction v0.1 ; première revue physic ; corrections v0.2 ; seconde revue physic PASS ; arbitrage ChatGPT PASS ; gel documentaire v0.2 ; audit architectural T1-CORE-FOUNDATION-0A PASS ; arbitrage architecture/core effectué ; implémentation socle core ; correctif fail-closed ; gouvernance Jupyter ; spécification scientifique PROPOSED de model0a (toy0a) ; revue ChatGPT PASS de specification.md ; synchronisation du workflow de conception model0a (physic/Opus réservés à l'escalade scientifique structurelle) ; fermeture LOCAL_DIMENSION=(2,2) et STATE_FAMILY=TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY ; création implementation-design.md ; implémentation states.py (MODEL0A_STATE_HEAD=d6b80f5) ; structure analytique de qualification du cocycle (LOG_COMMUTATOR_OBSTRUCTION, ORDINARY_GROUP_DEFECT, table N0/N1/N2) ; extension implementation-design.md avec diagnostics.py ; intégration du gel documentaire toy-en-implémentation et du canal current-task.md partagé (collaboration-governance.md §14, documentation-governance.md §11, agents/*.md) ; application de la règle à model0a ; implémentation de model0a/diagnostics.py (model0a_reference_state, log_commutator_obstruction, ordinary_group_defect) et de tests/models/model0a/test_diagnostics.py (lot MODEL0A-DIAGNOSTICS-IMPL-1) ; tentative de notebook de qualification bloquée sur runtime Jupyter absent (lot MODEL0A-NOTEBOOK-QUALIFICATION-1, aucune modification) ; ajout de l'extra optionnel `notebook` (nbformat==5.10.4, nbclient==0.11.0, ipykernel==7.3.0) à pyproject.toml et vérification par smoke test (lot JUPYTER-RUNTIME-1) ; création et exécution top-to-bottom du premier notebook de qualification exécutable de toy0a, experiments/toy0a/toy0a.ipynb (lot MODEL0A-NOTEBOOK-QUALIFICATION-1-R1) ; qualification de la covariance locale U_A⊗U_B des diagnostics structurels (tests COV1-COV7 dans test_diagnostics.py, §15 du notebook, aucune modification de src/), lot MODEL0A-LOCAL-UNITARY-COVARIANCE-1 ; ajout des contrôles négatifs NC1/NC2/NC3 (tests NC1-NC3 dans test_diagnostics.py, §16 du notebook), correction d'hygiène du helper de la §15, aucune modification de src/, lot MODEL0A-NEGATIVE-CONTROLS-1 ; clôture de la qualification NONCONFIRMATORY de model0a (§17 du notebook, bilan/limites/frontière suivante, aucune nouvelle équation), lot MODEL0A-QUALIFICATION-CLOSURE-1 ; création en un seul lot pré-implémentation de docs/toy-models/toy0b/specification.md et docs/toy-models/toy0b/implementation-design.md, transformant l'arbitrage ChatGPT/MODEL0B-OVERLAP-PROJECTION-REVIEW-1 en contrat explicite (générateur/dérivation algébrique relatif OVERLAP_RELATIVE_MODULAR_GENERATOR/OVERLAP_RELATIVE_MODULAR_DERIVATION sur le chevauchement B de rho_AB/rho_BC), lot MODEL0B-DESIGN-1 ; implémentation du socle complet de model0b — three_qubit_overlapping_pauli_relation_state (src/cosmotgg/models/model0b/states.py), overlap_relative_modular_generator/overlap_relative_modular_derivation par mécanisme modulaire réel (src/cosmotgg/models/model0b/relative.py), tests R0-R3/non-nullité/covariance locale U_A⊗U_B⊗U_C/fail-closed (tests/models/model0b/), sans modifier specification.md ni implementation-design.md, lot MODEL0B-IMPL-1 ; création et exécution top-to-bottom (kernel neuf, nbclient, sans état caché) du premier notebook de qualification exécutable de toy0b, experiments/toy0b/toy0b.ipynb (20 sections : famille d'états, états réduits, K_AB/K_BC, chevauchement B, Delta_B via overlap_relative_modular_generator, oracle analytique indépendant, dérivation, R0-R3, non-nullité, covariance locale, limitation de colinéarité, progrès vs toy0a, FINITE_FLOW_PARAMETER_PROBLEM=OPEN sans construire d'exponentielle, bilan, frontière suivante), sans modifier src/, tests/, specification.md ni implementation-design.md, lot MODEL0B-NOTEBOOK-QUALIFICATION-1 ; clôture par décision ChatGPT de la qualification NONCONFIRMATORY de model0b (§21 du notebook : ce qui est qualifié, progrès exact SHARED_PARAMETER_FALSE_POSITIVE=AVOIDED_AT_DELTA_LEVEL_ONLY, limites OVERLAP_DERIVATION_COLLINEAR_WITH_LOCAL_MODULAR_GENERATOR=TRUE_FOR_DECLARED_STATE_FAMILY et FINITE_FLOW_PARAMETER_PROBLEM=OPEN, frontière suivante), mise à jour de SOURCE_HEAD et réexécution top-to-bottom kernel neuf, sans modifier specification.md, implementation-design.md, src/ ni tests/, lot MODEL0B-QUALIFICATION-CLOSURE-1 ; création en un seul lot pré-implémentation de docs/toy-models/toy0c/specification.md et docs/toy-models/toy0c/implementation-design.md, transformant en contrat explicite la revue MODEL0C-NONCOLLINEAR-CANDIDATE-REVIEW (générateurs projetés chi_A ∝ X_B / chi_C ∝ Y_B sur le chevauchement B de rho_AB/rho_BC, générateur Delta=-chi_A+chi_C, diagnostic de non-colinéarité N=i[chi_A,chi_C] non nul ssi alpha*gamma*lambda*mu≠0, limitation N=0 explicitement déclarée, robustesse des axes/non-robustesse de l'amplitude, contrôle de sensibilité S2 prévu non implémenté, levée justifiée de OVERLAP_DERIVATION_COLLINEAR_WITH_LOCAL_MODULAR_GENERATOR pour cette famille sans modifier model0b, contrôles C0-C4, covariance locale U_A⊗U_B⊗U_C, FINITE_FLOW_PARAMETER_PROBLEM=OPEN), et audit architectural obligatoire concluant CORE_PROMOTION_NEEDED=YES pour conditional_expectation/traceless_part (candidats génériques, non exécuté, aucun code modifié), lot MODEL0C-DESIGN-1 ; promotion vers cosmotgg.core.states de conditional_expectation (conditional expectation traciale normalisée, réutilisant intégralement la validation de partial_trace) et traceless_part (X - Tr(X)/d * I_d, sans tolérance, sans hypothèse d'hermiticité/positivité), 22 tests model-free (CE1-CE9, TP1-TP8, tests/core/test_states.py), refactor de src/cosmotgg/models/model0b/relative.py consommant ces primitives (suppression de _traceless, mécanisme/API/comportement scientifique inchangés, 292 tests verts = 270 baseline + 22 nouveaux), aucun code model0c créé, lot CORE-OVERLAP-ALGEBRA-1
TRAVAIL_NON_REALISE         = state_parameter_values ; modular parameter domain ; numerical tolerances ; plan de validation toy0a ; définition opérationnelle de T1 ; exécution T1 ; BETA_VALUE/LAMBDA_VALUE/MU_VALUE de model0b ; implémentation de model0c (states.py/relative.py) ; ALPHA_VALUE/GAMMA_VALUE/LAMBDA_VALUE/MU_VALUE de model0c ; contrôle de sensibilité S2 de model0c
PROCHAINE_ACTION_AUTORISEE  = remote core promotion review by ChatGPT
QUESTIONS_OUVERTES          = T4_OPERATIONAL_CRITERION, DIMENSIONAL_CALIBRATION, TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE, ALGEBRAIC_GENERALIZATION_OF_DELTA
BACKLOG_NON_BLOQUANT        = K_ADDITIVE_CONSTANT_CONVENTION_FOR_R_AB, T1_NONTRIVIALITY_CRITERION, RELATIONAL_CLOCK_BOUNDARY_WORDING, BASE_COMMIT_FIELD_SEMANTICS_AMBIGUOUS
```
