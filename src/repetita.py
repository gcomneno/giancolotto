# Definiamo la fascia 20-28
fascia_20_28 = range(20, 29)

# Funzione per estrarre i numeri della fascia 20-28 da un'estrazione
def extract_fascia_20_28(estrazione):
    return [num for num in estrazione if num in fascia_20_28]

# Funzione per leggere il database dal file e convertirlo in una lista di liste
def read_database_from_file(filename):
    with open(filename, 'r') as f:
        # Leggi tutte le righe e separa ogni estrazione basandoti sulle virgole
        lines = f.readlines()
        # Converte le righe in liste di numeri
        database = [list(map(int, line.strip().split(','))) for line in lines if line.strip()]
    return database

# Leggiamo il file database.md
database = read_database_from_file('database.md')

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
success_percentage = (repetita_count / total_checks) * 100 if total_checks > 0 else 0

# Stampa i risultati
print("Total Checks Count:", total_checks + 1)
print("Repetita Iuvant (%):", success_percentage)
