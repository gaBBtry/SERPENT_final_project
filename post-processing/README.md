# Projet d'Analyse SERPENT - Documentation

## Description du projet

Ce projet est un ensemble d'outils d'analyse pour les simulations du projet final SERPENT. Les scripts permettent d'analyser et de visualiser les résultats des simulations de combustible MOXEUS dans un assemblage REP, qui est un concept de combustible homogène à base de plutonium et d'uranium enrichi.

Le projet fournit des outils pour analyser différents aspects des simulations, notamment :
- L'évolution du facteur de multiplication infini (k-inf)
- Les taux de fission
- L'inventaire isotopique
- Les sections efficaces
- L'évolution des flux neutroniques

## Structure du projet

```
.
├── data/                  # Données des simulations MOXEUS
│   ├── MOXEUS_00001/      # Simulation 1
│   ├── MOXEUS_00002/      # Simulation 2
│   └── ...                # Autres simulations
├── docs/                  # Documentation et références
├── figures/               # Graphiques générés par les scripts
├── scripts/               # Scripts d'analyse Python
│   ├── interpretations.py # Fonctions communes pour l'analyse des données
│   ├── plot_cross_sction.py
│   ├── plot_fission_rate.py
│   ├── plot_flow_evolution.py
│   ├── plot_inventory.py
│   └── plot_k_inf.py
└── run.sh                 # Script shell pour lancer les analyses
```

## Format des données

Chaque dossier de simulation (ex: MOXEUS_00001/) contient les fichiers suivants :
- `.se` : Fichier d'entrée SERPENT
- `.se.out` : Fichier de sortie SERPENT
- `.se.seed` : Fichier de graine pour la génération de nombres aléatoires
- `.se_dep.m` : Données d'évolution au format MATLAB
- `.se_res.m` : Données de résultats au format MATLAB
- `log.txt` : Journal de la simulation

## Utilisation

### Lancement des scripts

Pour exécuter les scripts d'analyse, utilisez le script `run.sh` :

```bash
./run.sh
```

Ce script affiche un menu interactif qui permet de sélectionner les analyses à exécuter :

1. `plot_cross_sction.py` - Analyse des sections efficaces
2. `plot_fission_rate.py` - Analyse des taux de fission
3. `plot_inventory.py` - Analyse de l'inventaire isotopique
4. `plot_flow_evolution.py` - Analyse de l'évolution des flux
5. `plot_k_inf.py` - Analyse de l'évolution du facteur k-infini

Vous pouvez exécuter un script spécifique en entrant son numéro, ou exécuter tous les scripts en entrant "a".

### Description des scripts

#### plot_k_inf.py
Extrait et trace l'évolution du facteur de multiplication infini (k-inf) en fonction du temps et du burnup. Les données sont extraites du fichier log.txt de chaque simulation.

#### plot_inventory.py
Analyse l'évolution de l'inventaire isotopique au cours de l'irradiation. Ce script extrait les données du fichier .se_dep.m et trace l'évolution des concentrations isotopiques.

#### plot_cross_sction.py
Analyse les sections efficaces microscopiques et macroscopiques des différents isotopes présents dans le combustible.

#### plot_fission_rate.py
Analyse les taux de fission des différents isotopes fissiles et leur contribution au taux de fission total.

#### plot_flow_evolution.py
Analyse l'évolution du flux neutronique et sa distribution énergétique au cours de l'irradiation.

#### interpretations.py
Contient des fonctions communes utilisées par les autres scripts pour l'extraction et l'analyse des données.

## Contexte technique

### Le combustible MOXEUS

Le MOXEUS est un concept de combustible homogène à base de plutonium et d'uranium enrichi, chargé dans les 264 crayons d'un assemblage standard de REP. L'homogénéité du combustible permet de s'affranchir des problématiques d'interface entre combustible à base d'uranium et combustible à base de plutonium.

Les simulations explorent une variété de compositions isotopiques initiales, en faisant varier :
- Les proportions des isotopes Pu-238 à Pu-242 dans le vecteur plutonium
- La teneur en plutonium (0-16%)
- L'enrichissement en U-235 (0.25-5%)

### Paramètres de simulation

Les simulations couvrent jusqu'à 2205 jours d'irradiation (~6 ans ou 75 GWj/t), avec une attention particulière aux premiers jours pour capturer la mise à l'équilibre du Xe-135. Le découpage temporel comprend généralement :
- Des pas de 1 jour durant les 5 premiers jours
- Des pas d'environ 30 jours (1 GWj/t) par la suite
- Un total d'environ 80 pas de temps

## Références

Pour plus d'informations sur les modèles et les paramètres de simulation, consultez les documents dans le dossier `docs/`, notamment :
- `doc.md` : Description détaillée du combustible MOXEUS et des paramètres de simulation
- `SERPENT_manual.pdf` : Manuel du code SERPENT
- `these_Courtin_Fanny.pdf` : Thèse contenant des informations sur le concept MOXEUS 