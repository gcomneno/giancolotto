#!/bin/bash

# Controlla se sono stati forniti al massimo 3 argomenti
if [ "$#" -gt 3 ]; then
    echo "Utilizzo: $0 <offset_finale> <num_estr> [reset]"
    exit 1
fi

# Script per l'aggiornamento del database in base all'analisi di più estrazioni
echo "Inizio esecuzione: $(date)"

# Ricevi l'offset e num_estr dal comando o imposta valori predefiniti
offset_estr=${1:-0}  # Se il primo argomento è omesso, usa 0
num_estr=${2:-33}     # Se il secondo argomento è omesso, usa 33

# Controlla se l'utente ha passato il parametro "reset"
if [ "$#" -eq 3 ] && [[ "$3" == "reset" ]]; then
    # Resetta il file database.md
    : > database.md
    echo "Il file database.md è stato resettato."
fi

# Loop per eseguire "ultima_su_tutte.sh" un certo numero di volte in base all'offset
for ((i=offset_estr; i>=0; i--)); do
    # Esegui ultimi.sh con un parametro che simula l'offset
    output=$(./ultima_su_tutte.sh "$i" "$num_estr")

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
