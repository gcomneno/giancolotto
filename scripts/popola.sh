#!/bin/bash

echo "Inizio esecuzione: $(date)"

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"

# Percorso assoluto del file di database
dataset_file="${project_root}/dataset/database.$(date +%Y).md"

# Percorso assoluto dello script principale
main_script="${project_root}/scripts/ultima_su_tutte.sh"

num_estr=${1:-999}

: > $dataset_file
echo "Il dataset è stato resettato."

for ((i=2; i<=$num_estr; i++)); do
    # Richiama lo script che produce l'output tabellare
    output=$("$main_script" "$i")

    # Estrai la riga contenente "Estrazione"
    estrazione_line=$(echo "$output" | grep "Estrazione:")

    # Estrai il numero dell'estrazione, rimuovendo eventuali zeri iniziali
    numero_estrazione=$(echo "$estrazione_line" | awk '{print $2}' | sed 's/^0*//')

    if [[ "$i" > "$numero_estrazione" ]]; then
        break
    fi

    # Estrai RUOTA e DIST, saltando righe non pertinenti e scartando le distanze "N/A"
    lines=$(echo "$output" | \
      awk -F'|' '
        /Inizio script|Fine script|^-|RUOTA|^$/ { next }   # salta intestazioni, separatori
        NF >= 4 {
          # ripulisce spazi
          gsub(/^ +| +$/, "", $1)   # RUOTA
          gsub(/^ +| +$/, "", $3)   # DIST
          ruota = $1
          dist  = $3

          # Scarta le righe se la distanza è "N/A"
          if (dist != "N/A") {
            # Stampa solo ruota e distanza
            print ruota "," dist
          }
        }
      ')

    if [[ -n "$lines" ]]; then
        # Aggiungi l’output al dataset
        echo "$lines" >> "$dataset_file"
        echo "Riga $lines aggiunta al dataset per l'estrazione $i"
    else
        echo "Nessun risultato valido (distanza != N/A) per l'estrazione $i"
    fi
done

echo "Fine esecuzione: $(date)"
