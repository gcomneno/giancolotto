#!/bin/bash

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"
script_root="$(realpath "${script_dir}/../scripts")"

# Percorso assoluto del file di configurazione
config_file="${project_root}/config.ini"
get_script="${script_root}/get.sh"

# Imposta i valori di default per gli offset, numero di estrazioni
OFFSET_INIZIO=0
OFFSET_FINE=0
NUM_ESTRAZIONI=999

# Leggi i parametri in ingresso
if [ "$#" -ge 1 ]; then
    OFFSET_INIZIO=$1
fi
if [ "$#" -ge 2 ]; then
    OFFSET_FINE=$2
fi
if [ "$#" -ge 3 ]; then
    NUM_ESTRAZIONI=$3
fi

# Calcola la differenza tra OFFSET_FINE e OFFSET_INIZIO e aggiungi sempre 1
DIFFERENZA=$((OFFSET_FINE - OFFSET_INIZIO + 1))

# Verifica che la differenza sia valida
if [ "$DIFFERENZA" -lt 0 ]; then
    echo "[ERROR] OFFSET_FINE deve essere maggiore o uguale a OFFSET_INIZIO."
    exit 1
fi

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.categorizer.bak"
cp "$config_file" "$backup_config"

# Aggiorna il file di configurazione con il numero di estrazioni ed il filtro sulle cifre
sed -i "s/^num_estr=.*/num_estr=${NUM_ESTRAZIONI}/" "$config_file"
sed -i "s/^filtro=.*/filtro=cifre/" "$config_file"

# FORZA il valore corretto di previsionale altrimenti non si genera la classifica CRIFROLOTTO
sed -i "s/^previsionale=.*/previsionale=True/" "$config_file"

# Loop per eseguire lo script Python con diversi offset
for ((i = 0; i < DIFFERENZA; i++)); do
    from=$((OFFSET_INIZIO + i))
    
    # Aggiorna offset nel file di configurazione
    sed -i "s/^offset_estr=.*/offset_estr=${from}/" "$config_file"

    # Esegui lo script Python passando direttamente l'offset
    ${get_script} | tail -1

    # Controllo errori
    if [ $? -ne 0 ]; then
        echo "[ERRORE] Errore durante l'esecuzione dello script Python nella iterazione $i. Terminazione."
        mv "$backup_config" "$config_file"
        exit 1
    fi
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"
