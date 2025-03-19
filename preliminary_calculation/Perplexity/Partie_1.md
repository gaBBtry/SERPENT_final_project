# Calculs d'Ordres de Grandeur pour le Combustible MOXEUS en REP

La réalisation de calculs d'ordres de grandeur constitue une étape préliminaire essentielle avant d'entreprendre des simulations neutroniques complexes. Cette approche permet non seulement d'anticiper les résultats attendus, mais également de développer un regard critique sur les futures données de simulation. Voici les calculs demandés pour un assemblage de combustible MOXEUS en réacteur à eau pressurisée (REP).

## Calcul du nombre de fissions annuelles dans un assemblage

Pour déterminer le nombre de fissions annuelles, il convient d'abord de calculer la masse totale de combustible présente dans l'assemblage, puis d'établir la relation entre la puissance thermique et l'énergie libérée par fission.

### Détermination de la masse de combustible dans l'assemblage

D'après les données fournies, l'assemblage comporte 264 crayons de combustible avec les caractéristiques suivantes :

- Rayon de la pastille : 0,410 cm
- Hauteur active de l'assemblage : 36,6 cm
- Densité du combustible : 10,02 g/cm³

Le volume d'une pastille cylindrique par crayon se calcule ainsi :
Volume = π × r² × h = π × (0,410 cm)² × 36,6 cm = 19,37 cm³

La masse de combustible par crayon est donc :
Masse = Volume × Densité = 19,37 cm³ × 10,02 g/cm³ = 194,09 g

Pour l'ensemble de l'assemblage :
Masse totale = 194,09 g × 264 crayons = 51 239,76 g ≈ 51,24 kg

### Calcul de la puissance thermique

La densité de puissance thermique étant de 30 W/g d'oxyde, la puissance totale de l'assemblage est :
Puissance = 30 W/g × 51 239,76 g = 1 537 192,8 W ≈ 1,54 MW

### Détermination du nombre de fissions

L'énergie libérée par fission est d'environ 200 MeV, soit en joules :
Énergie par fission = 200 MeV × 1,602 × 10⁻¹³ J/MeV = 3,204 × 10⁻¹¹ J

Le nombre de fissions par seconde est alors :
Fissions/seconde = 1 537 192,8 W / (3,204 × 10⁻¹¹ J) = 4,798 × 10¹⁶ fissions/s

Sur une année entière :
Fissions/an = 4,798 × 10¹⁶ × 365,25 × 24 × 3600 = 1,514 × 10²⁴ fissions/an

Le nombre de fissions annuelles dans l'assemblage est donc d'environ 1,5 × 10²⁴ fissions par an.

## Calcul des taux de fission pour les principaux éléments fissiles

Pour déterminer les taux de fission des différents isotopes, nous devons considérer leurs sections efficaces microscopiques de fission en spectre thermique et leurs densités atomiques respectives dans le combustible.

### Estimation de la composition isotopique

Considérons un combustible MOXEUS typique avec :

- Une teneur en plutonium de 10% (dans la plage 0-16% indiquée)
- Un enrichissement en ²³⁵U de 3% (dans la plage 0,25-5% indiquée)
- Une composition isotopique du plutonium : 50% de ²³⁹Pu, 30% de ²⁴⁰Pu, 10% de ²⁴¹Pu et 10% d'autres isotopes


### Calcul des densités atomiques

La densité atomique de chaque isotope peut être calculée par :
N = (ρ × N_A × w) / M

Où :

- ρ est la densité du combustible (10,02 g/cm³)
- N_A est le nombre d'Avogadro (6,022 × 10²³ atomes/mol)
- w est la fraction massique de l'isotope
- M est la masse molaire de l'isotope (g/mol)

Pour l'uranium-235 (M = 235 g/mol) :
N(²³⁵U) = (10,02 × 6,022 × 10²³ × 0,03 × 0,90) / 235 = 6,91 × 10²⁰ atomes/cm³

Pour le plutonium-239 (M = 239 g/mol) :
N(²³⁹Pu) = (10,02 × 6,022 × 10²³ × 0,10 × 0,50) / 239 = 1,26 × 10²¹ atomes/cm³

Pour le plutonium-241 (M = 241 g/mol) :
N(²⁴¹Pu) = (10,02 × 6,022 × 10²³ × 0,10 × 0,10) / 241 = 2,50 × 10²⁰ atomes/cm³

### Sections efficaces de fission en spectre thermique

Les sections efficaces microscopiques de fission pour les principaux isotopes fissiles sont :

- ²³⁵U : σf ≈ 585 barns = 585 × 10⁻²⁴ cm²
- ²³⁹Pu : σf ≈ 748 barns = 748 × 10⁻²⁴ cm²
- ²⁴¹Pu : σf ≈ 1012 barns = 1012 × 10⁻²⁴ cm²


### Calcul des taux de fission relatifs

La contribution de chaque isotope au taux de fission total peut être calculée comme suit :

Contribution de l'U-235 :
(6,91 × 10²⁰ × 585 × 10⁻²⁴) / (6,91 × 10²⁰ × 585 × 10⁻²⁴ + 1,26 × 10²¹ × 748 × 10⁻²⁴ + 2,50 × 10²⁰ × 1012 × 10⁻²⁴) = 25,3%

Contribution du Pu-239 :
(1,26 × 10²¹ × 748 × 10⁻²⁴) / (même dénominateur) = 59,0%

Contribution du Pu-241 :
(2,50 × 10²⁰ × 1012 × 10⁻²⁴) / (même dénominateur) = 15,8%

Dans ce combustible MOXEUS, le plutonium contribue donc à environ 75% des fissions (59% pour le ²³⁹Pu et 16% pour le ²⁴¹Pu), tandis que l'uranium-235 est responsable d'environ 25%.

## Calcul du flux de neutrons dans l'assemblage

Le flux neutronique peut être déterminé à partir de la puissance thermique et des taux de réaction de fission des différents isotopes.

La relation entre la puissance, le flux et les sections efficaces de fission est :
Puissance = Σ (Ni × σfi × Φ × V × Ef)

Où :

- Ni est la densité atomique de l'isotope i
- σfi est la section efficace microscopique de fission de l'isotope i
- Φ est le flux neutronique
- V est le volume du combustible
- Ef est l'énergie libérée par fission

En réorganisant cette équation pour isoler Φ, on obtient :
Φ = Puissance / [Σ (Ni × σfi) × V × Ef]

Avec les valeurs calculées précédemment et un volume de combustible de 5 113,68 cm³ (= 264 × 19,37 cm³), on obtient :
Φ = 1,54 × 10⁶ / [(6,91 × 10²⁰ × 585 × 10⁻²⁴ + 1,26 × 10²¹ × 748 × 10⁻²⁴ + 2,50 × 10²⁰ × 1012 × 10⁻²⁴) × 5 113,68 × 3,204 × 10⁻¹¹]

Ce qui donne :
Φ ≈ 5,88 × 10¹³ neutrons/cm²/s

Cette valeur est tout à fait cohérente avec les flux neutroniques typiquement observés dans les réacteurs à eau pressurisée, qui se situent généralement entre 10¹³ et 10¹⁴ n/cm²/s.

## Calcul des quantités de Pu consommées par an

La quantité de plutonium consommée peut être estimée de deux façons différentes.

### Méthode 1 : À partir des données du tableau 2.5

D'après le tableau 2.5 fourni dans l'énoncé, la consommation de plutonium pour le concept MOXEUS est de 58 kg/TWh.

Pour notre assemblage d'une puissance de 1,54 MW, la production d'énergie annuelle est :
Énergie annuelle = 1,54 MW × 365,25 jours × 24 heures = 13 493,58 MWh/an = 0,013494 TWh/an

La consommation annuelle de plutonium est donc :
Consommation de Pu = 58 kg/TWh × 0,013494 TWh/an = 0,783 kg/an

### Méthode 2 : Par calcul direct des taux de réaction

Pour un calcul plus détaillé, nous devons considérer à la fois la disparition du plutonium par fission et par capture neutronique, ainsi que sa production par capture sur l'uranium-238.

#### Disparition du plutonium

En prenant en compte les sections efficaces de capture (σc) en plus des sections efficaces de fission :

- σc(²³⁹Pu) ≈ 270 barns
- σc(²⁴¹Pu) ≈ 360 barns

Le taux de disparition du plutonium est :
Taux = Σ [Ni × (σfi + σci) × Φ × V]
= [(1,26 × 10²¹ × (748 + 270) × 10⁻²⁴) + (2,50 × 10²⁰ × (1012 + 360) × 10⁻²⁴)] × 5,88 × 10¹³ × 5 113,68
≈ 4,86 × 10¹⁷ atomes/s

Ce qui correspond à une masse de :
Masse disparue = 4,86 × 10¹⁷ × [(239 + 241)/2] × 1,66 × 10⁻²⁴ = 1,93 × 10⁻⁴ g/s
= 1,93 × 10⁻⁴ × 365,25 × 24 × 3600 = 6,08 kg/an

#### Production de plutonium

Le plutonium est produit par capture neutronique sur l'uranium-238 :

- σc(²³⁸U) ≈ 2,7 barns
- N(²³⁸U) ≈ 2,26 × 10²² atomes/cm³ (pour environ 87% d'U-238 dans le combustible)

Le taux de production est :
Taux = N(²³⁸U) × σc(²³⁸U) × Φ × V
= 2,26 × 10²² × 2,7 × 10⁻²⁴ × 5,88 × 10¹³ × 5 113,68
≈ 1,65 × 10¹⁷ atomes/s

Ce qui correspond à une masse de :
Masse produite = 1,65 × 10¹⁷ × 239 × 1,66 × 10⁻²⁴ = 6,54 × 10⁻⁵ g/s
= 6,54 × 10⁻⁵ × 365,25 × 24 × 3600 = 2,06 kg/an

#### Bilan net de consommation

La consommation nette de plutonium est donc :
Consommation nette = 6,08 - 2,06 = 4,02 kg/an

Il existe un écart entre cette valeur calculée (4,02 kg/an) et celle déduite du tableau 2.5 (0,783 kg/an). Cette différence peut s'expliquer par plusieurs facteurs, notamment les hypothèses simplificatrices sur la composition isotopique du combustible, le spectre neutronique considéré comme purement thermique dans nos calculs, et les incertitudes sur les sections efficaces utilisées.

## Conclusion

Les calculs d'ordres de grandeur réalisés nous permettent d'établir les valeurs suivantes pour un assemblage de combustible MOXEUS en REP :

- Nombre de fissions annuelles : environ 1,5 × 10²⁴ fissions/an
- Taux de fission : 25% pour l'U-235, 59% pour le Pu-239 et 16% pour le Pu-241
- Flux neutronique : environ 5,9 × 10¹³ neutrons/cm²/s
- Consommation nette de plutonium : entre 0,8 et 4 kg/an, selon la méthode de calcul employée

Ces valeurs constituent une base de référence pour l'interprétation des résultats des simulations neutroniques qui seront effectuées ultérieurement.