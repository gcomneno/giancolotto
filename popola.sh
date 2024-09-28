#!/bin/bash

# Script per l'aggiornamento del database in base all'analisi di più estrazioni
echo "Inizio esecuzione: $(date)"

# Controlla se l'utente ha passato il parametro "--reset"
if [[ "$1" == "--reset" ]]; then
    # Se è stato usato --reset, svuota il file database.md
    > database.md
    echo "Il file database.md è stato resettato."
fi

# Recupera l'offset_estr dall'input utente (se non fornito, default a 1)
offset_estr=${2:-1}

# Loop per eseguire "ultimi.sh" un certo numero di volte in base all'offset
for ((i=offset_estr; i>=1; i--)); do
    # Esegui ultimi.sh con un parametro che simula l'offset
    output=$(./ultimi.sh "$i")

    # Estrai i numeri tra parentesi quadre, rimuovi le parentesi, ordina e unisci con virgole
    numbers=$(echo "$output" | grep -o '\[[0-9]*\]' | tr -d '[]' | sort -n | paste -sd ',' -)

    # Aggiungi i numeri al file database.md in append con accapo alla fine
    if [[ -n "$numbers" ]]; then
        echo "$numbers" >> database.md
        echo "Numeri aggiunti a database.md (estrazione offset $i):"
        echo "$numbers"
    else
        echo "Nessun numero trovato per essere aggiunto a database.md (estrazione offset $i)."
    fi
done

echo "Fine esecuzione: $(date)"
