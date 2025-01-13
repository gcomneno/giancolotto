#!/bin/bash

echo "Inizio script: $(date)"

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"

# Percorso assoluto del file di configurazione
config_file="${project_root}/config.ini"

# Percorso assoluto dello script principale
main_script="${project_root}/src/main.py"

offset_estr=0
num_estr=${1:-999}

# Elenco delle ruote del Lotto (escludendo "Nazionale")
ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia")

# Dichiarazione di un array associativo per memorizzare i numeri per ciascuna ruota
declare -A numeri_per_ruota

# Dichiarazione di array associativi per memorizzare i risultati che vogliamo riepilogare
# Aggiungiamo un array per "distanza" e uno per "combinazione" (es. se troviamo ambo, terno, ecc.)
declare -A distanza_per_ruota
declare -A vincita_per_ruota

# Creazione di un backup del file di configurazione originale
backup_config="${config_file}.last.bak"
cp "$config_file" "$backup_config"

# Inizializza il file di configurazione prima dell'elaborazione
sed -i "s/^offset_estr=.*/offset_estr="$offset_estr"/" "$config_file"
sed -i "s/^num_estr=.*/num_estr="$num_estr"/" "$config_file"
sed -i "s/^previsionale=.*/previsionale=False/" "$config_file"
sed -i "s/^filtro=.*/filtro=numeri/" "$config_file"
sed -i "s/^numeri=.*/numeri=/" "$config_file"
sed -i "s/^cifre=.*/cifre=/" "$config_file"

### 1) Prima Fase: Acquisizione dei 5 numeri sortiti per ciascuna ruota
###     Per ogni ruota, manipola il config.ini ed invoca main.py per catturare i 5 numeri estratti (corrispondenti a [U] = ultima estrazione)
###     Popola l’array associativo numeri_per_ruota.
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"

    # Esegui il programma Python e filtra l'output per ottenere i 5 numeri
    numeri=$(python.exe "$main_script" | grep -v 'RUOTA' | awk '/[U]/ { print $6 "," $7 "," $8 "," $9 "," $10 }')

    # Associa i numeri estratti alla ruota corrente nell'array associativo
    numeri_per_ruota["$ruota"]="$numeri"
done
estrazione=$(python.exe "$main_script" | grep -v 'RUOTA' | awk '/[U]/ { print $2 " del " $4 }')

### 2) Seconda Fase: Calcolo della "distanza" e/o verifica di eventuali combinazioni vincenti
###     Per ogni ruota, scrive i numeri estratti di volta in volta in config.ini, e invoca di nuovo main.py ma filtrando <2>, <3>, <4>, <5>.
###     Calcola la “distanza” (catturando [0], [1], ecc.) e determina il tipo di combinazione (AMBO, TERNO…).
for ruota in "${ruote[@]}"; do
    # Modifica il file di configurazione per aggiornare la ruota ed i relativi numeri
    sed -i "s/^ruota=.*/ruota=${ruota}/" "$config_file"
    sed -i "s/^numeri=.*/numeri=${numeri_per_ruota[$ruota]}/" "$config_file"

    # Esegui il programma Python e filtra l'output in base alle combinazioni ottenute (dall'ambo in su!)
    output=$(python.exe "$main_script" | grep -E "<2>|<3>|<4>|<5>" | grep -v "\[U\]")

    #Calcolo "distance" se l'output mostra un [0], [1], ecc.
    dist=$(echo "$output" | grep -o '\[[0-9]*\]' | tr -d '[]')  # estrae 0, 1, 2...
    if [[ -z "$dist" ]]; then
        dist="N/A"
    fi

    # Catturiamo la tipologia di vincita (ambo, terno, ecc.) in base al tag <2>, <3>, ...
    if echo "$output" | grep -q "<2>"; then
        win="AMBO"
    elif echo "$output" | grep -q "<3>"; then
        win="TERNO"
    elif echo "$output" | grep -q "<4>"; then
        win="QUATERNA"
    elif echo "$output" | grep -q "<5>"; then
        win="CINQUINA"
    else
        win="Nessuna combinazione trovata"
    fi

    # Salviamo nei nostri array associativi
    distanza_per_ruota["$ruota"]="$dist"
    vincita_per_ruota["$ruota"]="$win"
done

# Ripristina il file di configurazione originale
mv "$backup_config" "$config_file"

echo "Estrazione: $estrazione"
echo "---------------------------------------------------------------------------"
printf "%-10s | %-14s | %-30s | %-20s\n" "RUOTA" "NUMERI" "DIST" "VINCITA"
echo "---------------------------------------------------------------------------"
for ruota in "${ruote[@]}"; do
    numeri="${numeri_per_ruota[$ruota]}"
    dist="${distanza_per_ruota[$ruota]}"
    win="${vincita_per_ruota[$ruota]}"

    # Se "DIST" contiene più righe, uniscile in una singola riga separata da virgole
    dist=$(echo "$dist" | tr '\n' ',' | sed 's/,$//') # Trasforma nuove righe in virgole e rimuove l'ultima virgola

    # Esempio di output tabellare
    printf "%-10s | %-14s | %-30s | %-20s\n" "$ruota" "$numeri" "$dist" "$win"
done
echo "---------------------------------------------------------------------------"
echo "Fine script: $(date)"
