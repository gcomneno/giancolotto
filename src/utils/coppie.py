from itertools import combinations

# Carica i dati dal file database.md
data = []

with open('database.md', 'r') as file:
    for line in file:
        numbers = list(map(int, line.strip().split(',')))
        data.append(numbers)

# Genera tutte le possibili coppie di numeri unici presenti nei dati
unique_numbers = set(num for row in data for num in row)
coppie = list(combinations(unique_numbers, 2))

# Contatore per le coppie
coppie_count = {coppia: 0 for coppia in coppie}

# Controllo quante volte le coppie appaiono nei dati
for row in data:
    for coppia in coppie:
        # Verifica se entrambi i numeri della coppia sono nella riga corrente
        if all(num in row for num in coppia):
            coppie_count[coppia] += 1

# Ordina le coppie per numero di volte in ordine decrescente
sorted_coppie = sorted(coppie_count.items(), key=lambda item: item[1], reverse=True)

# Stampa il risultato in un formato leggibile
print("Conteggio delle coppie trovate (in ordine decrescente):")
for coppia, count in sorted_coppie:
    print(f"Coppia {coppia}: {count} volta/e")
