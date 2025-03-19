# Guide d'installation et de configuration

Ce document fournit les instructions pour installer et configurer l'environnement nécessaire pour exécuter les scripts d'analyse du projet SERPENT.

## Prérequis

- Python 3.6 ou supérieur
- Accès aux fichiers de simulation SERPENT (format .se, .se.out, .se_dep.m, .se_res.m)

## Installation des dépendances

Les scripts utilisent plusieurs bibliothèques Python pour l'analyse de données et la visualisation. Installez-les avec pip :

```bash
pip install numpy matplotlib pandas seaborn scipy
```

## Structure des dossiers

Pour que les scripts fonctionnent correctement, assurez-vous d'avoir la structure de dossiers suivante :

```
.
├── data/
│   ├── MOXEUS_00001/
│   ├── MOXEUS_00002/
│   └── ...
├── docs/
├── figures/
│   ├── cross_sections/
│   ├── fission_rates/
│   ├── flux/
│   ├── inventory/
│   └── k_inf/
├── scripts/
└── run.sh
```

Si les dossiers de figures n'existent pas, ils seront créés automatiquement par les scripts.

## Préparation des données

1. Assurez-vous que chaque dossier de simulation (ex: MOXEUS_00001/) contient au minimum les fichiers suivants :
   - `MOXEUS_XXXXX.se_dep.m` - Fichier de données d'évolution
   - `MOXEUS_XXXXX.se_res.m` - Fichier de résultats
   - `log.txt` - Journal de la simulation

2. Placez tous les dossiers de simulation dans le répertoire `data/`.

## Configuration des scripts

Si vous souhaitez modifier les isotopes analysés ou d'autres paramètres, vous pouvez éditer les fichiers de script correspondants :

- `scripts/plot_inventory.py` : Modifiez les listes `plutonium_isotopes`, `uranium_isotopes`, `fission_products` ou `minor_actinides` pour changer les isotopes analysés.

- `scripts/plot_cross_sction.py` : Modifiez les réactions analysées dans la fonction principale.

- `scripts/plot_fission_rate.py` : Modifiez la liste `fissile_isotopes` pour changer les isotopes fissiles analysés.

## Personnalisation des graphiques

Pour personnaliser l'apparence des graphiques, vous pouvez modifier les paramètres suivants dans les scripts :

- Palette de couleurs : Modifiez les appels à `plt.cm` ou `sns.color_palette()`
- Taille des graphiques : Modifiez les paramètres `figsize` dans les appels à `plt.figure()`
- Étiquettes et titres : Modifiez les appels à `plt.xlabel()`, `plt.ylabel()` et `plt.title()`

## Exécution des scripts

Vous pouvez exécuter les scripts de deux façons :

### 1. Utilisation du script run.sh

Le script `run.sh` fournit une interface conviviale pour exécuter les scripts d'analyse :

```bash
./run.sh
```

Si le script n'est pas exécutable, accordez-lui les permissions nécessaires :

```bash
chmod +x run.sh
```

### 2. Exécution directe des scripts Python

Vous pouvez également exécuter chaque script individuellement :

```bash
python scripts/plot_k_inf.py
python scripts/plot_inventory.py
python scripts/plot_cross_sction.py
python scripts/plot_fission_rate.py
python scripts/plot_flow_evolution.py
```

## Résolution des problèmes courants

### Les graphiques ne s'affichent pas correctement

- Vérifiez que vous avez les versions à jour de matplotlib et seaborn
- Essayez d'exécuter `matplotlib.use('Agg')` avant d'importer pyplot si vous êtes dans un environnement sans interface graphique

### Erreurs d'analyse des fichiers .m

- Vérifiez que les fichiers .m suivent le format attendu
- Assurez-vous que les fichiers ne sont pas corrompus ou incomplets

### Fichiers manquants

- Si vous recevez des erreurs concernant des fichiers manquants, vérifiez que tous les fichiers nécessaires sont présents dans les dossiers de simulation

### Erreurs de mémoire

- Si vous rencontrez des erreurs de mémoire lors du traitement de grands fichiers, essayez de limiter le nombre de simulations traitées à la fois 