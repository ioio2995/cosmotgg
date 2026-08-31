# Dossier de qualification `T5a` — `model1c`

Statut : **qualification `T5a` acceptée (`PASS`)**

Ce document enregistre factuellement le verdict scientifique ChatGPT sur
la qualification `T5a` de `model1c`. Il n'ajoute, ne recalcule et
n'invente aucune valeur scientifique : il transcrit un arbitrage déjà
rendu, appuyé sur `docs/toy-models/toy1c/specification.md` (preuve
analytique, §10 et §12) et sur `docs/model/t5a-controlled-cross-scale-limit-criteria.md`
(référence normative opérationnelle gelée des critères `T5A1`–`T5A8`,
`T5A-C1`–`T5A-C6`, oracles négatifs `N1`–`N9`).

Ce document est **documentaire uniquement**. Il ne modifie ni la
spécification, ni la conception d'implémentation, ni le code, ni le
verdict scientifique qu'il transcrit.

---

## 1. Références normatives

```text
DESIGN_HEAD          = c2d8afdd9bdfb6db211d21c63a576d709c2cc8e4
IMPLEMENTATION_HEAD  = 456d3c46f8e64bb2f01271394d99d66591b4b66a
```

Documents amont, non rouverts par ce dossier :

```text
docs/toy-models/toy1c/specification.md          (T5A1-T5A8, T5A-C3, preuve
                                                  analytique §10/§12)
docs/toy-models/toy1c/implementation-design.md
docs/model/t5a-controlled-cross-scale-limit-criteria.md
```

---

## 2. Verdict scientifique ChatGPT

Verdict rendu, transcrit tel quel :

```text
CHATGPT_T5A_SCIENTIFIC_REVIEW = PASS

T5A1 = PASS
T5A2 = PASS
T5A3 = PASS
T5A4 = PASS
T5A5 = PASS
T5A6 = PASS
T5A7 = PASS
T5A8 = PASS

T5A-C3 = PASS

T5A_QUALIFICATION = PASS
T5A_PASS = ESTABLISHED

T5_PASS  = NOT_ESTABLISHED
T5B_PASS = NOT_ESTABLISHED

SCIENTIFIC_BLOCKING = NONE
```

---

## 3. Classes de revendication

```text
PRIMARY_CLAIM_CLASS = L2_STATE_OBSERVABLE_LIMIT

EVIDENCE_CLASS = A_ANALYTIC_LIMIT_PROOF

NUMERICAL_ROLE = NONE
```

---

## 4. Détail des critères `T5A1`–`T5A8` et routes conditionnelles

```text
T5A1 = PASS
T5A2 = PASS
T5A3 = PASS
T5A4 = PASS
T5A5 = PASS
T5A6 = PASS
T5A7 = PASS
T5A8 = PASS

T5A-C3 = PASS   (REDUCED_PARAMETRIZATION_CLOSURE, ACTIVÉ)

T5A-C1 = NOT_ACTIVATED
T5A-C2 = NOT_ACTIVATED
T5A-C4 = NOT_ACTIVATED
T5A-C5 = NOT_ACTIVATED
T5A-C6 = NOT_ACTIVATED
```

Oracles négatifs (`docs/toy-models/toy1c/specification.md` §21) :

```text
N1 = PASS
N3 = PASS
N6 = PASS
N9 = PASS
```

---

## 5. Résultats analytiques clés

Recopiés fidèlement depuis `docs/toy-models/toy1c/specification.md`
(§10, §12, §13), sans recalcul ni reformulation de sens.

Fermeture analytique (`T5A-C3`, §10) :

```text
I_{n+1} o G_n = Phi o I_n
```

Limite analytique (§12) :

```text
Phi^n = P_BELL + 2^-n (Id - P_BELL)
```

Non-trivialité (séparation de la classe triviale `T_MODEL1C`, §13) :

```text
dist_1(sigma_infinity, T_MODEL1C) >= 1/12 > 0
```

Anti-collapse (`N9`, §15) : les secteurs `kappa` Bell-distincts restent
distincts à la limite (`P_BELL(sigma_a) != P_BELL(sigma_b)` préservé
exactement).

Préenregistrement (`T5A8`, §19) : `P_CORE` complet, présent dans
`specification.md` à `DESIGN_HEAD`, avant toute implémentation.

---

## 6. Rôle des tests numériques d'implémentation

Les contrôles numériques/code déjà exécutés dans le cadre des lots
d'implémentation (`IMPLEMENTATION_HEAD`) sont explicitement hors du
dossier de qualification `T5a` :

```text
IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD
```

Ces contrôles n'établissent pas la limite analytique. La preuve `T5a`
retenue est exclusivement la preuve analytique fermée de
`specification.md` §10/§12 (`EVIDENCE_CLASS = A_ANALYTIC_LIMIT_PROOF`,
`NUMERICAL_ROLE = NONE`).

---

## 7. Statut final

```text
MODEL1C_STATUS = CLOSED_AT_T5A_QUALIFICATION_LEVEL

T5A_QUALIFICATION = PASS
T5A_PASS           = ESTABLISHED

T5_PASS  = NOT_ESTABLISHED
T5B_PASS = NOT_ESTABLISHED

CONTINUUM        = NOT_ESTABLISHED
LOCALITY         = NOT_ESTABLISHED
GEOMETRY         = NOT_ESTABLISHED
CURVATURE        = NOT_ESTABLISHED
GRAVITY          = NOT_ESTABLISHED
NONCLASSICALITY  = NOT_ESTABLISHED
```

---

## 8. Pare-feu scientifique préservé

Recopiés sans changement depuis `docs/toy-models/toy1c/specification.md`
(§2, §23) : ce dossier de qualification ne revendique et n'établit
aucun des éléments suivants.

```text
T5A_PASS != T5_PASS
T5A_PASS != T5B_PASS
T5A_PASS != CONTINUUM
T5A_PASS != LOCALITY
T5A_PASS != GEOMETRY
T5A_PASS != CURVATURE
T5A_PASS != GRAVITY
T5A_PASS != NONCLASSICALITY
T5A_PASS != TEMPS_RELATIONNEL
T5A_PASS != GENERATEUR_CONTINU
```

Aucun paramètre `OPEN` n'est fermé par ce dossier de qualification.
Aucun lot suivant, aucun nouveau toy et aucun nouveau modèle ne sont
autorisés par ce document.

---

## 9. Portée du présent document

Ce dossier de qualification n'établit, ne modifie et ne reformule
aucune décision scientifique. Il n'est pas une source normative
concurrente de `docs/toy-models/toy1c/specification.md` ni de
`docs/model/t5a-controlled-cross-scale-limit-criteria.md` : il en
constitue un enregistrement fidèle du verdict `T5a` déjà rendu par
ChatGPT, borné au périmètre `MODEL1C-T5A-QUALIFICATION-RECORD-1`.
