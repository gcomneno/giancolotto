#!/bin/bash

# Verifica che siano stati passati due argomenti
if [ $# -ne 2 ]; then
  echo "Utilizzo: $0 <numero_iterazioni> <limit>"
  exit 1
fi

# Numero di iterazioni (quante volte vuoi eseguire il programma)
iterations=$1

# Limite di righe da processare
limit=$2

# Loop per incrementare l'offset e chiamare il programma Python
for (( offset=0; offset<$iterations; offset++ ))
do
  # Cattura l'output del programma Python
  result=$(python.exe ./src/utils/imc.py --offset $offset --limit $limit)

  # Formattare l'output come richiesto
  echo "[$offset,$limit] => $result"
done
