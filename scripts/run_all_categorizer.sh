#!/bin/bash

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
script_root="$(realpath "${script_dir}")"

# Percorso assoluto del file di configurazione
script_file="${script_root}/run_categorizer.sh"

# Imposta i valori di default per gli offset, numero di estrazioni
GROUP_OFFSET_INIZIO=0
GROUP_OFFSET_FINE=0

# Leggi i parametri in ingresso
if [ "$#" -ge 1 ]; then
    GROUP_OFFSET_INIZIO=$1
fi
if [ "$#" -ge 2 ]; then
    GROUP_OFFSET_FINE=$2
fi

ANNO=$(date +"%Y") # Imposta il valore di default all'anno corrente
if [ "$#" -ge 3 ]; then
    ANNO=$3
fi

# Loop per eseguire lo script con diversi offset
for ((i=GROUP_OFFSET_INIZIO; i<=GROUP_OFFSET_FINE; i++)); do
    echo "[DEBUG] Dataset svuotato per la prossima esecuzione"
    > ./dataset/cifrolotto.data

    # Esegue lo script e filtra solo i log che iniziano con [INFO]
    echo "[INFO] Esecuzione da offset 0 a 9, con gruppo da $i estrazioni: anno $ANNO"
    bash "${script_file}" 0 200 "$i" "$ANNO" | grep "^\[INFO\]"    
done
