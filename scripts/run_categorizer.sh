#!/bin/bash

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"

# Percorso assoluto del file di configurazione
config_file="${project_root}/config.ini"

# Imposta i valori di default per gli offset, numero di estrazioni e file di output
OFFSET_INIZIO=0
OFFSET_FINE=0
NUM_ESTRAZIONI=999
OUTPUT_FILE="./dataset/cifrolotto.data"

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
if [ "$#" -ge 4 ]; then
    OUTPUT_FILE=$4
fi

# Calcola la differenza tra OFFSET_FINE e OFFSET_INIZIO e aggiungi sempre 1
DIFFERENZA=$((OFFSET_FINE - OFFSET_INIZIO + 1))

# Verifica che la differenza sia valida
if [ "$DIFFERENZA" -lt 0 ]; then
    echo "Errore: OFFSET_FINE deve essere maggiore o uguale a OFFSET_INIZIO."
    exit 1
fi

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.categorizer.bak"
cp "$config_file" "$backup_config"

# Aggiorna il file di configurazione con il numero di estrazioni ed il filtro sulle cifre
sed -i "s/^num_estr=.*/num_estr=${NUM_ESTRAZIONI}/" "$config_file"
sed -i "s/^filtro=.*/filtro=cifre/" "$config_file"

# Verifica se il file di output esiste già, in tal caso lo svuota
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Il file di output ${OUTPUT_FILE} esiste già. Verrà sovrascritto."
    > "$OUTPUT_FILE"
else
    touch "$OUTPUT_FILE"
fi

# Loop per eseguire lo script Python senza parametri DIFFERENZA volte
for ((i = 0; i < DIFFERENZA; i++)); do
    sed -i "s/^offset_estr=.*/offset_estr=${i}/" "$config_file"
    echo "Esecuzione ${i+1} di $DIFFERENZA"
    python.exe ./src/utils/cifrolotto_categorizer.py --output-file "$OUTPUT_FILE"
    if [ $? -ne 0 ]; then
        echo "Errore durante l'esecuzione dello script Python nella iterazione $i. Terminazione."
        # Ripristina il file di configurazione originale
        mv "$backup_config" "$config_file"
        exit 1
    fi
done

echo "Tutte le $DIFFERENZA esecuzioni sono state completate con successo."

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"

# Esecuzione del totalizzatore
echo "Esecuzione del Totalizzatore"
python.exe ./src/utils/cifrolotto.py
if [ $? -ne 0 ]; then
    echo "Errore durante l'esecuzione dello script totalizzatore. Terminazione."
    exit 1
fi
