# T1 — Critères opérationnels du changement physique relationnel

Statut : **T1_OPERATIONAL_DEFINITION_NOTE**

Ce document formalise l'étape définitionnelle bornée exigée par la revue
`T1-RELATIONAL-PHYSICAL-CHANGE-CRITERIA-REVIEW-1`. Il ne conçoit pas
`model0e`.

Il complète opérationnellement le test T1 gelé (`docs/model/hypothesis.md`
§15). Il ne modifie pas le critère PASS de `hypothesis.md`, ne remplace pas
`hypothesis.md`, ne constitue pas un plan de validation, ne préenregistre pas
T1 et n'autorise pas `model0e`.

---

## 1. Ancrage gelé

`docs/model/hypothesis.md` (§15) demande, pour T1 :

> Construction explicite d'un changement relatif entre au moins deux
> sous-structures, calculée depuis \(\{\rho_{ij},K_{ij}\}\), sans temps
> externe et sans degré de liberté supplémentaire désigné comme horloge
> fondamentale (cf. §7).

```text
FROZEN_BLOCK_CHALLENGE       = NOT_REQUIRED
NO_EXTERNAL_TIME             = REQUIRED
NO_FUNDAMENTAL_ADDED_CLOCK   = REQUIRED
NO_RELATIONAL_LABEL          = FALSE
```

`NO_RELATIONAL_LABEL = FALSE` : T1 n'interdit pas toute étiquette
relationnelle utilisée pour exprimer le changement ; il interdit un temps
externe et un degré de liberté supplémentaire désigné comme horloge
fondamentale.

---

## 2. Correction du verrou de paramètre

```text
EXTERNALLY_SUPPLIED_FREELY_CHOSEN_FLOW_PARAMETER = FORBIDDEN
INTERNALLY_DERIVED_RELATIONAL_LABEL              = ADMISSIBLE_UNDER_C1_TO_C7
MODULAR_PARAMETER                                = NOT_PHYSICAL_TIME
```

Pour le travail **futur**, l'interprétation ambiguë « aucun paramètre fini
ne doit exister » est remplacée par :

```text
FLOW_LABEL_DERIVATION_PROBLEM =
    any label used to express relational change must be
    internally derived/read from the relational system and
    must survive the reparametrization/reference-change firewall.
```

Aucune occurrence historique de `FINITE_FLOW_PARAMETER_PROBLEM` dans les
documents gelés (`docs/toy-models/toy0b/`, `docs/toy-models/toy0c/`,
`docs/toy-models/toy0d/`, `docs/governance/current-task.md`) n'est modifiée.

```text
LEGACY_FINITE_FLOW_PARAMETER_PROBLEM_WORDING =
    PRESERVED_HISTORICALLY_BUT_INTERPRETED_BY_FLOW_LABEL_DERIVATION_PROBLEM
```

---

## 3. Frontière model0d

```text
MODEL0D_PAIR_TRANSPORT_STATUS       = STRUCTURAL_PROGRESS_BUT_NOT_PHYSICAL_PROCESS
PARAMETER_FREE_FINITE_PAIR_TRANSPORT = QUALIFIED_AS_DECLARED_CONSTRUCTION
```

Mais :

```text
AUXILIARY_CONTEXTUAL_STATE_TRANSPORT != PHYSICAL_RELATIONAL_CHANGE
```

Résultat structural : pour un transport `model0d` non trivial,

\[
F\,\omega_{\text{source}}\,F^\dagger = \omega_{\text{target}}
\]

et il existe un état physique normalisé \(\sigma\) tel que

\[
\operatorname{Tr}(F\sigma F^\dagger) > 1.
\]

Donc :

```text
EXACT_PAIR_TRANSPORT_AND_CP_TRACE_NONINCREASING =
    INCOMPATIBLE_FOR_NONTRIVIAL_MODEL0D_F
```

sous la construction déclarée.

```text
STATUS = STRUCTURAL_ANALYTIC
```

`docs/toy-models/toy0d/specification.md` n'est pas modifié.

---

## 4. Composition

```text
HOLONOMY_ON_COMMON_OVERLAP = IDENTICALLY_TRIVIAL_FOR_MODEL0D
TRIVIAL_HOLONOMY_IS_FAILURE_CRITERION = NO
```

Le défaut discriminant de `model0d` est :

```text
MODEL0D_COMPOSITION_DEFECT = ZERO_INDEPENDENT_PREDICTIVE_CONTENT
```

car chaque transporteur est reconstruit directement depuis les deux
extrémités. Le futur candidat n'a pas à présenter une holonomie non
triviale.

---

## 5. Faux positifs

### FP1 — Réinitialisation CPTP arbitraire

Pour tout \(\sigma\), \(\Phi_\sigma(X) = \operatorname{Tr}(X)\,\sigma\) est
CPTP. Donc :

```text
CPTP_EXISTENCE_ALONE = NONDISCRIMINATING
```

Un futur candidat doit dériver la loi elle-même depuis les données
relationnelles ; la cible ne peut pas être donnée indépendamment.

### FP2 — Conditionnement statique

Des états conditionnels physiques différents \(\rho_{B|r_1} \neq
\rho_{B|r_2}\) peuvent provenir de corrélations/steering statiques. Donc :

```text
CONDITIONAL_STATE_VARIATION_ALONE = NOT_RELATIONAL_CHANGE
```

---

## 6. Critères nécessaires C1–C7

```text
STATUS = NECESSARY_FOR_FUTURE_NONCONFIRMATORY_CANDIDATE
NOT     = T1_PASS_CRITERION
NOT     = SUFFICIENT_CONDITIONS
NOT     = CONFIRMATORY_PROTOCOL
```

### C1 — PHYSICAL_CARRIERS

Les objets dont les prédictions changent doivent être des états réduits
physiques, des états conditionnels physiques, des observables physiques, ou
des équivalents opérationnels.

Sont insuffisants seuls : états auxiliaires reconstruits, états de
comptabilité (« bookkeeping »), objets de jauge/convention uniquement.

### C2 — INTERNAL_RELATIONAL_REFERENCE

Il existe au minimum deux lectures internes \(r_1 \neq r_2\). La référence
provient de la structure existante.

Interdit : temps externe \(t\) ; degré de liberté d'horloge fondamentale
ajouté ; paramètre de flot modulaire librement choisi.

Autorisé conditionnellement : étiquette relationnelle \(r\) dérivée
internement.

### C3 — OBSERVABLE_NONTRIVIALITY

Il doit exister un observable physique \(O\) tel que \(P(O \mid r_1) \neq
P(O \mid r_2)\), ou l'équivalent en espérances/probabilités physiques. Une
différence uniquement auxiliaire ne satisfait pas C3.

### C4A — REFERENCE_COVARIANCE

La famille de référence \(\{E_r\}\) doit être reliée par une loi de
covariance engendrée par une structure \(G\) fixe. \(E_r\) ne peut pas être
spécifié indépendamment pour chaque \(r\). \(G\) et la règle de covariance
doivent être dérivés des données CosmoTGG admissibles. Aucune POVM
d'horloge arbitrairement importée.

### C4B — FIXED_LAW_OVERDETERMINATION

Après fixation des données relationnelles, de la construction de référence,
du générateur/de la contrainte, et d'une éventuelle référence de départ
(« seed »), la famille complète \(r \to \rho_{B|r}\) doit être calculée. Il
est interdit de fournir librement un état cible indépendant pour chaque
\(r\).

```text
NUMBER_OF_INDEPENDENT_TARGET_STATE_INPUTS = ZERO
```

pour une famille dérivée. La loi doit donc posséder un contenu prédictif
indépendant.

### C4C — TWO_READING_PROBABILITY_CONSISTENCY

Le candidat doit définir explicitement des probabilités ou prédictions
relationnelles impliquant au moins deux lectures distinctes. Elles doivent
être positives, normalisées, calculées depuis la même structure relationnelle
fixe.

Interdit : inférer une « dynamique » uniquement à partir d'une liste d'états
conditionnels à une seule lecture.

Ce contrôle doit permettre un FAIL déterministe.

### C5 — PHYSICAL_ADMISSIBILITY

Le contenu prédictif final doit posséder un statut physique quantique
admissible. Selon la construction : canal CPTP, branche d'instrument CP à
trace non croissante, probabilités conditionnelles relationnelles
normalisées, équivalent invariant de jauge, peuvent être admissibles.

```text
PHYSICAL_ADMISSIBILITY_ALONE = NOT_SUFFICIENT
```

### C6 — REPARAMETRIZATION_FIREWALL

Tout paramètre auxiliaire de calcul doit disparaître du contenu physique
final. Les prédictions peuvent dépendre de la lecture relationnelle \(r\)
mais pas d'un paramètre de calcul arbitraire \(s\).

```text
C6_DOES_NOT_MEAN_NO_RELATIONAL_LABEL = TRUE
```

### C7 — REFERENCE_NON_PRIVILEGE

Une référence interne unique privilégiée ne suffit pas. Un futur candidat
doit démontrer : (1) au moins deux références admissibles issues des mêmes
données relationnelles ; (2) une règle explicite de changement de
référence ; (3) la compatibilité/invariance des prédictions physiques
communes sous ce changement.

Sinon : `INTERNAL_REFERENCE = HIDDEN_PRIVILEGED_CLOCK` et le candidat échoue
C7.

---

## 7. No-go mono-K

Résultat conditionnel :

Hypothèses :

1. une règle construit \(\{E_r(K)\}\) depuis \(K\) seul ;
2. aucune donnée supplémentaire de base/phase/référence ;
3. équivariance unitaire : \(E_r(U K U^\dagger) = U E_r(K) U^\dagger\).

Alors pour tout \(U\) dans le commutant de \(K\) : \(U K U^\dagger = K\),
donc \(E_r(K) = U E_r(K) U^\dagger\), et \(E_r(K)\) appartient au
bicommutant de \(K\). Par conséquent \([E_r(K), K] = 0\) et
\(\exp(iKs)\, E_r(K)\, \exp(-iKs) = E_r(K)\). Donc une covariance non
triviale \(E_{r+s} = \exp(iKs)\, E_r\, \exp(-iKs)\) est impossible.

```text
SINGLE_K_CANONICAL_REFERENCE = BLOCKED
STATUS = STRUCTURAL_ANALYTIC_UNDER_DECLARED_EQUIVARIANCE_ASSUMPTION
```

Ce résultat n'est pas généralisé au cas multi-K.

---

## 8. Dimension finie

```text
SELF_ADJOINT_CANONICAL_TIME_OPERATOR_WITH_[T,K]=iI = IMPOSSIBLE_IN_FINITE_DIMENSION
```

par la trace du commutateur. Donc une référence finie éventuelle devra être
de type POVM, discrète/cyclique, ou autrement non-canonique (pas un
opérateur de temps canonique).

Ne pas revendiquer : temps physique continu, flèche du temps, horloge
parfaite.

Pour un futur toy :

```text
REFERENCE_DIMENSION = MUST_BE_EXPLICITLY_CLOSED_BEFORE_DESIGN
```

Les fixtures qubit actuelles ne doivent pas être reprises automatiquement
par inertie. Un \(d\) exact n'est pas encore imposé.

---

## 9. Cible multi-K

```text
MODULAR_DERIVED_RELATIONAL_REFERENCE = PLAUSIBLE_OPEN_TARGET
SINGLE_K                             = BLOCKED
MULTI_K                              = OPEN
```

Pour une famille de structures non commutantes, calculer à l'avenir le
commutant commun \(\text{Comm}(\{K_1,\dots,K_n\})\).

Condition structurelle intéressante : \(\text{Comm}(\{K_i\}) = \mathbb{C} I\)
peut supprimer la liberté résiduelle de base/phase. Mais :

```text
TRIVIAL_COMMON_COMMUTANT_IS_SUFFICIENT_FOR_REFERENCE = NO
PHASE_FIXING_BY_NONCOMMUTING_MODULAR_FAMILY          = HYPOTHESIS_TO_TEST
```

Lien avec le résultat `model0c` (\(N \neq 0\)) mentionné comme motivation
structurelle uniquement. `model0c` n'a pas déjà construit une référence.

---

## 10. Guides de littérature

```text
PAGE_WOOTTERS                = PRIMARY_GUIDE
ROVELLI_COMPLETE_OBSERVABLES = USEFUL_CRITERIAL_GUIDE
CHANNELS_INSTRUMENTS         = ADMISSIBILITY_LANGUAGE_NOT_ORIGIN
PROCESS_MATRICES_COMBS       = NOT_SUITABLE_AS_ORIGIN_OF_T1_CHANGE
CONSISTENT_HISTORIES_RECORDS = USEFUL_LATER
```

---

## 11. Porte de conception

```text
NEXT_TOY_CONCEPTUAL_DESIGN = NOT_AUTHORIZED_BY_THIS_DOCUMENT
MODEL0E                    = NOT_DEFINED
```

Avant tout futur toy, il faudra disposer d'un candidat précis capable de
répondre simultanément à C1, C2, C3, C4A, C4B, C4C, C5, C6, C7 au niveau de
sa conception.

La prochaine question scientifique autorisée est :

> Can a noncommuting family of modular structures derived from the same
> relational state determine a nonprivileged reference family and an
> overdetermined conditional law?

---

## 12. Pare-feu T1

```text
RELATIONAL_REFERENCE        = NOT_ESTABLISHED
RELATIONAL_PHYSICAL_CHANGE  = NOT_ESTABLISHED
RELATIONAL_TIME             = NOT_ESTABLISHED
T1_NONTRIVIALITY_CRITERION  = OPEN
CONFIRMATORY_PROTOCOL       = NOT_DEFINED
T1                          = OPEN_NOT_EXECUTED
```
