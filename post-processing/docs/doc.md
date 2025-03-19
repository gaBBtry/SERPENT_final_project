De nombreux concepts de combustibles ou d'assemblages alternatifs pour le multi-recyclage du Pu en REP ont été étudiés et présentés dans la littérature. Le concept MOXEUS, appelé également MIX, est un combustible homogène à base de plutonium et d'uranium enrichi, chargé dans les 264 crayons d'un assemblage standard de REP. L'homogénéité du combustible permet de s'affranchir des problématiques d'interface : combustible à base d'uranium/combustible à base de plutonium. Cependant, de grandes capacités en termes de fabrication du combustible, transport et stockage seraient requises. A chaque recyclage, la teneur en plutonium dans le combustible est fixée à la valeur maximale autorisée. Ensuite, l'enrichissement en ${ }^{235} \mathrm{U}$ est ajusté, en tenant compte de l'isotopie du plutonium à recycler, de manière à assurer la longueur d'irradiation requise. Dans le cadre de ces travaux, c'est le combustible MOXEUS qui a été choisi pour l'étude de l'incinération du plutonium en REP. C'est un combustible homogène, pouvant s'intégrer à un assemblage de REP traditionnel, et donc plus simple à modéliser que d'autres concepts. Il présente, de plus, une capacité élevée d'incinération du plutonium comme le montre le tableau 2.5 ci-dessous.

**Table 2.5 - Consommation et production d'uranium, de plutonium et d'actinides mineurs, à l'équilibre, dans les cycles associés aux combustibles MOXEUS, CORAIL, APA et DUPLEX proposés dans [25]. La fraction du parc requise pour stabiliser l'inventaire en plutonium est également indiquée.**

| Concept | Consommation d'U <br> naturel $(\mathrm{kg} / \mathrm{TWh})$ | Consommation <br> de $\mathrm{Pu}(\mathrm{kg} / \mathrm{TWh})$ | Production <br> d'AM $(\mathrm{kg} / \mathrm{TWh})$ | Fraction <br> du parc |
| :--: | :--: | :--: | :--: | :--: |
| MOXEUS | 14.2 | 58 | 22.5 | 0.31 |
| CORAIL | 15.0 | 7 | 9.4 | 0.79 |
| DUPLEX | 14.4 | 25 | 9.5 | 0.51 |
| APA | 9.9 | 60 | 12.1 | 0.30 |
| MOX | 0 | 70 | 17.4 | - |

Comme le plutonium utilisé pour construire le combustible MOXEUS peut provenir de sources différentes (REP UOX, REP MOX, ...) ayant des burn-ups de décharge et des temps de refroidissement différents, son isotopie peut être très variée. En ajoutant un possible enrichissement en ${ }^{235} \mathrm{U}$, cela implique qu'une grande variété de compositions isotopiques de combustible MOXEUS neuf peut être rencontrée. Pour le combustible MOXEUS, l'espace isotopique est composé de 8 dimensions : les proportions des isotopes ${ }^{238-242} \mathrm{Pu}$ dans le vecteur plutonium, la teneur en plutonium ainsi que les proportions $\mathrm{d}^{\prime 235} \mathrm{U}$ et $\mathrm{d}^{\prime 238} \mathrm{U}$ dans le combustible MOXEUS. Ces dimensions sont ensuite contraintes par leurs valeurs minimales et maximales.

Pour contraindre l'espace isotopique du combustible MOXEUS, les limites de l'espace isotopique du combustible MOX sont prises comme point de départ. A partir de cet espace, la dimension de $\mathrm{I}^{\prime 235} \mathrm{U}$ (correspondant initialement à la proportion $\mathrm{d}^{\prime 235} \mathrm{U}$ dans le support d'uranium appauvri), est élargi jusqu'à l'enrichissement maximal, autorisé par l'ASN, lors de la fabrication du combustible UOX neuf, environ 5\%. La teneur en plutonium maximale dans le combustible est fixée à $16 \%$, soit l'ordre de grandeur de la teneur maximale estimée pour les REP. Ensuite, comme le combustible MOXEUS est dédié au multi-recyclage, les vecteurs plutonium rencontrés peuvent être très dégradés. Les proportions du ${ }^{240} \mathrm{Pu}$ et du ${ }^{242} \mathrm{Pu}$ dans le vecteur plutonium peuvent donc être amenées à augmenter et réciproquement celles du ${ }^{239} \mathrm{Pu}$ et du ${ }^{241} \mathrm{Pu}$ à diminuer. A partir de ces considérations, un premier espace isotopique contraint par les bornes minimales et maximales de chacune de ses dimensions est établi. Il est présenté dans le tableau 2.6 extrait de la thèse de F. Courtin.

**Table 2.6 - Proportions massiques minimales et maximales (en \%) de l' ${ }^{235} \mathrm{U}$ et du plutonium $\left(w_{\mathrm{Pu}}\right)$ dans le combustible neuf ainsi que de chaque isotope du plutonium dans le vecteur plutonium du combustible MOXEUS neuf.**

|  | ${ }^{235} \mathrm{U}$ | $\mathrm{w}_{\mathrm{Pu}}$ | ${ }^{238} \mathrm{Pu}$ | ${ }^{239} \mathrm{Pu}$ | ${ }^{240} \mathrm{Pu}$ | ${ }^{241} \mathrm{Pu}$ | ${ }^{242} \mathrm{Pu}$ |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| min | 0.25 | 0 | 0.5 | 10 | 10 | 0 | 1.5 |
| max | 5 | 16 | 8 | 80 | 40 | 25 | 35 |

La géométrie de la simulation est un assemblage infini de REP constitué d'un réseau de 17x17 crayons de combustibles. Des conditions aux limites réfléchissantes sont utilisées. Les données relatives à la géométrie ainsi qu'aux matériaux de cet assemblage sont regroupées dans les tableaux 2.8 et 2.9 .

**Table 2.8 - Données géométriques de l'assemblage de REP simulé.**

| Nombre de crayons de combustible | 264 |
| :-- | :-- |
| Nombre de tubes guides | 24 |
| Nombre de tubes d'instrumentation | 1 |
| Pas du réseau | 1.262 cm |
| Rayon de la pastille | 0.410 cm |
| Rayon externe de la gaine | 0.475 cm |
| Rayon interne des tubes guides | 0.550 cm |
| Rayon externe des tubes guides | 0.616 cm |
| Hauteur active de l'assemblage | 366 cm |

**Table 2.9 - Données des matériaux de l'assemblage de REP simulé.**

| Densité de puissance thermique | $30 \mathrm{~W} . \mathrm{g}^{-1}$ d'oxyde |
| :-- | :-- |
| Densité du combustible | $10.02 \mathrm{~g} . \mathrm{cm}^{-3}$ |
| Température du combustible | 923 K |
| Densité de l'eau | $0.716 \mathrm{~g} . \mathrm{cm}^{-3}$ |
| Température de l'eau | 577 K |
| Fraction molaire de Bore | 600 ppm |
| Matériau de la gaine | Zircaloy 4 |
| Densité de la gaine | $5.763 \mathrm{~g} . \mathrm{cm}^{-3}$ |
| Température de la gaine | 577 K |

Votre mission consistera à réaliser des simulations d'irradiation d'une vingtaine de compositions isotopiques de combustible MOXEUS, jusqu'à 2205 jours d'irradiation ( $\simeq 6$ ans ou $75 \mathrm{GWj} / \mathrm{t}$ ). Vos compositions isotopiques devront explorer l'espace des paramètres dans les limites du tableau 2.6 et permettre d'étudier à la fois la neutronique et l'évolution de la composition isotopique dans le temps en fonction des compositions de départ.

Une précaution doit être prise à propos de la production du ${ }^{135} \mathrm{Xe}$. En effet, cet isotope produit directement lors de la fission ou lors de la décroissance d'autres produits de fission, est caractérisé par une section efficace de capture des neutrons thermiques très élevée ( $\simeq 3 \cdot 10^{6}$ barns). Son impact sur le spectre neutronique est donc important et doit être correctement pris en compte. Comme sa demi-vie est faible ( $\simeq 9.14$ heures), la mise à l'équilibre de la quantité de ${ }^{135} \mathrm{Xe}$ en cœur est atteinte après 1 ou deux jours d'irradiation. Durant les premiers jours, un découpage en temps assez fin doit donc être réalisé. Pour les simulations réalisées ici, un découpage en pas en temps de 1 jour durant les 5 premiers jours d'irradiation sera choisi. Un découpage en 80 pas en temps au total ( 6 pas en temps pour la mise à l'équilibre du ${ }^{135} \mathrm{Xe}$ puis 74 pas en temps) sera choisi. Après la mise à l'équilibre du ${ }^{135} \mathrm{Xe}$, cela correspond à des pas en temps de 30 jours ou $1 \mathrm{GWj} / \mathrm{t}$.

Dans le tableau 2.7 ci-dessous, sont donnés des paramètres de simulation réalisés avec un autre code que SERPENT pour vous donner quelques repères quant à vos choix de simulation. Cependant le temps de calcul induit par le nombre de neutrons par cycles et le nombre de cycles pourrait vous conduire à adopter des nombres plus réduits.

**Table 2.7 - Paramètres de la simulation MURE d'un assemblage de REP.**

| Code de transport neutronique | MCNP6 |
| :-- | :-- |
| Code d'évolution | MURE |
| Nombre de cycles inactifs | 5 |
| Nombre de cycles actifs | 20 |
| Nombre de neutrons par cycle | 10000 |
| Nombre de groupes d'énergie | 17900 |
| Sections efficaces, rendements de fission, S( $\alpha, \beta$ ) | JEFF 3.1.1 |
| Seuil de demi-vie | 1 h |
| Seuil sur les sections efficaces | $10^{-6}$ barns |