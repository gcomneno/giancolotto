#!/bin/bash

# Script per trovare i numeri mancanti da un set completo (1-90) rispetto a un input fornito.
# L'input deve contenere numeri validi (da 1 a 90), uno per riga o separati da spazi.

# 1. Crea un array di tutti i numeri da 1 a 90, formattati con due cifre (es. 01, 02, ..., 90)
numeri_totali=($(seq -f "%02g" 1 90))

# 2. Leggi i numeri presenti dall'input standard
# - `cat -` legge dall'input standard (pipe o redirezione da file).
# - `sort -u` rimuove eventuali duplicati e ordina i numeri.
# - `awk '{printf "%02d\n", $1}'` assicura che tutti i numeri siano formattati con due cifre.
numeri_presenti=($(cat - | sort -u | awk '{printf "%02d\n", $1}'))

# 3. Trova i numeri mancanti confrontando i due array
echo "Numeri mancanti:"
echo "--------------------"

# Loop su tutti i numeri totali (01-90)
for numero in "${numeri_totali[@]}"; do
    # Controlla se il numero corrente è presente nell'array `numeri_presenti`
    if ! [[ " ${numeri_presenti[@]} " =~ " ${numero} " ]]; then
        # Stampa il numero se non è presente
        echo "$numero"
    fi
done
