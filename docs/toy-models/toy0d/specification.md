# toy0d — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0d`, construction candidate du toy `toy0d`.

Il transforme en contrat explicite la revue scientifique de ChatGPT sur le transporteur fini d'état contextuel relatif. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique de paramètre d'état, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy0d
MODEL_ID = model0d

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL0D_CLASS = T1_FINITE_RELATIVE_STATE_TRANSPORT_QUALIFICATION_NONCONFIRMATORY
```

---

## 2. Position dans les tests CosmoTGG

```text
COSMOTGG_TEST_TARGET = T1_RELATIONAL_FLOW
```

Explicitement :

```text
MODEL0D_IS_T1_CONFIRMATORY_TEST = NO
MODEL0D_PROVES_RELATIONAL_TIME  = NO
MODEL0D_PROVES_PHYSICAL_CHANGE  = NO

T1 = OPEN_NOT_EXECUTED
```

Le rôle de `model0d` est de tester si des contextes modulaires projetés admettent, sur leur algèbre de chevauchement commune, un transport fini, dirigé et composable de leurs états contextuels reconstruits, sans sélectionner de paramètre réel de flot modulaire. Il ne constitue pas :

```text
STATE_TRANSPORT != PHYSICAL_CHANGE
STATE_TRANSPORT != DYNAMICS
STATE_TRANSPORT != TIME
```

---

## 3. Continuité avec model0a, model0b, model0c

`model0a` a établi, au niveau `QUALIFICATION_NONCONFIRMATORY`, que le cocycle fini réel et son tangent \(\mathcal R_{AB}\) sont calculables (`docs/toy-models/toy0a/specification.md`).

`model0b` a établi, au même niveau, un générateur algébriquement relatif \(\Delta_{(A:C|B)}\) sur le chevauchement \(B\), sans paramètre \(s\) partagé dans sa définition (`docs/toy-models/toy0b/specification.md`).

`model0c` a établi, au même niveau, que deux structures modulaires chevauchantes peuvent produire, sur \(B\), deux générateurs projetés hermitiens sans trace \(\chi_A\), \(\chi_C\) réellement non colinéaires (`docs/toy-models/toy0c/specification.md`).

`model0d` change de question. Il ne cherche plus à obtenir un générateur relatif ou un diagnostic de non-colinéarité (déjà acquis par `model0b`/`model0c`) ; il teste si ces contextes modulaires projetés admettent, sur leur algèbre de chevauchement commune \(B\), un **transport** fini d'état contextuel, sans construire ni sélectionner de paramètre réel de flot modulaire.

Ce document ne modifie aucun contenu scientifique de `docs/toy-models/toy0a/specification.md`, `docs/toy-models/toy0b/specification.md`, `docs/toy-models/toy0c/specification.md`, ni de leurs `implementation-design.md` respectifs.

---

## 4. Entrée scientifique

`model0d` suppose deux générateurs projetés hermitiens sans trace sur une même algèbre de chevauchement finie \(B\) :

$$
\chi_{\text{source}},
\qquad
\chi_{\text{target}},
$$

obtenus en amont par la construction qualifiée par `model0c`.

La production de `model0d` ne dépend pas directement de la famille d'états spécifique de `model0c`. Le contrat scientifique d'entrée est :

```text
chi_source
chi_target
```

sur une algèbre de chevauchement déclarée commune.

Le notebook pourra ultérieurement reconstruire ces valeurs de \(\chi\) via `model0c` pour exhiber la chaîne complète CosmoTGG.

---

## 5. Reconstruction contextuelle de l'état

Étant donné :

$$
H_X = E_B(K_{\text{branch}}),
$$

et :

$$
\chi_X = \operatorname{tl}_B(H_X),
\qquad
H_X = \chi_X + c_X I,
$$

on définit :

$$
\omega_X
=
\frac{e^{-H_X}}{\operatorname{Tr} e^{-H_X}},
$$

ce qui est exactement :

$$
\omega_X
=
\frac{e^{-\chi_X}}{\operatorname{Tr} e^{-\chi_X}}.
$$

```text
CONTEXT_STATE_RECONSTRUCTION = NONBLOCKING_CONVENTION
```

et non :

```text
STRUCTURAL_IDENTITY
```

Frontière épistémique requise :

```text
omega_X IS NOT the reduced state rho_B.
```

Dans `model0c` :

$$
\rho_B = I/2
$$

alors que génériquement :

$$
\omega_A \neq \rho_B,
\qquad
\omega_C \neq \rho_B .
$$

Par conséquent :

```text
CONTEXTUAL_STATE = AUXILIARY_STATE_RECONSTRUCTED_FROM_PROJECTED_MODULAR_DATA
```

Interdit :

```text
"état du sous-système B"
"état physique de B dans le contexte A"
"B change de omega_A à omega_C"
```

---

## 6. Pourquoi la reconstruction n'est pas arbitraire, au sens faible

Motivation bornée enregistrée :

1. \(K = -\ln\rho\) est déjà la convention modulaire gelée.
2. \(\exp(-\cdot)\) en est le calcul fonctionnel inverse.
3. La normalisation supprime l'ambiguïté additive d'identité.
4. \(\beta=1\) dans \(\exp(-\beta\chi)\) n'est pas introduit comme un paramètre libre ; il est hérité de la convention \(K=-\ln\rho\).

Mais enregistré explicitement :

```text
PARAMETER_FREE_RECONSTRUCTION_IS_INHERITED_FROM_K_CONVENTION = TRUE
```

et non :

```text
independently derived parameter-free principle
```

---

## 7. Transporteur contextuel fini

Pour des états contextuels fidèles \(\omega_{\text{source}}\) et \(\omega_{\text{target}}\) sur la même algèbre de chevauchement \(B\), on définit :

$$
F_{\text{source}\to\text{target}}
=
\big[D\omega_{\text{target}} : D\omega_{\text{source}}\big]_{-i/2},
$$

et, en type I fini :

$$
F_{\text{source}\to\text{target}}
=
\omega_{\text{target}}^{1/2}\,
\omega_{\text{source}}^{-1/2}.
$$

Nom de travail :

```text
FINITE_RELATIVE_CONTEXTUAL_STATE_TRANSPORTER
```

Statut de transformation finie :

```text
FINITE_TRANSFORM_STATUS = FINITE_RELATIVE_STATE_TRANSPORT_ONLY
```

Interdit de nommer cet objet :

```text
finite relational change operator
evolution operator
time-step operator
```

---

## 8. Le point analytique \(-i/2\)

À distinguer :

```text
REAL_CONNES_COCYCLE:  [D c : D a]_t,  t réel
```

de :

```text
ANALYTIC_HALF_POINT:  [D c : D a]_(-i/2)
```

Enregistré :

```text
-i/2 IS NOT physical time.
-i/2 IS NOT duration.
-i/2 IS NOT an arbitrary real-flow instant.
```

On définit :

$$
G_\eta = c^\eta a^{-\eta} .
$$

Pour \(a \neq c\), identité analytique enregistrée : dans cette famille continuée,

$$
G_\eta\, a\, G_\eta^\dagger = c
\quad\Longleftrightarrow\quad
\eta = 1/2 .
$$

Par conséquent :

```text
HALF_POINT_STATUS = STRUCTURALLY_FIXED_WITHIN_DECLARED_ANALYTIC_FAMILY
```

Mais :

```text
UNIQUE_PARAMETER_FREE_TRANSPORTER_GLOBALLY = NO
```

---

## 9. Propriétés exactes de transport

Identités exactes enregistrées :

$$
F_{A\to C}\,\omega_A\,F_{A\to C}^\dagger = \omega_C .
$$

$$
F_{A\to A} = I .
$$

$$
F_{A\to C}^{-1} = F_{C\to A} .
$$

Pour des \(\omega_A, \omega_C, \omega_D\) fidèles :

$$
F_{C\to D}\,F_{A\to C} = F_{A\to D} .
$$

Sous \(U_B\) :

$$
\omega_X \to U_B\,\omega_X\,U_B^\dagger
\quad\Longrightarrow\quad
F \to U_B\,F\,U_B^\dagger .
$$

Aucun réel \(s\), \(t\), \(\tau\) n'apparaît dans \(F\).

---

## 10. Frontière de canonicité

L'équation :

$$
X\,\omega_A\,X^\dagger = \omega_C
$$

admet de nombreuses solutions inversibles.

Enregistré :

```text
TRANSPORTER_UNIQUENESS = RELATIVE_NOT_ABSOLUTE
```

\(F\) est distingué par :

1. la continuation analytique de Connes au point \(-i/2\) ;
2. une convention de multiplication à gauche sur les représentants racine-carrée canoniques :

$$
F\,\omega_A^{1/2} = \omega_C^{1/2} .
$$

Interdit d'affirmer :

```text
unique finite transporter
unique parameter-free transporter
```

D'autres transports finis canoniques existent, y compris des constructions positives de type moyenne géométrique/Bures. Ils ne sont pas transformés en candidats `model0d` concurrents.

---

## 11. Non-unitarité et absence de dynamique

Enregistré exactement :

$$
F^\dagger F
=
\omega_A^{-1/2}\,\omega_C\,\omega_A^{-1/2} .
$$

Par conséquent :

$$
F \text{ unitaire}
\iff
\omega_A = \omega_C
\iff
F = I .
$$

Pour tout transport non trivial :

```text
F IS NONUNITARY
```

Conséquences :

$$
X \to F X F^\dagger
$$

est CP en tant qu'application à un seul opérateur de Kraus, mais généralement :

```text
NOT_TRACE_PRESERVING
```

Sa duale :

$$
Y \to F^\dagger Y F
$$

est généralement :

```text
NOT_UNITAL
NOT_MULTIPLICATIVE
```

Donc :

```text
FINITE_TRANSPORTER_IS_CHANNEL           = NO
FINITE_TRANSPORTER_IS_STAR_AUTOMORPHISM = NO
FINITE_TRANSPORTER_IS_DYNAMICS          = NOT_ESTABLISHED
```

---

## 12. Décomposition polaire

Pour :

$$
F = U P,
\qquad
P = (F^\dagger F)^{1/2},
$$

enregistré :

$$
U = I
\iff
[\omega_A, \omega_C] = 0 .
$$

Dans la famille `model0c` amont déclarée :

$$
U \neq I
\iff
N_{(A:C\mid B)} \neq 0 .
$$

Statut :

```text
STRUCTURAL_ANALYTIC
BOUNDED_TO_DECLARED_UPSTREAM_FAMILY  (pour l'équivalence avec N)
```

Interprétation autorisée :

- \(U\) capture une composante de type non-commutation/orientation de la paire ;
- \(\operatorname{spectrum}(P)\) capture un désaccord spectral/d'amplitude.

Interdit :

```text
U = Uhlmann phase
```

Correction explicite : \(U\) est la phase polaire de \(\omega_C^{1/2}\,\omega_A^{-1/2}\), tandis que la phase relative d'Uhlmann usuelle est associée à une décomposition polaire portant sur \(\omega_C^{1/2}\,\omega_A^{+1/2}\).

Également enregistré :

$$
\text{RIGHT\_POSITIVE\_PART} \neq \text{LEFT\_POSITIVE\_PART}
$$

en tant qu'opérateurs, en général, bien que leurs spectres non nuls coïncident.

Aucun candidat séparé n'est créé à partir de \(U\) ou de \(P\).

---

## 13. Limitation de composition

Enregistré :

$$
F_{X\to Y} = g(Y)\,g(X)^{-1},
\qquad
g(X) = \omega_X^{1/2} .
$$

La loi de composition est donc une identité de cobord.

Pour toute boucle :

$$
F_{D\to A}\,F_{C\to D}\,F_{A\to C} = I
$$

identiquement.

Donc :

```text
COMPOSITION_STATUS = USEFUL_BUT_TAUTOLOGICAL
HOLONOMY            = IDENTICALLY_TRIVIAL_ON_COMMON_OVERLAP
```

Aucune :

```text
curvature
cyclic ordering
irreversibility
arrow
```

La composition est un contrôle de cohérence nécessaire, pas une évidence indépendante de changement.

---

## 14. Dépendance à la projection

Hérité de `model0c` :

```text
ROBUST_DIRECTION = YES
ROBUST_AMPLITUDE = NO
```

Puisque \(\omega_X = e^{-\chi_X}/Z\), \(F\) dépend des amplitudes.

Enregistré :

```text
PROJECTION_DEPENDENCE = BLOCKING_ONLY_FOR_FUTURE_PHYSICAL_INTERPRETATION
```

Pour la qualification sous la règle traciale déclarée :

```text
NON_BLOCKING
```

Contenu robuste attendu sous la comparaison `S2` déclarée :

- plan des axes/du contexte ;
- statut \(U = I\) contre \(U \neq I\).

Contenu non robuste attendu :

- module de \(F\) ;
- spectre de \(P\) ;
- angle/phase quantitatifs de \(U\).

Aucune revendication plus forte.

---

## 15. Conditionnement numérique

Près de la frontière fidèle, \(\omega_{\text{source}}^{-1/2}\) peut devenir mal conditionné.

Interdit :

```text
no silent regularization
no pseudoinverse
no eigenvalue clipping
no hidden ridge
```

Diagnostics de qualification définis, AVANT implémentation :

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
    (quand un oracle analytique d_B=2 est disponible)
```

Ces diagnostics sont :

```text
NUMERICAL_QUALIFICATION_GUARDS
```

et non :

```text
physical observables
```

Aucun seuil scientifique n'est fermé par ce document. Les tolérances d'implémentation/de test restent explicites et non normatives.

Aucune revendication de qualification à la frontière spectrale :

```text
BOUNDARY_REGIME = OUT_OF_SCOPE_FOR_MODEL0D_QUALIFICATION
```

---

## 16. Contrôles

**D0_IDENTITY** : \(\omega_A = \omega_C \implies F = I,\ U = I,\ P = I\).

**D1_COMMUTING_DISTINCT** : cas correspondant à une branche projetée inactive et une branche active, par exemple une entrée contextuelle de type C4 de `model0c` : \(\omega_A = I/2\), \(\omega_C \neq I/2\), donc \([\omega_A,\omega_C]=0\), \(F \neq I\), \(F\) positif, \(U = I\), \(P \neq I\). But : `FINITE_TRANSPORT_NONTRIVIAL` n'implique pas un contenu de non-commutation/orientation.

**D2_NONCOMMUTING** : entrées contextuelles de type C3 de `model0c`, \([\omega_A,\omega_C] \neq 0\), donc \(F \neq I\), \(U \neq I\). Vérifier la cohérence avec \(N \neq 0\).

**D3_ACTUAL_OVERLAP_STATE_UNCHANGED** : pour la fixture amont `model0c`, \(\rho_B = I/2\) alors que \(\omega_A \neq \omega_C\). But : le transport agit entre états contextuels auxiliaires, pas entre deux états réduits physiques successifs de \(B\). Ce contrôle négatif est obligatoire.

**D4_NONCHANNEL** : pour D2, \(F^\dagger F \neq I\). Exhiber au moins un état normalisé \(\sigma\) tel que \(\operatorname{Tr}(F\sigma F^\dagger) \neq 1\). Conclusion : `NOT_CPTP_DYNAMICS`.

**D5_COMPOSITION** : vérifier l'identité exacte de la chaîne à trois états, mais étiqueter le résultat `TAUTOLOGICAL_CHAIN_RULE`, et vérifier en outre qu'une boucle fermée redonne l'identité. Aucun score d'évidence n'est attaché.

**D6_PROJECTION_SENSITIVITY** : comparer les états contextuels/le transporteur traciaux officiels avec la reconstruction contextuelle pondérée `S2` déjà autorisée par l'analyse de sensibilité de `model0c`. Vérifier uniquement que le statut qualitatif de non-commutation/orientation survit. Démontrer explicitement que \(F_{\text{weighted}} \neq F_{\text{tracial}}\) génériquement. Conclusion : `ROBUST_ORIENTATION_CLASS`, `ROBUST_AMPLITUDE = NO`.

---

## 17. Claim maximal autorisé

Formulation maximale autorisée :

> Sur une algèbre de chevauchement finie de type I, à partir de deux contextes modulaires projetés et sous la convention de reconstruction déclarée, un transporteur d'état contextuel fini, dirigé, inversible et covariant sous changement de base peut être construit sans sélectionner de paramètre réel de flot modulaire. Il transporte exactement les deux états contextuels reconstruits et sa composante polaire non commutative s'aligne, dans la famille `model0c` déclarée, avec le régime déjà qualifié \(N \neq 0\). Ce transporteur n'est ni un canal, ni un automorphisme, ni une dynamique, et ne transporte pas deux états physiques réduits différents de \(B\).

---

## 18. Pare-feu T1

```text
FINITE_RELATIVE_STATE_TRANSPORT = CANDIDATE_FOR_QUALIFICATION

RELATIONAL_PHYSICAL_CHANGE = NOT_ESTABLISHED
RELATIONAL_TIME            = NOT_ESTABLISHED

FINITE_FLOW_PARAMETER_PROBLEM = OPEN
```

Raison : \(F\) est un transporteur fini par paire, PAS un flot/orbite fini.

Aucun :

```text
T1_PASS
```

```text
T1_NONTRIVIALITY_CRITERION = OPEN
CONFIRMATORY_PROTOCOL      = NOT_DEFINED
```

---

## 19. Ce que model0d ne teste pas

Sont exclus :

```text
finite physical evolution
physical time
relational clock
Page-Wootters implementation
QRF implementation
HSMI
causal order
time orientation
arrow of time
curvature
holonomy nontrivial
CPTP dynamics
star-automorphism dynamics
T1 PASS
T2+
geometry
gravity
```

---

## 20. Paramètres qui restent `OPEN`

```text
FINITE_RELATIVE_CONTEXTUAL_STATE_TRANSPORTER_DEFINITION = CLOSED — cf. §7
HALF_POINT_ANALYTIC_CONTINUATION                         = CLOSED — cf. §8
CONTEXT_STATE_RECONSTRUCTION_CONVENTION                  = CLOSED — cf. §5

MODEL0D_CONTEXT_FIXTURES      = OPEN / NON_NORMATIVE_AT_IMPLEMENTATION
NUMERICAL_TOLERANCES          = OPEN
MODEL0D_ACCEPTANCE_CRITERION  = OPEN
T1_NONTRIVIALITY_CRITERION    = OPEN
CONFIRMATORY_PROTOCOL         = NOT_DEFINED
FINITE_FLOW_PARAMETER_PROBLEM = OPEN
```

---

## 21. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

---

## 22. Statut et prochaine étape

```text
MODEL0D_SPECIFICATION_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
