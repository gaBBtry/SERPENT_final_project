# Documentation technique des scripts

Ce document fournit une documentation technique détaillée pour chaque script Python utilisé dans le projet d'analyse SERPENT.

## scripts/interpretations.py

Ce module contient des fonctions communes utilisées par les différents scripts d'analyse. Il est responsable de l'extraction, du traitement et de la visualisation des données des simulations SERPENT.

### Fonctions principales

#### `extract_corrector_data(log_file)`
- **Description** : Extrait les données de k_inf (corrector), le temps, le burnup et les erreurs du fichier log.txt.
- **Paramètres** : 
  - `log_file` : Chemin vers le fichier log.txt
- **Retour** : Quatre listes - temps (jours), burnup (MWd/kgU), k_inf, erreurs (en unité de k_eff)

#### `load_m_file(filename)`
- **Description** : Charge les données isotopiques depuis un fichier .m
- **Paramètres** :
  - `filename` : Chemin vers le fichier .m
- **Retour** : Données extraites (jours, identifiants ZAI, densités atomiques, burnup)

#### `get_isotope_data(days, zai, adens, total_adens, isotope_list)`
- **Description** : Extrait les données de densité atomique pour une liste d'isotopes spécifiques
- **Paramètres** :
  - `days` : Liste des jours
  - `zai` : Liste des identifiants ZAI
  - `adens` : Matrice des densités atomiques
  - `total_adens` : Densité atomique totale
  - `isotope_list` : Liste des isotopes à extraire
- **Retour** : Dictionnaire contenant les données pour chaque isotope

#### `calculate_k_inf_derivatives(times, k_infs)`
- **Description** : Calcule les dérivées première et seconde de k_inf par rapport au temps
- **Paramètres** :
  - `times` : Liste des temps
  - `k_infs` : Liste des valeurs de k_inf
- **Retour** : Deux listes - dérivée première, dérivée seconde

#### `calculate_pearson_correlations(k_infs, isotope_data)`
- **Description** : Calcule les corrélations de Pearson entre k_inf et les évolutions isotopiques
- **Paramètres** :
  - `k_infs` : Liste des valeurs de k_inf
  - `isotope_data` : Dictionnaire des données isotopiques
- **Retour** : Dictionnaire des corrélations pour chaque isotope

## scripts/plot_k_inf.py

Ce script analyse et visualise l'évolution du facteur de multiplication infini (k_inf) en fonction du temps et du burnup.

### Fonctions principales

#### `extract_corrector_data(log_file)`
- **Description** : Extrait les données de k_inf du fichier log.txt
- **Paramètres** :
  - `log_file` : Chemin vers le fichier log.txt
- **Retour** : Temps, burnup, k_inf, erreurs

#### `plot_k_inf_evolution(times, burnups, k_infs, errors, sim_name)`
- **Description** : Trace l'évolution de k_inf avec le temps en bas et le burnup en haut
- **Paramètres** :
  - `times` : Liste des temps
  - `burnups` : Liste des burnups
  - `k_infs` : Liste des valeurs de k_inf
  - `errors` : Liste des erreurs
  - `sim_name` : Nom de la simulation
- **Retour** : None (sauvegarde la figure dans figures/k_inf/)

#### Fonction principale
- Parcourt les dossiers de simulation dans data/
- Extrait les données k_inf
- Génère les graphiques d'évolution de k_inf
- Sauvegarde les figures dans le dossier figures/k_inf/

## scripts/plot_inventory.py

Ce script analyse et visualise l'évolution de l'inventaire isotopique au cours de l'irradiation.

### Fonctions principales

#### `load_m_file(filename)`
- **Description** : Charge les données isotopiques depuis un fichier .m
- **Paramètres** :
  - `filename` : Chemin vers le fichier .se_dep.m
- **Retour** : Jours, identifiants ZAI, densités atomiques, burnup

#### `get_isotope_name(zai)`
- **Description** : Convertit un identifiant ZAI en nom d'isotope lisible
- **Paramètres** :
  - `zai` : Identifiant ZAI (format ZZAAAM)
- **Retour** : Nom de l'isotope au format "A-Symbole"

#### `plot_isotope_evolution(days, isotope_data, sim_name, output_path)`
- **Description** : Trace l'évolution des concentrations isotopiques
- **Paramètres** :
  - `days` : Liste des jours
  - `isotope_data` : Dictionnaire des données isotopiques
  - `sim_name` : Nom de la simulation
  - `output_path` : Chemin pour sauvegarder la figure
- **Retour** : None (sauvegarde la figure)

#### Fonction principale
- Parcourt les dossiers de simulation dans data/
- Extrait les données isotopiques des fichiers .se_dep.m
- Génère des graphiques pour différents groupes d'isotopes :
  - Isotopes du plutonium (Pu-238 à Pu-242)
  - Isotopes de l'uranium (U-235, U-238)
  - Produits de fission importants (Xe-135, Cs-137, etc.)
  - Actinides mineurs (Am-241, Cm-244, etc.)
- Sauvegarde les figures dans le dossier figures/inventory/

## scripts/plot_cross_sction.py

Ce script analyse et visualise les sections efficaces microscopiques et macroscopiques des différents isotopes présents dans le combustible.

### Fonctions principales

#### `extract_cross_sections(res_file)`
- **Description** : Extrait les données de sections efficaces du fichier .se_res.m
- **Paramètres** :
  - `res_file` : Chemin vers le fichier .se_res.m
- **Retour** : Dictionnaire des sections efficaces par isotope et par réaction

#### `plot_cross_sections(cross_sections, sim_name, output_path)`
- **Description** : Trace les sections efficaces en fonction de l'énergie
- **Paramètres** :
  - `cross_sections` : Dictionnaire des sections efficaces
  - `sim_name` : Nom de la simulation
  - `output_path` : Chemin pour sauvegarder la figure
- **Retour** : None (sauvegarde la figure)

#### Fonction principale
- Parcourt les dossiers de simulation dans data/
- Extrait les données de sections efficaces des fichiers .se_res.m
- Génère des graphiques pour différentes réactions :
  - Fission
  - Capture
  - Diffusion élastique
  - Diffusion inélastique
- Sauvegarde les figures dans le dossier figures/cross_sections/

## scripts/plot_fission_rate.py

Ce script analyse et visualise les taux de fission des différents isotopes fissiles et leur contribution au taux de fission total.

### Fonctions principales

#### `extract_fission_rates(dep_file, res_file)`
- **Description** : Extrait les taux de fission des fichiers .se_dep.m et .se_res.m
- **Paramètres** :
  - `dep_file` : Chemin vers le fichier .se_dep.m
  - `res_file` : Chemin vers le fichier .se_res.m
- **Retour** : Dictionnaire des taux de fission par isotope en fonction du temps

#### `plot_fission_rates(days, fission_rates, sim_name, output_path)`
- **Description** : Trace l'évolution des taux de fission et leur contribution relative
- **Paramètres** :
  - `days` : Liste des jours
  - `fission_rates` : Dictionnaire des taux de fission
  - `sim_name` : Nom de la simulation
  - `output_path` : Chemin pour sauvegarder la figure
- **Retour** : None (sauvegarde la figure)

#### Fonction principale
- Parcourt les dossiers de simulation dans data/
- Extrait les taux de fission des fichiers .se_dep.m et .se_res.m
- Génère des graphiques montrant :
  - L'évolution des taux de fission absolus par isotope
  - Les contributions relatives au taux de fission total
  - La conversion isotopique (U-238 → Pu-239, etc.)
- Sauvegarde les figures dans le dossier figures/fission_rates/

## scripts/plot_flow_evolution.py

Ce script analyse et visualise l'évolution du flux neutronique et sa distribution énergétique au cours de l'irradiation.

### Fonctions principales

#### `extract_flux_data(res_file)`
- **Description** : Extrait les données de flux neutronique du fichier .se_res.m
- **Paramètres** :
  - `res_file` : Chemin vers le fichier .se_res.m
- **Retour** : Énergies, flux en fonction du temps

#### `plot_flux_spectrum(energies, fluxes, times, sim_name, output_path)`
- **Description** : Trace l'évolution du spectre neutronique
- **Paramètres** :
  - `energies` : Liste des énergies
  - `fluxes` : Flux à différents temps
  - `times` : Liste des temps
  - `sim_name` : Nom de la simulation
  - `output_path` : Chemin pour sauvegarder la figure
- **Retour** : None (sauvegarde la figure)

#### Fonction principale
- Parcourt les dossiers de simulation dans data/
- Extrait les données de flux des fichiers .se_res.m
- Génère des graphiques montrant :
  - Le spectre neutronique à différents temps d'irradiation
  - L'évolution du flux intégré en fonction du temps
  - Le durcissement/adoucissement du spectre au cours de l'irradiation
- Sauvegarde les figures dans le dossier figures/flux/ 