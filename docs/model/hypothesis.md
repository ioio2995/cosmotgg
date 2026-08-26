# CosmoTGG

## Temps, Géométrie et Gravitation depuis une structure quantique relationnelle

**Statut : note conceptuelle de travail — v0.2, corrigée après première contre-expertise scientifique, en attente de seconde revue**

### 1. Question de recherche

CosmoTGG étudie l’hypothèse suivante :

$$
\boxed{
\text{temps et géométrie pourraient être deux manifestations
d'une même structure quantique relationnelle}
}
$$

La gravitation serait alors recherchée dans un second temps comme propriété collective de la géométrie émergente.

Le programme ne suppose donc pas fondamentalement :

$$
t,\qquad g_{\mu\nu},\qquad G.
$$

La question minimale est :

$$
\boxed{
\text{Un même état quantique relationnel peut-il définir
à la fois une notion intrinsèque de changement
et une notion intrinsèque de courbure ?}
}
$$

Si la réponse est négative, le noyau de l’hypothèse est réfuté.

---

# 2. Règles méthodologiques

CosmoTGG distingue quatre statuts.

**[KNOWN]** : résultat établi dans la littérature, dans le domaine précisé.

**[DERIVED]** : conséquence mathématique directe de résultats connus, sans nouvelle hypothèse physique.

**[HYPOTHESIS]** : proposition propre à CosmoTGG.

**[OPEN]** : raccord nécessaire au programme mais non démontré.

Une relation démontrée en holographie, en QFT algébrique ou dans un modèle particulier ne doit jamais être présentée comme résultat général.

En particulier :

$$
\boxed{
\text{analogie}\neq\text{dérivation}
}
$$

et :

$$
\boxed{
\text{preuve dans un cadre particulier}\neq\text{loi fondamentale}.
}
$$

---

# 3. Niveau fondamental minimal

## [HYPOTHESIS]

Le niveau initial ne possède pas de coordonnées spatiales ou temporelles fondamentales.

On considère seulement des sous-systèmes quantiques :

$$
A,\;B,\;C,\ldots
$$

et un état global :

$$
\boxed{\rho_{ABC\ldots}}.
$$

Les objets élémentaires pertinents sont les **relations entre sous-systèmes**, décrites notamment par les états réduits :

$$
\rho_{AB},\quad\rho_{AC},\quad\rho_{BC},\ldots
$$

Il n’est initialement donné aucun :

$$
d_{AB},
$$

aucune métrique,

$$
g_{\mu\nu},
$$

et aucun temps extérieur :

$$
t.
$$

---

# 4. Structure modulaire

## [KNOWN]

CosmoTGG n'impose pas que l'état global \(\rho_{ABC\ldots}\) soit mixte ou de rang plein : un état global peut être pur.

En revanche, dans la réalisation matricielle finie utilisée actuellement, lorsqu'un état réduit \(\rho_X\) est utilisé pour définir un Hamiltonien modulaire fini sur l'algèbre complète, cet état réduit doit être **fidèle**, c'est-à-dire strictement positif / de rang plein en dimension finie :

$$
\boxed{\rho_X>0}
$$

On définit alors :

$$
\boxed{K_X=-\ln\rho_X}
$$

à une constante additive près selon la convention de normalisation.

\(K_X\) est appelé Hamiltonien modulaire.

Dans le cadre plus général des algèbres de von Neumann, la théorie de Tomita–Takesaki fournit la structure modulaire appropriée pour des états non nécessairement de rang plein (via restriction au support ou théorie modulaire algébrique) ; ces extensions existent mais ne font pas partie de la définition opérationnelle finie de v0.2. La simple formule matricielle ci-dessus est notre réalisation finie minimale de type I, utilisée comme banc d'essai.

Connes et Rovelli ont proposé que le flot modulaire déterminé par l’état puisse fournir le temps physique d’une théorie généralement covariante : c’est la **Thermal Time Hypothesis**. Il s’agit d’une hypothèse physique, non d’un théorème affirmant que tout flot modulaire est le temps physique. ([arXiv][1])

Pour une observable \(O\), le modèle fini possède le flot :

$$
\boxed{
O(s)=e^{+iKs}Oe^{-iKs}
}
$$

où \(s\) est un paramètre modulaire sans identification préalable à une durée mesurée en secondes.

Avec \(K=-\ln\rho\), CosmoTGG adopte la convention physique \(O(s)=e^{+iKs}Oe^{-iKs}\). Cette convention correspond au choix de signe utilisé par Connes–Rovelli pour le temps thermique et est opposée à une convention mathématique courante du paramètre modulaire de Tomita–Takesaki. Toute comparaison ultérieure doit conserver cette convention. ([arXiv][1])

## [OPEN]

La formulation actuelle \(\rho_X\)/\(K_X=-\ln\rho_X\) est une réalisation finie de type I utilisée comme banc d'essai minimal. Elle ne constitue pas encore la formulation adaptée aux algèbres locales de théorie quantique des champs, souvent de type III. Dans le cadre général des algèbres de von Neumann, l'entropie relative et les structures modulaires sont formulées à partir d'opérateurs modulaires relatifs, notamment dans la théorie d'Araki. ([DOI][10])

$$
\boxed{
\text{TYPE\_I\_TO\_ALGEBRAIC\_MODULAR\_BRIDGE}
}
$$

Le passage du modèle matriciel fini de type I à une structure modulaire algébrique appropriée à la QFT est un verrou scientifique **[OPEN]** de CosmoTGG.

---

# 5. La relation quantique entre deux sous-systèmes

Le domaine de travail v0.2 est celui d'un état réduit joint fidèle :

$$
\boxed{\rho_{AB}>0}
$$

ce qui garantit également la fidélité des marginales \(\rho_A,\rho_B\) dans ce cadre fini.

Pour \(A\) et \(B\), définissons :

$$
K_A=-\ln\rho_A,
$$

$$
K_B=-\ln\rho_B,
$$

$$
K_{AB}=-\ln\rho_{AB}.
$$

## [DERIVED]

On introduit uniquement comme notation de travail l’opérateur :

$$
\boxed{
\mathcal R_{AB}
=
K_A\otimes I_B
+
I_A\otimes K_B
-
K_{AB}
}
$$

soit :

$$
\mathcal R_{AB}
=
\ln\rho_{AB}
-
\ln(\rho_A\otimes\rho_B).
$$

Ce n’est **pas un nouvel objet physique postulé**. C’est simplement une combinaison des opérateurs modulaires connus. \(\mathcal R_{AB}\) est une combinaison opératorielle définie pour le modèle fini de CosmoTGG ; elle ne doit pas être identifiée au logarithme de l'opérateur modulaire relatif général de Tomita–Takesaki/Araki dans le cas non commutatif.

Or l’information mutuelle quantique satisfait :

$$
I(A:B)
=
D\!\left(
\rho_{AB}
\Vert
\rho_A\otimes\rho_B
\right),
$$

où \(D(\rho\Vert\sigma)\) est l’entropie relative d'Umegaki. Cette identité est standard en théorie de l’information quantique. ([DOI][9], [DOI][10])

Pour que \(D(\rho\Vert\sigma)\) soit finie, la condition générale à rappeler est :

$$
\boxed{\operatorname{supp}(\rho)\subseteq\operatorname{supp}(\sigma)}
$$

Cette condition n'est pas une exigence de rang plein général : dans le domaine fidèle \(\rho_{AB}>0\) considéré ici, elle est automatiquement satisfaite.

On obtient donc immédiatement :

$$
\boxed{
I(A:B)
=
\operatorname{Tr}
\left(
\rho_{AB}\mathcal R_{AB}
\right).
}
$$

Ainsi, la quantité moyenne associée à \(\mathcal R_{AB}\) mesure exactement le contenu corrélé de la relation \(A-B\).

Si :

$$
\rho_{AB}=\rho_A\otimes\rho_B,
$$

alors :

$$
\mathcal R_{AB}=0
$$

et :

$$
I(A:B)=0.
$$

---

# 6. Réponse à une perturbation

Considérons :

$$
\rho_{AB}\rightarrow\rho_{AB}+\delta\rho_{AB}.
$$

## [KNOWN]

La première loi de l’intrication affirme qu’autour d’un état de référence, au premier ordre :

$$
\boxed{
\delta S
=
\delta\langle K\rangle.
}
$$

Elle découle notamment du comportement de l’entropie relative entre deux états infinitésimalement proches. ([arXiv][3])

## [DERIVED]

Pour l’information mutuelle, on obtient au premier ordre, sous les hypothèses suivantes :

* famille différentiable d'états normalisés ;
* \(\operatorname{Tr}(\delta\rho_{AB})=0\) ;
* état de référence fidèle dans le voisinage considéré ;
* \(\mathcal R_{AB}\) évalué à l'état de référence ;
* la variation reste dans l'espace des états physiques ;

l'identité :

$$
\boxed{
\delta I(A:B)
=
\operatorname{Tr}
\left(
\delta\rho_{AB}\mathcal R_{AB}
\right).
}
$$

La variation des marginales \(\rho_A\) et \(\rho_B\) est bien incluse dans cette identité : elle n'est pas négligée, elle est portée implicitement par \(\delta\rho_{AB}\) via \(\mathcal R_{AB}\). Cette identité, comme celle du §5, reste un résultat standard de théorie de l'information quantique — elle n'est présentée ici comme aucun résultat nouveau propre à CosmoTGG.

Donc le même état relationnel détermine :

* sa quantité de corrélation ;
* sa réponse informationnelle à une perturbation ;
* sa structure modulaire.

Cela constitue notre premier raccord non arbitraire.

---

# 7. Première branche : le changement

## [KNOWN]

Un état détermine une structure modulaire et donc un flot modulaire.

La littérature existante propose déjà plusieurs formulations d'une dynamique quantique relationnelle sans temps externe :

* Page et Wootters montrent dès 1983 qu'une évolution observée peut être décrite relativement aux lectures d'une horloge interne dans un état global stationnaire ; ([DOI][11])
* les observables relationnelles / observables de Dirac constituent une autre famille de formulations relationnelles du changement ;
* Höhn, Smith et Lock montrent une équivalence entre plusieurs formulations modernes de dynamique quantique relationnelle ; ([arXiv][12])
* Connes et Rovelli proposent déjà l'utilisation du flot modulaire comme origine du temps thermique ([arXiv][1]).

## [HYPOTHESIS]

CosmoTGG propose de ne pas identifier immédiatement :

$$
s=t.
$$

$$
\boxed{
\text{MODULAR\_PARAMETER}\neq\text{PHYSICAL\_TIME}
}
$$

Le simple fait qu'un \(K\) génère un flot modulaire n'est pas, à lui seul, une validation du test T1 (§15).

Le contenu physique recherché est **relationnel**. Compte tenu de la littérature ci-dessus, la question propre à CosmoTGG n'est pas « peut-on avoir un changement relationnel sans temps externe ? » — cette question générale possède déjà des réponses dans la littérature citée. La question resserrée est :

$$
\boxed{
\text{Peut-on construire un temps relationnel physique à partir des relations
entre plusieurs structures modulaires, sans ajouter un degré de liberté
fondamental désigné comme horloge, et en utilisant la même famille de
structures relationnelles que celle dont la géométrie est supposée émerger ?}
}
$$

Pour deux sous-ensembles \(A\) et \(B\), on cherche si leurs flots peuvent définir une quantité indépendante d’une horloge extérieure correspondant à :

$$
\boxed{
\text{changement de }A
\text{ relativement au changement de }B.
}
$$

Le temps physique émergent devrait éventuellement être construit à partir de tels rapports.

Ainsi :

$$
\boxed{
\text{état relationnel}
\rightarrow
\text{structure modulaire}
\rightarrow
\text{rapports de changement}
}
$$

et non :

$$
t\rightarrow\text{évolution}.
$$

## [OPEN]

Il reste à démontrer qu’un paramètre relationnel ainsi construit possède, dans une limite collective appropriée, les propriétés du temps physique :

* ordre causal ;
* composition cohérente ;
* orientation ;
* limite continue ;
* relation au temps propre ;
* calibration physique.

La composition et l'orientation existent déjà pour le groupe modulaire lui-même ; elles restent à démontrer pour l'éventuel temps physique relationnel dérivé de la famille \(\{\rho_{ij},K_{ij}\}\).

---

# 8. Deuxième branche : la géométrie

Une relation unique \(A-B\) ne constitue pas une géométrie.

Il faut une famille de sous-systèmes :

$$
A,B,C,D,\ldots
$$

et une famille de structures :

$$
K_{AB},K_{AC},K_{BC},\ldots
$$

## [KNOWN — cadre particulier]

La littérature sur la **modular Berry connection** montre qu’une famille d’Hamiltoniens modulaires variant avec la région considérée possède une connexion naturelle. Dans une CFT bidimensionnelle avec dual holographique, certaines boucles de cette connexion calculent des longueurs dans \(AdS_3\). ([arXiv][4])

Plus fortement, dans certaines constructions holographiques semi-classiques, une courbure de Berry modulaire a été directement reliée à des données de courbure de l'espace-temps dual. ([arXiv][5])

Dans les constructions holographiques citées, sous leurs hypothèses propres, certaines données de connexion/courbure modulaire sont reliées à des données géométriques du bulk. CosmoTGG ne suppose aucune identité générale entre courbure modulaire et courbure de l'espace-temps ; ce résultat est établi sous des hypothèses holographiques précises et ne constitue pas une identité universelle entre structure modulaire et espace-temps.

## [HYPOTHESIS]

CosmoTGG demande si une construction analogue peut apparaître **sans supposer préalablement un bulk géométrique** :

$$
\boxed{
\{\rho_{ij}\}
\rightarrow
\{K_{ij}\}
\rightarrow
\text{connexion relationnelle}
\rightarrow
\text{courbure relationnelle}.
}
$$

La courbure serait alors définie avant son éventuelle interprétation comme courbure d’un espace-temps continu.

---

# 9. Hypothèse centrale CosmoTGG

Nous pouvons maintenant énoncer le cœur du projet sans ambiguïté :

$$
\boxed{
\rho
\rightarrow
K
\rightarrow
\begin{cases}
\text{flot relationnel}\\
\text{connexion/courbure relationnelle}
\end{cases}
}
$$

## [HYPOTHESIS]

Le temps et la géométrie ne seraient donc pas reliés par :

$$
\text{temps}\rightarrow\text{géométrie}
$$

ni :

$$
\text{géométrie}\rightarrow\text{temps}.
$$

Ils seraient deux propriétés collectives d’une **même structure quantique relationnelle**.

C’est l’hypothèse centrale qui doit être testée.

---

# 10. Pourquoi cela pourrait avoir un rapport avec la gravitation

À ce stade :

$$
\boxed{\text{courbure}\neq\text{encore gravitation}.}
$$

Il faut une étape supplémentaire.

## [KNOWN — holographie]

La première loi de l’intrication peut, dans les CFT holographiques appropriées, être traduite en contraintes sur la géométrie duale. Pour des perturbations autour du vide et toutes les régions sphériques, Faulkner et al. montrent que ces contraintes sont équivalentes aux équations gravitationnelles linéarisées du bulk ; avec la formule de Ryu–Takayanagi, on obtient les équations d’Einstein linéarisées. ([arXiv][6])

Ce résultat constitue une preuve de principe importante :

$$
\boxed{
\text{structure d'intrication}
\rightarrow
\text{dynamique géométrique}
}
$$

dans un cadre précis.

Mais \(G_N\) intervient déjà dans la traduction holographique via l’aire, donc ce résultat ne constitue pas une dérivation microscopique de \(G\).

---

# 11. Équilibre et équations d’Einstein

## [KNOWN]

Jacobson a montré en 1995 que, sous des hypothèses thermodynamiques locales, la relation :

$$
\delta Q=T\,dS
$$

associée à une entropie proportionnelle à l’aire des horizons locaux conduit à l’équation d’Einstein. Il interprète explicitement cette dernière comme une équation d’état de l’espace-temps. ([arXiv][7])

Le coefficient de proportionnalité entre entropie et aire fixe le couplage gravitationnel. Le résultat ne dérive donc pas la valeur de \(G\) à partir de zéro : Jacobson déplace la question de l'origine de \(G\) vers le coefficient entropie/aire, il ne la résout pas.

En 2016, il a montré qu’une hypothèse de stationnarité/maximalité de l’entropie d’intrication du vide pour de petites boules géodésiques **à volume fixé** conduit, sous certaines hypothèses, à l’équation d’Einstein semi-classique au premier ordre. ([arXiv][8]) Cette hypothèse entropique contient déjà un coefficient aire/entropie faisant intervenir le couplage gravitationnel : ce résultat est un précédent pour équilibre d'intrication → dynamique géométrique, mais pas une dérivation de \(G\).

Cela fournit un précédent important pour :

$$
\boxed{
\text{condition d'équilibre quantique}
\rightarrow
\text{dynamique gravitationnelle}.
}
$$

## [OPEN]

Ces constructions supposent déjà une quantité significative de structure géométrique.

CosmoTGG doit donc déterminer si une condition analogue peut être formulée **avant** l’apparition d’une géométrie continue.

---

# 12. Passage au collectif

## [HYPOTHESIS]

Une géométrie classique ne doit pas être attendue pour quelques degrés de liberté.

Considérons une observable géométrique relationnelle collective :

$$
\hat{\mathcal G}_N.
$$

On peut considérer :

$$
\boxed{
R_{\mathcal G}(N)
=
\frac{
\Delta\mathcal G_N
}{
|\langle\mathcal G_N\rangle|
}
}
$$

\(R_{\mathcal G}\) est un **indicateur possible** de faible fluctuation relative (\(R_{\mathcal G}\ll1\)), **ni nécessaire ni suffisant** pour établir une limite classique. Son utilisation est limitée aux observables pour lesquelles \(|\langle\mathcal G_N\rangle|\) est non nul et convenablement borné loin de zéro dans le régime testé. Si la moyenne peut s'annuler, une autre normalisation devra être définie et préenregistrée ; cette normalisation reste **[OPEN]** et n'est pas choisie dans le présent document.

T3 (§15) devra établir un régime collectif quasi classique au moyen de diagnostics de fluctuation/cohérence explicitement définis et préenregistrés. \(R_{\mathcal G}\) peut faire partie de ces diagnostics uniquement dans son domaine de validité ; le PASS de T3 ne dépend donc pas de ce seul quotient.

Il faudra également vérifier :

* cohérence entre observables ;
* stabilité sous coarse-graining ;
* émergence d’une notion locale ;
* dimension effective ;
* causalité ;
* décohérence ou mécanisme équivalent.

## [OPEN]

Le passage :

$$
\boxed{
\text{courbure relationnelle discrète}
\rightarrow
R_{\mu\nu\rho\sigma}(x)
}
$$

constitue l’un des verrous principaux du projet.

---

# 13. Gravitation : test seulement après émergence géométrique

Supposons que les étapes précédentes produisent une géométrie collective.

On perturbe alors le même état :

$$
\rho\rightarrow\rho+\delta\rho.
$$

Et l’on mesure simultanément :

$$
\delta\mathcal G
$$

et une observable énergétique/informationnelle appropriée :

$$
\delta\mathcal E.
$$

## [HYPOTHESIS]

On cherche une réponse collective :

$$
\boxed{
\delta\mathcal G
=
\kappa_{\rm eff}\,
\delta\mathcal E
+\cdots
}
$$

et surtout sa limite :

$$
\boxed{
\kappa_{\rm eff}
\longrightarrow
\kappa_*
}
$$

lorsque le nombre de degrés de liberté devient grand.

La propriété décisive est **l’universalité**, au sens suivant : dans une phase effective et une classe de systèmes explicitement déclarées, le même coefficient effectif \(\kappa_*\) doit gouverner la réponse géométrique aux différentes sources admissibles, à corrections contrôlées près. Cette condition n'exige pas que \(\kappa_*\) soit indépendant de toute microphysique.

Dans les scénarios de gravité induite de type Sakharov, la valeur de \(G_{\rm eff}\) peut dépendre du contenu microscopique et de l'échelle UV. Cela ne doit pas être confondu avec la question de l'universalité du couplage dans la théorie effective obtenue.

## [OPEN] DIMENSIONAL_CALIBRATION

Avant toute comparaison entre un coefficient émergent \(\kappa_*\) et \(8\pi G/c^4\), les observables émergentes doivent avoir reçu une interprétation dimensionnelle physique. Cette calibration doit être définie indépendamment de toute mesure gravitationnelle utilisée comme cible. La règle NO_GRAVITY_SCALE_INPUT (§14) reste inchangée. Aucune procédure concrète de calibration n'est définie dans ce document : \(\text{DIMENSIONAL\_CALIBRATION}=\text{OPEN}\).

\(c\) n'est pas utilisé comme échelle microscopique de calibration dans le modèle fondamental v0.2. Il n'intervient dans l'expression \(8\pi G/c^4\) qu'au stade de la comparaison finale avec l'écriture physique de l'équation d'Einstein, après émergence d'une structure causale et d'une conversion entre unités temporelles et spatiales. Le statut fondamental ou émergent de \(c\) dans une éventuelle théorie complète reste **[OPEN]**.

Seulement après cette démonstration serait-il légitime de tester :

$$
\boxed{
\kappa_*
\stackrel{?}{=}
\frac{8\pi G}{c^4}.
}
$$

\(G\) doit donc être une **sortie**, jamais un paramètre de calibration microscopique.

---

# 14. Contraintes de non-circularité

Un modèle CosmoTGG candidat échoue immédiatement s’il requiert en entrée :

$$
t_{\rm physical},
$$

$$
g_{\mu\nu},
$$

$$
G,
$$

$$
\ell_P=\sqrt{\frac{\hbar G}{c^3}},
$$

ou une aire déjà exprimée en unités de Planck.

La règle est :

$$
\boxed{\text{NO\_GRAVITY\_SCALE\_INPUT}}
$$

et :

$$
\boxed{\text{NO\_EXTERNAL\_TIME}}.
$$

L’utilisation de \(\hbar\) et des structures standards de mécanique quantique n’est évidemment pas interdite : CosmoTGG ne cherche pas actuellement à faire émerger la mécanique quantique elle-même.

---

# 15. Tests CosmoTGG

| Test                              | Question                                                                                           | PASS                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **T1 — Relational Flow**          | Les états réduits permettent-ils de comparer intrinsèquement les changements de sous-systèmes ?    | Construction explicite d'un changement relatif entre au moins deux sous-structures, calculée depuis \(\{\rho_{ij},K_{ij}\}\), sans temps externe et sans degré de liberté supplémentaire désigné comme horloge fondamentale (cf. §7) |
| **T2 — Modular Geometry**         | Une famille de structures modulaires produit-elle une connexion et une courbure non arbitraires ?  | Construction définie uniquement depuis les états          |
| **T3 — Classicalization**         | La structure relationnelle possède-t-elle une limite quasi classique ?                             | Régime collectif quasi classique établi par des diagnostics de fluctuation/cohérence explicitement définis et préenregistrés (cf. §12) ; \(R_{\mathcal G}\) peut y contribuer uniquement dans son domaine de validité |
| **T4 — Common Origin**            | Une même \(\delta\rho\) modifie-t-elle flot et courbure selon une structure commune ?              | T4_OPERATIONAL_CRITERION = **OPEN** (cf. note ci-dessous) |
| **T5 — Continuum**                | La courbure relationnelle tend-elle vers une géométrie continue ?                                  | Reconstruction effective de \(g_{\mu\nu}\) ou équivalent  |
| **T6 — Gravity**                  | La géométrie répond-elle universellement au contenu énergétique ?                                  | \(\kappa_{\rm eff}\rightarrow\kappa_*\) universel au sens du §13 (phase/classe de systèmes déclarées), sans exiger l'indépendance de toute microphysique |
| **T7 — Newton/Einstein coupling** | \(\kappa_*\) correspond-il au couplage gravitationnel observé ?                                    | (1) calibration dimensionnelle indépendante de toute mesure gravitationnelle cible définie ; (2) \(\kappa_*\) comparé à \(8\pi G/c^4\) ; (3) aucune valeur de \(G\) ni de longueur de Planck utilisée pour construire ou calibrer le modèle |

Chaque test doit pouvoir produire **FAIL**.

### Note sur T1

Le test T1 n'est pas satisfait par la seule existence séparée d'un flot modulaire pour chaque \(K_i\) ou \(K_{ij}\) (cf. §7, MODULAR_PARAMETER ≠ PHYSICAL_TIME).

### Note sur T4

T4 ne pourra être exécuté qu'après définition et préenregistrement d'un critère opératoire capable de distinguer :

A. deux constructions mathématiques indépendantes utilisant les mêmes données \(\rho\) ;

B. deux manifestations contraintes d'une structure commune.

La formulation « relation stable et non accidentelle » ne constitue pas, à elle seule, un critère de PASS. Cette formalisation sera traitée dans un lot scientifique ultérieur.

---

# 16. Ce que CosmoTGG ne prétend pas actuellement

CosmoTGG n’affirme pas que :

* le flot modulaire **est** déjà le temps physique ;
* l’information mutuelle **est** une distance ;
* la modular Berry curvature **est généralement** la courbure de l’espace-temps ;
* l’intrication **est** la gravitation ;
* \(G\) a été dérivé ;
* une géométrie classique a été obtenue ;
* les équations d’Einstein ont été reconstruites sans hypothèses géométriques préalables.

Ces propositions constituent précisément les raccords qui doivent être testés.

---

# 17. Formulation centrale gelée

Je proposerais de geler pour l’instant uniquement ceci :

$$
\boxed{
\textbf{Hypothèse CosmoTGG}
}
$$

> **Le temps et la géométrie ne sont pas supposés fondamentaux. CosmoTGG étudie s’ils peuvent émerger comme deux manifestations d’une même structure quantique relationnelle : le changement à travers sa structure de flot, et la géométrie à travers la compatibilité et la courbure de relations modulaires. La gravitation ne serait recherchée qu’au niveau collectif, comme réponse universelle de cette géométrie émergente au contenu énergétique.**

Sous forme compacte :

$$
\boxed{
\rho
\rightarrow
\text{structure modulaire}
\rightarrow
\begin{cases}
\text{changement relationnel}\\
\text{courbure relationnelle}
\end{cases}
}
$$

puis seulement :

$$
\boxed{
N\gg1
\rightarrow
\begin{cases}
\tau\\
g_{\mu\nu}
\end{cases}
}
$$

et enfin :

$$
\boxed{
\delta g
\stackrel{?}{=}
\kappa_*\delta T
}
$$

avec :

$$
\boxed{
\kappa_*
\stackrel{?}{=}
\frac{8\pi G}{c^4}.
}
$$

### Références fondatrices minimales

Connes & Rovelli (1994), *Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories*, Classical and Quantum Gravity 11 — temps thermique, flot modulaire et convention de signe adoptée par CosmoTGG (§4). ([arXiv][1])

Umegaki (1962), *Conditional expectation in an operator algebra, IV (Entropy and information)*, Kodai Mathematical Seminar Reports 14(2), 59–85 — entropie relative d'Umegaki. ([DOI][9])

Araki (1976), *Relative Entropy of States of von Neumann Algebras*, Publications RIMS 11(3), 809–833 — condition de finitude \(\operatorname{supp}(\rho)\subseteq\operatorname{supp}(\sigma)\) et opérateur modulaire relatif. ([DOI][10])

Page & Wootters (1983), *Evolution without evolution: Dynamics described by stationary observables*, Physical Review D 27, 2885 — dynamique relationnelle sans temps externe. ([DOI][11])

Höhn, Smith & Lock (2021), *Trinity of relational quantum dynamics*, Physical Review D 104, 066001 — équivalence de formulations relationnelles modernes. ([arXiv][12])

Jacobson (1995), *Thermodynamics of Spacetime: The Einstein Equation of State* — équation d’Einstein comme équation d’état ; \(G\) déplacé vers le coefficient entropie/aire, non dérivé. ([arXiv][7])

Blanco, Casini, Hung & Myers (2013), *Relative Entropy and Holography* — première loi de l’intrication \(\delta S=\delta\langle K\rangle\). ([arXiv][3])

Faulkner, Guica, Hartman, Myers & Van Raamsdonk (2014), *Gravitation from Entanglement in Holographic CFTs*, JHEP 03 (2014) 051 — première loi de l’intrication et équations gravitationnelles linéarisées dans le cadre holographique. ([arXiv][6])

Jacobson (2016), *Entanglement Equilibrium and the Einstein Equation*, Physical Review Letters 116, 201101 — équilibre d’intrication et équation d’Einstein semi-classique, sous condition de petites boules géodésiques à volume fixé ; pas une dérivation de \(G\). ([arXiv][8])

Czech, Lamprou, McCandlish & Sully (2018), *Modular Berry Connection for Entangled Subregions in AdS/CFT*, Physical Review Letters 120, 091601 — connexion modulaire et longueurs holographiques. ([arXiv][4])

Czech, de Boer, Ge & Lamprou (2019), *A Modular Sewing Kit for Entanglement Wedges*, JHEP 11 (2019) 094 — relation entre courbure de Berry modulaire et courbure de Riemann du bulk holographique, dans le cadre holographique étudié. ([arXiv][5])

[1]: https://arxiv.org/abs/gr-qc/9406019 "Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories"
[3]: https://arxiv.org/abs/1305.3182 "Relative Entropy and Holography"
[4]: https://arxiv.org/abs/1712.07123 "Modular Berry Connection for Entangled Subregions in AdS/CFT"
[5]: https://arxiv.org/abs/1903.04493 "A Modular Sewing Kit for Entanglement Wedges"
[6]: https://arxiv.org/abs/1312.7856 "Gravitation from Entanglement in Holographic CFTs"
[7]: https://arxiv.org/abs/gr-qc/9504004 "Thermodynamics of Spacetime: The Einstein Equation of State"
[8]: https://arxiv.org/abs/1505.04753 "Entanglement Equilibrium and the Einstein Equation"
[9]: https://doi.org/10.2996/kmj/1138844604 "Conditional expectation in an operator algebra, IV (Entropy and information)"
[10]: https://doi.org/10.2977/prims/1195191148 "Relative Entropy of States of von Neumann Algebras"
[11]: https://doi.org/10.1103/PhysRevD.27.2885 "Evolution without evolution: Dynamics described by stationary observables"
[12]: https://arxiv.org/abs/1912.00033 "Trinity of relational quantum dynamics"
