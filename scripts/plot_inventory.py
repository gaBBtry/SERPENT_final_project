import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d

# Fonction pour nettoyer une ligne en supprimant les commentaires
def clean_line(line):
    return line.split('%')[0].strip()

# Fonction pour parser un tableau MATLAB depuis une chaîne de texte
def parse_matlab_array(text):
    cleaned = re.sub(r'[\[\];]', '', text).strip()
    numbers = [float(x) for x in cleaned.split()]
    return np.array(numbers)

# Fonction pour parser une matrice MATLAB depuis plusieurs lignes
def parse_matlab_matrix(lines):
    matrix = []
    for line in lines:
        cleaned = clean_line(line)
        cleaned = re.sub(r'[\[\];]', '', cleaned)
        if cleaned:
            row = [float(x) for x in cleaned.split()]
            matrix.append(row)
    return np.array(matrix)

# Lecture du fichier .m avec débogage
def load_m_file(filename):
    days = None
    zai = None
    adens = None
    burnup = None
    adens_lines = []
    reading_adens = False

    with open(filename, 'r') as f:
        for line in f:
            cleaned_line = clean_line(line)
            if not cleaned_line:
                continue

            if cleaned_line.startswith('DAYS ='):
                days = parse_matlab_array(cleaned_line.split('=', 1)[1])
                print(f"DAYS: {days[:5]}... (length: {len(days)})")
            elif cleaned_line.startswith('BU ='):
                burnup = parse_matlab_array(cleaned_line.split('=', 1)[1])
                print(f"BURNUP: {burnup[:5]}... (length: {len(burnup)})")
            elif cleaned_line.startswith('ZAI ='):
                zai_lines = []
                zai_lines.append(cleaned_line.split('=', 1)[1])
                for next_line in f:
                    cleaned_next = clean_line(next_line)
                    if cleaned_next.endswith(';'):
                        zai_lines.append(cleaned_next)
                        break
                    elif cleaned_next:
                        zai_lines.append(cleaned_next)
                zai_text = ' '.join(zai_lines)
                zai = parse_matlab_array(zai_text)
                print(f"ZAI: {zai[:5]}... (length: {len(zai)})")
            elif cleaned_line.startswith('MAT_fuelp1r1_ADENS ='):
                reading_adens = True
                adens_lines.append(cleaned_line.split('=', 1)[1])
            elif reading_adens and ';' in cleaned_line:
                adens_lines.append(cleaned_line)
                adens = parse_matlab_matrix(adens_lines)
                print(f"ADENS shape: {adens.shape}")
                reading_adens = False
            elif reading_adens:
                adens_lines.append(cleaned_line)

    if days is None or zai is None or adens is None:
        raise ValueError("Erreur : DAYS, ZAI ou ADENS non trouvés dans le fichier.")
    
    if burnup is None:
        print("Burnup non trouvé, l'axe secondaire n'affichera pas cette information.")
        burnup = days  # Utiliser les jours comme fallback
    
    return days, zai, adens, burnup

# Définition des isotopes avec leurs numéros ZAI
isotopes = {
    'U-234': 922340,
    'U-235': 922350,
    'U-236': 922360,
    'U-238': 922380,
    'Pu-238': 942380,
    'Pu-239': 942390,
    'Pu-240': 942400,
    'Pu-241': 942410,
    'Pu-242': 942420,
    'Np-237': 932370,
    'Np-239': 932390,
    'Am-241': 952410,
    'Am-242m': 952421,
    'Am-243': 952430,
    'Cm-242': 962420,
    'Cm-243': 962430,
    'Cm-244': 962440,
    'Cm-245': 962450,
    'Cm-246': 962460,
}

# Groupement des isotopes
u_isotopes = ['U-234', 'U-235', 'U-236', 'U-238']
pu_isotopes = ['Pu-238', 'Pu-239', 'Pu-240', 'Pu-241', 'Pu-242']
ma_isotopes = ['Np-237', 'Np-239', 'Am-241', 'Am-242m', 'Am-243', 'Cm-242', 'Cm-243', 'Cm-244', 'Cm-245', 'Cm-246']

# Fonction pour tracer un groupe d'isotopes
def plot_group(group_name, isotope_list, days, zai, adens, total_adens, burnup, output_path, sim_name):
    """Trace l'évolution des isotopes individuels d'un groupe en échelle logarithmique."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    
    # Tracking pour statistiques
    max_values = {}
    final_values = {}
    
    for isotope in isotope_list:
        zai_num = isotopes[isotope]
        indices = np.where(zai == zai_num)[0]
        if len(indices) == 1:
            index = indices[0]
            percentage = (adens[index, :] / total_adens) * 100
            ax.plot(days, percentage, label=isotope, linewidth=2)
            
            # Stocker les valeurs max et finales pour les statistiques
            max_values[isotope] = np.max(percentage)
            final_values[isotope] = percentage[-1]
        else:
            print(f"Isotope {isotope} (ZAI={zai_num}) non trouvé dans le tableau ZAI.")
    
    # Configuration des axes
    ax.set_xlabel('Temps (jours)', fontsize=12)
    ax.set_ylabel('Pourcentage de densité atomique (%)', fontsize=12)
    ax.set_title(f'Évolution des isotopes de {group_name} - {sim_name}', fontsize=14, pad=15)
    
    # Configuration de la grille et graduations
    ax.grid(True, which='major', linestyle='--', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', alpha=0.4)
    
    # Définir le nombre de graduations majeures souhaité
    n_ticks = 10
    
    # Créer une échelle régulière pour le temps
    min_time = min(days)
    max_time = max(days)
    time_ticks = np.linspace(min_time, max_time, n_ticks)
    
    # Configurer l'axe du temps avec ces graduations
    ax.set_xticks(time_ticks)
    ax.set_xticklabels([f'{t:.1f}' for t in time_ticks])
    
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    
    # Échelle logarithmique pour mieux voir les isotopes en faible quantité
    ax.set_yscale('log')
    
    # Axe secondaire pour le burnup (en haut)
    ax3 = ax.twiny()
    ax3.set_xlim(ax.get_xlim())
    
    # Créer une fonction d'interpolation pour le burnup
    burnup_interp = interp1d(days, burnup, bounds_error=False, fill_value="extrapolate")
    
    # Calculer les valeurs de burnup correspondant aux ticks du temps
    burnup_ticks_values = burnup_interp(time_ticks)
    
    # Configurer l'axe du burnup
    ax3.set_xticks(time_ticks)
    ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
    ax3.set_xlabel('Burnup (MWd/kgU)')
    
    # Légende
    ax.legend(fontsize=10, loc='best')
    
    # Ajustement et sauvegarde
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return {'max_values': max_values, 'final_values': final_values}

# Fonction pour tracer le total d'un groupe d'isotopes
def plot_group_total(group_name, isotope_list, days, zai, adens, total_adens, burnup, output_path, sim_name):
    """Trace l'évolution du total d'un groupe d'isotopes en échelle linéaire."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    
    # Calcul de la somme des densités atomiques pour tous les isotopes du groupe
    group_total_percentage = np.zeros_like(days)
    for isotope in isotope_list:
        zai_num = isotopes[isotope]
        indices = np.where(zai == zai_num)[0]
        if len(indices) == 1:
            index = indices[0]
            percentage = (adens[index, :] / total_adens) * 100
            group_total_percentage += percentage
    
    # Tracer la courbe totale
    ax.plot(days, group_total_percentage, linewidth=3, color='red', 
            label=f'Total {group_name}')
    
    # Calculer les statistiques
    max_value = np.max(group_total_percentage)
    min_value = np.min(group_total_percentage)
    mean_value = np.mean(group_total_percentage)
    final_value = group_total_percentage[-1]
    
    # Configuration des axes
    ax.set_xlabel('Temps (jours)', fontsize=12)
    ax.set_ylabel('Pourcentage de densité atomique (%)', fontsize=12)
    ax.set_title(f'Évolution du {group_name} total - {sim_name}', fontsize=14, pad=15)
    
    # Configuration de la grille et graduations
    ax.grid(True, which='major', linestyle='--', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', alpha=0.4)
    
    # Définir le nombre de graduations majeures souhaité
    n_ticks = 10
    
    # Créer une échelle régulière pour le temps
    min_time = min(days)
    max_time = max(days)
    time_ticks = np.linspace(min_time, max_time, n_ticks)
    
    # Configurer l'axe du temps avec ces graduations
    ax.set_xticks(time_ticks)
    ax.set_xticklabels([f'{t:.1f}' for t in time_ticks])
    
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    
    # Axe secondaire pour le burnup (en haut)
    ax3 = ax.twiny()
    ax3.set_xlim(ax.get_xlim())
    
    # Créer une fonction d'interpolation pour le burnup
    burnup_interp = interp1d(days, burnup, bounds_error=False, fill_value="extrapolate")
    
    # Calculer les valeurs de burnup correspondant aux ticks du temps
    burnup_ticks_values = burnup_interp(time_ticks)
    
    # Configurer l'axe du burnup
    ax3.set_xticks(time_ticks)
    ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
    ax3.set_xlabel('Burnup (MWd/kgU)')
    
    # Ajouter une annotation avec les statistiques
    stats_text = (f"Min: {min_value:.2f}%\n"
                 f"Max: {max_value:.2f}%\n"
                 f"Moy: {mean_value:.2f}%\n"
                 f"Final: {final_value:.2f}%")
    
    ax.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction', 
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                va='top', ha='left', fontsize=10)
    
    # Légende
    ax.legend(fontsize=10, loc='best')
    
    # Ajustement et sauvegarde
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'min': min_value,
        'max': max_value,
        'mean': mean_value,
        'final': final_value
    }

def process_simulation(sim_dir):
    """Traite une simulation et génère tous les graphiques associés."""
    sim_name = os.path.basename(sim_dir)
    print(f"\nTraitement de la simulation {sim_name}")
    
    # Création du dossier de sortie pour cette simulation
    output_dir = os.path.join('figures/inventory', sim_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Recherche du fichier .m
    m_files = glob.glob(os.path.join(sim_dir, '*.se_dep.m'))
    if not m_files:
        print(f"Aucun fichier .se_dep.m trouvé dans {sim_dir}")
        return None
    
    # Chargement des données
    days, zai, adens, burnup = load_m_file(m_files[0])
    
    # Calcul du total
    total_adens = np.sum(adens[:-2, :], axis=0)  # Exclut 'lost' et 'total'
    
    # Dictionnaire pour stocker les statistiques
    stats = {}
    
    # Tracé pour chaque groupe
    stats['uranium'] = plot_group('Uranium', u_isotopes, days, zai, adens, total_adens, burnup, 
                                os.path.join(output_dir, 'uranium.png'), sim_name)
    
    stats['plutonium'] = plot_group('Plutonium', pu_isotopes, days, zai, adens, total_adens, burnup, 
                                  os.path.join(output_dir, 'plutonium.png'), sim_name)
    
    stats['actinides_mineurs'] = plot_group('Actinides mineurs', ma_isotopes, days, zai, adens, total_adens, burnup, 
                                          os.path.join(output_dir, 'actinides_mineurs.png'), sim_name)
    
    # Tracé du plutonium total
    stats['plutonium_total'] = plot_group_total('Plutonium', pu_isotopes, days, zai, adens, total_adens, burnup,
                                              os.path.join(output_dir, 'plutonium_total.png'), sim_name)
    
    # Tracé de l'uranium total
    stats['uranium_total'] = plot_group_total('Uranium', u_isotopes, days, zai, adens, total_adens, burnup,
                                            os.path.join(output_dir, 'uranium_total.png'), sim_name)
    
    # Tracé des actinides mineurs totaux
    stats['actinides_mineurs_total'] = plot_group_total('Actinides mineurs', ma_isotopes, days, zai, adens, total_adens, burnup,
                                                      os.path.join(output_dir, 'actinides_mineurs_total.png'), sim_name)
    
    print(f"Figures sauvegardées dans {output_dir}")
    
    # Ajouter des informations générales
    stats['total_time'] = max(days)
    stats['final_burnup'] = max(burnup)
    
    # Création d'un fichier summary.txt pour cette simulation
    summary_path = os.path.join(output_dir, 'summary.txt')
    with open(summary_path, 'w') as f:
        f.write(f"Résumé des statistiques d'inventaire pour la simulation {sim_name}\n")
        f.write("=" * 65 + "\n\n")
        
        f.write(f"Temps total: {stats['total_time']:.1f} jours\n")
        f.write(f"Burnup final: {stats['final_burnup']:.1f} MWd/kgU\n\n")
        
        # Statistiques pour le plutonium total
        f.write("Plutonium Total:\n")
        f.write(f"  Minimum       = {stats['plutonium_total']['min']:.3f}%\n")
        f.write(f"  Maximum       = {stats['plutonium_total']['max']:.3f}%\n")
        f.write(f"  Moyenne       = {stats['plutonium_total']['mean']:.3f}%\n")
        f.write(f"  Valeur finale = {stats['plutonium_total']['final']:.3f}%\n\n")
        
        # Statistiques pour chaque isotope de plutonium
        f.write("Valeurs finales des isotopes de plutonium:\n")
        for isotope, value in stats['plutonium']['final_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n")
            
        f.write("\nValeurs maximales des isotopes de plutonium:\n")
        for isotope, value in stats['plutonium']['max_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n\n")
        
        # Statistiques pour l'uranium total
        f.write("Uranium Total:\n")
        f.write(f"  Minimum       = {stats['uranium_total']['min']:.3f}%\n")
        f.write(f"  Maximum       = {stats['uranium_total']['max']:.3f}%\n")
        f.write(f"  Moyenne       = {stats['uranium_total']['mean']:.3f}%\n")
        f.write(f"  Valeur finale = {stats['uranium_total']['final']:.3f}%\n")
        
        # Statistiques pour chaque isotope d'uranium
        f.write("Valeurs finales des isotopes d'uranium:\n")
        for isotope, value in stats['uranium']['final_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n")
            
        f.write("\nValeurs maximales des isotopes d'uranium:\n")
        for isotope, value in stats['uranium']['max_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n\n")
        
        # Statistiques pour les actinides mineurs totaux
        f.write("Actinides mineurs Total:\n")
        f.write(f"  Minimum       = {stats['actinides_mineurs_total']['min']:.3f}%\n")
        f.write(f"  Maximum       = {stats['actinides_mineurs_total']['max']:.3f}%\n")
        f.write(f"  Moyenne       = {stats['actinides_mineurs_total']['mean']:.3f}%\n")
        f.write(f"  Valeur finale = {stats['actinides_mineurs_total']['final']:.3f}%\n\n")
        
        # Statistiques pour chaque actinide mineur
        f.write("Valeurs finales des actinides mineurs:\n")
        for isotope, value in stats['actinides_mineurs']['final_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n")
            
        f.write("\nValeurs maximales des actinides mineurs:\n")
        for isotope, value in stats['actinides_mineurs']['max_values'].items():
            f.write(f"  {isotope:<10} = {value:.6f}%\n")
    
    print(f"Résumé sauvegardé dans {summary_path}")
    
    return stats

if __name__ == "__main__":
    # Trouver tous les dossiers de simulation
    simulation_dirs = glob.glob('data/MOXEUS_*')
    
    if not simulation_dirs:
        print("Aucune simulation trouvée dans le dossier 'data/'.")
    else:
        # Compter les simulations réussies et échouées
        success_count = 0
        failed_count = 0
        
        # Traiter chaque simulation
        for sim_dir in sorted(simulation_dirs):
            stats = process_simulation(sim_dir)
            if stats:
                success_count += 1
            else:
                failed_count += 1
        
        # Afficher un résumé
        total = success_count + failed_count
        print(f"\nRésumé: {success_count}/{total} simulations traitées avec succès.")
        if failed_count > 0:
            print(f"{failed_count} simulations n'ont pas pu être traitées correctement.")