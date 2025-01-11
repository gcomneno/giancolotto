#!/bin/bash

echo "Inizio esecuzione: $(date)"

num_estr=${1:-999}

: > ../dataset/database.2025.md
echo "Il dataset è stato resettato."

for ((i=2; i<=999; i++)); do
    # Richiama lo script che produce l'output tabellare
    output=$(./ultima_su_tutte.sh "$i")

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
        echo "$lines" >> ../dataset/database.2025.md
        echo "Riga $lines aggiunta al dataset per l'estrazione $i"
    else
        echo "Nessun risultato valido (distanza != N/A) per l'estrazione $i"
    fi
done

echo "Fine esecuzione: $(date)"
