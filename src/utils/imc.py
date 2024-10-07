# INSIEME MINIMO di COPERTURA

from itertools import chain
from collections import defaultdict

# Carica i dati dal file database.md
data = []

with open('database.md', 'r') as file:
    for line in file:
        numbers = list(map(int, line.strip().split(',')))
        data.append(numbers)

# Step 1: Determinare la frequenza di ogni numero
frequency = defaultdict(int)
for row in data:
    for number in set(row):  # Usiamo set per evitare di contare duplicati nella stessa riga
        frequency[number] += 1

# Step 2: Ordinare i numeri per frequenza decrescente
sorted_numbers = sorted(frequency, key=frequency.get, reverse=True)

# Step 3: Costruire l'insieme di copertura minimo
covered_rows = set()
selected_numbers = set()

for number in sorted_numbers:
    new_rows_covered = [i for i, row in enumerate(data) if i not in covered_rows and number in row]
    if new_rows_covered:
        selected_numbers.add(number)
        covered_rows.update(new_rows_covered)
    if len(covered_rows) == len(data):  # Se tutte le righe sono coperte, interrompi
        break

print(selected_numbers)
