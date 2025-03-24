# Analyse de Simulations SERPENT - Documentation

## Description du projet

Ce projet permet d'analyser et de visualiser les résultats de simulations SERPENT du combustible MOXEUS dans un assemblage REP. Il génère automatiquement des graphiques pour :
- L'évolution du facteur de multiplication infini (k-inf)
- Les taux de fission
- L'inventaire isotopique
- Les sections efficaces
- L'évolution des flux neutroniques

## Installation

### Prérequis
- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation du projet

1. Cloner le projet :
```bash
git clone [URL_DU_PROJET]
cd SERPENT_final_project
```

2. Créer un environnement virtuel Python :
```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :
- Sur Windows :
```bash
.\.venv\Scripts\activate
```
- Sur macOS/Linux :
```bash
source .venv/bin/activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure du projet

```
.
├── data/                  # Dossier contenant les simulations MOXEUS
│   ├── MOXEUS_00001/     # Première simulation
│   └── ...               # Autres simulations
├── figures/              # Dossier où seront générés les graphiques
├── scripts/              # Scripts d'analyse Python
│   ├── interpretations.py
│   ├── plot_cross_sction.py
│   ├── plot_fission_rate.py
│   ├── plot_flow_evolution.py
│   ├── plot_inventory.py
│   └── plot_k_inf.py
└── run.sh                # Script principal pour lancer les analyses
```

## Utilisation

### Lancement des analyses

1. Assurez-vous que votre environnement virtuel est activé (vous devriez voir `(.venv)` au début de votre ligne de commande)

2. Exécutez le script principal :
```bash
./run.sh
```

3. Choisissez l'analyse souhaitée dans le menu qui s'affiche :
   - 1 : Analyse des sections efficaces
   - 2 : Analyse des taux de fission
   - 3 : Analyse de l'inventaire isotopique
   - 4 : Analyse de l'évolution des flux
   - 5 : Analyse de l'évolution du k-infini

### Description des analyses

1. **Analyse des sections efficaces**
   - Visualise les sections efficaces de capture et de fission
   - Montre l'évolution en fonction du burnup

2. **Analyse des taux de fission**
   - Affiche les taux de fission pour chaque isotope
   - Permet de comparer les contributions des différents isotopes

3. **Analyse de l'inventaire isotopique**
   - Montre l'évolution des concentrations en isotopes
   - Regroupe les isotopes par famille (Uranium, Plutonium, Actinides mineurs)

4. **Analyse de l'évolution des flux**
   - Visualise l'évolution du flux neutronique
   - Inclut un axe secondaire pour le burnup

5. **Analyse de l'évolution du k-infini**
   - Trace l'évolution du facteur de multiplication infini
   - Affiche les erreurs associées

## Résolution des problèmes courants

1. **Le script ne démarre pas**
   - Vérifiez que l'environnement virtuel est activé
   - Assurez-vous que toutes les dépendances sont installées

2. **Les graphiques ne se génèrent pas**
   - Vérifiez que le dossier `data/` contient les fichiers de simulation
   - Assurez-vous que les fichiers ont les extensions correctes (.se, .se.out, etc.)

3. **Erreurs de mémoire**
   - Réduisez le nombre de simulations traitées simultanément
   - Fermez les applications gourmandes en mémoire

## Support

Pour toute question ou problème, n'hésitez pas à :
1. Vérifier la documentation
2. Consulter les commentaires dans les scripts
3. Me contacter directement