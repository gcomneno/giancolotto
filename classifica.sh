#!/bin/bash

# Stampa intestazione
#echo "Numero  Occorrenze"
#echo "--------------------"

# Leggi l'input dalla pipe e processalo
while IFS= read -r line; do
    # Usa awk per isolare solo i 5 numeri centrali (da 4 a 8 posizioni)
    echo "$line" | awk '{for(i=6;i<=10;i++) if($i ~ /^[0-9]+$/) print $i}'
done | sort | uniq -c | sort -k1,1nr -k2,2 | awk '{printf "%-7s <%s>\n", $2, $1}' # Allineamento colonne
