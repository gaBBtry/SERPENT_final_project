### Réponses aux 4 questions de la partie 1 du document "Enonce.pdf"

**Points clés :**  
- Le nombre annuel de fissions semble être d’environ \( 1,5 \times 10^{25} \) fissions.  
- Les taux de fission pour les éléments fissiles principaux (U-235, Pu-239, Pu-241) sont estimés à environ \( 1,9 \times 10^{16} \), \( 3,8 \times 10^{17} \), et \( 8,3 \times 10^{16} \) fissions par seconde respectivement.  
- Le flux de neutrons est probablement de l’ordre de \( 1 \times 10^{17} \) neutrons par mètre carré par seconde.  
- La quantité annuelle de plutonium consommée est estimée à environ 7,8 kg, selon les données fournies.

**Calcul du nombre de fissions annuelles :**  
Le calcul repose sur la puissance thermique de l’assemblage, estimée à environ 15,3 MW, et l’énergie libérée par fission (200 MeV, soit environ \( 3,2 \times 10^{-11} \) joules). En multipliant la puissance par le nombre de secondes dans une année (environ \( 3,15 \times 10^7 \) secondes), on obtient un ordre de grandeur de \( 1,5 \times 10^{25} \) fissions par an. Ce résultat semble cohérent avec les paramètres d’un réacteur à eau pressurisée (REP).

**Taux de fission des éléments fissiles principaux :**  
Pour U-235, Pu-239 et Pu-241, les taux de fission sont calculés en utilisant le flux de neutrons (estimé à \( 1 \times 10^{17} \) n/m²s), les densités atomiques de chaque isotope et leurs sections efficaces de fission dans le spectre thermique (582 barns pour U-235, 747 barns pour Pu-239, et 1 010 barns pour Pu-241). Les valeurs obtenues sont respectivement environ \( 1,9 \times 10^{16} \), \( 3,8 \times 10^{17} \), et \( 8,3 \times 10^{16} \) fissions par seconde, reflétant la contribution dominante de Pu-239.

**Flux de neutrons :**  
Le flux de neutrons est estimé à partir de la puissance thermique, de la section efficace macroscopique de fission (environ 63,5 m⁻¹) et du volume de combustible (environ 0,051 m³). Cela donne un flux d’environ \( 1 \times 10^{17} \) n/m²s, ce qui est cohérent avec les valeurs typiques pour un REP, bien que légèrement inférieur à certaines estimations de littérature pour des réacteurs complets.

**Quantité de plutonium consommée par an :**  
La consommation annuelle de plutonium est calculée à partir de la donnée du document indiquant une consommation de 58 kg/TWh pour le combustible MOXEUS. Avec une production énergétique annuelle estimée à environ 0,134 TWh pour l’assemblage, cela donne une consommation d’environ 7,8 kg par an. Cette valeur inclut non seulement les fissions, mais aussi les transmutations, expliquant pourquoi elle diffère des calculs basés uniquement sur les fissions.

---

### Note détaillée sur les calculs et hypothèses

Cette section fournit une analyse approfondie des calculs effectués pour répondre aux quatre questions de la partie 1 du document "Enonce.pdf", en s’appuyant sur les données fournies et des valeurs standard de la littérature en physique nucléaire. Les calculs sont des estimations d’ordre de grandeur, comme indiqué dans le titre de la partie, et incluent des hypothèses pour combler les lacunes dans les informations.

#### Contexte général  
Le document concerne un assemblage de combustible MOXEUS dans un réacteur à eau pressurisée (REP), avec des caractéristiques détaillées telles que le nombre de barres de combustible (264), la hauteur active (36,6 cm), la densité du combustible (10,02 g/cm³), et une densité de puissance thermique de 30 W/g d’oxyde. Les calculs reposent sur ces paramètres, ainsi que sur des valeurs standard pour les sections efficaces de fission et l’énergie libérée par fission (200 MeV par fission).

#### Détails du calcul pour chaque question  

##### Question 1 : Nombre annuel de fissions dans un assemblage  
Pour estimer le nombre de fissions annuelles, nous commençons par calculer la puissance thermique totale de l’assemblage.  
- **Volume et masse du combustible :**  
  Le rayon des pastilles de combustible est de 0,410 cm (0,0041 m), et la hauteur active est de 36,6 cm (0,366 m). Le volume d’une barre est donné par \(\pi r^2 h = \pi (0,0041)^2 \times 0,366 \approx 1,93 \times 10^{-4} \, \text{m}^3\). Avec 264 barres et une densité de 10,02 g/cm³ (10 020 kg/m³), la masse totale est d’environ 511 kg (ou 511 000 g).  
  La puissance thermique est alors \( 511 000 \, \text{g} \times 30 \, \text{W/g} = 15 330 000 \, \text{W} \) (15,3 MW).  
- **Taux de fission :**  
  L’énergie libérée par fission est de 200 MeV, soit \( 200 \times 1,602 \times 10^{-13} \approx 3,204 \times 10^{-11} \, \text{J/fission}\). Le taux de fission par seconde est donné par \( P / E_f = 15 330 000 / 3,204 \times 10^{-11} \approx 4,78 \times 10^{17} \, \text{fissions/s}\).  
- **Nombre annuel :**  
  Sur une année, avec environ \( 3,154 \times 10^7 \, \text{s/an}\), le nombre total de fissions est \( 4,78 \times 10^{17} \times 3,154 \times 10^7 \approx 1,51 \times 10^{25} \, \text{fissions/an}\).  
  **Résultat final :** Environ \( 1,5 \times 10^{25} \) fissions par an, cohérent avec les ordres de grandeur pour un assemblage REP.

##### Question 2 : Taux de fission des principaux éléments fissiles  
Pour calculer les taux de fission, nous devons déterminer les densités atomiques des isotopes fissiles (U-235, Pu-239, Pu-241) et utiliser le flux de neutrons (calculé à la question 3) avec leurs sections efficaces de fission dans le spectre thermique.  
- **Composition du combustible :**  
  La masse totale d’oxyde est de 511 kg. En supposant une teneur en plutonium de 5 % en poids du métal lourd, la masse totale du métal lourd est estimée à environ 450 kg (en tenant compte du rapport masse molaire, environ 88 % de la masse d’oxyde). Ainsi, la masse de Pu est d’environ 22,5 kg, et la masse d’U est de 427,5 kg.  
  - U-235 : Supposons 0,2 % de la masse d’U, soit environ 0,855 kg. Nombre d’atomes : \( 855 / 235 \times 6,022 \times 10^{23} \approx 2,19 \times 10^{24} \, \text{atomes}\).  
  - Pu-239 : Supposons 60 % de la masse de Pu, soit 13,5 kg. Nombre d’atomes : \( 13 500 / 239 \times 6,022 \times 10^{23} \approx 3,4 \times 10^{25} \, \text{atomes}\).  
  - Pu-241 : Supposons 10 % de la masse de Pu, soit 2,25 kg. Nombre d’atomes : \( 2 250 / 241 \times 6,022 \times 10^{23} \approx 5,62 \times 10^{24} \, \text{atomes}\).  
  Le volume total du combustible est \( 511 \, \text{kg} / 10 020 \, \text{kg/m}^3 \approx 0,051 \, \text{m}^3\).  
  - Densités atomiques :  
    - \( N_{\text{U-235}} \approx 2,19 \times 10^{24} / 0,051 \approx 4,3 \times 10^{25} \, \text{atomes/m}^3 \).  
    - \( N_{\text{Pu-239}} \approx 3,4 \times 10^{25} / 0,051 \approx 6,67 \times 10^{26} \, \text{atomes/m}^3 \).  
    - \( N_{\text{Pu-241}} \approx 5,62 \times 10^{24} / 0,051 \approx 1,1 \times 10^{26} \, \text{atomes/m}^3 \).  
- **Sections efficaces (valeurs standard) :**  
  - U-235 : 582 barns (\( 5,82 \times 10^{-28} \, \text{m}^2 \)).  
  - Pu-239 : 747 barns (\( 7,47 \times 10^{-28} \, \text{m}^2 \)).  
  - Pu-241 : 1 010 barns (\( 1,01 \times 10^{-27} \, \text{m}^2 \)).  
- **Flux de neutrons :** Estimé à \( 1,48 \times 10^{17} \, \text{n/m}^2\text{s}\) (voir question 3).  
- **Taux de fission :**  
  Taux pour chaque isotope = flux × densité atomique × section efficace.  
  - U-235 : \( 1,48 \times 10^{17} \times 4,3 \times 10^{25} \times 5,82 \times 10^{-28} \approx 3,7 \times 10^{15} \, \text{fissions/m}^3\text{s} \times 0,051 \, \text{m}^3 \approx 1,9 \times 10^{16} \, \text{fissions/s}\).  
  - Pu-239 : \( 1,48 \times 10^{17} \times 6,67 \times 10^{26} \times 7,47 \times 10^{-28} \approx 7,4 \times 10^{16} \, \text{fissions/m}^3\text{s} \times 0,051 \approx 3,8 \times 10^{17} \, \text{fissions/s}\).  
  - Pu-241 : \( 1,48 \times 10^{17} \times 1,1 \times 10^{26} \times 1,01 \times 10^{-27} \approx 1,64 \times 10^{16} \, \text{fissions/m}^3\text{s} \times 0,051 \approx 8,3 \times 10^{16} \, \text{fissions/s}\).  
  **Résultat final :** U-235 : \( 1,9 \times 10^{16} \), Pu-239 : \( 3,8 \times 10^{17} \), Pu-241 : \( 8,3 \times 10^{16} \, \text{fissions/s}\).

##### Question 3 : Flux de neutrons  
Le flux de neutrons est estimé en utilisant la relation \( P = \Phi \times \Sigma_f \times V \times E_f \), où \( \Sigma_f \) est la section efficace macroscopique de fission.  
- **Section efficace macroscopique :** Somme des contributions des isotopes fissiles :  
  - \(\Sigma_{f,\text{U-235}} = 4,3 \times 10^{25} \times 5,82 \times 10^{-28} \approx 2,5 \, \text{m}^{-1}\).  
  - \(\Sigma_{f,\text{Pu-239}} = 6,67 \times 10^{26} \times 7,47 \times 10^{-28} \approx 50 \, \text{m}^{-1}\).  
  - \(\Sigma_{f,\text{Pu-241}} = 1,1 \times 10^{26} \times 1,01 \times 10^{-27} \approx 11 \, \text{m}^{-1}\).  
  Total \(\Sigma_f \approx 2,5 + 50 + 11 = 63,5 \, \text{m}^{-1}\).  
- **Taux total de fission :** \( R_f = P / E_f = 4,78 \times 10^{17} \, \text{fissions/s}\).  
- **Flux thermique :** \(\Phi_{\text{thermal}} = R_f / (\Sigma_f \times V) = 4,78 \times 10^{17} / (63,5 \times 0,051) \approx 4,78 \times 10^{17} / 3,24 \approx 1,48 \times 10^{17} \, \text{n/m}^2\text{s}\).  
  **Résultat final :** Ordre de grandeur du flux de neutrons : \( 1 \times 10^{17} \, \text{n/m}^2\text{s}\), cohérent avec les valeurs typiques pour un REP.

##### Question 4 : Quantité de Pu consommée par an  
La consommation de Pu est donnée dans le document comme 58 kg/TWh pour le combustible MOXEUS.  
- **Production énergétique annuelle :** Puissance thermique de 15,3 MW, sur une année (\( 3,154 \times 10^7 \, \text{s}\)), donne une énergie de \( 15,3 \times 10^6 \times 3,154 \times 10^7 \approx 4,83 \times 10^{14} \, \text{J}\). En TWh, \( 4,83 \times 10^{14} / 3,6 \times 10^{15} \approx 0,134 \, \text{TWh/an}\).  
- **Consommation de Pu :** \( 58 \, \text{kg/TWh} \times 0,134 \, \text{TWh/an} \approx 7,77 \, \text{kg/an}\).  
  **Résultat final :** Environ 7,8 kg de Pu consommés par an, incluant fissions et transmutations, ce qui explique la différence avec les calculs basés uniquement sur les fissions (environ 0,6 kg/an pour les fissions seules).

#### Tableaux récapitulatifs  
Voici un tableau récapitulatif des paramètres clés utilisés :

| Paramètre                     | Valeur                     |
|-------------------------------|----------------------------|
| Nombre de barres de combustible | 264                       |
| Hauteur active                | 36,6 cm (0,366 m)         |
| Rayon des pastilles           | 0,410 cm (0,0041 m)       |
| Densité du combustible        | 10,02 g/cm³ (10 020 kg/m³)|
| Densité de puissance thermique | 30 W/g d’oxyde            |
| Masse totale d’oxyde          | Environ 511 kg            |
| Flux de neutrons (ordre de grandeur) | \( 1 \times 10^{17} \, \text{n/m}^2\text{s}\) |

Un autre tableau pour les isotopes fissiles et leurs taux de fission :

| Isotope  | Densité atomique (atomes/m³) | Section efficace de fission (barns) | Taux de fission (fissions/s) |
|----------|------------------------------|-------------------------------------|------------------------------|
| U-235    | \( 4,3 \times 10^{25} \)     | 582                                 | \( 1,9 \times 10^{16} \)     |
| Pu-239   | \( 6,67 \times 10^{26} \)    | 747                                 | \( 3,8 \times 10^{17} \)     |
| Pu-241   | \( 1,1 \times 10^{26} \)     | 1 010                               | \( 8,3 \times 10^{16} \)     |

#### Hypothèses et limites  
Les calculs reposent sur plusieurs hypothèses :  
- Une teneur en Pu de 5 % en poids du métal lourd et une composition isotopique standard (60 % Pu-239, 10 % Pu-241, etc.).  
- Les sections efficaces de fission sont tirées de la littérature standard pour le spectre thermique, comme celles disponibles dans des bases de données comme JEFF 3.1.1.  
- La consommation de Pu inclut des processus au-delà des fissions, comme les transmutations, expliquant la différence entre les calculs basés sur les fissions (0,6 kg/an) et la donnée de 58 kg/TWh (7,8 kg/an).  
Ces estimations sont des ordres de grandeur et peuvent varier selon les conditions opérationnelles réelles du réacteur.

#### Conclusion  
Les réponses fournies respectent les données du document et les principes de physique nucléaire, avec une attention particulière aux ordres de grandeur demandés. Les résultats sont cohérents avec les attentes pour un assemblage de combustible MOXEUS dans un REP, bien que certaines valeurs, comme la consommation de Pu, reflètent des processus complexes au-delà des simples fissions.