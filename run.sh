#!/bin/bash

# Couleurs pour l'interface
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Titre
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}=      SERPENT Analysis Scripts      =${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Détection automatique des scripts Python
scripts=($(ls scripts/*.py 2>/dev/null | xargs -n 1 basename))

# Vérifier si des scripts ont été trouvés
if [ ${#scripts[@]} -eq 0 ]; then
    echo -e "${YELLOW}Aucun script Python trouvé dans le dossier scripts/${NC}"
    exit 1
fi

# Fonction pour afficher une barre de progression
progress_bar() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((width * current / total))
    local remaining=$((width - completed))
    
    printf "\r["
    printf "%${completed}s" | tr ' ' '='
    printf "%${remaining}s" | tr ' ' ' '
    printf "] %d%%" "$percentage"
}

# Fonction pour formater le temps
format_time() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(( (seconds % 3600) / 60 ))
    local secs=$((seconds % 60))
    
    if [ $hours -gt 0 ]; then
        printf "%dh %dm %ds" $hours $minutes $secs
    elif [ $minutes -gt 0 ]; then
        printf "%dm %ds" $minutes $secs
    else
        printf "%ds" $secs
    fi
}

# Fonction pour afficher le menu
display_menu() {
    echo -e "${BLUE}Scripts disponibles :${NC}"
    echo ""
    
    for i in "${!scripts[@]}"; do
        echo -e "  ${YELLOW}$((i+1))${NC}. ${scripts[$i]}"
    done
    
    echo -e "  ${YELLOW}a${NC}. Exécuter tous les scripts"
    echo -e "  ${YELLOW}q${NC}. Quitter"
    echo ""
    echo -e "${BLUE}Note: Pour exécuter plusieurs scripts, entrez les numéros séparés par des espaces (ex: 2 5 3)${NC}"
    echo ""
}

# Fonction pour exécuter un script
run_script() {
    local script=$1
    local start_time=$(date +%s)
    
    echo -e "${BLUE}Exécution de ${script}...${NC}"
    echo -e "${YELLOW}Début: $(date '+%H:%M:%S')${NC}"
    
    # Exécution du script avec capture de la sortie
    if python scripts/${script} 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo -e "${GREEN}Script ${script} terminé avec succès en $(format_time $duration)${NC}"
    else
        echo -e "${RED}Erreur lors de l'exécution du script ${script}${NC}"
    fi
    echo ""
}

# Fonction pour exécuter plusieurs scripts spécifiés par leurs numéros
run_multiple_scripts() {
    echo -n "Entrez les numéros des scripts à exécuter (séparés par des espaces): "
    read -a script_numbers
    
    for num in "${script_numbers[@]}"; do
        if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "${#scripts[@]}" ]; then
            run_script "${scripts[$((num-1))]}"
        else
            echo -e "${YELLOW}Numéro invalide: $num. Ignoré.${NC}"
        fi
    done
}

# Fonction pour exécuter tous les scripts avec barre de progression
run_all_scripts() {
    local total_scripts=${#scripts[@]}
    local current_script=0
    local start_time=$(date +%s)
    
    echo -e "${BLUE}Exécution de tous les scripts...${NC}"
    echo -e "${YELLOW}Début: $(date '+%H:%M:%S')${NC}"
    echo ""
    
    for script in "${scripts[@]}"; do
        ((current_script++))
        echo -e "${BLUE}[$current_script/$total_scripts] Exécution de ${script}...${NC}"
        progress_bar $current_script $total_scripts
        echo ""
        
        if python scripts/${script} 2>&1; then
            echo -e "${GREEN}✓ ${script} terminé${NC}"
        else
            echo -e "${RED}✗ Erreur dans ${script}${NC}"
        fi
        echo ""
    done
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    echo -e "${GREEN}Temps total d'exécution: $(format_time $duration)${NC}"
    echo ""
}

# Boucle principale
while true; do
    display_menu
    echo -n "Entrez votre choix (1-${#scripts[@]}, a, q ou plusieurs numéros): "
    read choice
    echo ""
    
    # Vérifier si l'entrée contient plusieurs numéros séparés par des espaces
    if [[ "$choice" =~ ^[0-9]+( [0-9]+)*$ ]]; then
        # Convertir l'entrée en tableau
        read -a script_numbers <<< "$choice"
        for num in "${script_numbers[@]}"; do
            if [ "$num" -ge 1 ] && [ "$num" -le "${#scripts[@]}" ]; then
                run_script "${scripts[$((num-1))]}"
            else
                echo -e "${YELLOW}Numéro invalide: $num. Ignoré.${NC}"
            fi
        done
        continue
    fi
    
    case $choice in
        [1-9]*)
            if [ "$choice" -le "${#scripts[@]}" ]; then
                run_script "${scripts[$((choice-1))]}";
            else
                echo -e "${YELLOW}Choix invalide. Veuillez réessayer.${NC}"
            fi
            ;;
        "a")
            run_all_scripts
            ;;
        "q")
            echo -e "${GREEN}Au revoir !${NC}"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Choix invalide. Veuillez réessayer.${NC}"
            ;;
    esac
done 