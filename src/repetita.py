# Ricostruisco i dati persi dall'estrazione precedente

# Definiamo l'estrazione dei dati del database per la fascia 20-28
database = [
    [8,11,16,18,20,23,28],
    [2,21,24,25],
    [2,3,6,7,8,9,13,23],
    [4,5,23,25],
    [2,6,11,13,19,20,23,23],
    [3,12,23,23],
    [1,8,11,12,12,17,17,20,22,28],
    [6,12,16,18,20,26],
    [1,9,12,14,15,20,22,23],
    [1,5,6,6,8,12,13,16,23,24,26],
    [1,7,9,12,15,15,16,18,24],
    [1,3,4,10,17,18,21,24],
    [0,3,10,14,15,20,24,26],
    [6,8,8,10,12,19,20,22,26],
    [0,1,7,7,18,20,21,24],
    [12,19,20,20,25,26],
    [2,5,8,11,13,25,25],
    [1,3,5,9,11,11,22,24],
    [3,6,10,14,14,17,27,28],
    [6,10,10,14,17,20]
]

# Definiamo la fascia 20-28
fascia_20_28 = range(20, 29)

# Funzione per estrarre i numeri della fascia 20-28 da un'estrazione
def extract_fascia_20_28(estrazione):
    return [num for num in estrazione if num in fascia_20_28]

# Controlliamo quante volte la tendenza "Repetita Iuvant" si è verificata
repetita_count = 0
total_checks = len(database) - 1  # Non possiamo confrontare la prima estrazione con una precedente

for i in range(1, len(database)):
    prev_fascia = set(extract_fascia_20_28(database[i-1]))
    current_fascia = set(extract_fascia_20_28(database[i]))
    
    # Se c'è almeno un numero ripetuto
    if prev_fascia & current_fascia:
        repetita_count += 1

# Calcolo della percentuale di successo
success_percentage = (repetita_count / total_checks) * 100
success_percentage

print("Total Checks Count:", total_checks + 1)
print("Repetita Juvant (%):", success_percentage)