from collections import Counter
from itertools import combinations

# Nuovo set di dati aggiornato
estrazioni = [
    [8,11,16,18,20,23,28],  # Estrazione 1
    [2,21,24,25],           # Estrazione 2
    [2,3,6,7,8,9,13,23],    # Estrazione 3
    [4,5,23,25],            # Estrazione 4
    [2,6,11,13,19,20,23,23],# Estrazione 5
    [3,12,23,23],           # Estrazione 6
    [1,8,11,12,12,17,17,20,22,28],  # Estrazione 7
    [6,12,16,18,20,26],     # Estrazione 8
    [1,9,12,14,15,20,22,23],# Estrazione 9
    [1,5,6,6,8,12,13,16,23,24,26]   # Estrazione 10
]

# Contiamo le occorrenze per ogni colonna (0-28)
tutti_numeri = [num for estrazione in estrazioni for num in estrazione]
frequenze = Counter(tutti_numeri)

# Suddivisione in fasce: Alta, Media, Bassa Frequenza
fascia_alta = {colonna: count for colonna, count in frequenze.items() if count >= 3}
fascia_media = {colonna: count for colonna, count in frequenze.items() if count == 2}
fascia_bassa = {colonna: count for colonna, count in frequenze.items() if count == 1}

print("Frequenze:", frequenze)
print("Fascia Alta:", fascia_alta)
print("Fascia Media:", fascia_media)
print("Fascia Bassa:", fascia_bassa)

# Generiamo tutte le coppie per ogni estrazione
coppie = []
for estrazione in estrazioni:
    coppie.extend(combinations(estrazione, 2))

# Contiamo la frequenza di ogni coppia
frequenze_coppie = Counter(coppie)

# Mostriamo le coppie più frequenti
frequenze_coppie.most_common(10)

print("Frequenze Coppie:", frequenze_coppie)
