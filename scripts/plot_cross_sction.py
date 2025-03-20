import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d

# Liste des isotopes d'intérêt avec leurs codes ZAI
isotopes = {
    'U-234': '922340', 'U-235': '922350', 'U-236': '922360', 'U-238': '922380',
    'Pu-238': '942380', 'Pu-239': '942390', 'Pu-240': '942400', 'Pu-241': '942410', 'Pu-242': '942420',
    'Np-237': '932370', 'Np-239': '932390',
    'Am-241': '952410', 'Am-242': '952420', 'Am-242m': '952421', 'Am-243': '952430',
    'Cm-242': '962420', 'Cm-243': '962430', 'Cm-244': '962440', 'Cm-245': '962450', 'Cm-246': '962460'
}

# Fonction pour parser une ligne et extraire les valeurs numériques
def parse_values(line):
    # Sépare les valeurs du commentaire (%) et prend la première partie
    values_part = line.split('%')[0].strip()
    # Convertit les valeurs en flottants, gérant les notations scientifiques
    return [float(val) for val in values_part.split()]

# Fonction pour lire les données du fichier
def read_dep_file(filename):
    bu = None
    days = None
    capt_xs = {}
    fiss_xs = {}
    current_matrix = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Extraction de BU
            if line.startswith('BU = ['):
                bu_values = line.replace('BU = [', '').replace('];', '').strip()
                bu = [float(val) for val in bu_values.split()]
            
            # Extraction de DAYS
            elif line.startswith('DAYS = ['):
                days_values = line.replace('DAYS = [', '').replace('];', '').strip()
                days = [float(val) for val in days_values.split()]
            
            # Début de la matrice CAPTXS
            elif line.startswith('MAT_fuelp1r1_CAPTXS = ['):
                current_matrix = 'capt_xs'
                continue
            
            # Début de la matrice FISSXS
            elif line.startswith('MAT_fuelp1r1_FISSXS = ['):
                current_matrix = 'fiss_xs'
                continue
            
            # Fin de la matrice
            elif line == '];' and current_matrix:
                current_matrix = None
                continue
            
            # Lecture des lignes de données
            elif current_matrix and '%' in line:
                values = parse_values(line)
                zai = line.split('%')[1].strip()  # Code ZAI après le %
                if current_matrix == 'capt_xs':
                    capt_xs[zai] = values
                elif current_matrix == 'fiss_xs':
                    fiss_xs[zai] = values
    
    return days, bu, capt_xs, fiss_xs

# Fonction pour tracer les sections efficaces
def plot_cross_sections(isotope, zai, days, bu, capt_xs, fiss_xs, sim_name, output_dir):
    # Vérifier si des données existent pour cet isotope
    has_capt = zai in capt_xs
    has_fiss = zai in fiss_xs
    
    if not has_capt and not has_fiss:
        print(f"Aucune donnée trouvée pour {isotope} (ZAI: {zai}).")
        return None
    
    # Créer une figure avec deux sous-graphiques
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Définir le nombre de graduations majeures souhaité
    n_ticks = 10
    
    # Créer une échelle régulière pour les jours
    min_days = min(days)
    max_days = max(days)
    days_ticks = np.linspace(min_days, max_days, n_ticks)
    
    # Statistiques des sections efficaces pour résumé
    stats = {
        'isotope': isotope,
        'zai': zai,
        'capture': {
            'min': None,
            'max': None,
            'mean': None,
            'ratio': None
        },
        'fission': {
            'min': None,
            'max': None,
            'mean': None,
            'ratio': None
        }
    }
    
    # Tracé de la section efficace de capture
    if has_capt:
        ax1.plot(days, capt_xs[zai], marker='o', linestyle='-', color='blue', 
                 markersize=3, label=f'{isotope} (n, γ)', linewidth=1.5)
        
        # Configuration des axes et de la grille
        ax1.set_ylabel('Section efficace de capture (barns)')
        ax1.yaxis.set_major_locator(MaxNLocator(8))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax1.grid(True, which='major', linestyle='--', alpha=0.7)
        ax1.grid(True, which='minor', linestyle=':', alpha=0.4)
        ax1.legend(loc='best', frameon=True, framealpha=0.9)
        
        # Calcul des statistiques pour la capture
        capt_min = min(capt_xs[zai])
        capt_max = max(capt_xs[zai])
        capt_mean = np.mean(capt_xs[zai])
        capt_ratio = capt_max / capt_min if capt_min > 0 else float('inf')
        
        stats['capture']['min'] = capt_min
        stats['capture']['max'] = capt_max
        stats['capture']['mean'] = capt_mean
        stats['capture']['ratio'] = capt_ratio
    else:
        ax1.text(0.5, 0.5, 'Données (n, γ) non disponibles', 
                 horizontalalignment='center', verticalalignment='center')
        ax1.set_ylabel('Section efficace de capture (barns)')
    
    # Tracé de la section efficace de fission
    if has_fiss:
        ax2.plot(days, fiss_xs[zai], marker='o', linestyle='-', color='red', 
                 markersize=3, label=f'{isotope} (n, f)', linewidth=1.5)
        
        # Configuration des axes et de la grille
        ax2.set_ylabel('Section efficace de fission (barns)')
        ax2.yaxis.set_major_locator(MaxNLocator(8))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax2.grid(True, which='major', linestyle='--', alpha=0.7)
        ax2.grid(True, which='minor', linestyle=':', alpha=0.4)
        ax2.legend(loc='best', frameon=True, framealpha=0.9)
        
        # Calcul des statistiques pour la fission
        fiss_min = min(fiss_xs[zai])
        fiss_max = max(fiss_xs[zai])
        fiss_mean = np.mean(fiss_xs[zai])
        fiss_ratio = fiss_max / fiss_min if fiss_min > 0 else float('inf')
        
        stats['fission']['min'] = fiss_min
        stats['fission']['max'] = fiss_max
        stats['fission']['mean'] = fiss_mean
        stats['fission']['ratio'] = fiss_ratio
    else:
        ax2.text(0.5, 0.5, 'Données (n, f) non disponibles', 
                 horizontalalignment='center', verticalalignment='center')
        ax2.set_ylabel('Section efficace de fission (barns)')
    
    # Configuration des ticks de l'axe x principal (jours)
    ax2.set_xticks(days_ticks)
    ax2.set_xticklabels([f'{d:.1f}' for d in days_ticks])
    ax2.set_xlabel('Temps (jours)')
    
    # Créer un axe secondaire pour le burnup (en haut)
    ax3 = ax1.twiny()
    ax3.set_xlim(ax1.get_xlim())
    
    # Créer une fonction d'interpolation pour le burnup
    burnup_interp = interp1d(days, bu, bounds_error=False, fill_value="extrapolate")
    
    # Calculer les valeurs de burnup correspondant aux ticks des jours
    burnup_ticks_values = burnup_interp(days_ticks)
    
    # Configurer l'axe du burnup
    ax3.set_xticks(days_ticks)
    ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
    ax3.set_xlabel('Burnup (MWd/kgU)')
    
    # Titre avec un écart supplémentaire et nom de la simulation
    plt.suptitle(f'Évolution des sections efficaces pour {isotope} - {sim_name}', 
                fontsize=14, fontweight='bold', y=0.98)
    
    # Ajuster les marges
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Sauvegarde du graphique
    output_filename = f"{output_dir}/{isotope}_cross_sections.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Graphique sauvegardé : {output_filename}")
    
    return stats

# Programme principal
def main():
    # Rechercher tous les fichiers de simulation dans data/
    sim_files = glob.glob('data/MOXEUS_*/MOXEUS_*.se_dep.m')
    
    for filename in sim_files:
        # Extraire le nom de la simulation (format MOXEUS_XXXXX)
        sim_name = os.path.basename(os.path.dirname(filename))
        
        print(f"Traitement de la simulation {sim_name}...")
        
        # Créer le dossier de sortie pour cette simulation
        output_dir = f"figures/cross_section/{sim_name}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Lire les données du fichier
        days, bu, capt_xs, fiss_xs = read_dep_file(filename)
        
        if days is None or bu is None:
            print(f"Erreur : impossible de lire les données de DAYS et BU pour {sim_name}.")
            continue
        
        # Dictionnaire pour stocker les statistiques de tous les isotopes pour cette simulation
        sim_stats = {
            'isotopes': {},
            'days_max': max(days),
            'bu_max': max(bu)
        }
        
        # Traçage pour chaque isotope
        for isotope, zai in isotopes.items():
            stats = plot_cross_sections(isotope, zai, days, bu, capt_xs, fiss_xs, sim_name, output_dir)
            if stats:
                sim_stats['isotopes'][isotope] = stats
        
        # Créer un résumé des statistiques dans un fichier texte pour cette simulation
        with open(f'{output_dir}/summary.txt', 'w') as f:
            f.write(f"Résumé des statistiques des sections efficaces pour {sim_name}\n")
            f.write("=" * 70 + "\n\n")
            
            # Informations générales sur la simulation
            f.write(f"Temps total      = {sim_stats['days_max']:.1f} jours\n")
            f.write(f"Burnup final     = {sim_stats['bu_max']:.1f} MWd/kgU\n\n")
            
            # Pour tous les isotopes disponibles
            f.write("Statistiques détaillées par isotope:\n")
            f.write("-" * 70 + "\n\n")
            
            # Trier les isotopes par ordre alphabétique
            sorted_isotopes = sorted(sim_stats['isotopes'].keys())
            
            for isotope in sorted_isotopes:
                stats = sim_stats['isotopes'][isotope]
                f.write(f"Isotope: {isotope} (ZAI: {stats['zai']})\n")
                
                # Section efficace de capture
                if stats['capture']['min'] is not None:
                    f.write("  Section efficace de capture (n,γ):\n")
                    f.write(f"    Minimum        = {stats['capture']['min']:.5e} barns\n")
                    f.write(f"    Maximum        = {stats['capture']['max']:.5e} barns\n")
                    f.write(f"    Moyenne        = {stats['capture']['mean']:.5e} barns\n")
                    f.write(f"    Ratio Max/Min  = {stats['capture']['ratio']:.5f}\n")
                else:
                    f.write("  Section efficace de capture (n,γ): Données non disponibles\n")
                
                # Section efficace de fission
                if stats['fission']['min'] is not None:
                    f.write("  Section efficace de fission (n,f):\n")
                    f.write(f"    Minimum        = {stats['fission']['min']:.5e} barns\n")
                    f.write(f"    Maximum        = {stats['fission']['max']:.5e} barns\n")
                    f.write(f"    Moyenne        = {stats['fission']['mean']:.5e} barns\n")
                    f.write(f"    Ratio Max/Min  = {stats['fission']['ratio']:.5f}\n")
                else:
                    f.write("  Section efficace de fission (n,f): Données non disponibles\n")
                
                f.write("\n")
                
            print(f"Fichier de résumé créé : {output_dir}/summary.txt")

if __name__ == "__main__":
    # Créer le dossier principal pour les figures
    os.makedirs('figures/cross_section', exist_ok=True)
    main()