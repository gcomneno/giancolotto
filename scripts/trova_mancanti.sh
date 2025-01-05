#!/bin/bash

# Crea un array di tutti i numeri da 1 a 90 (includendo gli zeri davanti per i numeri da 1 a 9)
numeri_totali=($(seq -f "%02g" 1 90))

# Leggi i numeri presenti dall'input standard
numeri_presenti=($(cat -))

# Trova i numeri mancanti confrontando i due array
echo "Numeri mancanti:"
echo "--------------------"

for numero in "${numeri_totali[@]}"; do
    if ! [[ " ${numeri_presenti[@]} " =~ " ${numero} " ]]; then
        echo $numero
    fi
done
