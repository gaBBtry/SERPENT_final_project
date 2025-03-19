import matplotlib.pyplot as plt
import numpy as np
import re
import os
import glob
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d

def parse_m_file(file_path, var_name):
    """Extrait un tableau à partir d'un fichier .m en cherchant une variable donnée."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Recherche de la variable avec un motif regex
        pattern = rf"{var_name}\s*=\s*\[(.*?)\];"
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(f"Variable {var_name} non trouvée dans le fichier.")
        
        # Extraire les valeurs et les convertir en liste de flottants
        values_str = match.group(1)
        # Supprimer tous les commentaires (% jusqu'à la fin de la ligne)
        values_str = re.sub(r'%.*$', '', values_str, flags=re.MULTILINE)
        values = [float(val) for val in values_str.split() if val.strip()]
        return np.array(values)
    
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors du parsing de {var_name} : {e}")
        return None

def process_simulation(sim_dir):
    """Traite une simulation et génère le graphique de flux neutronique."""
    # Construire le chemin vers le fichier .m
    sim_name = os.path.basename(sim_dir)
    file_path = os.path.join(sim_dir, f"{sim_name}.se_dep.m")
    
    if not os.path.exists(file_path):
        print(f"Fichier {file_path} non trouvé, simulation ignorée.")
        return False
    
    print(f"Traitement de la simulation {sim_name}...")
    
    # Extraire les données
    days = parse_m_file(file_path, 'DAYS')
    flux = parse_m_file(file_path, 'MAT_fuelp1r1_FLUX')
    burnup = parse_m_file(file_path, 'BU')  # Burnup pour l'axe secondaire
    
    # Vérifier que les données ont été correctement extraites
    if days is None or flux is None:
        print(f"Impossible de continuer sans les données nécessaires pour {sim_name}.")
        return False
    
    if burnup is None:
        print("Burnup non trouvé, l'axe secondaire n'affichera pas cette information.")
        use_burnup = False
    else:
        use_burnup = True
    
    # Vérifier la compatibilité des longueurs
    if len(days) != len(flux):
        print(f"Erreur : DAYS ({len(days)} points) et MAT_fuelp1r1_FLUX ({len(flux)} points) n'ont pas la même longueur pour {sim_name}.")
        return False
    
    # Calculer les statistiques
    flux_mean = np.mean(flux)
    flux_std = np.std(flux)
    flux_min = np.min(flux)
    flux_max = np.max(flux)
    flux_ratio = flux_max / flux_min
    total_time = max(days)
    final_burnup = max(burnup) if use_burnup else 0
    
    # Créer la figure
    fig = plt.figure(figsize=(12, 8))
    
    # Axe principal pour le flux
    ax1 = fig.add_subplot(111)
    ax1.plot(days, flux, marker='o', linestyle='-', color='blue', 
             markersize=3, label=f'Flux neutronique', linewidth=1)
    
    # Définir le nombre de graduations majeures souhaité
    n_ticks = 12
    
    # Créer une échelle régulière pour le temps
    min_time = min(days)
    max_time = max(days)
    time_ticks = np.linspace(min_time, max_time, n_ticks)
    
    # Configurer l'axe du temps avec ces graduations
    ax1.set_xticks(time_ticks)
    ax1.set_xticklabels([f'{t:.1f}' for t in time_ticks])
    
    # Configuration de l'axe y principal
    ax1.yaxis.set_major_locator(MaxNLocator(15))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax1.grid(True, which='major', linestyle='--', alpha=0.7)
    ax1.grid(True, which='minor', linestyle=':', alpha=0.4)
    
    ax1.set_xlabel('Temps (jours)')
    ax1.set_ylabel('Flux neutronique')
    
    # Axe secondaire pour le ratio de flux (à droite)
    ax2 = ax1.twinx()
    
    # Calculer le ratio par rapport au flux initial
    flux_ratio_arr = flux / flux[0]
    ax2.plot(days, flux_ratio_arr, 'r-', 
            label=f'Ratio de flux (max/min = {flux_ratio:.2f})', 
            linewidth=1.5)
    ax2.set_ylabel('Ratio de flux (par rapport à t=0)')
    
    # Axe secondaire pour le burnup (en haut) si disponible
    if use_burnup:
        ax3 = ax1.twiny()
        ax3.set_xlim(ax1.get_xlim())
        
        # Créer une fonction d'interpolation pour le burnup
        burnup_interp = interp1d(days, burnup, bounds_error=False, fill_value="extrapolate")
        
        # Calculer les valeurs de burnup correspondant aux ticks du temps
        burnup_ticks_values = burnup_interp(time_ticks)
        
        # Configurer l'axe du burnup
        ax3.set_xticks(time_ticks)
        ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
        ax3.set_xlabel('Burnup (MWd/kgU)')
    
    # Titre avec un écart supplémentaire
    plt.title(f'Évolution temporelle du flux neutronique - {sim_name}', pad=15)
    
    # Légendes combinées
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    # Ajuster les marges et sauvegarder
    plt.tight_layout()
    
    # Créer le dossier de sauvegarde s'il n'existe pas
    save_dir = 'figures/flow_evolution'
    os.makedirs(save_dir, exist_ok=True)
    
    # Sauvegarder la figure
    save_path = os.path.join(save_dir, f'{sim_name}.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()  # Fermer la figure pour libérer la mémoire
    
    print(f"Figure sauvegardée sous '{save_path}'.")
    
    # Retourner les statistiques pour un usage ultérieur
    stats = {
        'mean': flux_mean,
        'std': flux_std,
        'min': flux_min,
        'max': flux_max,
        'ratio': flux_ratio,
        'total_time': total_time,
        'final_burnup': final_burnup if use_burnup else None
    }
    
    return stats

# Trouver tous les dossiers de simulation
sim_directories = glob.glob('data/MOXEUS_*')

if not sim_directories:
    print("Aucune simulation trouvée dans le dossier 'data/'.")
else:
    # Dictionnaire pour stocker les statistiques
    all_stats = {}
    
    # Compter les simulations réussies et échouées
    success_count = 0
    failed_count = 0
    
    # Traiter chaque simulation
    for sim_dir in sorted(sim_directories):
        stats = process_simulation(sim_dir)
        if stats:
            all_stats[os.path.basename(sim_dir)] = stats
            success_count += 1
        else:
            failed_count += 1
    
    # Afficher un résumé
    total = success_count + failed_count
    print(f"\nRésumé: {success_count}/{total} simulations traitées avec succès.")
    if failed_count > 0:
        print(f"{failed_count} simulations n'ont pas pu être traitées correctement.")
    
    # Créer un résumé des statistiques dans un fichier texte
    with open('figures/flow_evolution/summary.txt', 'w') as f:
        f.write("Résumé des statistiques de flux neutronique pour toutes les simulations\n")
        f.write("=" * 65 + "\n\n")
        
        for sim_name, stats in all_stats.items():
            f.write(f"Simulation: {sim_name}\n")
            f.write(f"  Flux moyen       = {stats['mean']:.5e}\n")
            f.write(f"  Écart-type       = {stats['std']:.5e}\n")
            f.write(f"  Flux min         = {stats['min']:.5e}\n")
            f.write(f"  Flux max         = {stats['max']:.5e}\n")
            f.write(f"  Ratio max/min    = {stats['ratio']:.5f}\n")
            f.write(f"  Temps total      = {stats['total_time']:.1f} jours\n")
            
            if stats['final_burnup'] is not None:
                f.write(f"  Burnup final     = {stats['final_burnup']:.1f} MWd/kgU\n")
            
            f.write("\n")