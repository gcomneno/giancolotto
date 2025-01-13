#!/bin/bash

# Script per analizzare un set di dati numerici e calcolare la frequenza dei numeri centrali.
# L'input viene letto riga per riga da una pipe o un file, quindi:
# 1. Estrae i numeri centrali (6a-10a colonna) da ciascuna riga.
# 2. Conta le occorrenze di ciascun numero.
# 3. Ordina i risultati per frequenza decrescente e, a parità di frequenza, per numero crescente.
# 4. Stampa i risultati formattati in una tabella.

# Leggi l'input riga per riga e processalo
while IFS= read -r line; do
    # Per ogni riga dell'input:
    # - Usa awk per analizzare i campi della riga (separati da spazi).
    # - Seleziona i numeri nelle colonne dalla 6a alla 10a.
    # - Controlla che i campi contengano solo numeri utilizzando l'espressione regolare /^[0-9]+$/.
    echo "$line" | awk '{for(i=6; i<=10; i++) if($i ~ /^[0-9]+$/) print $i}'
done | 
# Dopo aver estratto i numeri:
# 1. `sort` ordina i numeri estratti in ordine crescente.
# 2. `uniq -c` conta le occorrenze di ciascun numero (il numero e il conteggio saranno nelle colonne 2 e 1, rispettivamente).
sort | uniq -c | 
# 3. `sort -k1,1nr -k2,2` ordina i risultati:
#    - Per la prima colonna (frequenza) in ordine numerico decrescente (-k1,1nr).
#    - Per la seconda colonna (numero) in ordine numerico crescente (-k2,2).
sort -k1,1nr -k2,2 | 
# 4. Usa awk per formattare l'output:
#    - La seconda colonna (il numero) è stampata con un allineamento di 7 caratteri a sinistra.
#    - La prima colonna (la frequenza) è racchiusa tra < e >.
awk '{printf "%-7s <%s>\n", $2, $1}'

# Esempio di utilizzo:
# Se hai un file `dati.txt` con contenuti simili:
#   1 2 3 4 5 6 7 8 9 10
#   2 3 4 5 6 7 8 9 10 11
#   3 4 5 6 7 8 9 10 11 12
# Puoi eseguire lo script con:
#   cat dati.txt | ./tuo_script.sh
# Risultato atteso:
#   6       <3>
#   7       <3>
#   8       <3>
#   9       <3>
#   10      <3>
