#!/bin/bash

echo "Inizio esecuzione: $(date)"

# Ricevi l'offset da e a per gli anni da considerare o imposta come valore predefinito l'anno corrente
offset_da=${1:-$(date +%Y)}
offset_a=${2:-$(date +%Y)}

# Elenco delle ruote del Lotto (escludendo "Nazionale")
ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

# Percorso del file di configurazione principale
config_file="../config.ini"

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.years.bak"
cp "$config_file" "$backup_config"

# Inizializza il file di configurazione prima dell'elaborazione
#sed -i "s/^previsionale=.*/previsionale=True/" "$config_file"

# Ciclo sugli anni da offset_da a offset_a
for anno in $(seq $offset_da $offset_a); do
    # Modifica il file di configurazione per aggiornare la pagina di scraping per anno
    sed -i "s/^url=.*/url=https:\/\/www.estrazionedellotto.it\/risultati\/archivio-lotto-${anno}/" "$config_file"

    # Ciclo su ogni ruota e richiamo il programma
    for ruota in "${ruote[@]}"; do
        # Modifica il file di configurazione per aggiornare la ruota
        sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"

        # Esegui il programma Python e filtra l'output in base al punteggio ottenuto
        python.exe ../src/main.py | tail -n +4
    done
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"

echo "Fine esecuzione: $(date)"
