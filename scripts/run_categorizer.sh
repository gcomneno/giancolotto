#!/bin/bash

# Imposta i valori di default per gli offset e il numero di estrazioni
OFFSET_INIZIO=0
OFFSET_FINE=0
NUM_ESTRAZIONI=999

# Leggi i parametri in ingresso
if [ "$#" -ge 1 ]; then
    OFFSET_INIZIO=$1
fi
if [ "$#" -ge 2 ]; then
    OFFSET_FINE=$2
fi
if [ "$#" -ge 3 ]; then
    NUM_ESTRAZIONI=$3
fi

# Calcola la differenza tra OFFSET_FINE e OFFSET_INIZIO e aggiungi sempre 1
DIFFERENZA=$((OFFSET_FINE - OFFSET_INIZIO + 1))

# Verifica che la differenza sia valida
if [ "$DIFFERENZA" -lt 0 ]; then
    echo "Errore: OFFSET_FINE deve essere maggiore o uguale a OFFSET_INIZIO."
    exit 1
fi

# Loop per eseguire lo script Python senza parametri DIFFERENZA volte
for ((i = 1; i <= DIFFERENZA; i++)); do
    echo "Esecuzione $i di $DIFFERENZA"
    python.exe ./src/utils/cifrolotto_categorizer.py
    if [ $? -ne 0 ]; then
        echo "Errore durante l'esecuzione dello script Python nella iterazione $i. Terminazione."
        exit 1
    fi
done

echo "Tutte le $DIFFERENZA esecuzioni sono state completate con successo."

echo "Esecuzione del Totalizzatore"
python.exe ./src/utils/cifrolotto.py
if [ $? -ne 0 ]; then
    echo "Errore durante l'esecuzione dello script totalizzatore. Terminazione."
    exit 1
fi
