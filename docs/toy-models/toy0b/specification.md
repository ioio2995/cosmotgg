# toy0b — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0b`, construction candidate du toy `toy0b`.

Il transforme en contrat explicite l'arbitrage scientifique de ChatGPT, appuyé par la contre-expertise `MODEL0B-OVERLAP-PROJECTION-REVIEW-1`. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique de paramètre d'état, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy0b
MODEL_ID = model0b

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL0B_CLASS = T1_RELATIVE_MODULAR_GENERATOR_QUALIFICATION_NONCONFIRMATORY
```

---

## 2. Position dans les tests CosmoTGG

```text
COSMOTGG_TEST_TARGET = T1_RELATIONAL_FLOW
```

Explicitement :

```text
MODEL0B_IS_T1_CONFIRMATORY_TEST = NO
MODEL0B_PROVES_T1                = NO
MODEL0B_PROVES_RELATIONAL_TIME   = NO
```

Le rôle de `model0b` est de qualifier une construction algébrique relative sur le chevauchement de deux relations modulaires. Il ne constitue pas encore :

```text
RELATIONAL_PHYSICAL_CHANGE
finite relational evolution
clock
time
```

---

## 3. Continuité avec model0a

`model0a` a établi, au niveau `QUALIFICATION_NONCONFIRMATORY` (`docs/toy-models/toy0a/specification.md`), que :

- le cocycle fini est calculable ;
- son tangent \(\mathcal R_{AB}\) est calculable ;
- la structure au-delà du premier ordre distingue régime commutant et régime non commutant ;
- cette qualification n'établit pas T1.

`model0b` change de question. Il ne cherche plus à mieux qualifier \(C_{AB}\) ou \(G(s_1,s_2)\) ; il compare deux structures modulaires chevauchantes sur une algèbre commune.

---

## 4. Cadre

$$
\mathcal H_A = \mathbb C^2,
\qquad
\mathcal H_B = \mathbb C^2,
\qquad
\mathcal H_C = \mathbb C^2,
$$

$$
\mathcal H_{ABC} = \mathcal H_A \otimes \mathcal H_B \otimes \mathcal H_C .
$$

La factorisation \(A|B|C\) est :

```text
DECLARED_MODEL_STRUCTURE
```

Elle n'est ni une géométrie, ni une distance, ni un espace émergé.

Le sous-système commun choisi est \(B\).

---

## 5. Famille d'états

```text
STATE_FAMILY = THREE_QUBIT_OVERLAPPING_PAULI_RELATION_FAMILY
```

$$
\rho_{ABC}(\beta,\lambda,\mu)
=
\frac18\Big[
I
+ \beta\, Z_B
+ \lambda\, X_A X_B
+ \mu\, Y_B Y_C
\Big].
$$

Les identités sur les facteurs non écrits sont implicites (par exemple \(Z_B\) désigne \(I_A \otimes Z_B \otimes I_C\)).

Les trois chaînes \(Z_B\), \(X_A X_B\), \(Y_B Y_C\) sont hermitiennes, de carré \(I\), et anticommutent deux à deux. Donc :

$$
V^2 = \big(\beta^2+\lambda^2+\mu^2\big)\, I,
\qquad
V = \beta Z_B + \lambda X_A X_B + \mu Y_B Y_C .
$$

---

## 6. Domaine fidèle exact

```text
STATUS = CLOSED
```

$$
\beta^2 + \lambda^2 + \mu^2 < 1 .
$$

Sous cette condition, le spectre de \(\rho_{ABC}\) est :

$$
\frac{1+r}{8}\ \text{(multiplicité 4)},
\qquad
\frac{1-r}{8}\ \text{(multiplicité 4)},
\qquad
r = \sqrt{\beta^2+\lambda^2+\mu^2} .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Aucune tolérance numérique n'intervient dans cette définition.

---

## 7. États réduits

$$
\rho_{AB}
=
\frac14\Big[I + \beta\, Z_B + \lambda\, X_A X_B\Big],
$$

$$
\rho_{BC}
=
\frac14\Big[I + \beta\, Z_B + \mu\, Y_B Y_C\Big],
$$

$$
\rho_B
=
\frac12\Big[I + \beta\, Z_B\Big],
\qquad
\rho_A = \frac{I_A}{2},
\qquad
\rho_C = \frac{I_C}{2}.
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Ces réductions résultent de la trace partielle exacte des chaînes de Pauli déclarées au §5 ; elles sont conséquence directe du domaine fidèle du §6 (\(\rho_{AB}\), \(\rho_{BC}\), \(\rho_B\) sont automatiquement fidèles dès que \(\rho_{ABC}\) l'est, puisque leurs rayons spectraux respectifs \(r_{AB}=\sqrt{\beta^2+\lambda^2}\), \(r_{BC}=\sqrt{\beta^2+\mu^2}\), \(|\beta|\) sont chacun \(\le r < 1\)).

---

## 8. Hamiltoniens modulaires

$$
K_{AB} = -\ln(\rho_{AB}),
\qquad
K_{BC} = -\ln(\rho_{BC}) .
$$

Le candidat `model0b` est formulé directement à partir de ces structures. \(\mathcal R_{AB}\)/\(\mathcal R_{BC}\) ne sont pas présentés comme des ingrédients nécessaires.

L'identité suivante est enregistrée comme définition primaire :

$$
\Delta_{(A:C|B)}
=
-\,\operatorname{tl}_B\!\Big[
E_B^A(K_{AB})
-
E_B^C(K_{BC})
\Big].
$$

Une formulation équivalente utilisant \(\mathcal R_{AB}\)/\(\mathcal R_{BC}\) peut être mentionnée comme identité dérivée, mais elle n'est pas la définition primaire.

---

## 9. Conditional expectation sur le chevauchement

$$
E_B^A(X_{AB}) = \frac{1}{d_A}\operatorname{Tr}_A(X_{AB}),
\qquad
E_B^C(X_{BC}) = \frac{1}{d_C}\operatorname{Tr}_C(X_{BC}),
$$

avec \(d_A = d_C = 2\).

```text
SELECTION_RULE = TRACE_PRESERVING_CONDITIONAL_EXPECTATION
```

```text
TRACIAL_CONDITIONAL_EXPECTATION = UNIQUE_UNDER_TRACE_PRESERVATION
```

dans le cadre fini de type I déclaré (§4). Elle est linéaire, complètement positive, unitale, bimodulaire, idempotente, et préserve la trace normalisée.

---

## 10. Frontière trace vs state-preserving

```text
OVERLAP_PROJECTION_IS_TRACIAL_TYPE_I_FINITE = TRUE
```

Pour la branche AB :

```text
STATE_PRESERVING_CONDITIONAL_EXPECTATION_ONTO_B = NONEXISTENT_FOR_lambda_NONZERO
```

au sens du critère de Takesaki applicable à l'état fidèle \(\rho_{AB}\).

Symétriquement, pour la branche BC :

```text
STATE_PRESERVING_CONDITIONAL_EXPECTATION_ONTO_B = NONEXISTENT_FOR_mu_NONZERO
```

Cette affirmation n'est pas généralisée hors du cadre exact déclaré.

```text
ALGEBRAIC_GENERALIZATION_OF_DELTA = OPEN
TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE = OPEN
```

---

## 11. Réduction sans trace

$$
\operatorname{tl}_B(X) = X - \frac{\operatorname{Tr}(X)}{d_B}\, I_B .
$$

Justification : la dérivation intérieure \(X \mapsto -i[X,\cdot]\) est insensible à \(X \mapsto X + c\,I\). Donc :

```text
TRACELESS_REDUCTION = JUSTIFIED
```

pour la définition du générateur. La partie scalaire de l'objet original n'est pas déclarée inexistante ou sans information ; elle est seulement non pertinente pour la dérivation intérieure.

---

## 12. Générateur relatif

$$
\chi_{(A\to B)} = \operatorname{tl}_B\big[E_B^A(K_{AB})\big],
\qquad
\chi_{(C\to B)} = \operatorname{tl}_B\big[E_B^C(K_{BC})\big].
$$

Convention fixée pour l'ensemble de ce document :

$$
\Delta_{(A:C|B)}
=
-\,\chi_{(A\to B)}
+
\chi_{(C\to B)},
$$

algébriquement équivalente à :

$$
\Delta_{(A:C|B)}
=
-\operatorname{tl}_B\big[E_B^A(K_{AB}) - E_B^C(K_{BC})\big] .
$$

Nom : `OVERLAP_RELATIVE_MODULAR_GENERATOR`.

```text
STATUS = RELATIVE_ALGEBRAIC_GENERATOR_CANDIDATE
```

---

## 13. Dérivation

$$
D_{(A:C|B)}(O_B) = -i\,\big[\Delta_{(A:C|B)},\, O_B\big] .
$$

Nom : `OVERLAP_RELATIVE_MODULAR_DERIVATION`.

```text
STATUS = RELATIVE_ALGEBRAIC_DERIVATION
```

`D` n'est appelé ni `temporal derivative`, ni `time derivative`, ni `relational change`, ni `flow`, ni `clock`.

---

## 14. Formule analytique

$$
r_{AB} = \sqrt{\beta^2+\lambda^2},
\qquad
r_{BC} = \sqrt{\beta^2+\mu^2},
\qquad
f(r) = \frac{\operatorname{atanh}(r)}{r},
\qquad
f(0)=1 .
$$

$$
\Delta_{(A:C|B)}
=
\beta\,\big[f(r_{AB}) - f(r_{BC})\big]\, Z_B .
$$

Notation :

$$
\delta = \beta\,\big[f(r_{AB}) - f(r_{BC})\big] .
$$

$$
D(X_B) = 2\delta\, Y_B,
\qquad
D(Y_B) = -2\delta\, X_B,
\qquad
D(Z_B) = 0 .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

---

## 15. Condition exacte de non-nullité

$$
\Delta \neq 0
\iff
\beta \neq 0
\ \text{et}\
\lambda^2 \neq \mu^2
$$

dans le domaine fidèle déclaré (§6). Raison : \(f\) est strictement croissante en \(r^2\) sur \([0,1)\).

```text
STATUS = STRUCTURAL_ANALYTIC
```

Le signe de \(\delta\) n'est pas interprété comme orientation causale, flèche du temps ou orientation temporelle.

---

## 16. Contrôles structurels

**R0_PRODUCT** : \(\lambda=0,\ \mu=0 \implies \Delta = 0\).

**R1_EQUAL_RELATIONS** : \(|\lambda|=|\mu|\neq0 \implies \Delta = 0\), alors que les deux relations peuvent être individuellement corrélées/non triviales. Interprétation : \(\Delta=0\) `DOES_NOT_IMPLY` `NO_RELATION`.

**R2_ASYMMETRIC_RELATIONS** : \(\beta\neq0,\ |\lambda|\neq|\mu| \implies \Delta \neq 0\).

**R3_MAXIMALLY_MIXED_OVERLAP** : \(\beta=0 \implies \rho_B = I/2,\ \Delta = 0\), même si \(|\lambda|\neq|\mu|\). Interprétation : l'absence de structure modulaire locale non triviale sur \(B\) implique que le candidat ne produit pas de générateur relatif.

```text
R3 = ACCEPTABLE_DEGENERACY / NEGATIVE_CONTROL
```

---

## 17. Antisymétrie

$$
\Delta_{(C:A|B)} = -\Delta_{(A:C|B)}
$$

est `TRIVIALLY_TRUE_BY_DEFINITION`.

De même :

$$
\chi_{(A\to B)} = \chi_{(C\to B)}
\implies
\Delta = 0
\implies
D = 0
$$

est `TRIVIALLY_TRUE_BY_DEFINITION`. Ces faits ne constituent pas une validation indépendante du caractère physique du candidat.

---

## 18. Point de limitation important — colinéarité

```text
OVERLAP_DERIVATION_COLLINEAR_WITH_LOCAL_MODULAR_GENERATOR = TRUE_FOR_DECLARED_STATE_FAMILY
```

Dans toute la famille déclarée au §5, \(\chi_{(A\to B)}\), \(\chi_{(C\to B)}\), \(\Delta\) et \(\operatorname{tl}_B(\ln \rho_B)\) sont colinéaires à \(Z_B\).

Pour \(\beta\neq0\), \(D\) est donc seulement un rescaling relationnellement déterminé de la dérivation modulaire locale de \(\rho_B\).

Conséquence — `model0b` ne démontre pas :

```text
new operator direction
independent relational dynamics
independent clock
physical rate of change
```

Le contenu relationnel supplémentaire de cette famille est essentiellement porté par \(\delta\).

```text
NON_BLOCKING_FOR_MODEL0B_QUALIFICATION
```

---

## 19. Paramètre de flot fini

```text
SHARED_PARAMETER_FALSE_POSITIVE = AVOIDED_AT_DELTA_LEVEL_ONLY
```

Aucun paramètre \(s\) n'apparaît dans \(\Delta\) ou \(D\). Mais si l'on construit :

$$
O(\tau) = e^{-i\tau\Delta}\, O\, e^{+i\tau\Delta},
$$

alors \(\tau\) n'est déterminé par aucune donnée du candidat. Donc :

```text
FINITE_FLOW_PARAMETER_PROBLEM = OPEN
```

`model0b` ne construit pas deux flots paramétrés puis n'élimine pas leur paramètre pour prétendre obtenir un temps relationnel.

```text
PARAMETER_ELIMINATION_ALONE = INSUFFICIENT
```

hérité de `model0a` (`docs/toy-models/toy0a/specification.md` §10).

---

## 20. Distinction épistémique centrale

```text
RELATIVE_ALGEBRAIC_DERIVATION = ESTABLISHED_AS_MODEL_CANDIDATE
RELATIONAL_PHYSICAL_CHANGE    = NOT_ESTABLISHED
RELATIONAL_TIME               = NOT_ESTABLISHED
T1                             = OPEN_NOT_EXECUTED
```

Formulation maximale autorisée :

> Sur un système fini type-I à factorisation \(A|B|C\) déclarée, avec sélection de la conditional expectation préservant la trace normalisée, deux structures modulaires chevauchantes peuvent être projetées sur l'algèbre commune \(B\) ; leur différence sans trace définit un générateur/dérivation algébrique relatif, déterminé par l'état et covariant sous les changements de bases locaux appropriés.

Aucune interprétation temporelle physique.

---

## 21. Covariance

La construction vise uniquement `LOCAL_PRODUCT_UNITARY_COVARIANCE`, avec \(U_A \otimes U_B \otimes U_C\).

La projection satisfait :

$$
E_B^A\big((U_A\otimes U_B)\,X\,(U_A\otimes U_B)^\dagger\big)
=
U_B\, E_B^A(X)\, U_B^\dagger,
$$

et analogiquement côté BC. Donc :

$$
\Delta \to U_B\,\Delta\,U_B^\dagger .
$$

`model0b` ne revendique pas : `arbitrary global unitary invariance`, `refactorization invariance`, `Lorentz covariance`, `general covariance`.

---

## 22. Ce que model0b ne teste pas

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
T1 PASS
T2+
geometry
gravity
```

---

## 23. Paramètres qui restent `OPEN`

```text
LOCAL_DIMENSION                = CLOSED — cf. §4, (2, 2, 2)
STATE_FAMILY                   = CLOSED — cf. §5, THREE_QUBIT_OVERLAPPING_PAULI_RELATION_FAMILY
FAITHFUL_DOMAIN                = CLOSED — cf. §6, beta^2+lambda^2+mu^2 < 1
SELECTION_RULE                 = CLOSED — cf. §9, TRACE_PRESERVING_CONDITIONAL_EXPECTATION
PRIMARY_GENERATOR_DEFINITION   = CLOSED — cf. §8, §12

BETA_VALUE                     = OPEN
LAMBDA_VALUE                   = OPEN
MU_VALUE                       = OPEN

NUMERICAL_TOLERANCES           = OPEN
MODEL0B_ACCEPTANCE_CRITERION   = OPEN
T1_NONTRIVIALITY_CRITERION     = OPEN
CONFIRMATORY_PROTOCOL          = NOT_DEFINED
```

Le domaine analytique (§6) est `CLOSED` ; les valeurs de fixtures ne le sont pas.

---

## 24. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

M. Takesaki, *Conditional Expectations in von Neumann Algebras*, J. Funct. Anal. 9 (1972) 306–321 — critère d'existence d'une conditional expectation préservant l'état, utilisé au §10.

---

## 25. Statut et prochaine étape

```text
MODEL0B_SPECIFICATION_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
