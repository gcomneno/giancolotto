#!/bin/bash

# Calcola la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Calcola la root del progetto come una directory sopra quella dello script
project_root="$(realpath "${script_dir}/..")"

# Percorsi assoluti per i file richiesti
config_file="${project_root}/config.ini"
main_script="${project_root}/src/main.py"

# La stringa da cercare è il primo argomento, usa "[U]" se non viene fornito nulla
string_to_grep="${1:-[U]}"

# Esegui l'escape dei caratteri speciali
string_to_grep=$(echo "$string_to_grep" | sed 's/[][\.*^$(){}?+]/\\&/g')

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.all.bak"
cp "$config_file" "$backup_config"

# Elenco delle ruote del Lotto (escludendo "Nazionale")
ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

# Intestazione
separator_line=$(printf '=%.0s' {1..80})
echo "$separator_line"
header="Estrazione\t\tRUOTA\t\t"
columns=""
for i in $(seq 1 5); do
    columns="${columns}${i}o\t"
done
header="${header}${columns}"
echo -e "$header"
echo "$separator_line"

# Ciclo su ogni ruota e richiamo il programma
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"

    # Esegui il programma Python e filtra l'output in base alla stringa fornita
    python.exe "$main_script" | grep -E "$string_to_grep"
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"
