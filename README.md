# Analyse de Simulations SERPENT - Documentation

## Description du projet

Ce projet fournit des outils d'analyse pour les simulations SERPENT du combustible MOXEUS dans un assemblage REP. Il permet d'analyser et visualiser:
- L'évolution du facteur de multiplication infini (k-inf)
- Les taux de fission
- L'inventaire isotopique
- Les sections efficaces
- L'évolution des flux neutroniques

## Prérequis

- Python 3.6+
- Dépendances: numpy, matplotlib, pandas, seaborn, scipy
  ```bash
  pip install numpy matplotlib pandas seaborn scipy
  ```

## Structure du projet

```
.
├── data/                  # Simulations MOXEUS
│   ├── MOXEUS_00001/      # Simulation 1 
│   └── ...                # Autres simulations
├── figures/               # Graphiques et résumés à générer
├── scripts/               # Scripts d'analyse Python
│   ├── interpretations.py
│   ├── plot_cross_sction.py
│   ├── plot_fission_rate.py
│   ├── plot_flow_evolution.py
│   ├── plot_inventory.py
│   └── plot_k_inf.py
└── run.sh                 # Script pour lancer les analyses
```

## Format des données

Chaque dossier de simulation contient:
- `.se` : Fichier d'entrée SERPENT
- `.se.out` : Fichier de sortie
- `.se_dep.m` : Données d'évolution (format MATLAB)
- `.se_res.m` : Résultats (format MATLAB)
- `log.txt` : Journal de la simulation

## Utilisation

### Lancement des analyses

Exécutez le script principal:
```bash
./run.sh
```

Ce script affiche un menu permettant de sélectionner:
1. Analyse des sections efficaces
2. Analyse des taux de fission
3. Analyse de l'inventaire isotopique
4. Analyse de l'évolution des flux
5. Analyse de l'évolution du k-infini

### Description des scripts

- **plot_k_inf.py**: Évolution du facteur de multiplication infini
- **plot_inventory.py**: Évolution de l'inventaire isotopique
- **plot_cross_sction.py**: Analyse des sections efficaces
- **plot_fission_rate.py**: Analyse des taux de fission
- **plot_flow_evolution.py**: Évolution du flux neutronique
- **interpretations.py**: Fonctions communes utilisées par les autres scripts

## Résolution des problèmes courants

- **Graphiques incorrects**: Vérifiez les versions de matplotlib et seaborn
- **Erreurs d'analyse des fichiers .m**: Vérifiez le format et l'intégrité des fichiers
- **Fichiers manquants**: Assurez-vous que tous les fichiers nécessaires sont présents
- **Erreurs de mémoire**: Limitez le nombre de simulations traitées simultanément 