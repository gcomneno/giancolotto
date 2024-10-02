#!/bin/bash

# Ricevi l'offset dal comando o imposta un valore predefinito
offset=${1:-0}

# Decrementa l'offset solo se è stato fornito un valore diverso da 0
if [ "$1" ]; then
    offset=$((offset - 1))
fi

# Elenco delle ruote del Lotto (escludendo "Nazionale")
ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

# Dichiarazione di un array associativo per memorizzare i numeri per ciascuna ruota
declare -A numeri_per_ruota

# Percorso del file di configurazione principale
config_file="./config.ini"

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.bak"
cp "$config_file" "$backup_config"

# Inizializza il file di configurazione prima dell'elaborazione
sed -i "s/^previsionale=.*/previsionale=True/" "$config_file"
sed -i "s/^numeri=.*/numeri=/" "$config_file"
sed -i "s/^cifre=.*/cifre=/" "$config_file"
sed -i "s/^offset_estr=.*/offset_estr=$offset/" "$config_file"

# Ciclo su ogni ruota e richiama il programma per conservare l'ultimissima estrazione
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"

    # Esegui il programma Python e filtra l'output per ottenere i 5 numeri
    numeri=$(python.exe ./src/main.py | grep -v 'RUOTA' | awk '/[U]/ { print $6 "," $7 "," $8 "," $9 "," $10 }')

    # Associa i numeri estratti alla ruota corrente nell'array associativo
    numeri_per_ruota["$ruota"]="$numeri"
done

# Ciclo su ogni ruota e richiamo il processo
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota ed i relativi numeri
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"
    sed -i "s/^numeri=.*/numeri=${numeri_per_ruota[$ruota]}/" "$config_file"

    # Esegui il programma Python e filtra l'output in base al punteggio ottenuto
    python.exe ./src/main.py | grep -E "<2>|<3>|<4>|<5>" | grep -v "\[U\]"
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"
