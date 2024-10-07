import pandas as pd
import matplotlib.pyplot as plt

# Funzione per massimizzare la finestra del grafico
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')  # Comando per massimizzare la finestra su sistemi Windows

# Carica i dati dal file database.md
data = []

with open('database.md', 'r') as file:
    for line in file:
        numbers = list(map(int, line.strip().split(',')))
        data.append(numbers)

# Creiamo un dizionario per contare le presenze di ogni numero
presence_count = {}

for row in data:
    for number in row:
        if number in presence_count:
            presence_count[number] += 1
        else:
            presence_count[number] = 1

# Ordinare il dizionario per presenze decrescenti
sorted_presence = sorted(presence_count.items(), key=lambda x: x[1], reverse=True)

# Conteggio per fasce di decine
decade_ranges = [(i, i + 9) for i in range(0, 80, 10)]
decade_counts = {f"{low:02}-{high:02}": 0 for low, high in decade_ranges}

# Conta i numeri per ogni fascia
for row in data:
    for number in row:
        for low, high in decade_ranges:
            if low <= number <= high:
                decade_counts[f"{low:02}-{high:02}"] += 1

# Converti in DataFrame
df_decades = pd.DataFrame(list(decade_counts.items()), columns=["Fascia di Decine", "Frequenza"])
df_decades.sort_values(by="Frequenza", ascending=False, inplace=True)

# Calcola la percentuale delle frequenze
total_count = df_decades["Frequenza"].sum()
df_decades["Percentuale"] = (df_decades["Frequenza"] / total_count) * 100

# Creiamo una griglia di 2 grafici (invertito l'ordine)
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Primo grafico: Presenze dei numeri
axs[0].bar([str(number) for number, _ in sorted_presence], [count for _, count in sorted_presence], color='salmon')
axs[0].set_title('Presenze dei Numeri')
axs[0].set_xlabel('Numero')
axs[0].set_ylabel('Presenze')
axs[0].grid(axis='y')
axs[0].tick_params(axis='x', rotation=45)

# Secondo grafico: Frequenza per fascia di decine
axs[1].bar(df_decades["Fascia di Decine"], df_decades["Frequenza"], color='lightblue')
axs[1].set_title('Frequenza per Fascia di Decine')
axs[1].set_xlabel('Fascia di Decine')
axs[1].set_ylabel('Frequenza')
axs[1].grid(axis='y')
axs[1].tick_params(axis='x', rotation=45)

# Migliora la disposizione
plt.tight_layout()

# Massimizza la finestra del grafico
mng = plt.get_current_fig_manager()
mng.window.state('normal')  # Massimizza la finestra (solo su sistemi Windows con backend tkinter)

# Mostra entrambi i grafici in una sola finestra
plt.show()
