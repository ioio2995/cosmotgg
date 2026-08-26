# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11 et porte le statut opérationnel courant du projet CosmoTGG.

---

## Git

```text
REPOSITORY    = ioio2995/cosmotgg
REMOTE        = https://github.com/ioio2995/cosmotgg.git
ACTIVE_BRANCH = master
BASE_COMMIT   = NONE
```

Aucun commit n'a encore été effectué sur ce dépôt. Ce document sera mis à jour à chaque jalon.

---

## État global

```text
PROJECT_STATUS = INITIALIZED
CURRENT_LOT    = NONE
PHASE          = GOVERNANCE_SETUP
```

Aucun modèle, spécification ou lot scientifique n'est encore engagé. La gouvernance transverse (`collaboration-governance.md`, `documentation-governance.md`, `software-architecture-governance.md`) et les contrats des rôles spécialisés (`docs/governance/agents/`) sont en place et prêts à s'appliquer dès l'ouverture du premier lot.

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
PHASE       = GOVERNANCE_SETUP
```

Aucun lot n'est ouvert. Ce bloc sera mis à jour au lancement du premier lot conformément au cycle défini dans `docs/governance/collaboration-governance.md` §2.

---

## Mémoire de session

```text
BRANCHE                     = master
COMMIT_DE_TETE              = NONE
LOT_COURANT                 = NONE
DERNIER_JALON_VALIDE        = NONE (initialisation de la gouvernance)
DOCUMENTS_APPLICABLES       = docs/governance/*
TRAVAIL_REALISE             = mise en place de la gouvernance transverse et des rôles spécialisés (docs, code, physic) pour CosmoTGG
TRAVAIL_NON_REALISE         = tout lot scientifique ou d'implémentation
PROCHAINE_ACTION_AUTORISEE  = commit initial, puis cadrage du premier lot par Lionel ORCIL / ChatGPT
QUESTIONS_OUVERTES          = aucune
```
