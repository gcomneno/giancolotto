#!/bin/bash

# Controlla se sono stati forniti argomenti
if [ "$#" -ne 4 ]; then
    echo "Utilizzo: $0 <numero_iniziale> <numero_finale> <min_consecutive> <max_tentativi>"
    exit 1
fi

# Assegna gli argomenti a variabili
NUM_INIZIALE=$1
NUM_FINALE=$2
MIN_CONSECUTIVE=$3
MAX_ATTEMPTS=$4

# Loop attraverso il range di numeri
for (( numero=$NUM_INIZIALE; numero<=$NUM_FINALE; numero++ )); do
    echo "Elaborazione del numero: $numero"
    python.exe ../src/utils/strategy.py "$numero" "$MIN_CONSECUTIVE" "$MAX_ATTEMPTS"
    echo "-----------------------------------"
done
