import argparse

from itertools import chain
from collections import defaultdict

def insieme_minimo_di_copertura(offset, limit):
    # Carica i dati dal dataset
    data = []
    with open('./dataset/database.2025.md', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            numeri_str = parts[1:]  # ignore ruota

            numbers = list(map(int, numeri_str))
            data.append(numbers)

    total_rows = len(data)

    # Gestione dell'offset negativo
    if offset < 0:
        # Se l'offset è negativo, si parte dalla fine del file
        start = total_rows + offset
        if start < 0:
            start = 0  # In caso di offset troppo negativo, iniziamo dalla prima riga
    else:
        # Offset normale, si parte dall'inizio
        start = offset

    # Se limit è None (non specificato), elaboriamo tutto il database dalla posizione 'start' in poi
    if limit is None:
        limit = total_rows - start  # Elaborare tutte le righe a partire da 'start'

    # Applica offset e limit per selezionare la porzione del dataset
    data_subset = data[start:start+limit]
    
    # Step 1: Determinare la frequenza di ogni numero
    frequency = defaultdict(int)
    for row in data_subset:
        for number in set(row):  # Usiamo set per evitare di contare duplicati nella stessa riga
            frequency[number] += 1

    # Step 2: Ordinare i numeri per frequenza decrescente
    sorted_numbers = sorted(frequency, key=frequency.get, reverse=True)

    # Step 3: Costruire l'insieme di copertura minimo
    covered_rows = set()
    selected_numbers = set()

    for number in sorted_numbers:
        new_rows_covered = [i for i, row in enumerate(data_subset) if i not in covered_rows and number in row]
        if new_rows_covered:
            selected_numbers.add(number)
            covered_rows.update(new_rows_covered)
        if len(covered_rows) == len(data_subset):  # Se tutte le righe sono coperte, interrompi
            break

    return selected_numbers

# Funzione per gestire i parametri da riga di comando
def main():
    parser = argparse.ArgumentParser(description='Calcola l\'insieme minimo di copertura di un dataset.')
    parser.add_argument('--offset', type=int, default=0, help='Numero di estrazioni da cui partire (offset). Può essere negativo. Default: 0')
    parser.add_argument('--limit', type=int, help='Numero di estrazioni da elaborare (limit). Default: tutte le righe.')

    args = parser.parse_args()

    risultato = insieme_minimo_di_copertura(args.offset, args.limit)

    # Formattare i numeri per essere stampati con due cifre
    formatted_result = ' '.join(f'{num:02}' for num in risultato)

    # Stampa il risultato formattato
    print(f"Insieme minimo di copertura: {formatted_result}")

if __name__ == '__main__':
    main()
