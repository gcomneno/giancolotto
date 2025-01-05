#!/bin/bash

# Controlla se sono stati forniti al massimo 3 argomenti
if [ "$#" -gt 3 ]; then
    echo "Utilizzo: $0 <offset_finale> <num_estr> [reset]"
    exit 1
fi

echo "Inizio esecuzione: $(date)"

# Ricevi l'offset e num_estr dal comando o imposta valori predefiniti
offset_estr=${1:-0}
num_estr=${2:-999}

# Se l'utente passa "reset" come 3° argomento
if [ "$#" -eq 3 ] && [[ "$3" == "reset" ]]; then
    : > ../dataset/database.2025.md
    echo "Il dataset è stato resettato."
fi

# Loop sugli offset
for ((i=offset_estr; i>=0; i--)); do
    # Richiama lo script che produce l'output tabellare
    output=$(./ultima_su_tutte.sh "$i" "$num_estr")

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
        echo "$lines" >> ../dataset/database.2025.md
        echo "Righe (ruota,distanza) aggiunte al dataset (estrazione offset $i):"
        echo "$lines"
    else
        echo "Nessun risultato valido (distanza != N/A) per l'offset $i."
    fi
done

echo "Fine esecuzione: $(date)"
