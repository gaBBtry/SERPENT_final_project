import numpy as np
import matplotlib.pyplot as plt
import re
import os
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import interp1d
from matplotlib.gridspec import GridSpec
from scipy.stats import pearsonr

# Extraction des données k_inf (repris de plot_k_inf.py)
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

# Fonctions pour extraction des données isotopiques (adaptées de plot_inventory.py)
def clean_line(line):
    return line.split('%')[0].strip()

def parse_matlab_array(text):
    cleaned = re.sub(r'[\[\];]', '', text).strip()
    numbers = [float(x) for x in cleaned.split()]
    return np.array(numbers)

def parse_matlab_matrix(lines):
    matrix = []
    for line in lines:
        cleaned = clean_line(line)
        cleaned = re.sub(r'[\[\];]', '', cleaned)
        if cleaned:
            row = [float(x) for x in cleaned.split()]
            matrix.append(row)
    return np.array(matrix)

def load_m_file(filename):
    """Charge les données isotopiques depuis un fichier .m"""
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
            elif cleaned_line.startswith('BU ='):
                burnup = parse_matlab_array(cleaned_line.split('=', 1)[1])
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
            elif cleaned_line.startswith('MAT_fuelp1r1_ADENS ='):
                reading_adens = True
                adens_lines.append(cleaned_line.split('=', 1)[1])
            elif reading_adens and ';' in cleaned_line:
                adens_lines.append(cleaned_line)
                adens = parse_matlab_matrix(adens_lines)
                reading_adens = False
            elif reading_adens:
                adens_lines.append(cleaned_line)

    if days is None or zai is None or adens is None:
        raise ValueError("Erreur : DAYS, ZAI ou ADENS non trouvés dans le fichier.")
    
    if burnup is None:
        print("Burnup non trouvé, l'axe secondaire n'affichera pas cette information.")
        burnup = days  # Utiliser les jours comme fallback
    
    return days, zai, adens, burnup

# Définition des isotopes importants
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
fissile_isotopes = ['U-235', 'Pu-239', 'Pu-241']
fertile_isotopes = ['U-238', 'Pu-240', 'Pu-242']
poison_isotopes = ['U-236', 'Np-237', 'Am-241', 'Am-243']

def get_isotope_data(days, zai, adens, total_adens, isotope_list):
    """Obtient les données de densité pour une liste d'isotopes"""
    isotope_data = {}
    
    for isotope in isotope_list:
        zai_num = isotopes[isotope]
        indices = np.where(zai == zai_num)[0]
        if len(indices) == 1:
            index = indices[0]
            percentage = (adens[index, :] / total_adens) * 100
            isotope_data[isotope] = percentage
    
    return isotope_data

def calculate_total_percentage(isotope_data):
    """Calcule le pourcentage total pour un groupe d'isotopes"""
    if not isotope_data:
        # Retourner un tableau de zéros si aucun isotope n'est trouvé
        return np.zeros(81)  # Valeur par défaut (81 points temporels)
    
    total = np.zeros_like(next(iter(isotope_data.values())))
    for isotope, data in isotope_data.items():
        total += data
    
    return total

def calculate_k_inf_derivatives(times, k_infs):
    """Calcule les dérivées de k_inf pour identifier les points de changement"""
    dk_dt = np.gradient(k_infs, times)
    d2k_dt2 = np.gradient(dk_dt, times)
    return dk_dt, d2k_dt2

def calculate_pearson_correlations(k_infs, isotope_data):
    """Calcule les corrélations de Pearson entre k_inf et les isotopes"""
    correlations = {}
    
    for isotope, data in isotope_data.items():
        if len(data) == len(k_infs):
            try:
                corr, p_value = pearsonr(k_infs, data)
                correlations[isotope] = (corr, p_value)
            except:
                print(f"Erreur de calcul de corrélation pour {isotope}")
                correlations[isotope] = (0.0, 1.0)  # Valeur par défaut en cas d'erreur
        else:
            # Interpolation si les échelles temporelles sont différentes
            print(f"Longueurs différentes pour {isotope}: {len(data)} vs {len(k_infs)}")
    
    return correlations

def plot_k_inf_isotopes(times, burnups, k_infs, iso_times, isotope_data, sim_name, output_path):
    """
    Trace l'évolution de k_inf et des isotopes importants sur le même graphique.
    """
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 1, height_ratios=[2, 1], hspace=0.3)
    
    # Axe principal pour k_inf
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(times, k_infs, 'b-', marker='o', linewidth=2, markersize=5, 
             label=r'$k_{\infty}$ (implicit - corrector)')
    
    # Configurer l'axe y principal
    ax1.set_ylabel(r'$k_{\infty}$', fontsize=14)
    ax1.grid(True, which='major', linestyle='--', alpha=0.7)
    ax1.grid(True, which='minor', linestyle=':', alpha=0.4)
    
    # Axe secondaire pour le burnup (en haut)
    ax3 = ax1.twiny()
    ax3.set_xlim(ax1.get_xlim())
    
    # Calculer les valeurs de burnup pour les ticks du temps
    min_time = min(times)
    max_time = max(times)
    n_ticks = 10
    time_ticks = np.linspace(min_time, max_time, n_ticks)
    
    # Créer une fonction d'interpolation pour le burnup
    burnup_interp = interp1d(times, burnups, bounds_error=False, fill_value="extrapolate")
    burnup_ticks_values = burnup_interp(time_ticks)
    
    # Configurer l'axe du burnup
    ax3.set_xticks(time_ticks)
    ax3.set_xticklabels([f'{b:.1f}' for b in burnup_ticks_values])
    ax3.set_xlabel('Burnup (MWd/kgU)', fontsize=12)
    
    # Axe principal pour les isotopes
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    
    # Calculer les pourcentages totaux pour chaque groupe
    total_fissile = calculate_total_percentage({k: v for k, v in isotope_data.items() if k in fissile_isotopes})
    total_fertile = calculate_total_percentage({k: v for k, v in isotope_data.items() if k in fertile_isotopes})
    total_poison = calculate_total_percentage({k: v for k, v in isotope_data.items() if k in poison_isotopes})
    
    # Tracer les isotopes sur l'axe secondaire (y de droite)
    ax2.plot(iso_times, total_fissile, 'r-', linewidth=2, label='Isotopes fissiles')
    ax2.plot(iso_times, total_fertile, 'g-', linewidth=2, label='Isotopes fertiles')
    ax2.plot(iso_times, total_poison, 'y-', linewidth=2, label='Isotopes poisons')
    
    # Configurer l'axe des isotopes
    ax2.set_xlabel('Temps (jours)', fontsize=12)
    ax2.set_ylabel('Pourcentage de densité atomique (%)', fontsize=12)
    ax2.grid(True, which='major', linestyle='--', alpha=0.7)
    ax2.legend(loc='upper right')
    
    # Titre global
    fig.suptitle(r'Analyse comparative $k_{\infty}$ et compositions isotopiques - ' + sim_name, fontsize=16)
    
    # Légendes
    ax1.legend(loc='lower left')
    
    # Sauvegarder
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_k_inf_derivatives(times, burnups, k_infs, dk_dt, d2k_dt2, sim_name, output_path):
    """
    Trace les dérivées de k_inf pour identifier les points de changement significatifs.
    """
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 1, height_ratios=[2, 1, 1], hspace=0.3)
    
    # Axe pour k_inf
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(times, k_infs, 'b-', marker='o', linewidth=2, markersize=5, 
             label=r'$k_{\infty}$ (implicit - corrector)')
    
    # Axe pour la première dérivée
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(times, dk_dt, 'r-', linewidth=2, 
             label=r'$\frac{dk_{\infty}}{dt}$ (1ère dérivée)')
    
    # Axe pour la seconde dérivée
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(times, d2k_dt2, 'g-', linewidth=2, 
             label=r'$\frac{d^2k_{\infty}}{dt^2}$ (2ème dérivée)')
    
    # Identification des points d'inflexion significatifs
    # Les points où d2k/dt2 change de signe = points d'inflexion
    inflection_points = []
    for i in range(1, len(d2k_dt2)):
        if d2k_dt2[i-1] * d2k_dt2[i] <= 0 and abs(d2k_dt2[i]) > np.std(d2k_dt2) * 0.2:
            inflection_points.append(i)
    
    # Marquer les points d'inflexion sur toutes les courbes
    for point in inflection_points:
        time = times[point]
        ax1.axvline(x=time, color='grey', linestyle='--', alpha=0.5)
        ax2.axvline(x=time, color='grey', linestyle='--', alpha=0.5)
        ax3.axvline(x=time, color='grey', linestyle='--', alpha=0.5)
        
        # Annoter les valeurs de burnup aux points d'inflexion
        burnup_val = burnups[point]
        ax1.annotate(f'{burnup_val:.1f} MWd/kgU', xy=(time, k_infs[point]),
                     xytext=(time+5, k_infs[point]), fontsize=8,
                     arrowprops=dict(arrowstyle='->'))
    
    # Configurer les axes
    ax1.set_ylabel(r'$k_{\infty}$', fontsize=14)
    ax2.set_ylabel(r'$\frac{dk_{\infty}}{dt}$', fontsize=14)
    ax3.set_ylabel(r'$\frac{d^2k_{\infty}}{dt^2}$', fontsize=14)
    ax3.set_xlabel('Temps (jours)', fontsize=12)
    
    # Ajouter des grilles
    for ax in [ax1, ax2, ax3]:
        ax.grid(True, which='major', linestyle='--', alpha=0.7)
        ax.legend(loc='best')
    
    # Titre global
    fig.suptitle(r'Analyse des dérivées de $k_{\infty}$ - ' + sim_name, fontsize=16)
    
    # Sauvegarder
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_correlation_matrix(correlations, sim_name, output_path):
    """
    Trace une matrice visuelle des corrélations entre k_inf et les isotopes.
    """
    # Extraire les isotopes, valeurs de corrélation et p-valeurs
    isotopes = list(correlations.keys())
    corr_values = [correlations[iso][0] for iso in isotopes]
    p_values = [correlations[iso][1] for iso in isotopes]
    
    # Créer une figure avec barres colorées selon la corrélation
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Tracer les barres de corrélation
    bars = ax.barh(isotopes, corr_values, height=0.6)
    
    # Colorier les barres selon le sens de la corrélation
    for i, bar in enumerate(bars):
        if corr_values[i] >= 0:
            bar.set_color('green')
        else:
            bar.set_color('red')
            
        # Ajouter des étiquettes avec les valeurs
        ax.text(corr_values[i] + np.sign(corr_values[i]) * 0.01, i, 
                f'{corr_values[i]:.3f}', va='center')
        
        # Marquer les corrélations statistiquement significatives
        if p_values[i] < 0.05:
            ax.text(0, i, '*', fontsize=15, ha='center', va='center')
    
    # Configurer l'axe
    ax.set_xlim(-1.1, 1.1)
    ax.axvline(x=0, color='black', linestyle='-')
    ax.set_xlabel('Coefficient de corrélation de Pearson (p < 0.05)', fontsize=12)
    ax.set_title(r'Corrélation entre $k_{\infty}$ et les isotopes - ' + sim_name, fontsize=14)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Sauvegarder
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def create_summary(sim_dir, k_inf_data, isotope_correlations, inflection_points):
    """Crée un résumé textuel de l'analyse pour une simulation donnée"""
    summary = []
    summary.append(f"=== Résumé de l'analyse pour {sim_dir} ===\n")
    
    # Informations sur k_inf
    k_inf_mean = np.mean(k_inf_data['k_infs'])
    k_inf_min = np.min(k_inf_data['k_infs'])
    k_inf_max = np.max(k_inf_data['k_infs'])
    time_at_max = k_inf_data['times'][np.argmax(k_inf_data['k_infs'])]
    burnup_at_max = k_inf_data['burnups'][np.argmax(k_inf_data['k_infs'])]
    
    summary.append(f"k_inf moyen: {k_inf_mean:.5f}")
    summary.append(f"k_inf min: {k_inf_min:.5f}")
    summary.append(f"k_inf max: {k_inf_max:.5f} (à {time_at_max:.1f} jours / {burnup_at_max:.1f} MWd/kgU)")
    summary.append(f"Burnup final: {k_inf_data['burnups'][-1]:.1f} MWd/kgU")
    summary.append("")
    
    # Points d'inflexion significatifs
    summary.append("Points d'inflexion significatifs:")
    for point in inflection_points:
        idx = point  # Index du point d'inflexion
        time = k_inf_data['times'][idx]
        burnup = k_inf_data['burnups'][idx]
        k = k_inf_data['k_infs'][idx]
        summary.append(f"- À {time:.1f} jours / {burnup:.1f} MWd/kgU: k_inf = {k:.5f}")
    summary.append("")
    
    # Top 5 des corrélations (positives et négatives)
    summary.append("Top 5 des isotopes ayant la plus forte influence positive:")
    positive_corr = []
    negative_corr = []
    
    for iso, (corr, _) in isotope_correlations.items():
        if np.isnan(corr):
            continue  # Ignorer les valeurs NaN
            
        if corr > 0:
            positive_corr.append((iso, corr))
        else:
            negative_corr.append((iso, corr))
    
    # Trier les corrélations
    positive_corr.sort(key=lambda x: x[1], reverse=True)
    negative_corr.sort(key=lambda x: x[1])
    
    # Afficher le top 5 positif
    for isotope, corr in positive_corr[:5]:
        summary.append(f"- {isotope}: coefficient = {corr:.3f}")
    
    summary.append("\nTop 5 des isotopes ayant la plus forte influence négative:")
    for isotope, corr in negative_corr[:5]:
        summary.append(f"- {isotope}: coefficient = {corr:.3f}")
    
    return "\n".join(summary)

def interpolate_isotope_data(isotope_data, iso_times, k_inf_times):
    """Interpole les données isotopiques pour qu'elles correspondent aux temps de k_inf"""
    interpolated_data = {}
    
    for isotope, data in isotope_data.items():
        try:
            interp_func = interp1d(iso_times, data, bounds_error=False, fill_value="extrapolate")
            interpolated_data[isotope] = interp_func(k_inf_times)
        except Exception as e:
            print(f"Erreur lors de l'interpolation pour {isotope}: {e}")
    
    return interpolated_data

def plot_isotope_correlation_matrix(isotope_data, sim_name, output_path):
    """
    Génère une matrice de corrélation carrée entre tous les isotopes.
    Visualisée sous forme de heatmap colorée.
    """
    # Créer un DataFrame pandas pour faciliter le calcul de la matrice de corrélation
    df = pd.DataFrame(isotope_data)
    
    # Calculer la matrice de corrélation
    corr_matrix = df.corr(method='pearson')
    
    # Créer une figure pour la heatmap
    plt.figure(figsize=(14, 12))
    
    # Créer la heatmap avec seaborn
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Masque pour le triangle supérieur
    cmap = sns.diverging_palette(230, 20, as_cmap=True)  # Palette de couleurs (bleu-rouge)
    
    # Tracer la heatmap
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5, annot=True, fmt=".2f", 
                cbar_kws={"shrink": .8})
    
    # Ajuster la mise en page et ajouter un titre
    plt.title(f'Matrice de corrélation entre isotopes - {sim_name}', fontsize=16, pad=20)
    plt.tight_layout()
    
    # Sauvegarder
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Recherche des simulations dans le répertoire data/
    data_dir = "data"
    print(f"Recherche de simulations dans {data_dir}/...")
    simulation_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    simulation_dirs.sort()
    
    # Créer le répertoire principal de sortie
    os.makedirs('figures/interpretations', exist_ok=True)
    
    # Dictionnaire pour stocker les résumés
    summaries = {}
    
    # Traiter chaque simulation
    for sim_dir in simulation_dirs:
        log_file = os.path.join(data_dir, sim_dir, 'log.txt')
        dep_file = os.path.join(data_dir, sim_dir, f"{sim_dir}.se_dep.m")
        
        print(f"Traitement de {sim_dir}...")
        
        # Créer un répertoire pour cette simulation
        output_dir = f'figures/interpretations/{sim_dir}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Vérifier que les fichiers nécessaires existent
        if not os.path.exists(log_file) or not os.path.exists(dep_file):
            print(f"Fichiers manquants pour {sim_dir}, log: {os.path.exists(log_file)}, dep: {os.path.exists(dep_file)}")
            continue
        
        # Extraire les données k_inf
        times, burnups, k_infs, errors = extract_corrector_data(log_file)
        if not times:
            print(f"Aucune donnée k_inf trouvée pour {sim_dir}")
            continue
        print(f"Données k_inf extraites : {len(times)} points")
        
        # Extraire les données isotopiques
        try:
            iso_times, zai, adens, iso_burnups = load_m_file(dep_file)
            print(f"Données isotopiques extraites : {len(iso_times)} points temporels, {len(zai)} isotopes")
            
            # Calculer la densité atomique totale
            total_adens = np.sum(adens, axis=0)
            
            # Obtenir les données pour les groupes d'isotopes
            isotope_data = {}
            for isotope in isotopes:
                try:
                    zai_num = isotopes[isotope]
                    indices = np.where(zai == zai_num)[0]
                    if len(indices) == 1:
                        index = indices[0]
                        percentage = (adens[index, :] / total_adens) * 100
                        isotope_data[isotope] = percentage
                except Exception as e:
                    print(f"Erreur lors de l'extraction des données pour {isotope}: {e}")
                    continue
            
            # Calculer les dérivées de k_inf
            dk_dt, d2k_dt2 = calculate_k_inf_derivatives(times, k_infs)
            
            # Identifier les points d'inflexion significatifs
            inflection_points = []
            for i in range(1, len(d2k_dt2)):
                if d2k_dt2[i-1] * d2k_dt2[i] <= 0 and abs(d2k_dt2[i]) > np.std(d2k_dt2) * 0.2:
                    inflection_points.append(i)
            
            # Calculer les corrélations avec k_inf
            # Si les échelles temporelles sont différentes, interpoler
            if len(iso_times) != len(times):
                print(f"Interpolation nécessaire: {len(iso_times)} points isotopiques vs {len(times)} points k_inf")
                iso_data_interp = interpolate_isotope_data(isotope_data, iso_times, times)
                isotope_correlations = calculate_pearson_correlations(k_infs, iso_data_interp)
                
                # Utiliser les données interpolées pour la matrice de corrélation
                plot_isotope_correlation_matrix(iso_data_interp, sim_dir,
                                              f'{output_dir}/matrice_correlation.png')
            else:
                isotope_correlations = calculate_pearson_correlations(k_infs, isotope_data)
                
                # Utiliser les données originales pour la matrice de corrélation
                plot_isotope_correlation_matrix(isotope_data, sim_dir,
                                              f'{output_dir}/matrice_correlation.png')
            
            # Générer les graphiques
            plot_k_inf_isotopes(times, burnups, k_infs, iso_times, isotope_data, sim_dir,
                               f'{output_dir}/comparaison_isotopes.png')
            
            plot_k_inf_derivatives(times, burnups, k_infs, dk_dt, d2k_dt2, sim_dir,
                                  f'{output_dir}/derivees.png')
            
            plot_correlation_matrix(isotope_correlations, sim_dir,
                                   f'{output_dir}/correlation_k_inf.png')
            
            # Créer un résumé pour cette simulation
            k_inf_data = {
                'times': times,
                'burnups': burnups,
                'k_infs': k_infs,
                'errors': errors
            }
            summary = create_summary(sim_dir, k_inf_data, isotope_correlations, inflection_points)
            summaries[sim_dir] = summary
            
            # Sauvegarder le résumé pour cette simulation dans son propre dossier
            with open(f'{output_dir}/resume.txt', 'w') as f:
                f.write(summary)
            
            print(f"Analyse complétée pour {sim_dir}")
            
        except Exception as e:
            print(f"Erreur lors du traitement de {sim_dir}: {e}")
            import traceback
            traceback.print_exc()