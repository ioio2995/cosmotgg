# toy0c — Conception d'implémentation (model0c)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model0c`, sur la base de `docs/toy-models/toy0c/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun critère ou verdict T1.

---

## 1. Périmètre

Ce document couvre :

- la construction de la famille d'états de `model0c` (`docs/toy-models/toy0c/specification.md` §5) ;
- le design minimal des générateurs relatifs projetés \(\chi_A\), \(\chi_C\), du générateur \(\Delta\) et du diagnostic de non-colinéarité \(N\) (spécification §8–§14) ;
- le design minimal des tests structurels C0–C4 et de covariance locale (spécification §18–§19) ;
- l'audit architectural obligatoire de réutilisation `core` (§4 ci-dessous), imposé par le fait qu'un second modèle concret (`model0b`, puis `model0c`) utilise désormais le même mécanisme conceptuel.

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les valeurs numériques de \(\alpha,\gamma,\lambda,\mu\) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire ;
- le plan de validation ;
- un critère d'acceptation de `model0c` ou de T1 ;
- tout flot fini paramétré (spécification §20, `FINITE_FLOW_PARAMETER_PROBLEM = OPEN`) ;
- l'implémentation du contrôle de sensibilité S2 (spécification §16), qui reste conceptuel à ce stade (§10 ci-dessous).

---

## 2. Vérification du contrat réel des primitives `core` réutilisées

`model0c` réutilise le même mécanisme conceptuel que `model0b` : trace partielle, hamiltonien modulaire, conditional expectation traciale, réduction sans trace, générateur relatif de chevauchement.

Le contrat réel des primitives `core` déjà vérifié par `docs/toy-models/toy0b/implementation-design.md` §2–§3 reste valable sans changement :

- `cosmotgg.core.states.validate_density_matrix` — validation générique d'une matrice densité, tolérances explicites sans valeur par défaut ;
- `cosmotgg.core.states.partial_trace` — trace partielle générique sur un produit tensoriel fini explicite, ne fait aucune hypothèse de structure bipartite/qubit ;
- `cosmotgg.core.modular.modular_hamiltonian` — \(K = -\ln(\rho)\) pour un état fidèle, restreint au domaine fidèle.

Décision (inchangée) :

```text
CORE_REUSE_DECISION = REUSE_CORE
```

Ces trois primitives sont réutilisées telles quelles pour construire \(\rho_{AB}\), \(\rho_{BC}\), \(K_{AB}\), \(K_{BC}\) (spécification §7–§8).

---

## 3. Primitives `core` réutilisées

Sont réutilisées telles quelles :

```text
cosmotgg.core.states.validate_density_matrix
cosmotgg.core.states.partial_trace

cosmotgg.core.modular.modular_hamiltonian
```

Aucune de ces primitives n'est dupliquée dans `model0c`.

Aucun commutateur générique n'existe dans `core` ; les commutateurs de la dérivation \(D(O_B) = -i[\Delta,O_B]\) (spécification §21, héritée de `model0b` §13) et du diagnostic \(N = i[\chi_A,\chi_C]\) (spécification §13) sont assemblés model-specific, à l'image de la construction déjà retenue par `model0a/diagnostics.py` et `model0b/relative.py`.

---

## 4. Audit de réutilisation obligatoire — promotion vers `core`

Conformément à `docs/governance/software-architecture-governance.md` §8 et à son principe de placement conservateur (§3.1 : « ambigu → model-specific », promotion « dès qu'un usage supplémentaire […] la justifie »), l'apparition d'un second modèle concret (`model0c`, après `model0b`) réutilisant identiquement deux constructions déjà identifiées mais non promues par `docs/toy-models/toy0b/implementation-design.md` §2 constitue précisément cet « usage supplémentaire ».

Deux candidats sont distingués :

1. **primitives établies génériques**, indépendantes de tout modèle :
   - la conditional expectation traciale normalisée \(E(X) = \operatorname{Tr}_{\text{out}}(X)/d_{\text{out}}\) (spécification `model0b` §9, `model0c` §8), c'est-à-dire une trace partielle suivie d'une division scalaire par la dimension tracée — construction mathématique standard (conditional expectation préservant la trace normalisée, unique dans le cadre fini de type I déclaré, cf. `docs/toy-models/toy0b/specification.md` §9), indépendante de l'identité de `model0b` ou de `model0c` ;
   - la réduction sans trace \(\operatorname{tl}(X) = X - \operatorname{Tr}(X)/d\, I\) (spécification `model0b` §11, `model0c` §9) — construction d'algèbre linéaire standard (partie sans trace d'un opérateur), également indépendante de l'identité de tout modèle ;
2. **assemblage project-defined**, propre à chaque modèle : le générateur relatif de chevauchement lui-même (`OVERLAP_RELATIVE_MODULAR_GENERATOR` de `model0b`, \(\chi_A\)/\(\chi_C\)/\(\Delta\)/\(N\) de `model0c`), qui choisit un sous-système commun, une paire de branches modulaires, une convention de signe et, pour `model0c`, un diagnostic de non-colinéarité — ce choix reste propre à chaque modèle et n'est pas candidat à `core`.

Décision :

```text
CORE_PROMOTION_NEEDED = YES
```

Primitives minimales proposées, strictement bornées au besoin déjà démontré par deux modèles (`model0b`, `model0c`), sans framework spéculatif :

```text
cosmotgg.core.states.conditional_expectation(
    operator, *, dimensions, keep
)
```

Définition proposée : `partial_trace(operator, dimensions=dimensions, keep=keep)` divisée par le produit des dimensions tracées (`dimensions[i]` pour `i` hors de `keep`). C'est exactement le calcul déjà dupliqué dans `model0b/relative.py` (`partial_trace(...) / d_A`, `partial_trace(...) / d_C`) et prévu à l'identique pour `model0c` (§7 ci-dessous).

```text
cosmotgg.core.states.traceless_part(
    operator
)
```

Définition proposée : `operator - (numpy.trace(operator) / d) * numpy.eye(d)`, avec `d = operator.shape[0]`. C'est exactement le calcul déjà privé `_traceless` de `model0b/relative.py`, dupliqué à l'identique dans le design de `model0c` (§7 ci-dessous) si aucune promotion n'a lieu avant l'implémentation de `model0c`.

Ces deux primitives, si promues, porteraient :

```python
SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}
```

conformément à `docs/governance/software-architecture-governance.md` §5.1 : ce sont des constructions mathématiques génériques, pas des propositions scientifiques propres à CosmoTGG. Le générateur relatif de chevauchement lui-même (assemblage project-defined) resterait, lui, `"status": "project-defined"`, avec `origin_model`/`normative_reference` pointant vers la spécification du modèle qui l'assemble (`model0b` ou `model0c`).

Portée de cette décision :

```text
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
CODE_MODIFIED_THIS_LOT           = FALSE
```

Aucun code n'est modifié par ce document. Cette décision n'ouvre ni ne planifie elle-même le lot de promotion : elle enregistre uniquement, conformément au mandat, qu'une promotion vers `core` est architecturalement justifiée pour ces deux primitives précises, à traiter par un futur lot dédié relevant du rôle `code`. Ce document ne fixe aucun ordre d'exécution entre un tel lot de promotion et le futur lot d'implémentation de `model0c` (`MODEL0C-IMPL`) : le §7 ci-dessous décrit l'implémentation de `model0c` telle qu'elle serait conçue sur l'état actuel de `core` (sans promotion), à défaut d'un lot de promotion antérieur. Si un lot de promotion précède `MODEL0C-IMPL`, ce dernier doit réutiliser les primitives promues plutôt que de dupliquer une construction déjà extraite dans `core` (`docs/governance/software-architecture-governance.md` §8).

Aucun framework spéculatif n'est créé : ces deux primitives sont les seules candidates identifiées, strictement limitées au besoin déjà démontré deux fois.

---

## 5. Arborescence cible minimale

```text
src/cosmotgg/models/model0c/__init__.py
src/cosmotgg/models/model0c/states.py
src/cosmotgg/models/model0c/relative.py

tests/models/model0c/test_states.py
tests/models/model0c/test_relative.py
```

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model0C
```

---

## 6. Responsabilité de `model0c/states.py`

Responsabilité scientifique strictement bornée à la famille d'états de `docs/toy-models/toy0c/specification.md` §5 :

- construire \(\rho_{ABC}(\alpha,\gamma,\lambda,\mu)\) selon la matrice normative du §5 ;
- déclarer et valider son domaine analytique (§6), de façon fail-closed et sans tolérance numérique implicite ;
- fournir, si utile, les états réduits \(\rho_{AB}\), \(\rho_{BC}\), \(\rho_B\), \(\rho_A\), \(\rho_C\) (§7 de la spécification), par assemblage explicite des chaînes de Pauli ou via `cosmotgg.core.states.partial_trace`.

Ce module ne réimplémente pas : logarithme matriciel, hamiltonien modulaire, partial trace générique, conditional expectation.

### 6.1 Validation du domaine analytique

La construction échoue (fail-closed) sur des paramètres \(\alpha,\gamma,\lambda,\mu\) hors du domaine analytique normatif du §6 de la spécification (\(|\alpha|+|\gamma|+\sqrt{\lambda^2+\mu^2} < 1\)). Cette définition de domaine n'est ni approximée ni assouplie par une tolérance numérique locale au module.

---

## 7. Responsabilité de `model0c/relative.py`

Responsabilité scientifique strictement bornée aux §8–§14 et §21 de la spécification :

- construire \(K_{AB} = -\ln(\rho_{AB})\), \(K_{BC} = -\ln(\rho_{BC})\) via `cosmotgg.core.modular.modular_hamiltonian` ;
- construire \(E_B^A(K_{AB})\), \(E_B^C(K_{BC})\) via `cosmotgg.core.states.partial_trace` et division scalaire par \(d_A\)/\(d_C\) (§4 ci-dessus — remplaçable par `cosmotgg.core.states.conditional_expectation` si ce dernier est promu avant l'implémentation) ;
- appliquer \(\operatorname{tl}_B\) (§9 de la spécification, réduction sans trace privée model-specific, sauf promotion préalable de `traceless_part`, §4 ci-dessus) ;
- assembler \(\chi_A\), \(\chi_C\) (§10 de la spécification) ;
- assembler \(\Delta = -\chi_A + \chi_C\) (§10 de la spécification, convention de signe fixée une fois, identique à `model0b`) ;
- assembler le diagnostic de non-colinéarité \(N = i[\chi_A,\chi_C]\) (§13 de la spécification) ;
- appliquer la dérivation \(D(O_B) = -i[\Delta, O_B]\) (héritée de `model0b` §13, spécification `model0c` §21).

Ce module ne construit aucun flot fini paramétré : `FINITE_FLOW_PARAMETER_PROBLEM = OPEN` (§20 de la spécification) n'est pas fermé par ce lot, et aucune fonction du type `exp(-i tau Delta) O exp(+i tau Delta)` n'est prévue.

---

## 8. API proposée — famille d'états

```text
three_qubit_noncollinear_overlap_relation_state(alpha, gamma, lambda_, mu)
```

Ce nom technique reprend l'identifiant `STATE_FAMILY = THREE_QUBIT_NONCOLLINEAR_OVERLAP_RELATION_FAMILY` de la spécification à des fins de traçabilité ; il ne porte aucune sémantique scientifique supplémentaire par rapport à celle-ci. Le paramètre est nommé `lambda_` (`lambda` étant un mot réservé Python), comme dans `model0b`.

Le rôle `code` reste libre d'ajuster ce nom lors de l'implémentation, dans la mesure où il reste descriptif et ne modifie pas le sens de la construction.

---

## 9. API proposée — générateurs relatifs et diagnostic de non-colinéarité

```text
overlap_relative_modular_projections(
    rho_abc,
    *,
    hermiticity_tolerance,
    trace_tolerance,
    positivity_tolerance,
)
```

Retourne les **matrices** \((\chi_A, \chi_C)\) agissant sur \(\mathcal H_B\) (§10 de la spécification), jamais leurs formes analytiques scalaires du §11.

```text
overlap_relative_modular_generator(chi_a, chi_c)
```

Assemble \(\Delta = -\chi_A + \chi_C\) (§10 de la spécification, convention de signe fixée).

```text
overlap_projected_noncollinearity_operator(chi_a, chi_c)
```

Assemble \(N = i[\chi_A, \chi_C]\) (§13 de la spécification). Aucune tolérance numérique n'est introduite par cette fonction ; \(N\) est hermitien par construction lorsque \(\chi_A\), \(\chi_C\) le sont.

```text
overlap_relative_modular_derivation(delta, observable_b)
```

Applique uniquement \(-i[\Delta, O_B]\), héritée de `model0b/relative.py` sans changement de définition. Aucun flot fini n'est exposé par cette fonction ni par une autre fonction de ce module.

Les tolérances numériques (`hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`) sont explicites, keyword-only, sans valeur par défaut, transmises telles quelles à `cosmotgg.core.states.validate_density_matrix` et `cosmotgg.core.modular.modular_hamiltonian`, à l'image des conventions déjà en place dans `cosmotgg.core` et `model0b/relative.py`. Aucune tolérance n'est inventée localement par `model0c`.

Ces noms techniques peuvent être ajustés par le rôle `code` sans changer leur définition normative.

---

## 10. Contrôle de sensibilité S2 — statut de conception

Le contrôle de sensibilité S2 (spécification §16, comparaison avec \(E_{\rho_A}\)/\(E_{\rho_C}\)) reste, à ce stade, un contrôle analytique conceptuel documenté par la spécification. Il n'est associé à aucune API committée par ce document : aucune fonction `model0c/relative.py` n'est proposée pour l'exécuter dans le premier lot d'implémentation.

```text
S2_IMPLEMENTATION = NOT_INCLUDED_IN_THIS_DESIGN
S2_FUTURE_LOT      = SEPARATE_MANDATE_REQUIRED
```

Cette section ne crée pas de framework spéculatif ; elle enregistre seulement que la spécification prévoit ce contrôle pour une qualification future distincte.

---

## 11. Tests prévus — famille d'états (`tests/models/model0c/test_states.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

- matrice d'état exacte pour des paramètres de développement `NON_NORMATIVE_TEST_FIXTURE` ;
- trace analytique égale à 1 ;
- fidélité dans le domaine (§6 de la spécification) ;
- rejet fail-closed des paramètres hors domaine, y compris via le corollaire d'exécutabilité (§6 de la spécification) ;
- états réduits exacts \(\rho_{AB}\), \(\rho_{BC}\), \(\rho_B\), \(\rho_A\), \(\rho_C\) (§7 de la spécification).

---

## 12. Tests prévus — générateurs relatifs et diagnostic (`tests/models/model0c/test_relative.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

- identité analytique de \(\chi_A\), \(\chi_C\) (§11 de la spécification) ;
- condition exacte de non-nullité \(\chi_A \neq 0 \iff \alpha\lambda \neq 0\), \(\chi_C \neq 0 \iff \gamma\mu \neq 0\) (§12 de la spécification) ;
- condition exacte de non-nullité de \(N\), \(N \neq 0 \iff \alpha\gamma\lambda\mu \neq 0\) (§13 de la spécification) ;
- hermiticité de \(\chi_A\), \(\chi_C\), \(\Delta\), \(N\), et absence de trace de \(\chi_A\), \(\chi_C\), \(\Delta\) ;
- C0 (`lambda=0, mu=0` ⟹ `chi_A=chi_C=Delta=N=0`) ;
- C1 (`alpha=0, lambda≠0` ⟹ `chi_A=0`) ;
- C2 (`gamma=0, mu≠0` ⟹ `chi_C=0`) ;
- C3 (`alpha*gamma*lambda*mu≠0` ⟹ `chi_A≠0, chi_C≠0, N≠0`) ;
- C4 (`alpha=0, lambda≠0, gamma*mu≠0` ⟹ `chi_A=0, chi_C≠0, Delta≠0, N=0`) ;
- covariance sous \(U_A\otimes U_B\otimes U_C\) : \(\chi_A \to U_B\chi_A U_B^\dagger\), \(\chi_C \to U_B\chi_C U_B^\dagger\), \(\Delta \to U_B\Delta U_B^\dagger\), \(N \to U_B N U_B^\dagger\) (§19 de la spécification), bornée à `LOCAL_PRODUCT_UNITARY_COVARIANCE` ;
- absence de toute API de flot fini paramétré dans `model0c/relative.py` (contrôle structurel/d'architecture, pas un test numérique) ;
- absence de toute API exécutant le contrôle de sensibilité S2 dans le module de production (contrôle structurel, cf. §10 ci-dessus).

Les valeurs de test restent, comme au §11, explicitement marquées `NON_NORMATIVE_TEST_FIXTURE` et ne constituent pas des `ALPHA_VALUE`/`GAMMA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` normatifs (§23 de la spécification, qui restent `OPEN`).

---

## 13. Absence de scalaire normatif

Ce document ne définit aucun `threshold`, `normalized score`, `ratio`, ni indicateur scalaire de temps. De telles quantités pourront être introduites ultérieurement par un futur plan de validation ; elles ne font pas partie de la définition scientifique actuelle.

---

## 14. Paramètres non fermés par ce document

```text
ALPHA_VALUE                     = OPEN
GAMMA_VALUE                     = OPEN
LAMBDA_VALUE                    = OPEN
MU_VALUE                        = OPEN
NUMERICAL_TOLERANCES            = OPEN
MODEL0C_ACCEPTANCE_CRITERION    = OPEN
T1_NONTRIVIALITY_CRITERION      = OPEN
CONFIRMATORY_PROTOCOL           = NOT_DEFINED
FINITE_FLOW_PARAMETER_PROBLEM   = OPEN
```

---

## 15. Statut et prochaine étape

```text
MODEL0C_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
