import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal dataset
data = []

with open('../dataset/database.2025.md', 'r') as file:
    for line in file:
        numbers = list(map(int, line.strip().split(',')))
        data.append(numbers)

# Inizializza un dizionario per memorizzare i filotti
filotti = {i: 0 for i in range(1, 367)}

# Itera su ogni numero da 1 a 366
for number in range(1, 367):
    current_streak = 0  # Reset per ogni numero

    # Verifica le righe nel database
    for row in data:
        if number in row:  # Se il numero è presente nella riga
            current_streak += 1
        else:
            filotti[number] = max(filotti[number], current_streak)  # Aggiorna il filotto se necessario
            current_streak = 0  # Resetta il conteggio se il numero non è presente

    # Aggiorna il filotto per l'ultimo streak se è in corso
    filotti[number] = max(filotti[number], current_streak)

# Trova il numero con il filotto più lungo
longest_filot = max(filotti.items(), key=lambda x: x[1])
print(f"Numero con il filotto più lungo: {longest_filot[0]}, Lunghezza: {longest_filot[1]}")

# Filtra i filotti per il grafico e l'output (escludendo quelli con lunghezza 0)
filtered_filotti = {num: filotto for num, filotto in filotti.items() if filotto > 0}

# Stampa l'elenco dei filotti per verifica (solo quelli > 0)
print("\nElenco dei filotti per ogni numero (solo lunghezza > 0):")
for num, filotto in filtered_filotti.items():
    print(f"Numero: {num}, Filotto: {filotto}")

# Crea il grafico solo per i filotti con lunghezza > 0
plt.figure(figsize=(12, 6))
plt.bar(filtered_filotti.keys(), filtered_filotti.values())
plt.title('Filotti Massimi per Numero (Solo Lunghezza > 0)')
plt.xlabel('Numero')
plt.ylabel('Lunghezza del Filotto')
plt.xticks(range(0, 31, 10))  # Mostra i numeri ogni 10 unità sull'asse x
plt.grid(axis='y')

# Mostra il grafico
plt.show()
