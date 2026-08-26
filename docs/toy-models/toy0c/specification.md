# toy0c — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0c`, construction candidate du toy `toy0c`.

Il transforme en contrat explicite l'arbitrage scientifique de ChatGPT, appuyé par la revue `MODEL0C-NONCOLLINEAR-CANDIDATE-REVIEW`. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique de paramètre d'état, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy0c
MODEL_ID = model0c

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL0C_CLASS = T1_NONCOLLINEAR_RELATIVE_MODULAR_GENERATOR_QUALIFICATION_NONCONFIRMATORY
```

---

## 2. Position dans les tests CosmoTGG

```text
COSMOTGG_TEST_TARGET = T1_RELATIONAL_FLOW
```

Explicitement :

```text
MODEL0C_IS_T1_CONFIRMATORY_TEST = NO
MODEL0C_PROVES_RELATIONAL_TIME  = NO

T1 = OPEN_NOT_EXECUTED
```

Le rôle de `model0c` est de tester si deux relations modulaires chevauchantes peuvent produire, sur leur sous-système commun \(B\), deux directions opératorielles non colinéaires. Il ne constitue pas encore :

```text
RELATIONAL_PHYSICAL_CHANGE
finite relational evolution
clock
time
```

---

## 3. Continuité avec model0a et model0b

`model0a` a établi, au niveau `QUALIFICATION_NONCONFIRMATORY` (`docs/toy-models/toy0a/specification.md`), que le cocycle fini et son tangent \(\mathcal R_{AB}\) sont calculables, et que cette qualification n'établit pas T1.

`model0b` a établi, au niveau `QUALIFICATION_NONCONFIRMATORY` (`docs/toy-models/toy0b/specification.md`), un générateur algébriquement relatif \(\Delta_{(A:C|B)}\) sur le chevauchement \(B\) de deux structures modulaires, sans paramètre \(s\) partagé dans sa définition. Cependant, dans la famille d'états déclarée par `model0b`, les contributions projetées restent colinéaires (`OVERLAP_DERIVATION_COLLINEAR_WITH_LOCAL_MODULAR_GENERATOR = TRUE_FOR_DECLARED_STATE_FAMILY`, `docs/toy-models/toy0b/specification.md` §18).

`model0c` change de question. Il ne cherche plus à obtenir un générateur relatif sans paramètre partagé (déjà acquis par `model0b`) ; il teste si deux relations modulaires chevauchantes peuvent produire deux directions opératorielles non colinéaires sur \(B\).

Portée de l'interprétation `R3` de `model0b` :

```text
MODEL0B_R3_INTERPRETATION_SCOPE = MODEL0B_DECLARED_STATE_FAMILY_ONLY
```

L'interprétation `R3` de `model0b` (\(\rho_B = I/2 \implies \Delta = 0\), lue comme « absence de structure modulaire locale non triviale sur \(B\) implique absence de générateur relatif ») est bornée à la famille d'états déclarée par `model0b` (`docs/toy-models/toy0b/specification.md` §16, `R3_MAXIMALLY_MIXED_OVERLAP`). Elle n'est ni généralisée ni contredite ici : `model0c` montre (§18 ci-dessous) qu'elle ne s'étend pas telle quelle à sa propre famille d'états, sans rouvrir ni modifier aucun document de `model0b`.

Ce document ne modifie aucun contenu scientifique de `docs/toy-models/toy0b/specification.md` ni de `docs/toy-models/toy0b/implementation-design.md`.

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

$$
\alpha, \gamma, \lambda, \mu \in \mathbb R .
$$

---

## 5. Famille d'états

```text
STATE_FAMILY = THREE_QUBIT_NONCOLLINEAR_OVERLAP_RELATION_FAMILY
```

$$
\rho_{ABC}(\alpha,\gamma,\lambda,\mu)
=
\frac18\Big[
I
+ \alpha\, X_A
+ \gamma\, Z_C
+ \lambda\, X_A X_B
+ \mu\, Y_B Z_C
\Big].
$$

Les identités sur les facteurs non écrits sont implicites (par exemple \(X_A\) désigne \(X_A \otimes I_B \otimes I_C\)).

---

## 6. Domaine fidèle exact

```text
STATUS = CLOSED
```

$$
|\alpha| + |\gamma| + \sqrt{\lambda^2+\mu^2} < 1 .
$$

Condition nécessaire et suffisante.

Spectre, pour \(x,z \in \{-1,+1\}\) :

$$
\frac{1 + \alpha x + \gamma z \pm \sqrt{\lambda^2+\mu^2}}{8} .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Corollaire d'exécutabilité :

$$
|\alpha| + |\lambda| < 1,
\qquad
|\gamma| + |\mu| < 1
$$

donc \(\rho_{AB}\) et \(\rho_{BC}\) (§7) sont automatiquement fidèles.

Aucune tolérance normative n'intervient dans cette définition.

---

## 7. États réduits

$$
\rho_{AB}
=
\frac14\Big[I + \alpha\, X_A + \lambda\, X_A X_B\Big],
$$

$$
\rho_{BC}
=
\frac14\Big[I + \gamma\, Z_C + \mu\, Y_B Z_C\Big],
$$

$$
\rho_B = \frac{I_B}{2},
\qquad
\rho_A = \frac12\Big[I + \alpha\, X_A\Big],
\qquad
\rho_C = \frac12\Big[I + \gamma\, Z_C\Big].
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

---

## 8. Hamiltoniens modulaires et conditional expectation héritée

$$
K_{AB} = -\ln(\rho_{AB}),
\qquad
K_{BC} = -\ln(\rho_{BC}) .
$$

Règle primaire héritée de `model0b` (`docs/toy-models/toy0b/specification.md` §9), sans redéfinition :

```text
SELECTION_RULE = TRACE_PRESERVING_CONDITIONAL_EXPECTATION
```

$$
E_B^A(X) = \frac{\operatorname{Tr}_A(X)}{2},
\qquad
E_B^C(X) = \frac{\operatorname{Tr}_C(X)}{2} .
$$

---

## 9. Réduction sans trace

$$
\operatorname{tl}_B(X) = X - \frac{\operatorname{Tr}(X)}{d_B}\, I_B,
\qquad d_B = 2 .
$$

Définition et justification héritées de `model0b` (`docs/toy-models/toy0b/specification.md` §11) : la dérivation intérieure \(X \mapsto -i[X,\cdot]\) est insensible à \(X \mapsto X + c\,I\). Elles ne sont pas reformulées ici.

---

## 10. Générateurs relatifs projetés et générateur \(\Delta\)

$$
\chi_A = \operatorname{tl}_B\big[E_B^A(K_{AB})\big],
\qquad
\chi_C = \operatorname{tl}_B\big[E_B^C(K_{BC})\big],
$$

$$
\Delta = -\chi_A + \chi_C .
$$

```text
STATUS = RELATIVE_ALGEBRAIC_GENERATOR_CANDIDATE
```

---

## 11. Formules analytiques

$$
g(q,r) = \frac{\operatorname{atanh}(r/q)}{r},
\qquad
g(q,0) = \frac1q .
$$

$$
\chi_A
=
-\frac{\lambda}{2}
\Big[
g(1+\alpha,|\lambda|) - g(1-\alpha,|\lambda|)
\Big]\, X_B,
$$

$$
\chi_C
=
-\frac{\mu}{2}
\Big[
g(1+\gamma,|\mu|) - g(1-\gamma,|\mu|)
\Big]\, Y_B .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

---

## 12. Condition exacte de non-nullité des générateurs projetés

$$
\chi_A \neq 0 \iff \alpha\lambda \neq 0,
\qquad
\chi_C \neq 0 \iff \gamma\mu \neq 0 .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

---

## 13. Diagnostic de non-colinéarité

$$
N_{(A:C|B)} = i\,[\chi_A, \chi_C] .
$$

Nom : `OVERLAP_PROJECTED_NONCOLLINEARITY_OPERATOR`.

\(N\) est hermitien.

Dans le cadre \(d_B = 2\) déclaré :

$$
N \neq 0 \iff \alpha\gamma\lambda\mu \neq 0 .
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Borne obligatoire :

```text
NONCOLLINEARITY_COMMUTATOR_EQUIVALENCE = QUBIT_OVERLAP_ONLY
```

Cette équivalence n'est pas généralisée à \(d_B > 2\).

---

## 14. Limitation du diagnostic de non-colinéarité

\(N = 0\) peut signifier :

- des contributions colinéaires ;
- **ou** l'une des contributions nulle.

Dans la famille `model0c` particulière déclarée au §5, les directions non nulles de \(\chi_A\) et \(\chi_C\) sont forcées respectivement à \(X_B\) et \(Y_B\). Cette famille ne réalise donc **pas** le cas :

$$
\chi_A \neq 0,
\qquad
\chi_C \neq 0,
\qquad
\chi_A \parallel \chi_C .
$$

Cette limitation est déclarée explicitement, pas masquée.

---

## 15. Robustesse à la règle de projection

```text
TRACIAL_SELECTION_DEPENDENCE = ROBUST_DIRECTION
```

Signification exacte : pour toute projection \(B\)-bimodulaire, la branche \(AB\) projette dans \(\operatorname{span}\{I_B, X_B\}\), et sa partie sans trace dans \(\mathbb R X_B\) ; la branche \(BC\) projette dans \(\operatorname{span}\{I_B, Y_B\}\), et sa partie sans trace dans \(\mathbb R Y_B\). Les **axes** sont donc structurels.

Mais :

```text
ROBUST_AMPLITUDE = NO

NONNULLITY_UNDER_ARBITRARY_BIMODULAR_EXPECTATION = NOT_GUARANTEED
```

Aucune revendication au-delà de ce qui précède.

---

## 16. Contrôle de sensibilité S2

Prévu explicitement, pour qualification future, une comparaison avec :

$$
E_{\rho_A}(X) = \operatorname{Tr}_A\big[(\rho_A \otimes I_B)\, X\big],
\qquad
E_{\rho_C}(X) = \operatorname{Tr}_C\big[(I_B \otimes \rho_C)\, X\big] .
$$

Sous cette règle pondérée particulière, la direction de \(\chi_A\) reste \(X_B\) et celle de \(\chi_C\) reste \(Y_B\), et les conditions de non-nullité restent \(\alpha\lambda \neq 0\), \(\gamma\mu \neq 0\).

Cette comparaison est un **contrôle de sensibilité**, pas une seconde définition officielle de \(\Delta\).

---

## 17. Levée de la limitation de colinéarité de model0b

```text
MODEL0B_COLLINEARITY_LIMIT = REMOVED_IN_MODEL0C_CANDIDATE
```

Justifiée par :

$$
\chi_A \propto X_B,
\qquad
\chi_C \propto Y_B,
\qquad
[\chi_A, \chi_C] \neq 0,
$$

et **non** simplement par \(\rho_B = I/2\).

En effet :

$$
\rho_B = I/2
\implies
\operatorname{tl}_B(K_B) = 0 .
$$

Donc un \(\Delta\) non nul ne peut pas être un rescaling d'un générateur modulaire local non trivial de \(B\).

Mais :

```text
LOCAL_MODULAR_SOURCE_SHIFTED_FROM_B_TO_A_AND_C = TRUE
```

\(\chi_A\) non nul exige \(\alpha \neq 0\), donc \(\rho_A \neq I/2\). \(\chi_C\) non nul exige \(\gamma \neq 0\), donc \(\rho_C \neq I/2\).

Est interdit d'affirmer : « aucun générateur modulaire local n'est requis ».

---

## 18. Contrôles structurels

**C0_NO_AB_BC_OVERLAP_RELATIONS** : \(\lambda = 0,\ \mu = 0 \implies \rho_{AB} = \rho_A \otimes \rho_B,\ \rho_{BC} = \rho_B \otimes \rho_C,\ \chi_A = \chi_C = \Delta = N = 0\).

En général, \(\rho_{ABC} \neq \rho_A \otimes \rho_B \otimes \rho_C\) si \(\alpha\gamma \neq 0\) ; ce contrôle n'affirme pas que \(\rho_{ABC}\) est un état produit global.

**C1_CORRELATED_BUT_ZERO_PROJECTED_A** : \(\alpha = 0,\ \lambda \neq 0 \implies \rho_{AB}\) peut être corrélé, \(\chi_A = 0\).

**C2_CORRELATED_BUT_ZERO_PROJECTED_C** : \(\gamma = 0,\ \mu \neq 0 \implies \rho_{BC}\) peut être corrélé, \(\chi_C = 0\).

**C3_NONCOLLINEAR** : \(\alpha\gamma\lambda\mu \neq 0 \implies \chi_A \neq 0,\ \chi_C \neq 0,\ N \neq 0\).

**C4_DELTA_NONZERO_BUT_N_ZERO** : en choisissant une branche projetée inactive et l'autre active, par exemple \(\alpha = 0,\ \lambda \neq 0,\ \gamma\mu \neq 0 \implies \chi_A = 0,\ \chi_C \neq 0,\ \Delta \neq 0,\ N = 0\).

But : \(\Delta \neq 0\) n'est pas suffisant pour établir deux directions non colinéaires.

---

## 19. Covariance

$$
U = U_A \otimes U_B \otimes U_C .
$$

$$
\chi_A \to U_B\,\chi_A\,U_B^\dagger,
\qquad
\chi_C \to U_B\,\chi_C\,U_B^\dagger,
\qquad
\Delta \to U_B\,\Delta\,U_B^\dagger,
\qquad
N \to U_B\,N\,U_B^\dagger .
$$

Donc le statut \(N = 0\) / \(N \neq 0\) est invariant sous :

```text
LOCAL_PRODUCT_UNITARY_COVARIANCE
```

Aucune revendication globale, Lorentz ou de covariance générale.

---

## 20. Paramètre de flot fini

```text
FINITE_FLOW_PARAMETER_PROBLEM = OPEN
```

Aucun paramètre \(s\), \(t\) ou \(\tau\) n'entre dans \(\chi_A\), \(\chi_C\), \(\Delta\), \(N\). Mais aucune évolution physique finie n'est produite par cette construction.

```text
MODEL0C_SUCCESS != T1
```

---

## 21. Distinction épistémique centrale — claim maximal

```text
RELATIONAL_PHYSICAL_CHANGE = NOT_ESTABLISHED
RELATIONAL_TIME            = NOT_ESTABLISHED
T1                          = OPEN_NOT_EXECUTED
```

Formulation maximale autorisée :

> Sur un système fini type-I \((2,2,2)\), sous la règle traciale déclarée, deux structures modulaires chevauchantes peuvent produire sur \(B\) deux générateurs projetés non colinéaires, dont le commutateur hermitianisé \(N\) est non nul exactement lorsque \(\alpha\gamma\lambda\mu \neq 0\) dans la famille déclarée. Les directions \(X_B/Y_B\) sont robustes sous toute projection \(B\)-bimodulaire ; les amplitudes ne le sont pas.

Aucune interprétation temporelle physique, aucun changement physique fini, aucun T1.

---

## 22. Ce que model0c ne teste pas

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
LOCAL_DIMENSION                 = CLOSED — cf. §4, (2, 2, 2)
STATE_FAMILY                    = CLOSED — cf. §5, THREE_QUBIT_NONCOLLINEAR_OVERLAP_RELATION_FAMILY
FAITHFUL_DOMAIN                 = CLOSED — cf. §6, |alpha|+|gamma|+sqrt(lambda^2+mu^2) < 1
SELECTION_RULE                  = CLOSED — cf. §8, TRACE_PRESERVING_CONDITIONAL_EXPECTATION
PRIMARY_GENERATOR_DEFINITION    = CLOSED — cf. §10
NONCOLLINEARITY_OPERATOR        = CLOSED — cf. §13

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

Le domaine analytique (§6) est `CLOSED` ; les valeurs de fixtures ne le sont pas.

---

## 24. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

---

## 25. Statut et prochaine étape

```text
MODEL0C_SPECIFICATION_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
