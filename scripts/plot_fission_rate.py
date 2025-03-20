import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
import pandas as pd
from matplotlib.ticker import MaxNLocator, AutoMinorLocator

# Liste des isotopes d'intérêt avec leurs codes ZAI
ISOTOPES = {
    'U-234': '922340', 'U-235': '922350', 'U-236': '922360', 'U-238': '922380',
    'Pu-238': '942380', 'Pu-239': '942390', 'Pu-240': '942400', 'Pu-241': '942410', 'Pu-242': '942420',
    'Np-237': '932370', 'Np-239': '932390',
    'Am-241': '952410', 'Am-242': '952420', 'Am-242m': '952421', 'Am-243': '952430',
    'Cm-242': '962420', 'Cm-243': '962430', 'Cm-244': '962440', 'Cm-245': '962450', 'Cm-246': '962460'
}

def extract_fission_fractions(out_file):
    """
    Extrait les fractions de fission pour chaque isotope à partir du fichier .se.out
    """
    fission_fractions = {}
    
    with open(out_file, 'r') as file:
        content = file.read()
        
        # Recherche de la section des fractions de fission
        pattern = r"Fission \(total (\d+) reactions\):(.*?)=+"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            total_reactions = int(match.group(1))
            fission_section = match.group(2)
            # Extrait chaque ligne d'isotope
            iso_lines = re.findall(r'(\d+\.\d+c)\s+(\d+)\s+(\d+)\s+([\d.]+)', fission_section)
            
            for iso in iso_lines:
                nuclide_id = iso[1]  # Identifiant ZAI (comme 922350 pour U-235)
                fraction = float(iso[3])
                fission_fractions[nuclide_id] = fraction
            
            return fission_fractions, total_reactions
    
    return {}, 0

def extract_burnup_info(out_file):
    """
    Tente d'extraire les informations de burnup du fichier .se.out
    """
    # Cette fonction est une approximation car les fichiers .se.out peuvent ne pas contenir 
    # toutes les informations de burnup détaillées
    
    with open(out_file, 'r') as file:
        content = file.read()
        
        # Recherche d'informations de burnup ou de temps
        burnup_match = re.search(r"BU\s*=\s*([\d.]+)\s*MWd/kgU", content)
        time_match = re.search(r"time\s*=\s*([\d.]+)\s*days", content)
        
        burnup = float(burnup_match.group(1)) if burnup_match else None
        time = float(time_match.group(1)) if time_match else None
        
        return burnup, time

def plot_fission_contribution(simulation_dir, simulation_name):
    """
    Trace les contributions aux fissions des principaux isotopes.
    """
    # Chemin du fichier de sortie
    out_file = os.path.join(simulation_dir, f"{simulation_name}.se.out")
    
    # Vérifier que le fichier existe
    if not os.path.exists(out_file):
        print(f"Fichier {out_file} non trouvé, graphique de contribution aux fissions non généré.")
        return False
    
    # Extraction des fractions de fission
    fission_fractions, total_reactions = extract_fission_fractions(out_file)
    
    if not fission_fractions:
        print(f"Aucune donnée de fraction de fission trouvée dans {out_file}")
        return False
    
    # Extraire les informations de burnup si disponibles
    burnup, time = extract_burnup_info(out_file)
    burnup_info = f" (Burnup: {burnup:.2f} MWd/kgU)" if burnup else ""
    time_info = f" (Temps: {time:.1f} jours)" if time else ""
    
    # Créer un dataframe pour faciliter le tracé
    data = []
    for zai, fraction in fission_fractions.items():
        # Trouver le nom de l'isotope correspondant au ZAI s'il existe
        isotope_name = next((name for name, z in ISOTOPES.items() if z == zai), zai)
        if fraction > 0.001:  # Ne montrer que les isotopes avec une contribution significative
            data.append({'Isotope': isotope_name, 'Fraction': fraction})
    
    df = pd.DataFrame(data)
    df = df.sort_values('Fraction', ascending=False)
    
    # Définir le dossier de sortie
    figures_dir = os.path.join("figures", "fission_rate", simulation_name)
    os.makedirs(figures_dir, exist_ok=True)
    
    # ------ Graphique de contribution aux fissions ------
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df['Isotope'], df['Fraction'] * 100, color='skyblue')
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{height:.1f}%', ha='center', va='bottom', rotation=0)
    
    plt.ylabel('Contribution aux fissions (%)', fontsize=12)
    title = f'Contribution des isotopes aux fissions - {simulation_name}{burnup_info}{time_info}'
    plt.title(title, fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Sauvegarde
    plt.savefig(os.path.join(figures_dir, "fission_contribution.png"), dpi=300)
    plt.close()
    
    # ------ Graphique complémentaire: diagramme camembert pour les contributions principales ------
    plt.figure(figsize=(10, 8))
    
    # Ne garder que les isotopes avec plus de 1% de contribution
    major_isotopes = df[df['Fraction'] >= 0.01].copy()
    
    # Si on a trop d'isotopes avec une petite contribution, regrouper
    if len(df) > len(major_isotopes):
        other_fraction = df[df['Fraction'] < 0.01]['Fraction'].sum()
        if other_fraction > 0:
            major_isotopes = pd.concat([major_isotopes, pd.DataFrame([{'Isotope': 'Autres', 'Fraction': other_fraction}])])
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(major_isotopes)))
    
    plt.pie(major_isotopes['Fraction'] * 100,
           labels=major_isotopes['Isotope'],
           autopct='%1.1f%%',
           startangle=90,
           colors=colors,
           wedgeprops={'edgecolor': 'w', 'linewidth': 1},
           textprops={'fontsize': 12})
    
    plt.axis('equal')
    plt.title(f'Répartition des fissions - {simulation_name}{burnup_info}', fontsize=14)
    
    # Sauvegarde
    plt.savefig(os.path.join(figures_dir, "fission_pie_chart.png"), dpi=300)
    plt.close()
    
    # Génération d'un rapport de synthèse
    with open(os.path.join(figures_dir, "summary.txt"), 'w') as f:
        f.write(f"Résumé des contributions aux fissions - {simulation_name}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Nombre total de réactions de fission: {total_reactions}\n\n")
        
        if burnup:
            f.write(f"Burnup: {burnup:.2f} MWd/kgU\n")
        if time:
            f.write(f"Temps: {time:.1f} jours\n")
        
        f.write("\nContributions aux fissions par isotope:\n")
        for idx, row in df.iterrows():
            iso = row['Isotope']
            frac = row['Fraction']
            f.write(f"  {iso}: {frac*100:.2f}%\n")
        
        f.write("\nIsotopes dominants (>1%):\n")
        for idx, row in df[df['Fraction'] >= 0.01].iterrows():
            iso = row['Isotope']
            frac = row['Fraction']
            f.write(f"  {iso}: {frac*100:.2f}%\n")
    
    print(f"Graphiques et rapport de synthèse générés pour {simulation_name}")
    return True

def process_all_simulations():
    """
    Traite toutes les simulations pour générer les graphiques de contribution aux fissions
    """
    # Récupérer tous les dossiers de simulation dans data/
    simulation_dirs = glob.glob("data/MOXEUS_*")
    
    if not simulation_dirs:
        print("Aucun dossier de simulation trouvé dans le répertoire data/")
        exit(1)
    
    success_count = 0
    
    # Traiter chaque simulation
    for sim_dir in sorted(simulation_dirs):
        simulation_name = os.path.basename(sim_dir)
        
        # Générer le graphique de contribution aux fissions
        if plot_fission_contribution(sim_dir, simulation_name):
            success_count += 1
            print(f"Traitement réussi pour {simulation_name}")
        else:
            print(f"Échec du traitement pour {simulation_name}")
    
    print(f"\nTraitement terminé. {success_count}/{len(simulation_dirs)} simulations traitées avec succès.")

if __name__ == "__main__":
    process_all_simulations()