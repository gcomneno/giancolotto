#!/bin/bash

# Verifica che siano stati passati due argomenti
if [ $# -ne 3 ]; then
  echo "Utilizzo: $0 <numero_iterazioni> <offset> <limit>"
  exit 1
fi

# Numero di iterazioni (quante volte vuoi eseguire il programma)
iterations=$1

# Prima riga da processare
starting_offset=$2

# Limite di righe da processare
limit=$3

# Loop per incrementare l'offset e chiamare il programma Python IMC
for (( offset=$starting_offset; offset<$starting_offset + $iterations; offset++ ))
do
  # Cattura l'output del programma Python
  result=$(python.exe ../src/utils/imc.py --offset $offset --limit $limit)

  echo "[$offset,$limit] $result"
done
