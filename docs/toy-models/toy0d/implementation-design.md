# toy0d — Conception d'implémentation (model0d)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model0d`, sur la base de `docs/toy-models/toy0d/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun critère ou verdict T1.

---

## 1. Périmètre

Ce document couvre :

- l'audit architectural obligatoire de la primitive analytique générique du demi-point de Connes (§3 ci-dessous) ;
- le design minimal de la reconstruction d'état contextuel `omega_X` à partir d'un générateur projeté `chi_X` (spécification §5) ;
- le design minimal du transporteur d'état contextuel fini `F` (spécification §7) ;
- le design minimal des diagnostics numériques de qualification (spécification §15) ;
- le design minimal des contrôles D0–D6 (spécification §16).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les fixtures numériques de contextes (`MODEL0D_CONTEXT_FIXTURES`, spécification §20) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire d'acceptation ;
- le plan de validation ;
- un critère d'acceptation de `model0d` ou de T1 ;
- tout flot fini paramétré (spécification §18, `FINITE_FLOW_PARAMETER_PROBLEM = OPEN`).

---

## 2. Vérification du contrat réel des primitives `core` existantes

`model0d` réutilise le mécanisme modulaire déjà établi dans `cosmotgg.core.modular` :

- `cosmotgg.core.modular.modular_hamiltonian` — \(K=-\ln(\rho)\) pour un état fidèle, tolérances explicites sans valeur par défaut ;
- `cosmotgg.core.modular.finite_connes_cocycle` — cocycle de Connes réel fini \(v_s(\rho,\sigma)=\rho^{-is}\sigma^{+is}\), paramètre \(s\) réel, fini, sans interprétation de temps physique ;
- `cosmotgg.core.modular._modular_unitary` (auxiliaire privé) — évaluation spectrale de \(\exp(+i\,H\,s)\) par diagonalisation hermitienne (`numpy.linalg.eigh`), sans dépendance `scipy` ;
- `cosmotgg.core.states.conditional_expectation`, `cosmotgg.core.states.traceless_part` — réutilisées en amont par `model0c` pour produire `chi_source`/`chi_target` (hors périmètre de production de `model0d`, §11 ci-dessous).

Ces primitives sont déjà `established` (`SCIENTIFIC_METADATA.status = "established"`) et ne sont pas modifiées par ce document. Le point analytique \(-i/2\) requis par le transporteur \(F\) (spécification §7–§8) n'est en revanche couvert par aucune primitive existante : `finite_connes_cocycle` est paramétrée par un réel \(s\), pas par le point analytique continué \(-i/2\).

---

## 3. Audit architectural obligatoire — primitive `core` du demi-point analytique

Conformément à `docs/governance/software-architecture-governance.md` §3 (l'API du demi-point de Connes ne référence l'identité d'aucun modèle particulier, ne code en dur aucune constante propre à `model0d`, possède une signification mathématique propre et est testable unitairement sans reconstruire `model0d`) et à son principe de placement conservateur (§3.1 : le caractère générique de cette construction est déjà intrinsèque et non ambigu, ce qui écarte le défaut « ambigu → model-specific »), la construction analytique du demi-point est elle-même finie-dimensionnelle et indépendante de tout modèle :

$$
[D\rho : D\sigma]_{-i/2} = \rho^{1/2}\,\sigma^{-1/2},
$$

exactement comme `finite_connes_cocycle` implémente déjà `v_s(\rho,\sigma) = \rho^{-is}\sigma^{+is}` pour tout réel `s`, sans référence à un modèle particulier.

Décision :

```text
CORE_HALF_COCYCLE_PRIMITIVE = YES
CORE_TARGET                 = cosmotgg.core.modular
```

API candidate :

```python
connes_cocycle_at_minus_i_half(
    rho,
    sigma,
    *,
    hermiticity_tolerance,
    trace_tolerance,
    positivity_tolerance,
) -> np.ndarray
```

Signification exacte :

$$
[D\rho : D\sigma]_{-i/2} = \rho^{1/2}\,\sigma^{-1/2} .
$$

`rho` et `sigma` doivent toutes deux être des matrices densité fidèles de dimensions correspondantes, validées via le même mécanisme que `modular_hamiltonian`/`finite_connes_cocycle` (`cosmotgg.core.states.validate_density_matrix`, tolérances explicites, keyword-only, sans valeur par défaut). Cette primitive est portée par le module existant :

```text
SCIENTIFIC_METADATA.status = established
```

sans nouveau champ ni nouvelle catégorie de métadonnée.

Cette API n'est **pas** généralisée à un paramètre complexe arbitraire de cocycle : seule la primitive du demi-point démontrée par la spécification (§7–§8) est introduite. Aucune fonction `connes_cocycle_at(rho, sigma, z)` à paramètre complexe libre n'est proposée.

Portée de cette décision :

```text
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
CODE_MODIFIED_THIS_LOT           = FALSE
```

Aucun code n'est modifié par ce document. Cette décision n'ouvre ni ne planifie elle-même le lot d'implémentation : elle enregistre uniquement, conformément au mandat, que l'ajout de cette primitive à `cosmotgg.core.modular` est architecturalement justifié, à traiter par un futur lot dédié relevant du rôle `code`.

---

## 4. Arborescence cible minimale

```text
src/cosmotgg/core/modular.py                        (extension)

src/cosmotgg/models/model0d/__init__.py
src/cosmotgg/models/model0d/transport.py

tests/core/test_modular.py                           (extension)

tests/models/model0d/__init__.py
tests/models/model0d/test_transport.py
```

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model0D
class Transport
graph/groupoid abstraction
```

`model0d` n'importe pas `model0c` en production :

```text
MODEL0D_PRODUCTION_IMPORTS_MODEL0C = NO
```

---

## 5. Responsabilité de `model0d/transport.py`

Responsabilité scientifique strictement bornée aux §5, §7 et §15–§16 de la spécification :

- reconstruire l'état contextuel `omega_X` à partir d'un générateur projeté hermitien sans trace `chi_X`, selon la convention `omega_X = exp(-chi_X) / Tr exp(-chi_X)` (spécification §5), en utilisant le calcul fonctionnel hermitien déjà disponible dans `core` (diagonalisation spectrale, cohérente avec `hermitian_log`/`modular_hamiltonian`) ;
- assembler le transporteur fini `F = omega_target^(1/2) omega_source^(-1/2)`, en délégant la mathématique effective du demi-cocycle à `connes_cocycle_at_minus_i_half` si `CORE_HALF_COCYCLE_PRIMITIVE = YES` est exécuté avant l'implémentation de `model0d` (§3 ci-dessus) ;
- fournir les diagnostics numériques de qualification listés à la spécification §15 (`lambda_min_source`, `lambda_min_target`, `sqrt_inverse_residual_source`, `transport_residual`, `inverse_residual`), sans aucune régularisation silencieuse, pseudoinverse, écrêtage spectral ou ridge caché.

Ce module ne construit aucun flot fini paramétré, aucune classe `Transport` générique, et n'importe pas `model0c`.

---

## 6. API proposée — `core` (`cosmotgg.core.modular`)

```python
connes_cocycle_at_minus_i_half(
    rho, sigma, *,
    hermiticity_tolerance,
    trace_tolerance,
    positivity_tolerance,
) -> np.ndarray
```

Voir §3 ci-dessus pour la signification exacte et le statut scientifique. Les noms techniques peuvent être ajustés par le rôle `code` sans changer leur définition normative.

---

## 7. API proposée — `model0d` (`cosmotgg.models.model0d.transport`)

```python
contextual_state_from_projected_generator(
    chi, *,
    hermiticity_tolerance,
    positivity_tolerance,
)
```

Construit `omega = exp(-chi) / Tr exp(-chi)` (spécification §5), à partir d'un générateur projeté hermitien sans trace `chi` sur l'algèbre de chevauchement `B`. N'impose aucune hypothèse sur la provenance de `chi` (pas d'import `model0c`).

```python
finite_relative_contextual_state_transporter(
    omega_source, omega_target, *,
    hermiticity_tolerance,
    trace_tolerance,
    positivity_tolerance,
)
```

Assemble `F = omega_target^(1/2) omega_source^(-1/2)` (spécification §7), en délégant le calcul du demi-cocycle à `connes_cocycle_at_minus_i_half` (§3, §6 ci-dessus) si celui-ci est promu avant l'implémentation, sinon en le construisant localement à partir du calcul fonctionnel hermitien déjà disponible dans `core`. Aucun paramètre `s`, `t`, `tau` n'est exposé par cette fonction.

Ces noms techniques peuvent être ajustés par le rôle `code` sans changer leur définition normative. Aucune classe `Transport`, aucune abstraction de graphe/groupoïde, aucun framework générique n'est introduit.

---

## 8. Diagnostics numériques de qualification — statut de conception

Diagnostics prévus par la spécification (§15), à exposer comme fonctions ou valeurs auxiliaires du module `model0d/transport.py`, sans seuil normatif :

```text
lambda_min_source
lambda_min_target

sqrt_inverse_residual_source =
    || sqrt(omega_source) invsqrt(omega_source) - I ||

transport_residual =
    || F omega_source F^dagger - omega_target ||

inverse_residual =
    || F_target_source F_source_target - I ||

analytic_oracle_residual
    (uniquement lorsqu'un oracle analytique d_B=2 est disponible)
```

Ce sont des `NUMERICAL_QUALIFICATION_GUARDS`, pas des observables physiques. Aucun seuil scientifique n'est fixé par ce document ; les tolérances numériques d'un futur protocole restent `OPEN` (spécification §20).

```text
BOUNDARY_REGIME = OUT_OF_SCOPE_FOR_MODEL0D_QUALIFICATION
```

Aucune fonction de ce module ne doit régulariser silencieusement, tronquer le spectre ou substituer un pseudoinverse à `omega_source^(-1/2)`.

---

## 9. Tests prévus — `core` (`tests/core/test_modular.py`, extension)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum, pour `connes_cocycle_at_minus_i_half` :

- identité analytique \([D\rho:D\sigma]_{-i/2} = \rho^{1/2}\sigma^{-1/2}\) sur des matrices densité fidèles de développement `NON_NORMATIVE_TEST_FIXTURE` ;
- cas \(\rho=\sigma\) : résultat égal à l'identité ;
- rejet fail-closed d'un état non fidèle (cohérent avec `modular_hamiltonian`) ;
- rejet fail-closed de dimensions non correspondantes ;
- absence de tolérance par défaut (tous les arguments de tolérance sont keyword-only, sans valeur par défaut, cohérent avec `docs/governance/software-architecture-governance.md` §9).

---

## 10. Tests prévus — `model0d` (`tests/models/model0d/test_transport.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum, en correspondance directe avec la spécification §16 :

- **D0_IDENTITY** : `omega_A = omega_C` ⟹ `F = I`, `U = I`, `P = I` ;
- **D1_COMMUTING_DISTINCT** : `omega_A = I/2`, `omega_C != I/2` ⟹ `[omega_A, omega_C] = 0`, `F != I`, `F` positif, `U = I`, `P != I` ;
- **D2_NONCOMMUTING** : `[omega_A, omega_C] != 0` ⟹ `F != I`, `U != I`, cohérence avec `N != 0` ;
- **D3_ACTUAL_OVERLAP_STATE_UNCHANGED** (contrôle négatif obligatoire) : pour une fixture amont où `rho_B = I/2` alors que `omega_A != omega_C`, vérifier que le transport agit entre états contextuels auxiliaires et non entre deux états réduits physiques successifs de `B` ;
- **D4_NONCHANNEL** : pour un cas D2, `F^dagger F != I` et il existe un état normalisé `sigma` tel que `Tr(F sigma F^dagger) != 1` (conclusion `NOT_CPTP_DYNAMICS`) ;
- **D5_COMPOSITION** : identité exacte de la chaîne à trois états (`F_(C->D) F_(A->C) = F_(A->D)`) et identité de boucle fermée (`F_(D->A) F_(C->D) F_(A->C) = I`), étiquetées `TAUTOLOGICAL_CHAIN_RULE`, sans score d'évidence attaché ;
- **D6_PROJECTION_SENSITIVITY** : comparaison entre le transporteur tracial officiel et une reconstruction contextuelle pondérée `S2` (héritée du contrôle de sensibilité déjà autorisé par `model0c`), vérifiant uniquement la survie qualitative du statut de non-commutation/orientation et démontrant `F_weighted != F_tracial` génériquement (conclusion `ROBUST_ORIENTATION_CLASS`, `ROBUST_AMPLITUDE = NO`) ;
- absence de toute API de flot fini paramétré dans `model0d/transport.py` (contrôle structurel/d'architecture, pas un test numérique) ;
- absence d'import de `model0c` dans `src/cosmotgg/models/model0d/` (contrôle structurel, cohérent avec `MODEL0D_PRODUCTION_IMPORTS_MODEL0C = NO`, §4 ci-dessus).

Les valeurs de test restent explicitement marquées `NON_NORMATIVE_TEST_FIXTURE` et ne constituent pas des `MODEL0D_CONTEXT_FIXTURES` normatifs (spécification §20, qui restent `OPEN`).

---

## 11. Intégration croisée `model0d`/`model0c`

Dépendance de production :

```text
model0d -X-> model0c
```

préférée et respectée par ce design : `model0d` accepte des générateurs projetés (`chi_source`, `chi_target`) en entrée, sans importer `model0c`.

Le futur notebook pourra importer à la fois `model0c` et `model0d` pour exhiber la chaîne complète :

$$
\rho_{ABC}
\to
\chi_A, \chi_C
\to
\omega_A, \omega_C
\to
F .
$$

Il s'agit d'une intégration expérimentale, pas d'une dépendance de production.

---

## 12. Absence de scalaire normatif

Ce document ne définit aucun `threshold`, `normalized score`, `ratio`, ni indicateur scalaire de temps. De telles quantités pourront être introduites ultérieurement par un futur plan de validation ; elles ne font pas partie de la définition scientifique actuelle.

---

## 13. Paramètres non fermés par ce document

```text
MODEL0D_CONTEXT_FIXTURES       = OPEN / NON_NORMATIVE_AT_IMPLEMENTATION
NUMERICAL_TOLERANCES           = OPEN
MODEL0D_ACCEPTANCE_CRITERION   = OPEN
T1_NONTRIVIALITY_CRITERION     = OPEN
CONFIRMATORY_PROTOCOL          = NOT_DEFINED
FINITE_FLOW_PARAMETER_PROBLEM  = OPEN
```

---

## 14. Statut et prochaine étape

```text
MODEL0D_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
