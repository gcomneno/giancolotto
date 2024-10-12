#!/bin/bash

# Controlla se è stato passato un argomento
if [ $# -eq 0 ]; then
    echo "Devi fornire una stringa da cercare."
    exit 1
fi

# La stringa da cercare è il primo argomento
string_to_grep="$1"

# La stringa che contiene caratteri speciali (come parentesi quadre) ?
string_to_grep=$(echo "$1" | sed 's/[][\.*^$(){}?+]/\\&/g')

# Percorso del file di configurazione principale
config_file="./config.ini"

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.all.bak"
cp "$config_file" "$backup_config"

# Inizializza il file di configurazione prima dell'elaborazione
#sed -i "s/^previsionale=.*/previsionale=False/" "$config_file"

# Elenco delle ruote del Lotto (escludendo "Nazionale")
ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

# Ciclo su ogni ruota e richiamo il programma
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"

    # Esegui il programma Python e filtra l'output in base alla stringa fornita
    python.exe ./src/main.py | grep -E "$string_to_grep"
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"
