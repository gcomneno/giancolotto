#!/bin/bash

# Verifica se lo script riceve dati dallo standard input
if [[ -t 0 ]]; then
    echo "Errore: nessun input ricevuto."
    exit 1
fi

# Elaborazione dei dati
awk -F '|' '
{
    for (i=1; i<=NF; i++) {
        split($i, pair, " ")
        if (length(pair) == 2) {
            count[pair[2]] += pair[1]
        }
    }
}
END {
    for (category in count) {
        print category, count[category]
    }
}' | sort -k2,2nr
