# toy0a — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model0a`, première construction candidate du toy `toy0a`.

Il intègre des décisions scientifiques déjà arbitrées par ChatGPT (revue physique bornée `MODEL0A_T1_BOUNDARY_REVIEW = PASS_WITH_CHATGPT_CORRECTIONS`). Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune dimension choisie, aucune valeur numérique d'état et aucun seuil.

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

La dimension locale exacte reste :

```text
LOCAL_DIMENSION = OPEN
```

Les états utilisés pour la construction modulaire doivent être **fidèles** lorsqu'un logarithme matriciel ordinaire est requis, conformément au domaine de travail fixé par `docs/model/hypothesis.md` §4–5 (\(\rho_X>0\)).

---

## 3. Paire relationnelle canonique

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

## 4. Objet mathématique candidat

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

## 5. Raccord à \(\mathcal R_{AB}\)

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

## 6. Identités structurelles

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

avec la convention CosmoTGG correspondante (§4, flot \(O(s)=e^{+iKs}Oe^{-iKs}\)).

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

## 7. Régimes algébriques

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

## 8. Faux positif central

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

## 9. Frontière HSMI

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

## 10. Référence relationnelle

```text
FUNDAMENTAL_PRIVILEGED_CLOCK = FORBIDDEN

RELATIONAL_REFERENCE_CHOICE = CONCEPTUALLY_COMPATIBLE_WITH_KNOWN_RELATIONAL_FRAMEWORKS
```

Page–Wootters / Höhn–Smith–Lock / QRF ne sont pas importés comme théorèmes techniques de `model0a`.

La chain rule du cocycle (§6) montre une propriété algébrique de composition entre références. Elle ne démontre pas à elle seule :

```text
physical clock covariance
absence physique d'horloge privilégiée
emergent time
```

---

## 11. Voies exclues de toy0a

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

## 12. Ce que toy0a pourra tester

`toy0a` pourra ultérieurement qualifier/falsifier :

- l'implémentabilité exacte du cocycle fini ;
- son raccord avec \(\mathcal R_{AB}\) ;
- la distinction correcte des régimes N0 / N1 / N2 ;
- sa covariance sous transformations unitaires déclarées ;
- la robustesse du porteur candidat face aux contrôles négatifs préenregistrés ;
- l'hypothèse plus restreinte : « ce cocycle constitue un porteur mathématique non trivial susceptible d'être utilisé dans une future définition opérationnelle de T1 ».

---

## 13. Ce que toy0a ne pourra pas établir

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

## 14. Paramètres qui restent `OPEN`

```text
LOCAL_DIMENSION               = OPEN
STATE_FAMILY                  = OPEN
STATE_PARAMETER_VALUES        = OPEN
MODULAR_PARAMETER_DOMAIN      = OPEN
NUMERICAL_TOLERANCES          = OPEN
T1_NONTRIVIALITY_CRITERION    = OPEN
MODEL0A_ACCEPTANCE_CRITERION  = OPEN
CONFIRMATORY_PROTOCOL         = NOT_DEFINED
```

Aucune valeur n'est fixée dans ce document.

---

## 15. Sources

Alain Connes, *Une classification des facteurs de type III*, Ann. Sci. ENS 6 (1973) 133–252, DOI [10.24033/asens.1247](https://doi.org/10.24033/asens.1247).

H.-W. Wiesbrock, *Half-Sided Modular Inclusions of von-Neumann-Algebras*, Commun. Math. Phys. 157 (1993) 83–92, DOI [10.1007/BF02098019](https://doi.org/10.1007/BF02098019).

Parrikar, Rajgadia, Singh, Sorce, *Relational bulk reconstruction from modular flow*, JHEP 07 (2024) 138, [arXiv:2403.02377](https://arxiv.org/abs/2403.02377) — utilisée uniquement pour la présentation explicite moderne des identités modulaires générales citées aux §5–6, pas pour son interprétation holographique.

---

## 16. Statut et prochaine étape

```text
MODEL0A_SPECIFICATION_STATUS = PROPOSED
```

La prochaine étape autorisée est une revue physique bornée de ce document, après revue du commit distant par ChatGPT.
