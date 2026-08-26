# CosmoTGG

## Temps, Géométrie et Gravitation depuis une structure quantique relationnelle

**Statut : note conceptuelle de travail — v0.1**

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

Dans un système quantique fini, pour un état de densité strictement positif \(\rho\), on peut définir :

$$
\boxed{K=-\ln\rho}
$$

à une constante additive près selon la convention de normalisation.

\(K\) est appelé Hamiltonien modulaire.

Dans le cadre plus général des algèbres de von Neumann, la théorie de Tomita–Takesaki fournit la structure modulaire appropriée ; la simple formule matricielle ci-dessus est notre réalisation finie minimale.

Connes et Rovelli ont proposé que le flot modulaire déterminé par l’état puisse fournir le temps physique d’une théorie généralement covariante : c’est la **Thermal Time Hypothesis**. Il s’agit d’une hypothèse physique, non d’un théorème affirmant que tout flot modulaire est le temps physique. ([arXiv][1])

Pour une observable \(O\), le modèle fini possède le flot :

$$
\boxed{
O(s)=e^{iKs}Oe^{-iKs}
}
$$

où \(s\) est un paramètre modulaire sans identification préalable à une durée mesurée en secondes.

---

# 5. La relation quantique entre deux sous-systèmes

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

Ce n’est **pas un nouvel objet physique postulé**. C’est simplement une combinaison des opérateurs modulaires connus.

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

où \(D(\rho\Vert\sigma)\) est l’entropie relative quantique. Cette identité est standard en théorie de l’information quantique. ([arXiv][2])

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

Pour l’information mutuelle, on obtient au premier ordre, sous les conditions régulières précédentes :

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

Donc le même état relationnel détermine :

* sa quantité de corrélation ;
* sa réponse informationnelle à une perturbation ;
* sa structure modulaire.

Cela constitue notre premier raccord non arbitraire.

---

# 7. Première branche : le changement

## [KNOWN]

Un état détermine une structure modulaire et donc un flot modulaire.

## [HYPOTHESIS]

CosmoTGG propose de ne pas identifier immédiatement :

$$
s=t.
$$

Le contenu physique recherché est **relationnel**.

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

Plus fortement, dans certaines constructions holographiques semi-classiques, la courbure de Berry modulaire a été directement reliée à la courbure de Riemann de l’espace-temps dual :

$$
\boxed{
\mathcal F_{\rm mod}
\longleftrightarrow
R_{\mu\nu\rho\sigma}^{\rm bulk}.
}
$$

Ce résultat est établi sous des hypothèses holographiques précises ; il ne constitue pas une identité universelle entre structure modulaire et espace-temps. ([arXiv][5])

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

En 2015, il a montré qu’une hypothèse de stationnarité/maximalité de l’entropie d’intrication du vide pour de petites boules géodésiques conduit, sous certaines hypothèses, à l’équation d’Einstein semi-classique au premier ordre. ([arXiv][8])

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

Son régime quasi classique devrait satisfaire au minimum :

$$
\boxed{
R_{\mathcal G}(N)
=
\frac{
\Delta\mathcal G_N
}{
|\langle\mathcal G_N\rangle|
}
\ll1.
}
$$

Cette condition est nécessaire comme critère de faible fluctuation, mais elle n’est pas suffisante à elle seule pour établir une limite classique.

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

La propriété décisive est **l’universalité** :

$$
\kappa_*
$$

ne doit pas dépendre arbitrairement de la composition microscopique de l’état.

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
| **T1 — Relational Flow**          | Les états réduits permettent-ils de comparer intrinsèquement les changements de sous-systèmes ?    | Aucun temps externe nécessaire                            |
| **T2 — Modular Geometry**         | Une famille de structures modulaires produit-elle une connexion et une courbure non arbitraires ?  | Construction définie uniquement depuis les états          |
| **T3 — Classicalization**         | La structure relationnelle possède-t-elle une limite quasi classique ?                             | Fluctuations relatives faibles + cohérence collective     |
| **T4 — Common Origin**            | Une même \(\delta\rho\) modifie-t-elle flot et courbure selon une structure commune ?              | Relation stable et non accidentelle                       |
| **T5 — Continuum**                | La courbure relationnelle tend-elle vers une géométrie continue ?                                  | Reconstruction effective de \(g_{\mu\nu}\) ou équivalent  |
| **T6 — Gravity**                  | La géométrie répond-elle universellement au contenu énergétique ?                                  | \(\kappa_{\rm eff}\rightarrow\kappa_*\) universel          |
| **T7 — Newton/Einstein coupling** | \(\kappa_*\) correspond-il au couplage gravitationnel observé ?                                    | \(8\pi G/c^4\) obtenu sans \(G\) en entrée                 |

Chaque test doit pouvoir produire **FAIL**.

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

Connes & Rovelli (1994), *Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories* — temps thermique et flot modulaire. ([arXiv][1])

Jacobson (1995), *Thermodynamics of Spacetime: The Einstein Equation of State* — équation d’Einstein comme équation d’état. ([arXiv][7])

Blanco, Casini, Hung & Myers (2013), *Relative Entropy and Holography* — première loi de l’intrication \(\delta S=\delta\langle K\rangle\). ([arXiv][3])

Faulkner et al. (2013), *Gravitation from Entanglement in Holographic CFTs* — première loi de l’intrication et équations gravitationnelles linéarisées dans le cadre holographique. ([arXiv][6])

Jacobson (2015), *Entanglement Equilibrium and the Einstein Equation* — équilibre d’intrication et équation d’Einstein semi-classique. ([arXiv][8])

Czech et al. (2017), *Modular Berry Connection* — connexion modulaire et longueurs holographiques. ([arXiv][4])

Czech, de Boer, Ge & Lamprou (2019), *A Modular Sewing Kit for Entanglement Wedges* — relation entre courbure de Berry modulaire et courbure de Riemann du bulk holographique. ([arXiv][5])

[1]: https://arxiv.org/abs/gr-qc/9406019 "Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories"
[2]: https://arxiv.org/pdf/2305.18519 "Quantum chi-squared tomography and mutual information"
[3]: https://arxiv.org/abs/1305.3182 "Relative Entropy and Holography"
[4]: https://arxiv.org/abs/1712.07123 "Modular Berry Connection"
[5]: https://arxiv.org/abs/1903.04493 "A Modular Sewing Kit for Entanglement Wedges"
[6]: https://arxiv.org/abs/1312.7856 "Gravitation from Entanglement in Holographic CFTs"
[7]: https://arxiv.org/abs/gr-qc/9504004 "Thermodynamics of Spacetime: The Einstein Equation of State"
[8]: https://arxiv.org/abs/1505.04753 "Entanglement Equilibrium and the Einstein Equation"
