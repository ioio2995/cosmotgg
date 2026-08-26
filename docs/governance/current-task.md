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
PROJECT_STATUS = FOUNDING_HYPOTHESIS_FROZEN
CURRENT_LOT    = NONE
PHASE          = FOUNDING_HYPOTHESIS_FROZEN
```

La gouvernance transverse (`collaboration-governance.md`, `documentation-governance.md`, `software-architecture-governance.md`) et les contrats des rôles spécialisés (`docs/governance/agents/`) sont en place. Aucun modèle jouet, plan de validation ou lot scientifique n'est encore engagé.

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
CURRENT_LOT = NONE
PHASE       = FOUNDING_HYPOTHESIS_FROZEN
```

Aucun lot n'est actuellement engagé. Le dernier lot exécuté (rôle `docs`) a effectué le gel documentaire (`VALIDATED_FOR_FREEZE` → `FROZEN`) de `docs/model/hypothesis.md` et `docs/model/hypothesis-annex-a.md` (v0.2), suite à la seconde contre-expertise `physic` PASS et à l'arbitrage scientifique de ChatGPT. Base du lot : `EXPECTED_HEAD = 589b0727ad880670435bfbb50a268d7472e5410f`.

---

## Mémoire de session

```text
BRANCHE                     = master
LOT_COURANT                 = NONE
DERNIER_JALON_VALIDE        = hypothèse fondatrice CosmoTGG v0.2 gelée
DOCUMENTS_APPLICABLES       = docs/governance/*, docs/model/hypothesis.md, docs/model/hypothesis-annex-a.md
TRAVAIL_REALISE             = rédaction v0.1 ; première revue physic ; corrections v0.2 ; seconde revue physic PASS ; arbitrage ChatGPT PASS ; gel documentaire v0.2
TRAVAIL_NON_REALISE         = définition opératoire de T1 ; définition opératoire de T4 ; tout modèle numérique ; tout test T1-T7 effectif
PROCHAINE_ACTION_AUTORISEE  = cadrage scientifique par ChatGPT du premier lot post-gel, après décision explicite de Lionel ORCIL
QUESTIONS_OUVERTES          = T4_OPERATIONAL_CRITERION, DIMENSIONAL_CALIBRATION, TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE
BACKLOG_NON_BLOQUANT        = K_ADDITIVE_CONSTANT_CONVENTION_FOR_R_AB, T1_NONTRIVIALITY_CRITERION, RELATIONAL_CLOCK_BOUNDARY_WORDING
```
