# toy0e — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0e`, construction candidate du toy `toy0e`.

Il transforme en contrat explicite la position scientifique d'un candidat de référence relationnelle discrète multi-modulaire. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy0e
MODEL_ID = model0e

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL0E_CLASS = T1_DISCRETE_MULTI_MODULAR_RELATIONAL_REFERENCE_QUALIFICATION_NONCONFIRMATORY
```

---

## 2. Position dans les tests CosmoTGG

```text
COSMOTGG_TEST_TARGET = T1_RELATIONAL_FLOW
```

Explicitement :

```text
MODEL0E_IS_T1_CONFIRMATORY_TEST            = NO
MODEL0E_PROVES_RELATIONAL_PHYSICAL_CHANGE  = NO
MODEL0E_PROVES_RELATIONAL_TIME             = NO

T1 = OPEN_NOT_EXECUTED
```

Cible scientifique de `model0e` :

```text
MODEL0E_TARGET = STATE_DERIVED_NONPRIVILEGED_DISCRETE_REFERENCE_AND_CONDITIONAL_LAW
```

Enregistré explicitement :

```text
MODEL0E != TIME_MODEL
RELATIONAL_REFERENCE_CANDIDATE != RELATIONAL_TIME
```

---

## 3. Référence normative opérationnelle

La référence normative opérationnelle de ce document est `docs/model/t1-relational-physical-change-criteria.md`.

`model0e` cible explicitement C1, C2, C3, C4A, C4B, C4C, C5, C6, C7. Ces critères sont :

```text
STATUS = NECESSARY_FOR_FUTURE_NONCONFIRMATORY_CANDIDATE
```

et non :

```text
T1_PASS_CRITERION
sufficient conditions
confirmatory protocol
```

---

## 4. Continuité avec model0a, model0b, model0c, model0d

`model0a` a établi, au niveau `QUALIFICATION_NONCONFIRMATORY`, la structure modulaire/porteuse (`docs/toy-models/toy0a/specification.md`).

`model0b` a établi, au même niveau, un générateur algébrique relatif (`docs/toy-models/toy0b/specification.md`).

`model0c` a établi, au même niveau, que deux structures modulaires projetées peuvent être non colinéaires (`docs/toy-models/toy0c/specification.md`).

`model0d` a établi, au même niveau, un transport fini sans paramètre entre paires d'états contextuels auxiliaires, mais sans processus physique (`docs/toy-models/toy0d/specification.md`).

`model0e` change de question. Il teste si une structure **multi-modulaire** peut dériver :

1. une référence relationnelle interne discrète ;
2. des états physiques conditionnels de sous-système ;
3. une loi unique surdéterminée reliant toutes les lectures ;
4. une seconde description de référence non privilégiée.

Ce document ne modifie aucun contenu scientifique de `docs/toy-models/toy0a/specification.md`, `docs/toy-models/toy0b/specification.md`, `docs/toy-models/toy0c/specification.md`, `docs/toy-models/toy0d/specification.md`, ni de leurs `implementation-design.md` respectifs.

---

## 5. Système

```text
H_A = C^3
H_B = C^3
H_C = C^2
H_D = C^2
```

Ordre tensoriel : \(A, B, C, D\).

Interprétation :

- \(A\) et \(B\) sont des sous-structures physiques qutrit ;
- \(C\) et \(D\) sont des sous-structures de contexte relationnel.

Aucun sous-système n'est :

```text
point spatial
horloge
variable de temps externe
```

---

## 6. Représentant canonique qutrit

Sur \(\mathcal H_A \otimes \mathcal H_B\) :

$$
|\Phi_3\rangle
=
\frac{|00\rangle + |11\rangle + |22\rangle}{\sqrt 3},
\qquad
P_\Phi = |\Phi_3\rangle\langle\Phi_3|,
\qquad
S_{AB} = 9\, P_\Phi - I_{AB}.
$$

Alors \(\|S_{AB}\| = 8\).

Sur le représentant qutrit canonique :

$$
N = \operatorname{diag}(-1,0,+1),
\qquad
|q_0\rangle = \frac{|0\rangle+|1\rangle+|2\rangle}{\sqrt3},
\qquad
Q = |q_0\rangle\langle q_0| - \frac{I}{3}.
$$

Propriétés :

$$
\operatorname{Tr} N = 0,
\qquad
\operatorname{Tr} Q = 0,
$$

$$
\operatorname{spec}(N) = \{-1,0,+1\},
\qquad
\operatorname{spec}(Q) = \{2/3,-1/3,-1/3\},
$$

$$
\|N\| = 1,
\qquad
\|Q\| = 2/3,
\qquad
[N,Q] \neq 0.
$$

Semence canonique :

$$
Q_A = Q,
\quad
Q_B = Q,
\qquad
N_A = N,
\quad
N_B = N.
$$

Ces matrices étant réelles :

$$
Q_A = Q_B^{\mathsf T},
\qquad
N_A = N_B^{\mathsf T}.
$$

**Important :** ces égalités définissent uniquement un représentant canonique. Toute revendication physique/modèle doit rester covariante sous transformation de base locale arbitraire (§13). Aucune revendication de base computationnelle préférée n'est faite.

---

## 7. Famille d'états globale

Sept paramètres réels : \(\eta, \gamma, \mu_A, \mu_B, \delta, \nu_A, \nu_B\).

$$
\rho_{ABCD}
=
\frac{1}{36}\Big[
I
+ \eta\, S_{AB}
+ \gamma\, Z_C
+ (\mu_A Q_A + \mu_B Q_B)\, Z_C
+ \delta\, Z_D
+ (\nu_A N_A + \nu_B N_B)\, Z_D
\Big].
$$

Convention Pauli : \(Z_C = \operatorname{diag}(1,-1)\) sur \(\mathcal H_C = \mathbb C^2\) et \(Z_D = \operatorname{diag}(1,-1)\) sur \(\mathcal H_D = \mathbb C^2\), au sens de la même convention de Pauli déjà utilisée par `docs/toy-models/toy0b/specification.md` et `docs/toy-models/toy0c/specification.md` (\(X_B, Y_B, Z_B\)). Les facteurs tensoriels omis sont des identités (même convention).

Développement tensoriel non ambigu :

$$
\rho_{ABCD}
=
\frac{1}{36}\Big[
I_A\!\otimes\! I_B\!\otimes\! I_C\!\otimes\! I_D
+ \eta\,(S_{AB}\!\otimes\! I_C\!\otimes\! I_D)
+ \gamma\,(I_A\!\otimes\! I_B\!\otimes\! Z_C\!\otimes\! I_D)
$$
$$
+ \mu_A\,(Q_A\!\otimes\! I_B\!\otimes\! Z_C\!\otimes\! I_D)
+ \mu_B\,(I_A\!\otimes\! Q_B\!\otimes\! Z_C\!\otimes\! I_D)
+ \delta\,(I_A\!\otimes\! I_B\!\otimes\! I_C\!\otimes\! Z_D)
$$
$$
+ \nu_A\,(N_A\!\otimes\! I_B\!\otimes\! I_C\!\otimes\! Z_D)
+ \nu_B\,(I_A\!\otimes\! N_B\!\otimes\! I_C\!\otimes\! Z_D)
\Big].
$$

Nom de la famille d'états :

```text
FOUR_PARTITE_DISCRETE_MULTIMODULAR_REFERENCE_FAMILY
```

La sous-famille précédemment auditée est la sous-famille symétrique :

$$
\mu_A = \mu_B,
\qquad
\nu_A = \nu_B.
$$

```text
SYMMETRIC_FEASIBILITY_SUBFAMILY = ANALYTICALLY_AND_COMPUTATIONALLY_AUDITED
```

L'extension amplitude-asymétrique n'est introduite que pour tester la non-privilège de référence et la robustesse d'amplitude (§21).

---

## 8. Domaine fidèle

Domaine suffisant, délibérément non serré, obtenu par l'inégalité triangulaire de norme d'opérateur :

$$
8|\eta|
+ |\gamma|
+ \frac23\big(|\mu_A|+|\mu_B|\big)
+ |\delta|
+ |\nu_A|+|\nu_B|
< 1.
$$

Aucune tentative n'est faite pour établir le domaine exact global de positivité.

Conditions de branche déclarées additionnelles :

$$
\eta > 0,
\qquad
\gamma \ge 0,
\qquad
\mu_A > 0,
\qquad
\mu_B > 0,
$$
$$
\delta > 0,
\qquad
0 < \nu_A < \delta,
\qquad
0 < \nu_B < \delta.
$$

Ces conditions assurent les branches spectrales visées (§11–§12).

```text
NO_TOLERANCE
NO_EPSILON
BOUNDARY_REJECTED
```

Le constructeur d'état devra ultérieurement échouer de façon fermée (`fail-closed`), sans tolérance.

---

## 9. Réductions

$$
\rho_{AB} = (1-\eta)\,\frac{I_{AB}}{9} + \eta\, |\Phi_3\rangle\langle\Phi_3|,
\qquad
\rho_A = \frac{I_A}{3},
\qquad
\rho_B = \frac{I_B}{3}.
$$

Pour \(X=A\) :

$$
\rho_{AC} = \frac16\Big[I_{AC} + \gamma Z_C + \mu_A Q_A Z_C\Big],
\qquad
\rho_{AD} = \frac16\Big[I_{AD} + \delta Z_D + \nu_A N_A Z_D\Big].
$$

Pour \(X=B\) :

$$
\rho_{BC} = \frac16\Big[I_{BC} + \gamma Z_C + \mu_B Q_B Z_C\Big],
\qquad
\rho_{BD} = \frac16\Big[I_{BD} + \delta Z_D + \nu_B N_B Z_D\Big].
$$

Tous les termes du côté opposé non désirés s'annulent exactement sous trace.

---

## 10. Contextes modulaires

Pour \(X \in \{A,B\}\) :

$$
K_{XC} = -\ln\rho_{XC},
\qquad
K_{XD} = -\ln\rho_{XD}.
$$

Espérance conditionnelle traciale établie sur \(X\) :

$$
E_X^C(Y) = \frac{\operatorname{Tr}_C(Y)}{2},
\qquad
E_X^D(Y) = \frac{\operatorname{Tr}_D(Y)}{2}.
$$

Définitions :

$$
H_Q^X = \operatorname{tl}\big(E_X^C(K_{XC})\big),
\qquad
H_N^X = \operatorname{tl}\big(E_X^D(K_{XD})\big).
$$

Noms :

```text
H_Q^X = PROJECTED_PHASE_FIXING_MODULAR_CONTEXT
H_N^X = PROJECTED_ORDERING_MODULAR_CONTEXT
```

Ces noms sont purement structurels. Interdit d'appeler :

```text
Q = phase du temps
N = hamiltonien d'horloge
```

---

## 11. Branche analytique Q

Pour une valeur propre \(q\) de \(Q_X\), on définit :

$$
a_q = \gamma + \mu_X q,
\qquad
h_Q(q) = \ln 6 - \frac12 \ln\big[1 - a_q^2\big].
$$

Valeurs propres de \(Q\) : \(q_+ = 2/3\), \(q_- = -1/3\).

$$
\Delta_Q^X = h_Q(2/3) - h_Q(-1/3)
= \frac12 \ln\!\left[
\frac{1-(\gamma - \mu_X/3)^2}{1-(\gamma + 2\mu_X/3)^2}
\right].
$$

Sous \(\gamma \ge 0\), \(\mu_X > 0\), sur le domaine fidèle : \(\Delta_Q^X > 0\).

Par conséquent :

$$
H_Q^X = \Delta_Q^X\, Q_X.
$$

Conséquence : le vecteur propre maximal unique de \(H_Q^X\) est \(|q_{0,X}\rangle\), à phase globale près.

Cette identité analytique doit devenir un oracle de test ultérieurement.

---

## 12. Branche analytique N

Pour \(n \in \{-1,0,+1\}\) :

$$
h_N^X(n) = \ln 6 - \frac12\ln\big[1-(\delta+\nu_X n)^2\big].
$$

Sous \(\delta > \nu_X > 0\) et fidélité :

$$
h_N^X(-1) < h_N^X(0) < h_N^X(+1).
$$

Donc \(H_N^X\) possède trois valeurs propres non dégénérées, avec projecteurs ordonnés \(P_0^X, P_1^X, P_2^X\) correspondant respectivement à \(n=-1,0,+1\).

Aucune revendication que \(H_N^X\) est proportionnel à \(N_X\). Seuls sa base propre et son ordre sont utilisés.

---

## 13. Commutant commun

Pour la paire qutrit déclarée :

$$
\operatorname{Comm}(\{H_N^X, H_Q^X\}) = \mathbb C I.
$$

```text
STATUS = STRUCTURAL_ANALYTIC_FOR_DECLARED_FAMILY
```

Mais préservé :

```text
TRIVIAL_COMMON_COMMUTANT_IS_SUFFICIENT_FOR_REFERENCE = NO
```

L'extraction de référence effective (§14) est indépendamment requise.

---

## 14. Extraction de référence

À partir de \(H_N^X\) :

1. diagonaliser ;
2. exiger trois valeurs propres non dégénérées ;
3. trier par ordre croissant ;
4. former les projecteurs spectraux ordonnés \(P_0, P_1, P_2\).

Définir l'opérateur de rang sans dimension :

$$
R_X = 0\,P_0 + 1\,P_1 + 2\,P_2.
$$

**Important :** les écarts numériques de \(H_N^X\) ne sont PAS utilisés.

$$
U_X = \exp\!\Big(-\frac{2\pi i}{3} R_X\Big)
= P_0 + e^{-2\pi i/3} P_1 + e^{-4\pi i/3} P_2.
$$

Aucun paramètre réel de flot.

À partir de \(H_Q^X\) : prendre son projecteur propre maximal unique \(E_0^X\). Ne pas dépendre d'une phase arbitraire de vecteur propre. L'extraction doit être formulée en priorité au niveau des projecteurs.

$$
E_k^X = U_X^k\, E_0^X\, U_X^{-k},
\qquad k = 0,1,2.
$$

Propriétés exactes requises :

$$
E_j E_k = \delta_{jk} E_k,
\qquad
\sum_k E_k = I_X,
\qquad
E_{k+1} = U_X E_k U_X^\dagger,
\qquad
U_X^3 = I_X.
$$

Objet de référence :

```text
DERIVED_Z3_RELATIONAL_REFERENCE_PVM
```

---

## 15. Portail de module égal

Dans la base propre de \(H_N\), l'état extrémal unique de \(H_Q\) doit satisfaire :

$$
|\langle n | q_0\rangle|^2 = \frac13
\quad \text{pour les trois } n.
$$

C'est ce qui fait de \(\{U^k E_0 U^{-k}\}\) une PVM orthogonale complète.

La production devra à terme valider ceci avec une tolérance numérique explicite.

```text
NO_SILENT_GRAM_SCHMIDT
NO_REPAIR
NO_REPLACEMENT_SEED
```

Si le portail échoue :

```text
REFERENCE_EXTRACTION = FAIL
```

Ceci constitue le contrôle de faux positif F3 (§25).

---

## 16. Étiquette relationnelle

L'étiquette physique est \(k \in \mathbb Z_3\), associée à un résultat de PVM physique dérivée.

```text
RELATIONAL_LABEL_SOURCE                = DERIVED_REFERENCE_PVM_OUTCOME
EXTERNAL_TIME                          = NONE
FREELY_CHOSEN_REAL_MODULAR_PARAMETER   = NONE
```

Mais : \(k\) N'EST PAS le temps physique.

Langage préféré : « lecture relationnelle \(k\) ».

---

## 17. Jauge d'étiquette de référence

Les étiquettes \(0,1,2\) ne sont pas elles-mêmes physiques.

Relabellisations affines \(\mathbb Z_3\) autorisées :

$$
k \to a + \varepsilon k \pmod 3,
\qquad a \in \mathbb Z_3,\ \varepsilon \in \{+1,-1\}.
$$

```text
REFERENCE_LABEL_GAUGE = AFFINE_Z3_RELABELLING
```

Un renversement \(k \to -k\) ne doit pas être interprété comme :

```text
temps physique renversé
renversement causal
renversement de flèche
```

Toute comparaison croisée de référence doit être formulée modulo cette jauge d'étiquette. Ceci résout explicitement la sensibilité d'orientation identifiée lors de l'audit de faisabilité.

---

## 18. Covariance de base locale

Pour un unitaire produit local arbitraire \(V_A \otimes V_B \otimes V_C \otimes V_D\), transformer l'état global et tout recalculer à partir de l'état transformé. Requis :

$$
H_Q^A \to V_A H_Q^A V_A^\dagger,
\qquad
H_N^A \to V_A H_N^A V_A^\dagger,
$$
$$
H_Q^B \to V_B H_Q^B V_B^\dagger,
\qquad
H_N^B \to V_B H_N^B V_B^\dagger,
$$
$$
E_k^A \to V_A E_k^A V_A^\dagger,
\qquad
E_k^B \to V_B E_k^B V_B^\dagger,
$$

à la jauge d'étiquette \(\mathbb Z_3\) affine autorisée près (§17). Aucune dépendance de base canonique. Aucune revendication de refactorisation globale.

---

## 19. États conditionnels physiques

En utilisant l'état physique \(\rho_{AB}\) et la PVM de référence dérivée de \(B\) :

$$
p_B(k) = \operatorname{Tr}\big[(I_A \otimes E_k^B)\,\rho_{AB}\big],
$$
$$
\rho_{A|k} = \frac{\operatorname{Tr}_B\big[(I_A \otimes E_k^B)\,\rho_{AB}\big]}{p_B(k)}.
$$

Ce sont des :

```text
ACTUAL_PHYSICAL_CONDITIONAL_STATES_OF_A
```

et non des états auxiliaires reconstruits.

Oracle exact dans le représentant canonique :

$$
p_B(k) = \frac13,
\qquad
\rho_{A|k} = (1-\eta)\,\frac{I_A}{3} + \eta\,(E_k^B)^{\mathsf T}.
$$

Valeurs propres :

$$
\frac{1+2\eta}{3},\qquad \frac{1-\eta}{3},\qquad \frac{1-\eta}{3}.
$$

Sous le domaine déclaré \(\eta>0\) : fidèles, distinctes pour \(k\) différents.

Ceci constitue l'avancée centrale de C1 par rapport à `model0d`.

---

## 20. C3 — non-trivialité observable

Exiger des statistiques physiques explicites. En utilisant la PVM de référence dérivée indépendamment de \(A\), \(\{E_j^A\}\) :

$$
p_A(j \mid k_B) = \operatorname{Tr}\big[E_j^A\, \rho_{A|k}\big].
$$

Au moins un \(j\) doit satisfaire :

$$
p_A(j \mid k_1) \neq p_A(j \mid k_2)
\qquad \text{pour } k_1 \neq k_2
$$

lorsque \(\eta \neq 0\). C3 ne doit pas être inféré uniquement d'une inégalité matricielle.

---

## 21. Carte de corrélation depuis \(\rho_{AB}\)

Pour \(\eta > 0\) : \(\rho_{AB}\) admet un unique vecteur propre maximal \(|\Psi_{AB}\rangle\). Pour la famille déclarée, ce vecteur est \(|\Phi_3\rangle\) à phase près.

Reformer ses coefficients en \(\Psi_{\text{matrix}}\) :

$$
M_{AB} = \sqrt3\, \Psi_{\text{matrix}}.
$$

Pour un vecteur maximalement intriqué : \(M_{AB}\) est unitaire, à tolérance numérique près.

Ceci définit le transfert de corrélation anti-linéaire :

$$
J_{AB}(b) = M_{AB}\, b^*.
$$

Ne pas exposer \(J\) comme une opération de « renversement du temps ». C'est une carte de corrélation entre les deux facteurs qutrit.

---

## 22. Loi fixe dérivée

Transférer l'unitaire de cycle de référence de \(B\) vers \(A\) :

$$
V_A = M_{AB}\, U_B^*\, M_{AB}^\dagger.
$$

Oracle en base canonique uniquement : \(V_A = U_B^*\).

La production doit dériver \(V_A\) à partir de \(\rho_{AB}\) et \(U_B\), sans transposition/conjugaison codée en dur.

Requis : \(V_A^3 = I\), à phase globale non pertinente près.

Pour tout \(k\) :

$$
\rho_{A|(k+1)} = V_A\, \rho_{A|k}\, V_A^\dagger.
$$

Plus généralement :

$$
\Lambda_{(k_2 \leftarrow k_1)}(X) = V_A^{\Delta k}\, X\, V_A^{-\Delta k},
\qquad
\Delta k = k_2 - k_1 \pmod 3.
$$

\(\Lambda\) est unitaire, CPTP, indépendant de la cible une fois \(V_A\) dérivé. Aucun état cible fourni indépendamment.

```text
NUMBER_OF_INDEPENDENT_TARGET_STATE_INPUTS = ZERO
```

Ceci constitue C4B.

---

## 23. Contenu prédictif

Distinction explicite avec `model0d` : dans `model0d`, \(F_{X \to Y} = g(Y) g(X)^{-1}\) est reconstruit depuis les deux extrémités.

Candidat `model0e` : dériver \(V_A\) une seule fois, puis :

$$
\rho_{A|0} \to \text{prédire } \rho_{A|1} \to \text{prédire } \rho_{A|2}.
$$

Les états cibles \(k=1\) et \(k=2\) ne sont PAS des entrées de \(\Lambda\).

```text
INDEPENDENT_PREDICTIVE_CONTENT = PRESENT_AT_THREE_READING_LEVEL
```

Cette revendication reste bornée à la famille déclarée.

---

## 24. C4A — covariance de référence

Les lectures de PVM obéissent à une loi unique :

$$
E_{(k+1)}^B = U_B\, E_k^B\, U_B^\dagger.
$$

Les états conditionnels physiques obéissent à une loi unique :

$$
\rho_{A|(k+1)} = V_A\, \rho_{A|k}\, V_A^\dagger.
$$

Ni \(U_B\) ni \(V_A\) n'est ajusté séparément pour chaque \(k\).

```text
C4A_CANDIDATE_STATUS = REFERENCE_COVARIANCE_CANDIDATE
```

---

## 25. C4C — cohérence à deux lectures

Pour au moins \(k_1 \neq k_2\) et une PVM/observable physique de sonde sur \(A\), dérivée ou déclarée indépendamment de l'état cible :

Direct :

$$
p_{\text{direct}}(j \mid k_2) = \operatorname{Tr}\big[M_j\, \rho_{A|k_2}\big].
$$

Prédit par la loi :

$$
p_{\text{law}}(j \mid k_2; k_1) = \operatorname{Tr}\big[M_j\, \Lambda_{(k_2 \leftarrow k_1)}(\rho_{A|k_1})\big].
$$

Exiger \(p_{\text{law}} = p_{\text{direct}}\) pour tous les résultats de sonde \(j\), ainsi que positivité et normalisation.

Statut autorisé si ceci passe :

```text
C4C = PASS_CANDIDATE_STATE_LAW_LEVEL
```

Limitation explicite :

```text
SEQUENTIAL_REFERENCE_INSTRUMENT = NOT_DEFINED
```

Donc la qualification candidate C4C n'est pas une démonstration de séquence temporelle. Aucun instrument séquentiel n'a besoin d'être construit dans `toy0e`.

---

## 26. C5 — admissibilité physique

Les états conditionnels physiques sont des matrices densité normalisées. \(\Lambda\) est un canal unitaire.

```text
PHYSICAL_ADMISSIBILITY = PASS_CANDIDATE
```

Mais explicitement : le caractère CPTP de \(\Lambda\) N'EST PAS en soi une évidence de changement. Sa pertinence vient de sa dérivation depuis l'état relationnel, d'une loi unique, de la prédiction indépendante de la cible, et de la cohérence avec les états conditionnels directs.

---

## 27. C6 — pare-feu de reparamétrisation

Aucun réel arbitraire \(s\), \(t\), \(\tau\) ne fait partie des prédictions finales.

Le facteur fixe \(2\pi/3\) provient uniquement de la dimension cyclique de référence à trois lectures. Ce n'est pas une durée de flot ajustée.

Les prédictions finales dépendent de \(k \in \mathbb Z_3\) en tant que résultat relationnel dérivé.

```text
C6_DOES_NOT_MEAN_NO_RELATIONAL_LABEL = TRUE
```

---

## 28. Seconde référence

Dériver indépendamment, depuis AC/AD : \(H_Q^A\), \(H_N^A\), \(U_A\), \(\{E_j^A\}\).

Ne pas obtenir la référence de \(A\) en transportant la référence de \(B\). Seulement APRÈS extraction indépendante, comparer avec le transfert de corrélation impliqué par \(\rho_{AB}\).

Ceci est obligatoire pour C7.

---

## 29. Changement de référence

En utilisant \(\rho_{AB}\) :

$$
p(j_A, k_B) = \operatorname{Tr}\big[(E_j^A \otimes E_k^B)\, \rho_{AB}\big].
$$

Structure exacte de la famille canonique :

$$
p(j,k) = \frac{1-\eta}{9} + \frac{\eta}{3}\,\operatorname{Tr}\big[E_j^A\,(E_k^B)^{\mathsf T}\big].
$$

Lorsque les références dérivées indépendamment coïncident via la carte de corrélation AB, leur matrice de recouvrement doit être une permutation :

$$
\operatorname{Tr}\big[E_j^A\, J_{AB}(E_k^B)\big] \in \{0,1\},
$$

avec une entrée unité par ligne/colonne. Extraire la carte d'étiquette :

$$
\pi : \mathbb Z_{3,B} \to \mathbb Z_{3,A}.
$$

Exiger que \(\pi\) soit une relabellisation affine \(\mathbb Z_3\) :

$$
\pi(k) = a + \varepsilon k \pmod 3.
$$

Ne pas exiger l'égalité exacte des étiquettes. Ceci constitue la règle explicite de changement de référence.

---

## 30. C7 — non-privilège de référence

Le candidat C7 requiert :

1. référence de \(B\) dérivée indépendamment depuis BC/BD ;
2. référence de \(A\) dérivée indépendamment depuis AC/AD ;
3. relation entre les deux dérivée depuis \(\rho_{AB}\) ;
4. probabilités conjointes physiques communes compatibles sous les deux directions de conditionnement ;
5. conditionnelles réciproques normalisées ;
6. seule l'ambiguïté de relabellisation affine \(\mathbb Z_3\) subsiste.

Alors :

```text
REFERENCE_NONPRIVILEGE = PASS_CANDIDATE_FOR_DECLARED_FAMILY
```

Reste interdit : « aucune référence n'est fondamentalement privilégiée en général ». La revendication n'est faite que pour la famille candidate déclarée.

---

## 31. Contrôle d'asymétrie d'amplitude A/B

Contrôle de sensibilité obligatoire : choisir \(\mu_A \neq \mu_B\), \(\nu_A \neq \nu_B\), en respectant les conditions de signe/domaine (§8).

Vérifier que l'amplitude de \(H_Q^A\) diffère génériquement de celle de \(H_Q^B\), et que le spectre de \(H_N^A\) diffère génériquement de celui de \(H_N^B\), mais que les PVM de référence extraites indépendamment restent compatibles par corrélation.

But : C7 ne doit pas passer uniquement parce que les amplitudes de contexte ont été rendues égales par construction.

Statut recherché :

```text
REFERENCE_STRUCTURE_ROBUST_TO_A_B_AMPLITUDE_ASYMMETRY = YES_FOR_DECLARED_FAMILY
```

Aucune revendication au-delà de l'asymétrie d'amplitude.

---

## 32. Sensibilité de projection pondérée

Règle officielle : espérance conditionnelle traciale (§10).

Règle de sensibilité : pour la projection de XC sur X, utiliser une trace pondérée par la marginale sur C :

$$
E_{\text{weighted},X}^C(K) = \operatorname{Tr}_C\big[(I_X \otimes \rho_C)\, K\big].
$$

Pour XD :

$$
E_{\text{weighted},X}^D(K) = \operatorname{Tr}_D\big[(I_X \otimes \rho_D)\, K\big].
$$

Vérifier uniquement : les projecteurs propres de \(H_Q\) inchangés, les projecteurs propres/ordre de \(H_N\) inchangés, la PVM de référence extraite inchangée sur la famille déclarée. Les amplitudes peuvent changer.

Résultat borné recherché :

```text
REFERENCE_STRUCTURE_ROBUST_TO_WEIGHTED_PROJECTION = YES_FOR_DECLARED_FAMILY
ROBUST_MODULAR_AMPLITUDE                           = NO
```

Aucune définition officielle alternative.

---

## 33. Contrôles de faux positifs

**F0 — absence de contenu de changement physique** : \(\eta = 0\). Les contextes de référence peuvent toujours exister, mais \(\rho_{A|k} = I/3\) pour tout \(k\). Attendu : `C3 = FAIL`.

**F1 — absence de contexte de fixation de phase** : \(\mu_X = 0\) sur le côté testé. \(H_Q^X\) ne peut alors pas fournir la semence de référence unique de fixation de phase déclarée sous le contrat du modèle. Attendu : `REFERENCE_EXTRACTION = FAIL`. Aucun remplacement arbitraire de semence.

**F2 — absence de contexte d'ordre** : \(\nu_X = 0\). \(H_N\) n'a alors pas de spectre de référence ordonné non dégénéré déclaré. Attendu : `REFERENCE_EXTRACTION = FAIL`.

**F3 — semence de module inégal** : perturbation test-only construisant un état extrémal unique de \(H_Q\) dont les amplitudes au carré dans la base de \(H_N\) ne sont pas \(1/3, 1/3, 1/3\). Attendu : `Z3_PVM_GATE = FAIL`. Aucun Gram-Schmidt ni réparation.

**F4 — trois états conditionnels arbitraires** : fournir, test-only, trois états qutrit fidèles ne se situant pas sur une orbite unitaire \(\mathbb Z_3\) dérivée commune. Attendu : `FIXED_LAW_OVERDETERMINATION = FAIL`. Ceci constitue le contrôle de faux positif principal du steering statique.

**F5 — rupture de la covariance de corrélation AB** : perturber \(\rho_{AB}\) par un terme hermitien de trace nulle, explicitement déclaré, préservant la validité de matrice densité mais brisant l'orbite \(V_A\) dérivée. Attendu : les états conditionnels directs peuvent rester distincts, tandis que `FIXED_LAW = FAIL` ou `REFERENCE_CHANGE_COMPATIBILITY = FAIL`. Ceci démontre : `STATIC_CONDITIONAL_VARIATION != RELATIONAL_LAW`.

**F6 — relabellisation d'étiquette** : appliquer une relabellisation affine \(\mathbb Z_3\) autorisée. Attendu : toutes les probabilités physiques inchangées après la transformation d'étiquette de référence correspondante. But : l'étiquette/l'origine zéro n'est pas physique.

---

## 34. Fixtures non normatives

Fixture primaire de faisabilité symétrique :

```text
eta   = 0.02
gamma = 0.10

mu_A = 0.10
mu_B = 0.10

delta = 0.20

nu_A = 0.05
nu_B = 0.05
```

Vérification :

$$
8\eta + \gamma + \frac23(\mu_A+\mu_B) + \delta + \nu_A + \nu_B < 1.
$$

Fixture de sensibilité amplitude-asymétrique :

```text
eta   = 0.02
gamma = 0.10

mu_A = 0.08
mu_B = 0.12

delta = 0.20

nu_A = 0.04
nu_B = 0.06
```

```text
NON_NORMATIVE_QUALIFICATION_FIXTURE
```

Aucun paramètre n'est fermé par ces fixtures.

---

## 35. Claim maximal autorisé

Formulation maximale autorisée :

> Dans la famille finie de type I \((3,3,2,2)\) déclarée, deux contextes modulaires non commutants dérivés indépendamment sur chaque qutrit physique peuvent déterminer une PVM de référence cyclique à trois résultats. Conditionner l'état physique AB sur une référence produit trois états conditionnels physiques réels du sous-système opposé. Une loi unitaire unique, dérivée de la même corrélation AB et du cycle de référence, prédit la famille complète à trois lectures, sans fournir indépendamment les états cibles. Le sous-système opposé admet une référence dérivée indépendamment, compatible avec la première à relabellisation affine \(\mathbb Z_3\) près. Ceci constitue un candidat satisfaisant les portails opérationnels nécessaires C1–C7 au niveau de la qualification.

Ceci n'établit PAS :

```text
physical time
continuous time
proper time
temporal duration
temporal arrow
causal order
sequential measurement history
physical relational change as accepted fact
T1 PASS
geometry
gravity
```

---

## 36. Pare-feu T1

```text
RELATIONAL_REFERENCE       = CANDIDATE_ONLY
RELATIONAL_PHYSICAL_CHANGE = CANDIDATE_NOT_ESTABLISHED
RELATIONAL_TIME            = NOT_ESTABLISHED

T1_NONTRIVIALITY_CRITERION = OPEN
CONFIRMATORY_PROTOCOL      = NOT_DEFINED

T1 = OPEN_NOT_EXECUTED
```

---

## 37. Ce que model0e ne teste pas

Sont exclus :

```text
physical time
continuous time
proper time
temporal duration
temporal arrow
causal order
sequential measurement history
Page-Wootters implementation
QRF implementation
HSMI
curvature
holonomy
CPTP dynamics beyond the declared unitary law
star-automorphism dynamics beyond the declared unitary law
T1 PASS
T2+
geometry
gravity
```

---

## 38. Paramètres qui restent `OPEN`

```text
SYSTEM_DECLARATION                              = CLOSED — cf. §5
CANONICAL_REPRESENTATIVE                        = CLOSED — cf. §6
STATE_FAMILY_DEFINITION                         = CLOSED — cf. §7
SUFFICIENT_FAITHFUL_DOMAIN                      = CLOSED — cf. §8
REDUCTIONS                                       = CLOSED — cf. §9
MODULAR_CONTEXT_DEFINITION                       = CLOSED — cf. §10
Q_BRANCH_ANALYTIC_STRUCTURE                      = CLOSED — cf. §11
N_BRANCH_ANALYTIC_STRUCTURE                      = CLOSED — cf. §12
REFERENCE_EXTRACTION_PROCEDURE                   = CLOSED — cf. §14
REFERENCE_LABEL_GAUGE                            = CLOSED — cf. §17
PHYSICAL_CONDITIONAL_STATE_DEFINITION            = CLOSED — cf. §19
CORRELATION_MAP_DEFINITION                       = CLOSED — cf. §21
FIXED_LAW_DEFINITION                             = CLOSED — cf. §22
REFERENCE_CHANGE_RULE                            = CLOSED — cf. §29

MODEL0E_QUALIFICATION_FIXTURES     = OPEN / NON_NORMATIVE_AT_IMPLEMENTATION
NUMERICAL_TOLERANCES               = OPEN
REFERENCE_SPECTRAL_TOLERANCE       = OPEN
REFERENCE_EQUAL_MODULUS_TOLERANCE  = OPEN
MODEL0E_ACCEPTANCE_CRITERION       = OPEN
T1_NONTRIVIALITY_CRITERION         = OPEN
CONFIRMATORY_PROTOCOL              = NOT_DEFINED
```

Aucune valeur n'est fermée par cette spécification.

---

## 39. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

Guides de littérature applicables déjà enregistrés par `docs/model/t1-relational-physical-change-criteria.md` §10 (`PAGE_WOOTTERS = PRIMARY_GUIDE`, `ROVELLI_COMPLETE_OBSERVABLES = USEFUL_CRITERIAL_GUIDE`).

---

## 40. Statut et prochaine étape

```text
MODEL0E_SPECIFICATION_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
