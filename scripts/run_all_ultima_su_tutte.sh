#!/bin/bash

# Controlla se sono stati forniti argomenti
if [ "$#" -ne 3 ]; then
    echo "Utilizzo: $0 <offset_iniziale> <offset_finale> <num_estr>"
    exit 1
fi

# Assegna gli argomenti a variabili
OFFSET_INIZIALE=$1
OFFSET_FINALE=$2
NUM_ESTR=$3

for (( offset=$OFFSET_INIZIALE; offset<=$OFFSET_FINALE; offset++ )); do
    output=$(./ultima_su_tutte.sh "$offset" "$NUM_ESTR")
    echo "OFFSET [$offset] NU_ESTR [$NUM_ESTR]"
    echo "$output"
done
