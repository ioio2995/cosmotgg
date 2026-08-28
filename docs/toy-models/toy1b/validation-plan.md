# toy1b — Plan de validation proposé (qualification confirmatoire `T5-FLOW`)

**Statut : `PROPOSED_MODEL1B_T5_FLOW_VALIDATION_PLAN_CORRECTED`.**

```text
STATUS                 = PROPOSED_MODEL1B_T5_FLOW_VALIDATION_PLAN_CORRECTED
NOT_FROZEN              = TRUE
CHATGPT_REVIEW          = PENDING_FINAL_REVIEW
CONFIRMATORY_EXECUTION  = NOT_AUTHORIZED

MODEL1B_IMPLEMENTATION            = ACCEPTED
MODEL1B_IMPLEMENTATION_ACCEPTED_HEAD = 788337f4d383962947586084c342edcf395af234

T5_FLOW_EXECUTION_STATUS = NOT_EXECUTED
T5_FLOW_QUALIFICATION    = NOT_EXECUTED
T5                        = OPEN_NOT_EXECUTED
```

Ce document définit le protocole confirmatoire préenregistré de qualification `T5-FLOW` de `model1b`, conformément à `docs/governance/documentation-governance.md` §11.4 (`CONFIRMATORY_PROTOCOL_FREEZE_BEFORE_EXECUTION = REQUIRED`) et au pare-feu confirmatoire de `docs/toy-models/toy1b/specification.md` §22.

Sources normatives, non modifiées par ce document :

```text
docs/model/t5-modular-cross-scale-flow-criteria.md   (FROZEN, T5F1-T5F11)
docs/toy-models/toy1b/specification.md               (FROZEN_MODEL1B_T5_FLOW_DESIGN)
docs/toy-models/toy1b/implementation-design.md        (FROZEN_MODEL1B_T5_FLOW_DESIGN)
```

Ce document n'exécute rien. Il ne contient aucun résultat, aucune sortie numérique, aucun verdict.

---

## 1. Identification

```text
TOY_ID   = toy1b
MODEL_ID = model1b

VALIDATION_PLAN_STATUS = PROPOSED_MODEL1B_T5_FLOW_VALIDATION_PLAN_CORRECTED
```

Une fois gelé, ce document devient `READ_ONLY_DURING_CONFIRMATORY_EXECUTION` (`docs/governance/documentation-governance.md` §11.4) : il ne peut plus être modifié en fonction des résultats observés.

---

## V1. Pare-feu confirmatoire

```text
PREVIOUS_SCRATCH_RESULTS = NONCONFIRMATORY
UNIT_TEST_RESULTS         = IMPLEMENTATION_EVIDENCE_ONLY

FIXTURE_SELECTION_AFTER_CONFIRMATORY_OBSERVATION      = FORBIDDEN
PARAMETER_RETUNING_AFTER_CONFIRMATORY_OBSERVATION     = FORBIDDEN
EXTRACTION_LAW_CHANGE_AFTER_CONFIRMATORY_OBSERVATION  = FORBIDDEN
THRESHOLD_CHANGE_AFTER_CONFIRMATORY_OBSERVATION       = FORBIDDEN
```

```text
T5_FLOW_PASS          != T5_PASS
FINITE_SCALE_RUNNING  != CONTINUUM
FINITE_SCALE_RUNNING  != CURVATURE
MODULAR_SUPPORT       != PHYSICAL_GEOMETRY
WEIGHT4               != CURVATURE
```

Aucun résultat des audits de scratch exploratoires antérieurs (`8->6->4`, `6->5->4`, audits perturbatifs `lambda`, audits d'ordre 7, scratch modulaire global) ni des tests unitaires d'implémentation (`MODEL1B-IMPL-1`, `MODEL1B-IMPL-CORRECTION-1`) ne compte comme preuve de qualification confirmatoire de `toy1b` : ils restent `NONCONFIRMATORY`/`IMPLEMENTATION_EVIDENCE_ONLY`.

---

## V2. Construction SU(2) fixe

Pour toute fixture du protocole, utiliser exclusivement :

$$
U(\alpha;\vec n) = \cos\!\left(\frac\alpha2\right) I - i\sin\!\left(\frac\alpha2\right)\frac{n_x\sigma_x+n_y\sigma_y+n_z\sigma_z}{\|\vec n\|},
$$

angles en radians.

Ceci est uniquement une construction unitaire déterministe de dimension finie. Aucune interprétation d'angle physique ni d'axe spatial.

---

## V3. Fixture générique non centrale

Ordre fixe des arêtes fines :

```text
e_0 = AX
e_1 = XY
e_2 = YB
e_3 = BC
e_4 = CP
e_5 = PQ
e_6 = QD
e_7 = DA
```

Pour \(i = 0,\dots,7\) :

$$
\theta_i = 0.10 + 0.02\,i,
\qquad
\alpha_i = 0.30 + 0.10\,i,
\qquad
\vec n_i = (1,\ 1+(i \bmod 3),\ 2),
\qquad
M_{e_i} = U(\alpha_i;\vec n_i).
$$

Valeurs explicites (calculées directement des formules ci-dessus, avant toute exécution) :

| \(i\) | arête | \(\theta_i\) | \(\alpha_i\) | \(\vec n_i\) |
|---|---|---|---|---|
| 0 | AX | 0.10 | 0.30 | (1, 1, 2) |
| 1 | XY | 0.12 | 0.40 | (1, 2, 2) |
| 2 | YB | 0.14 | 0.50 | (1, 3, 2) |
| 3 | BC | 0.16 | 0.60 | (1, 1, 2) |
| 4 | CP | 0.18 | 0.70 | (1, 2, 2) |
| 5 | PQ | 0.20 | 0.80 | (1, 3, 2) |
| 6 | QD | 0.22 | 0.90 | (1, 1, 2) |
| 7 | DA | 0.24 | 1.00 | (1, 2, 2) |

Soit, en valeurs \(\theta\) seules :

```text
AX = 0.10
XY = 0.12
YB = 0.14
BC = 0.16
CP = 0.18
PQ = 0.20
QD = 0.22
DA = 0.24
```

Cette fixture est sélectionnée AVANT l'exécution confirmatoire. C'est la fixture générique déterministe déjà utilisée pour la vérification de bon sens d'implémentation ordinaire, mais aucune de ses sorties de qualification `T5-FLOW` n'a été utilisée pour sélectionner ou ajuster ces valeurs.

Aucune valeur ne peut être modifiée après le gel du plan de validation.

### Contrôle de non-centralité préenregistré

Définir :

$$
H_M = M_{AX}\,\overline{M_{XY}}\,M_{YB}\,\overline{M_{BC}}\,M_{CP}\,\overline{M_{PQ}}\,M_{QD}\,\overline{M_{DA}}.
$$

Définir :

$$
r_{\mathrm{noncentral}} = \left\| H_M - \frac{\mathrm{Tr}(H_M)}2 I_2 \right\|_F.
$$

Admissibilité de la fixture requise :

$$
r_{\mathrm{noncentral}} > \mathrm{SIGNAL\_FLOOR}.
$$

Si cet échec se produit :

```text
GENERIC_FIXTURE = PREDECLARED_FIXTURE_NOT_NONCENTRAL
```

Ne pas remplacer ni ajuster la fixture.

---

## V4. Fixture de jauge pure

Ordre fixe des sites :

```text
s_0 = A
s_1 = X
s_2 = Y
s_3 = B
s_4 = C
s_5 = P
s_6 = Q
s_7 = D
```

Pour \(k = 0,\dots,7\) :

$$
\beta_k = 0.20 + 0.09\,k,
\qquad
\vec m_k = (1,\ 1+(k \bmod 3),\ 2),
\qquad
G_k = U(\beta_k;\vec m_k).
$$

Valeurs explicites :

| \(k\) | site | \(\beta_k\) | \(\vec m_k\) |
|---|---|---|---|
| 0 | A | 0.20 | (1, 1, 2) |
| 1 | X | 0.29 | (1, 2, 2) |
| 2 | Y | 0.38 | (1, 3, 2) |
| 3 | B | 0.47 | (1, 1, 2) |
| 4 | C | 0.56 | (1, 2, 2) |
| 5 | P | 0.65 | (1, 3, 2) |
| 6 | Q | 0.74 | (1, 1, 2) |
| 7 | D | 0.83 | (1, 2, 2) |

Pour toute arête fine orientée \(i \leftarrow j\) :

$$
M_{i\leftarrow j} = G_i\,G_j^{\mathsf T}.
$$

Utiliser les MÊMES forces relationnelles que V3 :

```text
theta_e = 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24
```

dans l'ordre d'arête déclaré (§V3).

Cette fixture est de jauge pure PAR CONSTRUCTION. Aucune exigence d'invariance d'amplitude.

Comportement confirmatoire requis :

```text
Q_2 défini et plat
Q_1 défini et plat
Q_0 défini et plat
```

---

## V5. Oracle négatif d'arbre — fixture

Utiliser les matrices d'arête génériques exactes de V3 sur :

```text
AX, XY, YB, BC, CP, PQ, QD
```

Retirer la relation de fermeture `DA` :

$$
\theta_{DA} = 0,
\qquad
M_{DA} = I_2.
$$

Pour toutes les autres arêtes, conserver les valeurs \(\theta\)/\(M\) de V3.

C'est la fixture d'arbre déclarée. Aucune boucle ne peut être fabriquée depuis cette fixture.

### Première décimation \(8 \to 6\)

Chemin fin :

$$
C \leftarrow P \leftarrow Q \leftarrow D.
$$

$$
O_{\mathrm{path},8\to6} = O_{CP}\,O_{PQ}\,O_{QD}.
$$

Comparer avec le facteur directionnel grossier réel \(O_{CD}^{(1)}\) issu de \(K_1\).

Définir :

$$
D_{\mathrm{tree},8\to6} = O_{\mathrm{path},8\to6}^{\mathsf T}\,O_{CD}^{(1)}.
$$

### Seconde décimation \(6 \to 4\)

Chemin de niveau 1 :

$$
A \leftarrow X \leftarrow Y \leftarrow B.
$$

$$
O_{\mathrm{path},6\to4} = O_{AX}^{(1)}\,O_{XY}^{(1)}\,O_{YB}^{(1)}.
$$

Comparer avec \(O_{AB}^{(0)}\) issu de \(K_0\).

Définir :

$$
D_{\mathrm{tree},6\to4} = O_{\mathrm{path},6\to4}^{\mathsf T}\,O_{AB}^{(0)}.
$$

Comportement d'oracle négatif requis :

$$
D_{\mathrm{tree},8\to6} = I,
\qquad
D_{\mathrm{tree},6\to4} = I,
$$

dans la tolérance numérique préenregistrée (§V8, §V20).

```text
TREE_DIRECTIONAL_RUNNING = ABSENT
```

est le résultat candidat requis.

---

## V6. Fixture de domaine à relation nulle

Pour toutes les arêtes :

$$
\theta_e = 0,
\qquad
M_e = I_2.
$$

Chaîne requise :

$$
H_{\mathrm{rel}} = 0,
\qquad
\rho_2 = \frac I{256},
\qquad
\rho_1 = \frac I{64},
\qquad
\rho_0 = \frac I{16},
$$

$$
K_n = \log(2^{N_n})\,I,
$$

tout coefficient de Pauli non-identité s'annule, tout bloc \(J\) actif s'annule.

`directional_factor(J)` lève :

```text
reason = SINGULAR_DIRECTIONAL_FACTOR
```

Aucune orientation ne peut être construite.

---

## V7. Fixture de covariance de repère local

Partir de la fixture générique V3.

Pour chaque site fin \(s_k\) (même étiquetage de site que V4, \(s_0=A,\dots,s_7=D\)) :

$$
\gamma_k = 0.18 + 0.07\,k,
\qquad
\vec r_k = (2,\ 1+(k \bmod 2),\ 1+(k \bmod 3)),
\qquad
F_k = U(\gamma_k;\vec r_k).
$$

Valeurs explicites :

| \(k\) | site | \(\gamma_k\) | \(\vec r_k\) |
|---|---|---|---|
| 0 | A | 0.18 | (2, 1, 1) |
| 1 | X | 0.25 | (2, 2, 2) |
| 2 | Y | 0.32 | (2, 1, 3) |
| 3 | B | 0.39 | (2, 2, 1) |
| 4 | C | 0.46 | (2, 1, 2) |
| 5 | P | 0.53 | (2, 2, 3) |
| 6 | Q | 0.60 | (2, 1, 1) |
| 7 | D | 0.67 | (2, 2, 2) |

Définir :

$$
F_{\mathrm{fine}} = \bigotimes F_k \quad \text{(ordre canonique des sites fins)}.
$$

Transformer :

$$
\rho_2' = F_{\mathrm{fine}}\,\rho_2\,F_{\mathrm{fine}}^\dagger.
$$

Appliquer ensuite EXACTEMENT les mêmes réductions/extractions gelées.

Produits de repère survivants attendus :

$$
\text{niveau 1 :}\quad F_A\otimes F_X\otimes F_Y\otimes F_B\otimes F_C\otimes F_D,
$$
$$
\text{niveau 0 :}\quad F_A\otimes F_B\otimes F_C\otimes F_D.
$$

### Convention de repère \(SU(2) \to SO(3)\)

Pour tout \(F \in SU(2)\), le repère orthogonal réel \(R(F) \in SO(3)\) utilisé pour les contrôles de covariance ci-dessous est fixé, avant exécution, comme :

$$
R(F)_{ab} = \frac12\,\mathrm{Tr}\big[\sigma_a\,F\,\sigma_b\,F^\dagger\big],
\qquad a,b \in \{x,y,z\}.
$$

C'est cette convention, et uniquement celle-ci, qui définit \(R_i\), \(R_j\), \(R_A\) dans :

$$
J' = R_i\,J\,R_j^{\mathsf T},
\qquad
O' = R_i\,O\,R_j^{\mathsf T},
\qquad
Q' = R_A\,Q\,R_A^{\mathsf T}.
$$

Aucun choix de transposée ni de convention alternative ne peut être modifié après observation.

Contrôles requis :

$$
\rho_n' = F_n\,\rho_n\,F_n^\dagger,
\qquad
K_n' = F_n\,K_n\,F_n^\dagger,
$$
$$
J'_{i\leftarrow j} = R_i\,J_{i\leftarrow j}\,R_j^{\mathsf T},
\qquad
O'_{i\leftarrow j} = R_i\,O_{i\leftarrow j}\,R_j^{\mathsf T},
$$
$$
Q_n' = R_A\,Q_n\,R_A^{\mathsf T},
\qquad
d_{\mathrm{flat}}' = d_{\mathrm{flat}},
\qquad
\chi_n' = \chi_n.
$$

Aucune revendication de symétrie physique au-delà de la covariance de repère local.

---

## V8. Tolérances numériques fixées

Préenregistrées :

```text
UNITARY_INPUT_TOLERANCE           = 1e-10
HERMITICITY_TOLERANCE             = 1e-10
TRACE_TOLERANCE                   = 1e-10
POSITIVITY_TOLERANCE              = 1e-12
STATE_COMPOSITION_TOLERANCE       = 1e-10
MODULAR_PATH_TOLERANCE            = 1e-9
PAULI_RECONSTRUCTION_TOLERANCE    = 1e-8
COVARIANCE_TOLERANCE              = 1e-8
PURE_GAUGE_FLATNESS_TOLERANCE     = 1e-8
TREE_AGREEMENT_TOLERANCE          = 1e-8
ZERO_RELATION_J_TOLERANCE         = 1e-10
SIGNAL_FLOOR                      = 1e-8
ORTHOGONALITY_REGRESSION_TOLERANCE = 1e-10
```

Aucune tolérance n'est une échelle physique.

Aucun seuil d'admissibilité de conditionnement n'est introduit.

```text
CONDITIONING_ADMISSIBILITY_THRESHOLD = NONE
```

Toutes les valeurs singulières et tous les nombres de conditionnement utilisés dans l'extraction directionnelle doivent néanmoins être rapportés. Un bloc non nul mais mal conditionné n'est jamais exclu silencieusement.

### Câblage déterministe des tolérances vers les appels de production

Table fixée avant exécution, reliant chaque tolérance ci-dessus au paramètre nommé exact de l'appel de production correspondant :

```text
fine_relational_hamiltonian:
    max_entanglement_unitarity_tolerance = UNITARY_INPUT_TOLERANCE

fine_relational_gibbs_state:
    hermiticity_tolerance = HERMITICITY_TOLERANCE
    trace_tolerance       = TRACE_TOLERANCE
    positivity_tolerance  = POSITIVITY_TOLERANCE

modular_datum (à tous les niveaux n = 2, 1, 0) :
    hermiticity_tolerance = HERMITICITY_TOLERANCE
    trace_tolerance       = TRACE_TOLERANCE
    positivity_tolerance  = POSITIVITY_TOLERANCE
```

Les autres tolérances (`STATE_COMPOSITION_TOLERANCE`, `MODULAR_PATH_TOLERANCE`, `PAULI_RECONSTRUCTION_TOLERANCE`, `COVARIANCE_TOLERANCE`, `PURE_GAUGE_FLATNESS_TOLERANCE`, `TREE_AGREEMENT_TOLERANCE`, `ZERO_RELATION_J_TOLERANCE`, `SIGNAL_FLOOR`, `ORTHOGONALITY_REGRESSION_TOLERANCE`) restent affectées exactement aux résidus déjà déclarés dans les sections `V11`–`V21` où elles apparaissent.

Aucune tolérance implicite, aucune valeur par défaut de production, pendant l'exécution confirmatoire.

---

## V9. Résidu matriciel normalisé

Chaque fois qu'une égalité matricielle \(A = B\) est testée, sauf lorsqu'un critère ci-dessous spécifie directement un scalaire, utiliser :

$$
R(A,B) = \frac{\|A-B\|_F}{\max(1,\ \|A\|_F,\ \|B\|_F)}.
$$

Cette définition est fixée avant exécution.

---

## V10. `T5F1` / `T5F2`

`T5F1` `PASS` requiert :

- \(\rho_1\) obtenu uniquement via `partial_trace(rho_2)` (`reduce_to_level_1`) ;
- \(\rho_0\) obtenu uniquement via `partial_trace(rho_1)` (`reduce_to_level_0`) ;
- aucune cible grossière indépendante ;
- aucun réajustement.

`T5F2` `PASS` requiert exactement :

```text
E_2 = vide
E_1 = {P, Q}
E_0 = {P, Q, X, Y}
```

et les ordres de sites gelés (`FINE_SITE_ORDER`, `LEVEL_1_SITES`, `LEVEL_0_SITES`).

Tout écart : `FAIL`.

---

## V11. `T5F3` — Composition d'états

Calculer :

$$
\rho_{0,\mathrm{seq}} = \texttt{reduce\_to\_level\_0}(\texttt{reduce\_to\_level\_1}(\rho_2)),
\qquad
\rho_{0,\mathrm{direct}} = \texttt{reduce\_to\_level\_0\_direct}(\rho_2).
$$

Requis :

$$
R(\rho_{0,\mathrm{seq}}, \rho_{0,\mathrm{direct}}) \le \mathrm{STATE\_COMPOSITION\_TOLERANCE}.
$$

Classification : `SATISFIED_BY_CONSTRUCTION`, avec confirmation de régression exécutable.

Obligatoire :

```text
THIS_IS_NOT_GEOMETRY_EVIDENCE
```

---

## V12. `T5F4` — Donnée modulaire

Pour \(n = 2,1,0\) :

- exiger \(\rho_n\) fidèle sous le domaine de validation déclaré ;
- calculer UNIQUEMENT \(K_n = -\log(\rho_n)\) depuis le \(\rho_n\) réel (`modular_datum`).

Calculer également \(K_0\) depuis \(\rho_{0,\mathrm{direct}}\).

Requis :

$$
R(K_{0,\mathrm{seq}}, K_{0,\mathrm{direct}}) \le \mathrm{MODULAR\_PATH\_TOLERANCE}.
$$

Aucun flot autonome de \(K\). Aucun \(K\) cible.

### Convention scalaire additive du datum modulaire

Déclarée explicitement et fixée avant exécution :

```text
MODULAR_ADDITIVE_SCALAR_CONVENTION = ABSOLUTE_FROM_NORMALIZED_RHO
K_ADDITIVE_SHIFT                    = NONE
IDENTITY_COMPONENT_RETAINED         = TRUE
TRACE_CENTERING_OF_K                = FORBIDDEN
```

\(K_n\) est exactement \(-\log(\rho_n)\) pour le \(\rho_n\) normalisé réel (`modular_datum`, spec §9) : aucune comparaison modulo l'identité, aucun retrait de trace, aucun décalage scalaire post-hoc. \(K_{0,\mathrm{seq}}\) et \(K_{0,\mathrm{direct}}\) sont comparés comme matrices complètes (résidu \(R\) ci-dessus), pas via une quantité réduite ou centrée.

---

## V13. `T5F5` — Support modulaire complet

Pour \(K_2, K_1, K_0\) : calculer la décomposition de Pauli COMPLÈTE (`modular_pauli_coefficients`).

Requérir la reconstruction (`reconstruct_from_pauli_coefficients`) :

$$
R\big(K_n,\ \mathrm{reconstruct}(\mathrm{coefficients}(K_n))\big) \le \mathrm{PAULI\_RECONSTRUCTION\_TOLERANCE}
$$

à tous les niveaux.

Norme à \(N\) corps \(\ge 3\) :

$$
H_{\ge3}(K_n) = \sqrt{\sum_{w\ge3} W_w(K_n)^2}.
$$

Contrôle d'état fin :

$$
H_{\ge3}(K_2) \le \mathrm{SIGNAL\_FLOOR}
$$

car \(K_2\) dérive du \(H_{\mathrm{rel}}\) explicitement à deux corps plus l'identité (identité exacte, spécification §8).

Rapporter, à titre d'observation (jamais comme condition de `PASS`/`FAIL`) :

$$
H_{\ge3}(K_1),\qquad H_{\ge3}(K_0).
$$

Définir la troncature par paire exacte :

$$
K_n^{(\le2)} = \mathrm{reconstruction\ utilisant\ uniquement\ les\ poids\ } 0,1,2,
$$

et :

$$
R_{\mathrm{pair}}(n) = \frac{\|K_n - K_n^{(\le2)}\|_F}{\max(1,\ \|K_n\|_F)}.
$$

Rapporter également, à titre d'observation, \(R_{\mathrm{pair}}(1)\) et \(R_{\mathrm{pair}}(0)\).

### Classification informative — fermeture par paire

Le design gelé de `model1b` (`docs/toy-models/toy1b/specification.md` §21) est explicite : « aucun secteur à \(N\) corps particulier n'est requis non nul par définition ; la génération effectivement observée reste une preuve de qualification, pas un axiome imposé a priori ». La fermeture ou non-fermeture par paire doit donc être MESURÉE et RAPPORTÉE, jamais imposée a priori comme condition de `PASS`.

Définir, à titre purement informatif :

```text
PAIR_TRUNCATION_FLOW_OBSERVATION =
    CLOSED_WITHIN_SIGNAL_FLOOR
    |
    NONCLOSED_ABOVE_SIGNAL_FLOOR
```

`CLOSED_WITHIN_SIGNAL_FLOOR` si \(R_{\mathrm{pair}}(1) \le \mathrm{SIGNAL\_FLOOR}\) ET \(R_{\mathrm{pair}}(0) \le \mathrm{SIGNAL\_FLOOR}\) ; `NONCLOSED_ABOVE_SIGNAL_FLOOR` sinon. Cette classification ne modifie à elle seule ni `T5F5 = PASS` ni `T5F5 = FAIL`.

### `T5F5` `PASS`/`FAIL`

`T5F5` `PASS` requiert UNIQUEMENT :

- la complétude du support canonique (reconstruction ci-dessus, à tous les niveaux, dans `PAULI_RECONSTRUCTION_TOLERANCE`) ;
- l'absence de substitution d'une troncature par paire à la donnée canonique \(K_n\) complète (`CANONICAL_SCALE_DATUM = FULL_K_n` effectivement utilisée par la route de production, jamais \(K_n^{(\le2)}\)).

`T5F5` `FAIL` si :

- un secteur de support effectivement présent est silencieusement écarté ;
- la reconstruction de Pauli ne reconstruit pas le \(K_n\) complet ;
- une troncature par paire est substituée à la donnée canonique ;
- une projection de poids \(\le2\) est utilisée comme flux exact.

Aucun support généré ne peut être écarté de la donnée canonique. Aucune exigence de non-nullité d'un secteur \(H_{\ge3}\) ou d'un résidu \(R_{\mathrm{pair}}\) particulier n'est imposée par ce critère : ces quantités restent des observations rapportées, jamais des conditions de verdict.

---

## V14. `T5F6` — Covariance de repère local

En utilisant V7, exiger tous les résidus normalisés applicables :

```text
covariance de rho
covariance de K
covariance de J
covariance de O
covariance de Q
```

\(\le \mathrm{COVARIANCE\_TOLERANCE}\).

Exiger également :

$$
|d_{\mathrm{flat}}' - d_{\mathrm{flat}}| \le \mathrm{COVARIANCE\_TOLERANCE},
\qquad
|\chi' - \chi| \le \mathrm{COVARIANCE\_TOLERANCE}.
$$

Tous les facteurs directionnels requis doivent rester définis avec la même classification de domaine.

---

## V15. `T5F7` — Platitude de jauge pure

En utilisant V4 : tous les objets \(J\)/\(O\)/\(Q\) requis doivent être définis et correctement typés \(\mathbb Z_2\).

Requis à chaque niveau \(n=2,1,0\) :

$$
d_{\mathrm{flat}}(Q_n) \le \mathrm{PURE\_GAUGE\_FLATNESS\_TOLERANCE}.
$$

Si un niveau devient non plat au-delà de la tolérance :

```text
T5F7 = FAIL
```

Si une direction requise devient indéfinie/en inadéquation de type :

```text
T5F7 = FAIL_DOMAIN
```

Aucun remplacement de fixture.

---

## V16. `T5F8` — Variation inter-échelles finie

En utilisant V3 : le contrôle de configuration de non-centralité générique doit passer V3.

Tous les \(Q_2, Q_1, Q_0\) doivent être définis.

Calculer \(\chi_2, \chi_1, \chi_0\) :

$$
\Delta_{21} = |\chi_2-\chi_1|,
\qquad
\Delta_{10} = |\chi_1-\chi_0|,
\qquad
\Delta_{20} = |\chi_2-\chi_0|.
$$

Requis :

$$
\max(\Delta_{21},\Delta_{10},\Delta_{20}) > \mathrm{SIGNAL\_FLOOR}
$$

pour `T5F8 = PASS`, à forces relationnelles finies non nulles.

Aucune limite de couplage faible utilisée. Aucune extrapolation \(\theta\to0\).

Classification uniquement :

```text
FINITE_SCALE_STATE_DERIVED_DIRECTIONAL_RUNNING
```

Jamais courbure ou continuum.

---

## V17. `T5F9` — Préenregistrement

Ce plan de validation lui-même se gèle avant exécution confirmatoire :

- fixtures ;
- lois d'extraction ;
- hiérarchie de sites ;
- définitions des diagnostics ;
- définitions des résidus ;
- tolérances ;
- conditions `PASS`/`FAIL`.

Après gel : tout changement sémantique ou réajustement de paramètre invalide l'exécution confirmatoire correspondante.

---

## V18. `T5F10` — Domaine fail-closed

`T5F10` couvre les DEUX échecs de domaine directionnel distincts, préservés séparément et jamais confondus (spec §12).

### V18.a — Facteur singulier (fixture V6)

En utilisant V6, exiger :

tous les blocs \(J\) actifs satisfont

$$
\|J\|_F \le \mathrm{ZERO\_RELATION\_J\_TOLERANCE},
$$

et la route directionnelle de production réelle produit :

```text
DIRECTIONAL_FACTOR            = UNDEFINED
DIRECTIONAL_UNDEFINED_REASON  = SINGULAR_DIRECTIONAL_FACTOR
```

et jamais `Z2_DIRECTIONAL_TYPE_MISMATCH`.

### V18.b — Inadéquation de type \(\mathbb Z_2\) (`TYPE_MISMATCH_DOMAIN_FIXTURE`)

Fixture négative déterministe, distincte de V6 et préenregistrée avant exécution :

$$
J_{\mathrm{TYPE\_MISMATCH}} = I_3,
\qquad
J_{\mathrm{VALID\_MINUS}} = \mathrm{diag}(-1,\ 1,\ 1).
$$

**Oracle direct obligatoire.** \(J_{\mathrm{TYPE\_MISMATCH}}=I_3\) est inversible (toutes ses valeurs singulières valent \(1\)) ; son facteur polaire est \(O=I_3\), \(\det(O)=+1\). `directional_factor(J_TYPE_MISMATCH)` doit donc échouer fail-closed avec exactement :

```text
DIRECTIONAL_RELATIONAL_TYPE  = TYPE_MISMATCH_FAIL_CLOSED
DIRECTIONAL_UNDEFINED_REASON = Z2_DIRECTIONAL_TYPE_MISMATCH
```

et jamais `SINGULAR_DIRECTIONAL_FACTOR`.

\(J_{\mathrm{VALID\_MINUS}}=\mathrm{diag}(-1,1,1)\) est déjà orthogonal, \(\det(J_{\mathrm{VALID\_MINUS}})=-1\) : son facteur polaire est lui-même, typé correctement (\(\det(O)=-1\)), et sert de comparaison valide.

**Contrôle de propagation obligatoire**, via la route de production réelle `active_cycle_loop_object_from_blocks`, sur un cycle actif de niveau 0 (longueur 4, `ACTIVE_CYCLE_EDGE_COUNTS`), avec exactement un \(J_{\mathrm{TYPE\_MISMATCH}}\) et trois \(J_{\mathrm{VALID\_MINUS}}\), dans cet ordre préenregistré :

$$
(J_{\mathrm{TYPE\_MISMATCH}},\ J_{\mathrm{VALID\_MINUS}},\ J_{\mathrm{VALID\_MINUS}},\ J_{\mathrm{VALID\_MINUS}}).
$$

Résultat obligatoire :

```text
LOOP_DIAGNOSTIC       = UNDEFINED_DIRECTIONAL_DOMAIN
LOOP_UNDEFINED_REASON = Z2_DIRECTIONAL_TYPE_MISMATCH
```

Aucun \(Q\), \(d_{\mathrm{flat}}\) ou \(\chi\) ne doit être construit dans ce cas.

### Fermeture sur échec — commune aux deux fixtures

Aucune pseudo-inverse. Aucune réparation epsilon. Aucune réparation de signe. Aucune inversion d'axe. Aucun ajustement d'orientation (`orientation fitting`). Aucune orientation arbitraire.

```text
SINGULAR_DIRECTIONAL_FACTOR   != Z2_DIRECTIONAL_TYPE_MISMATCH
```

Les deux raisons restent explicitement non confondues dans les deux sens.

Enregistrer également les valeurs singulières (`directional_conditioning`) pour tous les blocs directionnels de V3/V4/V5/V7 (y compris \(J_{\mathrm{TYPE\_MISMATCH}}\)/\(J_{\mathrm{VALID\_MINUS}}\) ci-dessus).

Aucun rejet d'échantillon fondé sur le conditionnement.

`T5F10` `PASS` requiert V18.a ET V18.b, chacune avec la raison exacte préservée. `T5F10` `FAIL` si une pseudo-inverse/réparation/orientation arbitraire est utilisée, ou si la raison retournée pour l'une des deux fixtures est incorrecte ou confondue avec l'autre.

---

## V19. `T5F11` — Flux multi-étapes

Chaîne explicite requise :

$$
\rho_2 \to \rho_1 \to \rho_0
$$

et contrôle direct indépendant :

$$
\rho_2 \to \rho_{0,\mathrm{direct}}.
$$

La même loi d'extraction est utilisée aux trois niveaux.

Objets rapportés requis, pour les fixtures pertinentes :

```text
rho_n
K_n
W_w(K_n)
tous les blocs J actifs
toutes les valeurs singulières directionnelles actives
tous les blocs O définis
Q_n
d_flat(Q_n)
chi_n
```

---

## V20. Oracle négatif d'arbre — critère chiffré

En utilisant V5, définir :

$$
\mathrm{tree\_residual}_{8\to6} = \frac{\|D_{\mathrm{tree},8\to6} - I\|_F}{\sqrt8},
\qquad
\mathrm{tree\_residual}_{6\to4} = \frac{\|D_{\mathrm{tree},6\to4} - I\|_F}{\sqrt8}.
$$

Requis :

$$
\mathrm{tree\_residual}_{8\to6} \le \mathrm{TREE\_AGREEMENT\_TOLERANCE},
\qquad
\mathrm{tree\_residual}_{6\to4} \le \mathrm{TREE\_AGREEMENT\_TOLERANCE}.
$$

Sinon :

```text
TREE_DIRECTIONAL_RUNNING = PRESENT
```

et l'oracle négatif de la route Gibbs déclarée échoue.

---

## V21. Contrôles mécaniques d'orthogonalité

Ce sont des gardes d'implémentation uniquement.

Pour tout \(O\) défini :

$$
\|O^{\mathsf T}O - I\|_F \le \mathrm{ORTHOGONALITY\_REGRESSION\_TOLERANCE}.
$$

Pour tout \(Q\) défini :

$$
\|Q^{\mathsf T}Q - I\|_F \le \mathrm{ORTHOGONALITY\_REGRESSION\_TOLERANCE},
\qquad
\det(Q) > 0.
$$

Aucune revendication physique. Ces contrôles ne redéfinissent pas le domaine directionnel de production.

---

## V22. Agrégation des résultats

### Algèbre de statut

Le contrat `T5-FLOW` gelé (`docs/model/t5-modular-cross-scale-flow-criteria.md` §18) n'autorise que :

```text
T5_FLOW_QUALIFICATION = PASS | FAIL | NOT_EXECUTED
```

`BLOCKED` n'est jamais un quatrième verdict de qualification. Le statut d'exécution du protocole et le verdict de qualification sont donc séparés explicitement :

```text
T5_FLOW_EXECUTION_STATUS = NOT_EXECUTED | COMPLETED | BLOCKED
T5_FLOW_QUALIFICATION    = NOT_EXECUTED | PASS | FAIL
```

Si `T5_FLOW_EXECUTION_STATUS = BLOCKED` (impossibilité réelle d'exécuter le protocole gelé — panne, dépendance manquante, incohérence bloquante), alors `T5_FLOW_QUALIFICATION` reste `NOT_EXECUTED`.

### Rapport par critère

Rapporter `T5F1`…`T5F11` individuellement comme :

```text
PASS
FAIL
```

avec, le cas échéant, le sous-type explicite `FAIL_DOMAIN / <raison exacte>` lorsqu'un échec de domaine d'une fixture obligatoire, survenu pendant une exécution confirmatoire achevée (`T5_FLOW_EXECUTION_STATUS = COMPLETED`), empêche l'évaluation normale du critère — par exemple :

```text
FAIL_DOMAIN / SINGULAR_DIRECTIONAL_FACTOR
FAIL_DOMAIN / Z2_DIRECTIONAL_TYPE_MISMATCH
```

`FAIL_DOMAIN` est un sous-type de `FAIL`, jamais un troisième statut de critère ni une valeur de `T5_FLOW_QUALIFICATION`. `T5F3` peut en outre indiquer `SATISFIED_BY_CONSTRUCTION_CONFIRMED` (`PASS` par construction, confirmé par régression).

Aucun critère ne peut être silencieusement omis.

### Verdict global

Si `T5_FLOW_EXECUTION_STATUS = COMPLETED`, définir :

```text
T5_FLOW_QUALIFICATION = PASS
```

UNIQUEMENT SI chaque exigence gelée `T5F1`–`T5F11` obtient `PASS` (ou `SATISFIED_BY_CONSTRUCTION_CONFIRMED` pour `T5F3`) sous ce protocole gelé et qu'aucun oracle négatif obligatoire n'échoue.

Sinon :

```text
T5_FLOW_QUALIFICATION = FAIL
```

avec le ou les critères en échec exacts (y compris tout `FAIL_DOMAIN / <raison>`).

Pare-feu obligatoire :

```text
T5_FLOW_QUALIFICATION = PASS
    N'IMPLIQUE PAS T5 PASS.
```

---

## V23. Protocole d'exécution du notebook

Chemin futur du notebook confirmatoire :

```text
experiments/toy1b/toy1b.ipynb
```

Ne PAS le créer dans ce lot.

La future exécution doit être :

- kernel neuf ;
- top-to-bottom ;
- sans état caché ;
- `HEAD` d'implémentation gelée exact enregistré ;
- `HEAD` de plan de validation gelé exact enregistré ;
- aucune modification de paramètre pendant l'exécution ;
- aucune cellule en échec ignorée manuellement ;
- tous les résidus bruts imprimés avant le verdict ;
- table finale des critères `T5F1`–`T5F11` ;
- section finale de pare-feu.

---

## Sources

Contrat gelé `T5-FLOW` : `docs/model/t5-modular-cross-scale-flow-criteria.md` (`T5F1`–`T5F11`).

Design gelé `model1b` : `docs/toy-models/toy1b/specification.md`, `docs/toy-models/toy1b/implementation-design.md`.

Implémentation acceptée : `src/cosmotgg/models/model1b/{states,hierarchy,modular_support,directional}.py` (`MODEL1B_IMPLEMENTATION_ACCEPTED_HEAD = 788337f4d383962947586084c342edcf395af234`).

Pare-feu confirmatoire transverse : `docs/governance/software-architecture-governance.md` §23.7–§23.8 ; cycle documentaire : `docs/governance/documentation-governance.md` §11.4.

---

## Paramètres qui restent `OPEN`/non exécutés par ce document

```text
T5_FLOW_EXECUTION_STATUS = NOT_EXECUTED
T5_FLOW_QUALIFICATION     = NOT_EXECUTED
T5                         = OPEN_NOT_EXECUTED

CONFIRMATORY_EXECUTION = NOT_AUTHORIZED
NOTEBOOK_CREATION       = NOT_AUTHORIZED
```

Aucune valeur numérique de ce document n'est encore validée par exécution : elle est préenregistrée, en attente de gel puis d'exécution confirmatoire sur mandat distinct.

---

## Statut et prochaine étape

```text
MODEL1B_VALIDATION_PLAN_STATUS = PROPOSED_MODEL1B_T5_FLOW_VALIDATION_PLAN_CORRECTED
MODEL1B_VALIDATION_PLAN_FREEZE = NOT_FROZEN
CHATGPT_REVIEW                  = PENDING_FINAL_REVIEW
CONFIRMATORY_EXECUTION          = NOT_AUTHORIZED
T5_FLOW_QUALIFICATION           = NOT_EXECUTED
T5                               = OPEN_NOT_EXECUTED
```

Corrections apportées par le lot `MODEL1B-T5-FLOW-VALIDATION-PLAN-CORRECTION-1`, à la suite de la revue ChatGPT `REVISION_REQUIRED` : (C1) `T5F5` recentré sur la seule complétude du support canonique et l'absence de substitution d'une troncature par paire, `H_{\ge3}(K_1)`/`H_{\ge3}(K_0)`/`R_pair(1)`/`R_pair(0)` rapportés à titre d'observation via la classification informative `PAIR_TRUNCATION_FLOW_OBSERVATION`, sans exiger leur non-nullité (§V13) ; (C2) ajout de la fixture négative déterministe `TYPE_MISMATCH_DOMAIN_FIXTURE` (\(J_{\mathrm{TYPE\_MISMATCH}}=I_3\), \(J_{\mathrm{VALID\_MINUS}}=\mathrm{diag}(-1,1,1)\)) et de son contrôle de propagation par `active_cycle_loop_object_from_blocks` sur un cycle actif de niveau 0, `T5F10` couvrant désormais explicitement les deux échecs de domaine distincts (§V18) ; (C3) séparation de `T5_FLOW_EXECUTION_STATUS` (`NOT_EXECUTED`/`COMPLETED`/`BLOCKED`) et de `T5_FLOW_QUALIFICATION` (`NOT_EXECUTED`/`PASS`/`FAIL`, sans `BLOCKED`), `FAIL_DOMAIN` reclassé sous-type de `FAIL` (§V22) ; (C4) convention scalaire additive du datum modulaire déclarée explicitement (`K_ADDITIVE_SHIFT=NONE`, `TRACE_CENTERING_OF_K=FORBIDDEN`, §V12) ; (C5) convention de repère \(SU(2)\to SO(3)\) explicitée, \(R(F)_{ab}=\tfrac12\mathrm{Tr}[\sigma_aF\sigma_bF^\dagger]\) (§V7) ; (C6) table de câblage déterministe des tolérances vers les paramètres nommés de production (`fine_relational_hamiltonian`, `fine_relational_gibbs_state`, `modular_datum`, §V8). Les fixtures V3/V4/V5/V6/V7 numériques, les treize tolérances déjà préenregistrées, `CONDITIONING_ADMISSIBILITY_THRESHOLD=NONE`, le critère `T5F8`, les oracles négatifs d'arbre et de jauge pure, le pare-feu `T5_FLOW_PASS != T5_PASS`, et `MODEL1B_IMPLEMENTATION_ACCEPTED_HEAD=788337f4d383962947586084c342edcf395af234` restent inchangés. Aucune exécution confirmatoire, aucun gel de ce document dans ce lot.

La prochaine étape autorisée est la revue finale à distance de ce plan de validation corrigé par ChatGPT.
