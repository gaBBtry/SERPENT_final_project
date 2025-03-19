import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d

def extract_corrector_data(log_file):
    """
    Extrait les données de k_inf (corrector), le temps, le burnup et les erreurs du fichier log.txt.
    Retourne quatre listes : temps (jours), burnup (MWd/kgU), k_inf, erreurs (en unité de k_eff).
    """
    with open(log_file, 'r') as file:
        lines = file.readlines()

    times = []
    burnups = []
    k_infs = []
    errors = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Chercher les étapes "corrector"
        if "Transport calculation: step =" in line and "(corrector)" in line:
            # Extraire le numéro de l'étape
            step_match = re.search(r'step = (\d+) / (\d+)', line)
            if step_match:
                step_num = int(step_match.group(1))
                # Trouver la ligne du burnup
                while i < len(lines):
                    i += 1
                    if "BU   =" in lines[i]:
                        bu_match = re.search(r'BU   = ([\d.]+) MWd/kgU', lines[i])
                        if bu_match:
                            burnup = float(bu_match.group(1))
                            break
                # Trouver la ligne du temps
                while i < len(lines):
                    i += 1
                    if "time =" in lines[i]:
                        time_match = re.search(r'time = ([\d.]+) days', lines[i])
                        if time_match:
                            time = float(time_match.group(1))
                            break
                # Trouver la dernière ligne k-eff (implicit) pour cette étape
                k_inf_line = None
                while i < len(lines):
                    i += 1
                    if "k-eff (implicit) =" in lines[i]:
                        k_inf_line = lines[i]
                    elif "Finished after" in lines[i]:
                        break
                if k_inf_line:
                    # Extraire k_inf et l'erreur
                    k_inf_match = re.search(r'k-eff \(implicit\) = ([\d.]+) \+/- ([\d.]+)', k_inf_line)
                    if k_inf_match:
                        k_inf = float(k_inf_match.group(1))
                        error = float(k_inf_match.group(2))
                        times.append(time)
                        burnups.append(burnup)
                        k_infs.append(k_inf)
                        errors.append(error)
        i += 1

    return times, burnups, k_infs, errors

def plot_k_inf_evolution(times, burnups, k_infs, errors, sim_name):
    """
    Trace l'évolution de k_inf avec le temps en bas et le burnup en haut.
    Sauvegarde la figure dans figures/k_inf/
    """
    # Convertir les erreurs en pcm (1 pcm = 10^-5, donc erreur * 10^5)
    errors_pcm = [error * 1e5 for error in errors]

    # Calculer les statistiques
    k_inf_mean = np.mean(k_infs)
    k_inf_std = np.std(k_infs)
    k_inf_min = np.min(k_infs)
    k_inf_max = np.max(k_infs)
    error_mean = np.mean(errors_pcm)
    error_min = np.min(errors_pcm)
    error_max = np.max(errors_pcm)
    total_time = max(times)
    final_burnup = max(burnups)

    # Créer la figure
    fig = plt.figure(figsize=(12, 8))
    
    # Axe principal pour k_inf
    ax1 = fig.add_subplot(111)
    ax1.errorbar(times, k_infs, yerr=errors, fmt='o', capsize=5, color='blue', 
                ecolor='red', markersize=3, label=r'$k_{\infty}$ (implicit - corrector)', 
                linestyle=':', linewidth=0.8)
    
    # Définir le nombre de graduations majeures souhaité
    n_ticks = 12
    
    # Créer une échelle régulière pour le temps
    min_time = min(times)
    max_time = max(times)
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
    ax1.set_ylabel(r'$k_{\infty}$')
    
    # Axe secondaire pour l'erreur (à droite)
    ax2 = ax1.twinx()
    ax2.plot(times, errors_pcm, 'y-', 
            label=f'Erreur (min = {error_min:.1f}, moy = {error_mean:.1f}, max = {error_max:.1f} pcm)', 
            linewidth=1.5)
    ax2.set_ylabel('Erreur (pcm)')
    
    # Axe secondaire pour le burnup (en haut)
    ax3 = ax1.twiny()
    ax3.set_xlim(ax1.get_xlim())
    
    # Créer une fonction d'interpolation pour le burnup
    burnup_interp = interp1d(times, burnups, bounds_error=False, fill_value="extrapolate")
    
    # Calculer les valeurs de burnup correspondant exactement aux ticks du temps
    burnup_ticks_values = burnup_interp(time_ticks)
    
    # Configurer l'axe du burnup pour qu'il corresponde exactement à l'axe du temps
    ax3.set_xticks(time_ticks)
    ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
    ax3.set_xlabel('Burnup (MWd/kgU)')
    
    # Titre avec un écart supplémentaire
    plt.title(fr'Évolution de $k_{{\infty}}$ - {sim_name}', pad=15)
    
    # Légendes combinées
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    # Ajuster les marges et sauvegarder
    plt.tight_layout()
    plt.savefig(f'figures/k_inf/{sim_name}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Retourner les statistiques pour un éventuel usage ultérieur
    return {
        'mean': k_inf_mean,
        'std': k_inf_std,
        'min': k_inf_min,
        'max': k_inf_max,
        'error_mean': error_mean,
        'error_min': error_min,
        'error_max': error_max,
        'total_time': total_time,
        'final_burnup': final_burnup
    }

if __name__ == "__main__":
    # Trouver tous les fichiers log.txt dans data/
    data_dir = "data"
    print(f"Recherche des fichiers log.txt dans {data_dir}/...")
    simulation_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    simulation_dirs.sort()  # Trier les répertoires pour un traitement ordonné
    print(f"Nombre de répertoires trouvés : {len(simulation_dirs)}")
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs('figures/k_inf', exist_ok=True)
    
    # Dictionnaire pour stocker les statistiques de toutes les simulations
    all_stats = {}
    
    for sim_dir in simulation_dirs:
        log_file = os.path.join(data_dir, sim_dir, 'log.txt')
        print(f"Vérification de {log_file}...")
        if os.path.exists(log_file):
            print(f"Traitement de {sim_dir}...")
            
            # Extraire les données
            times, burnups, k_infs, errors = extract_corrector_data(log_file)
            print(f"Données extraites : {len(times)} points")
            
            # Tracer et sauvegarder le graphique
            stats = plot_k_inf_evolution(times, burnups, k_infs, errors, sim_dir)
            all_stats[sim_dir] = stats
            print(f"Figure sauvegardée dans figures/k_inf/{sim_dir}.png")
            print(f"k_inf moyen = {stats['mean']:.5f} ± {stats['std']:.5f}")
            print(f"Burnup final = {stats['final_burnup']:.1f} MWd/kgU")
        else:
            print(f"Fichier log.txt non trouvé dans {sim_dir}")
    
    # Créer un résumé des statistiques dans un fichier texte
    with open('figures/k_inf/summary.txt', 'w') as f:
        f.write("Résumé des statistiques de criticité pour toutes les simulations\n")
        f.write("=" * 50 + "\n\n")
        for sim_dir, stats in all_stats.items():
            f.write(f"Simulation: {sim_dir}\n")
            f.write(f"  k_inf moyen      = {stats['mean']:.5f}\n")
            f.write(f"  Écart-type       = {stats['std']:.5f}\n")
            f.write(f"  k_inf min        = {stats['min']:.5f}\n")
            f.write(f"  k_inf max        = {stats['max']:.5f}\n")
            f.write(f"  Erreur moyenne   = {stats['error_mean']:.1f} pcm\n")
            f.write(f"  Erreur min       = {stats['error_min']:.1f} pcm\n")
            f.write(f"  Erreur max       = {stats['error_max']:.1f} pcm\n")
            f.write(f"  Temps total      = {stats['total_time']:.1f} jours\n")
            f.write(f"  Burnup final     = {stats['final_burnup']:.1f} MWd/kgU\n")
            f.write("\n")