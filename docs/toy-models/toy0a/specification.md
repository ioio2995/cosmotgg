# toy0a — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0a`, première construction candidate du toy `toy0a`.

Il intègre des décisions scientifiques déjà arbitrées par ChatGPT (revue physique bornée `MODEL0A_T1_BOUNDARY_REVIEW = PASS_WITH_CHATGPT_CORRECTIONS` ; fermeture de `LOCAL_DIMENSION` et de `STATE_FAMILY` au lot `MODEL0A-DESIGN-1` ; structure analytique de qualification du cocycle au lot `MODEL0A-DIAGNOSTICS-DESIGN-1`). Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique de paramètre d'état, aucun domaine de paramètre modulaire, aucune norme ni seuil scalaire.

---

## 1. Identification

```text
TOY_ID   = toy0a
MODEL_ID = model0a

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL0A_CLASS   = QUALIFICATION_NONCONFIRMATORY
MODEL0A_PURPOSE = qualifier une construction modulaire relationnelle candidate
                  pour la future opérationnalisation de T1
```

Explicitement :

```text
MODEL0A_IS_T1_CONFIRMATORY_TEST      = NO
MODEL0A_PROVES_RELATIONAL_TIME       = NO
MODULAR_PARAMETER_IS_PHYSICAL_TIME   = NO
```

`model0a` ne constitue ni une exécution de T1, ni une preuve d'existence d'un temps relationnel, ni une identification du paramètre modulaire au temps physique (cf. `docs/model/hypothesis.md` §7, `MODULAR_PARAMETER ≠ PHYSICAL_TIME`).

---

## 2. Cadre déjà fixé

Le toy reste :

```text
finite-dimensional
type I
```

avec une décomposition tensorielle finie :

$$
\mathcal H = \mathcal H_A \otimes \mathcal H_B .
$$

La dimension locale est fixée :

```text
LOCAL_DIMENSION = (2, 2)
```

Sens :

$$
\mathcal H_A = \mathbb C^2,
\qquad
\mathcal H_B = \mathbb C^2,
\qquad
\mathcal H_{AB} = \mathbb C^4.
$$

Justification : une dimension locale 1 implique un état nécessairement produit relativement à ce facteur et ne permet donc pas les régimes N1/N2 (§8) ; \(2\times2\) est le cadre minimal suffisant pour réaliser les trois régimes. Cette dimension n'est pas présentée comme fondamentale ; elle est un choix de banc d'essai minimal pour `toy0a`.

Les états utilisés pour la construction modulaire doivent être **fidèles** lorsqu'un logarithme matriciel ordinaire est requis, conformément au domaine de travail fixé par `docs/model/hypothesis.md` §4–5 (\(\rho_X>0\)).

---

## 3. Famille d'états candidate

```text
STATE_FAMILY = TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY
```

Dans la base \(|00\rangle,|01\rangle,|10\rangle,|11\rangle\), on définit :

$$
\rho_{AB}(a,b,c,\eta)
=
\begin{pmatrix}
ab+c & 0 & 0 & \eta \\
0 & a(1-b)-c & 0 & 0 \\
0 & 0 & (1-a)b-c & 0 \\
\eta & 0 & 0 & (1-a)(1-b)+c
\end{pmatrix}
$$

avec paramètres réels \(a,b,c,\eta\).

### 3.1 Marginales exactes

Les identités analytiques suivantes sont enregistrées :

$$
\rho_A = \operatorname{diag}(a,\,1-a),
\qquad
\rho_B = \operatorname{diag}(b,\,1-b),
$$

indépendamment de \(c\) et de \(\eta\). Donc :

$$
\sigma_{AB} = \rho_A \otimes \rho_B
=
\operatorname{diag}\!\big(ab,\ a(1-b),\ (1-a)b,\ (1-a)(1-b)\big).
$$

À \(a,b\) fixés, \(\sigma_{AB}\) est fixe lorsque \(c\) et \(\eta\) sont modifiés.

```text
DESIGN_RATIONALE = isoler les modifications de la structure de corrélation
                    sans faire varier simultanément les marginales
```

### 3.2 Domaine fidèle

Le domaine analytique suivant est normatif :

$$
0 < a < 1,
\qquad
0 < b < 1,
$$

$$
-\min\big(ab,\ (1-a)(1-b)\big)
<
c
<
\min\big(a(1-b),\ (1-a)b\big),
$$

$$
\eta^2
<
\big(ab+c\big)\big((1-a)(1-b)+c\big).
$$

Ces inégalités sont strictes ; elles définissent un \(\rho_{AB}\) strictement positif. Aucune tolérance numérique n'intervient dans cette définition et aucune correction d'entrée n'est autorisée : la définition analytique du domaine est la source normative du domaine scientifique. Des tolérances numériques pourront être introduites par un futur protocole d'implémentation ou de validation, mais elles ne redéfinissent pas ce domaine analytique.

### 3.3 Régimes canoniques

Les tranches suivantes sont les constructions canoniques retenues pour produire les trois régimes (§8) dans `toy0a`.

**N0 :** \(c=0\), \(\eta=0\) donne exactement :

$$
\rho_{AB} = \rho_A \otimes \rho_B.
$$

**N1 — tranche canonique :** \(c\neq0\), \(\eta=0\) donne :

$$
\rho_{AB} \neq \rho_A \otimes \rho_B,
\qquad
[\rho_{AB},\sigma_{AB}] = 0.
$$

Ce régime reste `COMMUTING_CORRELATED_REGIME` (N1, §8) et n'est pas un `FAIL` de T1.

**N2 — tranche canonique :** \(\eta\neq0\) et \(a+b\neq1\), car exactement :

$$
[\rho_{AB},\sigma_{AB}]_{(00,11)} = \eta\,(1-a-b),
$$

l'élément conjugué portant le signe opposé. Donc :

$$
[\rho_{AB},\sigma_{AB}] \neq 0.
$$

Ce régime reste `NONCOMMUTING_CORRELATED_REGIME` (N2, §8) et n'est pas un `PASS` de T1.

**Important :** la classification conceptuelle N0/N1/N2 de §8 reste définie par les propriétés des états. Les tranches ci-dessus sont les constructions canoniques retenues pour produire les trois régimes dans `toy0a`, et non une redéfinition de cette classification.

---

## 4. Paire relationnelle canonique

À partir d'un état fidèle \(\rho_{AB}\) sur \(\mathcal H_A\otimes\mathcal H_B\), on construit :

$$
\rho_A = \operatorname{Tr}_B(\rho_{AB}),
\qquad
\rho_B = \operatorname{Tr}_A(\rho_{AB}),
$$

puis :

$$
\sigma_{AB} = \rho_A \otimes \rho_B .
$$

La paire primaire de `toy0a` est :

$$
(\rho_{AB},\ \sigma_{AB}).
$$

Les deux états agissent donc sur la même algèbre :

$$
\mathcal B(\mathcal H_A \otimes \mathcal H_B).
$$

Aucun cocycle direct entre \(K_A\) et \(K_B\) n'est défini.

---

## 5. Objet mathématique candidat

Convention CosmoTGG (cf. `docs/model/hypothesis.md` §4) :

$$
K = -\ln(\rho).
$$

On définit le cocycle fini :

$$
v_s(\rho,\sigma) = \rho^{-is}\,\sigma^{+is},
$$

qui correspond au cocycle de Connes usuel au paramètre \(-s\) dans la convention Tomita–Takesaki standard.

Pour la paire primaire :

$$
v_s^{AB}
=
\rho_{AB}^{-is}\,
(\rho_A\otimes\rho_B)^{+is}.
$$

---

## 6. Raccord à \(\mathcal R_{AB}\)

La science gelée (`docs/model/hypothesis.md` §5) définit :

$$
\mathcal R_{AB} = \ln(\rho_{AB}) - \ln(\rho_A \otimes \rho_B).
$$

La présente spécification enregistre l'identité exacte :

$$
\left.\frac{d}{ds} v_s^{AB}\right|_{s=0}
=
-i\,\mathcal R_{AB}.
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Cette identité n'établit pas que \(\mathcal R_{AB}\) est l'opérateur modulaire relatif général au sens de Tomita–Takesaki/Araki. Elle n'établit pas non plus que le cocycle constitue un nouvel observable physique.

---

## 7. Identités structurelles

Les propriétés analytiques suivantes sont documentées pour un usage ultérieur comme oracles :

$$
v_0 = I,
$$

\(v_s\) est unitaire,

$$
v_s^{(\rho,\sigma)}\,
\sigma_s^{\sigma}(O)\,
v_s^{(\rho,\sigma)\dagger}
=
\sigma_s^{\rho}(O),
$$

avec la convention CosmoTGG correspondante (§5, flot \(O(s)=e^{+iKs}Oe^{-iKs}\)).

Relation de cocycle :

$$
v_{s+s'} = v_s\,\sigma_s^{\sigma}(v_{s'}).
$$

Chain rule pour trois états fidèles sur **une même algèbre** :

$$
v_s^{(\rho,\sigma)}\, v_s^{(\sigma,\omega)} = v_s^{(\rho,\omega)}.
$$

Inverse :

$$
v_s^{(\sigma,\rho)} = v_s^{(\rho,\sigma)\dagger}.
$$

---

## 8. Régimes algébriques

Sont définies uniquement les classifications neutres suivantes.

### N0 = `PRODUCT_TRIVIAL_REGIME`

$$
\rho_{AB} = \rho_A \otimes \rho_B
$$

alors :

$$
v_s = I \ \ \forall s,
\qquad
\mathcal R_{AB} = 0,
\qquad
I(A:B) = 0.
$$

### N1 = `COMMUTING_CORRELATED_REGIME`

$$
\rho_{AB} \neq \rho_A \otimes \rho_B
$$

et :

$$
[\rho_{AB},\ \rho_A\otimes\rho_B] = 0,
$$

alors :

$$
v_s = \exp(-is\,\mathcal R_{AB}).
$$

**Important :**

- N1 n'est pas déclaré « absence de changement relationnel ».
- N1 n'est pas un `FAIL` de T1.
- Le statut physique de ce régime reste `OPEN`.

### N2 = `NONCOMMUTING_CORRELATED_REGIME`

$$
[\rho_{AB},\ \rho_A\otimes\rho_B] \neq 0,
$$

alors le cocycle n'est pas identiquement réductible à \(\exp(-is\,\mathcal R_{AB})\) sur tout le flot.

**Important :**

- N2 n'est pas déclaré « temps relationnel ».
- La non-commutativité n'est pas promue en condition nécessaire ou suffisante de T1.

---

## 9. Structure analytique de qualification du cocycle

Cette section enregistre la structure analytique retenue par ChatGPT (lot `MODEL0A-DIAGNOSTICS-DESIGN-1`) pour qualifier le cocycle au-delà de son seul tangent \(\mathcal R_{AB}\). Elle ne définit ni temps physique, ni critère d'acceptation de T1, ni seuil numérique.

### 9.1 Notations

Pour la paire primaire \(\rho=\rho_{AB}\), \(\sigma=\sigma_{AB}=\rho_A\otimes\rho_B\), on pose dans cette section :

$$
A=\ln(\rho),
\qquad
B=\ln(\sigma),
$$

et l'on rappelle (§6) :

$$
\mathcal R_{AB} = A - B.
$$

Le cocycle reste :

$$
v_s = \exp(-isA)\exp(+isB).
$$

### 9.2 Premier ordre

Identité déjà enregistrée (§6) :

$$
v_0 = I,
\qquad
\left.\frac{d}{ds}v_s\right|_{s=0} = -i\,\mathcal R_{AB}.
$$

### 9.3 Second ordre

Identité analytique :

$$
v_s
=
I
- is\,\mathcal R_{AB}
+ \frac{s^2}{2}\big([A,B] - \mathcal R_{AB}^2\big)
+ O(s^3),
$$

avec \(A=\ln(\rho)\), \(B=\ln(\sigma)\).

```text
STATUS = STRUCTURAL_ANALYTIC
```

Aucune interprétation temporelle physique n'est attribuée à ce développement.

### 9.4 Obstruction de non-commutativité — `LOG_COMMUTATOR_OBSTRUCTION`

Diagnostic matriciel :

$$
C_{AB} = [\ln(\rho),\ln(\sigma)] = \ln(\rho)\ln(\sigma) - \ln(\sigma)\ln(\rho).
$$

`C_AB` n'est appelé ni courbure (`curvature`), ni générateur temporel (`time generator`), ni générateur causal (`causal generator`), ni gravité (`gravity`).

Équivalence enregistrée pour des états fidèles :

$$
C_{AB} = 0 \iff [\rho,\sigma] = 0.
$$

Justification : le logarithme est une fonction spectrale injective sur les matrices strictement positives ; si \(\rho\) et \(\sigma\) commutent, leurs logarithmes commutent ; si leurs logarithmes commutent, leurs exponentielles \(\rho\) et \(\sigma\) commutent.

### 9.5 Défaut de groupe ordinaire — `ORDINARY_GROUP_DEFECT`

$$
G(s_1,s_2) = v_{s_1+s_2} - v_{s_1}v_{s_2}.
$$

**Important :** le cocycle de Connes satisfait sa propre identité de cocycle (§7). `G` mesure uniquement son défaut à être un groupe unitaire ordinaire sous multiplication directe. `G` n'est jamais appelé « cocycle defect » sans cette qualification, car le cocycle lui-même n'est pas défectueux.

### 9.6 Identité locale

$$
\left.\frac{\partial^2 G}{\partial s_1\,\partial s_2}\right|_{(0,0)}
=
[\ln(\rho),\ln(\sigma)]
=
C_{AB}.
$$

```text
STATUS = STRUCTURAL_ANALYTIC
```

Cette identité relie l'obstruction statique \(C_{AB}\) à la première obstruction locale à la propriété de groupe ordinaire du cocycle.

### 9.7 Table normative de qualification N0 / N1 / N2

**N0 = `PRODUCT_TRIVIAL_REGIME`** : \(\rho=\sigma\).

$$
I(A:B)=0,\quad \mathcal R_{AB}=0,\quad C_{AB}=0,\quad v_s=I,\quad G(s_1,s_2)=0\ \ \forall s_1,s_2.
$$

**N1 = `COMMUTING_CORRELATED_REGIME`** : \(\rho\neq\sigma\), \([\rho,\sigma]=0\).

$$
I(A:B)>0,\quad \mathcal R_{AB}\neq0,\quad C_{AB}=0,\quad v_s=\exp(-is\,\mathcal R_{AB}),\quad G(s_1,s_2)=0\ \ \forall s_1,s_2.
$$

**Important :** N1 \(\neq\) `T1_FAIL`.

**N2 = `NONCOMMUTING_CORRELATED_REGIME`** : \([\rho,\sigma]\neq0\).

$$
I(A:B)>0,\quad \mathcal R_{AB}\neq0,\quad C_{AB}\neq0,
$$

\(v_s\) n'est pas identiquement \(\exp(-is\,\mathcal R_{AB})\), et \(G(s_1,s_2)\) n'est pas identiquement nul.

**Important :** il n'est pas affirmé que \(G(s_1,s_2)\neq0\) pour toute paire particulière \((s_1,s_2)\) ; il peut exister des zéros accidentels. La propriété structurale porte sur `NOT_IDENTICALLY_ZERO`. Et N2 \(\neq\) `T1_PASS`.

### 9.8 Interprétation autorisée

La structure ci-dessus permet de distinguer :

- la corrélation (\(I(A:B)\)) ;
- la commutativité/non-commutativité modulaire (\(C_{AB}\)) ;
- la structure de groupe ordinaire ou non ordinaire du cocycle (\(G\)).

Elle permet de tester si le cocycle contient une structure d'ordre supérieur à son seul tangent \(\mathcal R_{AB}\).

Formulation maximale autorisée :

> « Le cocycle fournit une organisation paramétrique calculable dont la structure au-delà du premier ordre distingue le régime commutant du régime non commutant. »

Ne sont pas écrits : `emergent time`, `time flow established`, `arrow of time`, `causal order`.

### 9.9 Statut de l'information

```text
COCYCLE_ADDS_NEW_INFORMATION_BEYOND_FULL_PAIR = NO
```

car \(v_s\) est entièrement déterminé par \((\rho,\sigma)\).

```text
COCYCLE_ADDS_STRUCTURE_BEYOND_FIRST_ORDER_R_AB = YES
```

au sens où son développement au-delà du tangent dépend notamment de \([\ln(\rho),\ln(\sigma)]\). Cette distinction n'est pas transformée en affirmation physique.

### 9.10 Absence de scalaire normatif

Cette section ne définit aucun \(\|C_{AB}\|\), \(\|G\|\), seuil, score normalisé, ratio, ni indicateur scalaire de temps. De telles normes pourront être utilisées ultérieurement comme diagnostics numériques/de présentation si un futur plan de validation les préenregistre explicitement ; elles ne font pas partie de la définition scientifique actuelle.

---

## 10. Faux positif central

```text
PARAMETER_ELIMINATION_ALONE = INSUFFICIENT
```

Le simple fait d'obtenir \(X_A(s)\), \(X_B(s)\), puis d'éliminer \(s\) pour écrire \(X_B = f(X_A)\), ne constitue pas à lui seul une construction de temps relationnel.

Le paramètre \(s\) reste :

```text
modular_parameter
```

et non :

```text
physical_time.
```

---

## 11. Frontière HSMI

Borne interprétative :

```text
FINITE_HSMI_NONTRIVIAL_TRANSLATION = IMPOSSIBLE
```

sous la covariance Borchers/Wiesbrock avec générateur positif dans le cadre fini.

Conséquences — `model0a` ne doit pas revendiquer :

```text
HSMI translation emergence
positive translation generator emergence
causal order
global time orientation
arrow of time
```

Cette borne ne constitue pas un échec de `model0a`.

---

## 12. Référence relationnelle

```text
FUNDAMENTAL_PRIVILEGED_CLOCK = FORBIDDEN

RELATIONAL_REFERENCE_CHOICE = CONCEPTUALLY_COMPATIBLE_WITH_KNOWN_RELATIONAL_FRAMEWORKS
```

Page–Wootters / Höhn–Smith–Lock / QRF ne sont pas importés comme théorèmes techniques de `model0a`.

La chain rule du cocycle (§7) montre une propriété algébrique de composition entre références. Elle ne démontre pas à elle seule :

```text
physical clock covariance
absence physique d'horloge privilégiée
emergent time
```

---

## 13. Voies exclues de toy0a

Sont exclues de `toy0a` :

- la comparaison directe \(K_A\) vs \(K_B\) comme construction non dégénérée ;
- la paire \((\rho_{AB},\rho_{BC})\) sans plongement commun explicitement défini ;
- HSMI ;
- l'implémentation Page–Wootters ;
- l'implémentation quantum-reference-frame ;
- la Berry modulaire ;
- la géométrie ;
- la gravitation.

---

## 14. Ce que toy0a pourra tester

`toy0a` pourra ultérieurement qualifier/falsifier :

- l'implémentabilité exacte du cocycle fini ;
- son raccord avec \(\mathcal R_{AB}\) ;
- la distinction correcte des régimes N0 / N1 / N2 ;
- sa covariance sous transformations unitaires déclarées ;
- la robustesse du porteur candidat face aux contrôles négatifs préenregistrés ;
- l'hypothèse plus restreinte : « ce cocycle constitue un porteur mathématique non trivial susceptible d'être utilisé dans une future définition opérationnelle de T1 ».

---

## 15. Ce que toy0a ne pourra pas établir

`toy0a` ne peut pas établir :

```text
T1 = PASS
emergence of physical time
causal ordering
time orientation
arrow of time
continuum limit
type-I -> type-III bridge
geometry
gravity
T2-T7
```

Il ne peut pas falsifier l'existence de toute construction possible de temps relationnel en dimension finie. Il ne peut falsifier que la construction candidate explicitement testée.

---

## 16. Paramètres qui restent `OPEN`

```text
LOCAL_DIMENSION               = CLOSED — cf. §2, (2, 2)
STATE_FAMILY                  = CLOSED — cf. §3, TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY
STATE_PARAMETER_VALUES        = OPEN
MODULAR_PARAMETER_DOMAIN      = OPEN
NUMERICAL_TOLERANCES          = OPEN
T1_NONTRIVIALITY_CRITERION    = OPEN
MODEL0A_ACCEPTANCE_CRITERION  = OPEN
CONFIRMATORY_PROTOCOL         = NOT_DEFINED
```

`LOCAL_DIMENSION` et `STATE_FAMILY` ont été fermés au lot `MODEL0A-DESIGN-1` par décision scientifique ChatGPT (§2, §3). La structure analytique de qualification du cocycle (§9) a été fermée au lot `MODEL0A-DIAGNOSTICS-DESIGN-1`, sans fixer de valeur numérique, de seuil ou de norme (§9.10). Aucune autre valeur n'est fixée dans ce document.

---

## 17. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

H.-W. Wiesbrock, *Half-Sided Modular Inclusions of von-Neumann-Algebras*, Commun. Math. Phys. 157 (1993) 83–92, DOI [10.1007/BF02098019](https://doi.org/10.1007/BF02098019).

Parrikar, Rajgadia, Singh, Sorce, *Relational bulk reconstruction from modular flow*, JHEP 07 (2024) 138, [arXiv:2403.02377](https://arxiv.org/abs/2403.02377) — utilisée uniquement pour la présentation explicite moderne des identités modulaires générales citées aux §6–7 et §9, pas pour son interprétation holographique.

---

## 18. Statut et prochaine étape

```text
MODEL0A_SPECIFICATION_STATUS = ACCEPTED_AS_DESIGN_BASIS
```

La prochaine étape autorisée est l'implémentation bornée des diagnostics de qualification du cocycle de `model0a` (§9) par le rôle `code` (Claude Sonnet 5), sur la base du présent document et de `docs/toy-models/toy0a/implementation-design.md`.
