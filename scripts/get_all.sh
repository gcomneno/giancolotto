#!/bin/bash

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"

# Percorso assoluto del file di configurazione
config_file="${project_root}/config.ini"

# Percorso assoluto dello script principale
main_script="${project_root}/src/main.py"

# Verifica che il file di configurazione esista
if [[ ! -f "${config_file}" ]]; then
    echo "[ERROR] File di configurazione non trovato: ${config_file}"
    exit 1
fi

# Esegui lo scraping
offset_da=${1:-$(date +%Y)}
offset_a=${2:-$(date +%Y)}

ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

backup_config="${config_file}.all.bak"
cp "$config_file" "$backup_config"

for anno in $(seq $offset_da $offset_a); do
    sed -i "s|^url=.*|url=https://www.estrazionedellotto.it/risultati/archivio-lotto-${anno}|" "$config_file"

    for ruota in "${ruote[@]}"; do
        sed -i "s|^ruota=.*|ruota=${ruota}|" "$config_file"
        python "${main_script}"
    done
done

mv "$backup_config" "$config_file"
