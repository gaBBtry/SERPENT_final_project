import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d
import pandas as pd
import seaborn as sns

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

def compare_pu_incineration(simulation_stats):
    """Compare plutonium incineration performance across different simulations."""
    if not simulation_stats:
        print("Aucune donnée de simulation disponible pour la comparaison.")
        return
    
    # Create output directory
    os.makedirs('figures/comparison', exist_ok=True)
    
    # Extract sim names and plutonium data
    sim_names = list(simulation_stats.keys())
    
    # Prepare dataframes for comparisons
    pu_final_df = pd.DataFrame(index=sim_names)
    pu_reduction_df = pd.DataFrame(index=sim_names)
    pu_isotope_final_df = pd.DataFrame(index=sim_names)
    pu_efficiency_df = pd.DataFrame(index=sim_names)  # Nouvelle dataframe pour les métriques d'efficacité
    
    # Fill dataframes with data
    for sim in sim_names:
        stats = simulation_stats[sim]
        
        # Final plutonium total percentage
        pu_final_df.loc[sim, 'Total Pu (%)'] = stats['plutonium_total']['final']
        
        # Calculate plutonium reduction (initial - final)
        initial_pu = stats['plutonium_total']['max']  # Using max as proxy for initial in some cases
        final_pu = stats['plutonium_total']['final']
        reduction = initial_pu - final_pu
        reduction_percent = (reduction / initial_pu) * 100 if initial_pu > 0 else 0
        
        pu_reduction_df.loc[sim, 'Reduction (%)'] = reduction_percent
        pu_reduction_df.loc[sim, 'Absolute Reduction (%)'] = reduction
        
        # Get final values for each Pu isotope
        for isotope in ['Pu-238', 'Pu-239', 'Pu-240', 'Pu-241', 'Pu-242']:
            if isotope in stats['plutonium']['final_values']:
                pu_isotope_final_df.loc[sim, isotope] = stats['plutonium']['final_values'][isotope]
            else:
                pu_isotope_final_df.loc[sim, isotope] = 0
        
        # Nouvelles métriques d'efficacité
        # 1. Taux d'incinération par unité de burnup
        if 'final_burnup' in stats and stats['final_burnup'] > 0:
            incineration_rate = reduction_percent / stats['final_burnup']
            pu_efficiency_df.loc[sim, 'Taux incinération (%/MWd/kgU)'] = incineration_rate
        else:
            pu_efficiency_df.loc[sim, 'Taux incinération (%/MWd/kgU)'] = 0
            
        # 2. Efficacité de transmutation: Pu éliminé / AM produits
        if 'actinides_mineurs_total' in stats:
            initial_am = stats['actinides_mineurs_total'].get('min', 0)  # Utiliser min comme approximation de la valeur initiale
            final_am = stats['actinides_mineurs_total'].get('final', 0)
            am_production = max(0, final_am - initial_am)  # Production d'actinides mineurs
            
            # Calculer le ratio (éviter division par zéro)
            if am_production > 0:
                transmutation_efficiency = reduction / am_production
            else:
                transmutation_efficiency = float('inf') if reduction > 0 else 0
                
            pu_efficiency_df.loc[sim, 'Efficacité transmutation (Pu/AM)'] = transmutation_efficiency
        else:
            pu_efficiency_df.loc[sim, 'Efficacité transmutation (Pu/AM)'] = 0
    
    # Sort dataframes by total Pu
    pu_final_df = pu_final_df.sort_values('Total Pu (%)')
    pu_reduction_df = pu_reduction_df.sort_values('Reduction (%)', ascending=False)
    pu_efficiency_df = pu_efficiency_df.sort_values('Taux incinération (%/MWd/kgU)', ascending=False)
    
    # Create bar charts
    plt.figure(figsize=(12, 8))
    pu_final_df.plot(kind='bar', color='darkred', alpha=0.7)
    plt.title('Pourcentage final de Pu total par simulation')
    plt.ylabel('Pourcentage de Pu (%)')
    plt.xlabel('Simulation')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_final_comparison.png', dpi=300)
    plt.close()
    
    plt.figure(figsize=(12, 8))
    pu_reduction_df['Reduction (%)'].plot(kind='bar', color='green', alpha=0.7)
    plt.title('Pourcentage de réduction du Pu par simulation')
    plt.ylabel('Réduction (%)')
    plt.xlabel('Simulation')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_reduction_comparison.png', dpi=300)
    plt.close()
    
    # Nouveau graphique pour le taux d'incinération par unité de burnup
    plt.figure(figsize=(12, 8))
    pu_efficiency_df['Taux incinération (%/MWd/kgU)'].plot(kind='bar', color='blue', alpha=0.7)
    plt.title("Taux d'incinération du Pu par unité de burnup")
    plt.ylabel('Taux (%/MWd/kgU)')
    plt.xlabel('Simulation')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_incineration_rate.png', dpi=300)
    plt.close()
    
    # Nouveau graphique pour l'efficacité de transmutation
    plt.figure(figsize=(12, 8))
    # Remplacer les valeurs infinies par le maximum des valeurs finies * 1.5 pour l'affichage
    efficiency_values = pu_efficiency_df['Efficacité transmutation (Pu/AM)'].replace([float('inf')], 
                         pu_efficiency_df['Efficacité transmutation (Pu/AM)'].replace([float('inf')], 0).max() * 1.5)
    efficiency_values.plot(kind='bar', color='purple', alpha=0.7)
    plt.title('Efficacité de transmutation (Pu éliminé / AM produits)')
    plt.ylabel('Ratio Pu/AM')
    plt.xlabel('Simulation')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_transmutation_efficiency.png', dpi=300)
    plt.close()
    
    # Stacked bar chart for isotopic composition
    plt.figure(figsize=(14, 10))
    pu_isotope_final_df.plot(kind='bar', stacked=True, 
                             colormap='viridis',
                             figsize=(14, 8))
    plt.title('Composition isotopique finale du Pu par simulation')
    plt.ylabel('Pourcentage de l\'isotope (%)')
    plt.xlabel('Simulation')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Isotopes')
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_isotope_comparison.png', dpi=300)
    plt.close()
    
    # Analyse statistique approfondie
    # 1. Regroupement des simulations par performances similaires (clustering)
    from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
    from scipy.spatial.distance import pdist
    
    # Préparation des données pour clustering
    if len(sim_names) >= 3:  # Besoin d'au moins 3 simulations pour le clustering
        clustering_data = pd.DataFrame(index=sim_names)
        clustering_data['Reduction (%)'] = pu_reduction_df['Reduction (%)']
        clustering_data['Taux incinération'] = pu_efficiency_df['Taux incinération (%/MWd/kgU)']
        
        # Normalisation des données
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clustering_data.fillna(0))
        
        # Clustering hiérarchique
        plt.figure(figsize=(14, 8))
        Z = linkage(scaled_data, 'ward')
        dendrogram(Z, labels=clustering_data.index)
        plt.title('Regroupement des simulations par performances similaires')
        plt.xlabel('Simulations')
        plt.ylabel('Distance')
        plt.tight_layout()
        plt.savefig('figures/comparison/pu_performance_clustering.png', dpi=300)
        plt.close()
        
        # Identifier les clusters
        n_clusters = min(4, len(sim_names) // 2) if len(sim_names) >= 4 else 2
        clusters = fcluster(Z, n_clusters, criterion='maxclust')
        clustering_data['Cluster'] = clusters
        
        # Statistiques par cluster
        cluster_stats = pd.DataFrame(index=range(1, n_clusters+1))
        for i in range(1, n_clusters+1):
            cluster_sims = clustering_data[clustering_data['Cluster'] == i].index
            cluster_stats.loc[i, 'Nombre de simulations'] = len(cluster_sims)
            cluster_stats.loc[i, 'Réduction moyenne (%)'] = pu_reduction_df.loc[cluster_sims, 'Reduction (%)'].mean()
            cluster_stats.loc[i, 'Taux incinération moyen'] = pu_efficiency_df.loc[cluster_sims, 'Taux incinération (%/MWd/kgU)'].mean()
            cluster_stats.loc[i, 'Simulations'] = ', '.join(cluster_sims)
    else:
        cluster_stats = pd.DataFrame()
    
    # 2. Analyse de corrélation entre différentes métriques
    correlation_data = pd.DataFrame(index=sim_names)
    correlation_data['Reduction (%)'] = pu_reduction_df['Reduction (%)']
    correlation_data['Taux incinération'] = pu_efficiency_df['Taux incinération (%/MWd/kgU)']
    correlation_data['Pu-239 final'] = pu_isotope_final_df['Pu-239']
    correlation_data['Pu-241 final'] = pu_isotope_final_df['Pu-241']
    
    # Matrice de corrélation
    plt.figure(figsize=(10, 8))
    corr_matrix = correlation_data.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Corrélations entre les différentes métriques de performance')
    plt.tight_layout()
    plt.savefig('figures/comparison/pu_metrics_correlation.png', dpi=300)
    plt.close()
    
    # 3. Test statistique pour comparer les top performers
    top_performers = pu_reduction_df.nlargest(min(5, len(sim_names)), 'Reduction (%)')
    
    # Create a comprehensive summary file
    with open('figures/comparison/pu_incineration_summary.txt', 'w') as f:
        f.write("Comparaison des performances d'incinération du Plutonium\n")
        f.write("====================================================\n\n")
        
        f.write("Performances classées par réduction relative de Pu :\n")
        f.write(pu_reduction_df.sort_values('Reduction (%)', ascending=False).to_string())
        f.write("\n\n")
        
        f.write("Pourcentages finaux de Pu total :\n")
        f.write(pu_final_df.to_string())
        f.write("\n\n")
        
        f.write("Composition isotopique finale du Pu (%) :\n")
        f.write(pu_isotope_final_df.to_string())
        f.write("\n\n")
        
        f.write("Métriques d'efficacité d'incinération :\n")
        f.write(pu_efficiency_df.to_string())
        f.write("\n\n")
        
        if not cluster_stats.empty:
            f.write("Statistiques par groupe de performance similaire :\n")
            f.write(cluster_stats.to_string())
            f.write("\n\n")
        
        f.write("Top 5 des simulations les plus performantes :\n")
        f.write(top_performers.to_string())
        f.write("\n\n")
        
        f.write("Matrice de corrélation entre métriques :\n")
        f.write(corr_matrix.to_string())
        f.write("\n\n")
        
        f.write("Recommandations basées sur l'analyse :\n")
        f.write("1. Les simulations avec le plus haut taux d'incinération par unité de burnup sont : " + 
                ", ".join(pu_efficiency_df.nlargest(3, 'Taux incinération (%/MWd/kgU)').index) + "\n")
        f.write("2. Les simulations avec la meilleure efficacité de transmutation sont : " +
                ", ".join(pu_efficiency_df.nlargest(3, 'Efficacité transmutation (Pu/AM)').index) + "\n")
        f.write("3. Les simulations offrant le meilleur compromis entre réduction et efficacité sont : " +
                ", ".join(top_performers.index[:3]) + "\n")
    
    print(f"Comparaison des performances d'incinération du Pu sauvegardée dans figures/comparison/")
    
    return {
        'pu_final': pu_final_df,
        'pu_reduction': pu_reduction_df,
        'pu_isotopes': pu_isotope_final_df,
        'pu_efficiency': pu_efficiency_df
    }

if __name__ == "__main__":
    # Trouver tous les dossiers de simulation
    simulation_dirs = glob.glob('data/MOXEUS_*')
    
    if not simulation_dirs:
        print("Aucune simulation trouvée dans le dossier 'data/'.")
    else:
        # Compter les simulations réussies et échouées
        success_count = 0
        failed_count = 0
        
        # Dictionnaire pour stocker les statistiques de toutes les simulations
        all_stats = {}
        
        # Traiter chaque simulation
        for sim_dir in sorted(simulation_dirs):
            sim_name = os.path.basename(sim_dir)
            stats = process_simulation(sim_dir)
            if stats:
                all_stats[sim_name] = stats
                success_count += 1
            else:
                failed_count += 1
        
        # Afficher un résumé
        total = success_count + failed_count
        print(f"\nRésumé: {success_count}/{total} simulations traitées avec succès.")
        if failed_count > 0:
            print(f"{failed_count} simulations n'ont pas pu être traitées correctement.")
        
        # Comparer les performances d'incinération du Pu
        if success_count > 1:
            compare_pu_incineration(all_stats)
        elif success_count == 1:
            print("Une seule simulation traitée, la comparaison nécessite au moins deux simulations.")