import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal file database.md
data = []

with open('database.md', 'r') as file:
    for line in file:
        numbers = list(map(int, line.strip().split(',')))
        data.append(numbers)

# Conteggio per fasce di decine
decade_ranges = [(i, i + 9) for i in range(0, 80, 10)]
decade_counts = {f"{low:02}-{high:02}": 0 for low, high in decade_ranges}  # Cambiato per l'allineamento

# Conta i numeri per ogni fascia
for row in data:
    for number in row:
        for low, high in decade_ranges:
            if low <= number <= high:
                decade_counts[f"{low:02}-{high:02}"] += 1  # Cambiato per l'allineamento

# Converti in DataFrame
df_decades = pd.DataFrame(list(decade_counts.items()), columns=["Fascia di Decine", "Frequenza"])
df_decades.sort_values(by="Frequenza", ascending=False, inplace=True)

# Calcola la percentuale delle frequenze
total_count = df_decades["Frequenza"].sum()
df_decades["Percentuale"] = (df_decades["Frequenza"] / total_count) * 100

# Stampa i dati delle percentuali
print("Dati delle Percentuali:")
for index, row in df_decades.iterrows():
    print(f"Fascia di Decine: {row['Fascia di Decine']}, Frequenza: {row['Frequenza']}, Percentuale: {row['Percentuale']:.2f}%")

# Grafico a barre delle frequenze
plt.figure(figsize=(10, 6))
plt.bar(df_decades["Fascia di Decine"], df_decades["Frequenza"], color='lightblue')
plt.title('Frequenza per Fascia di Decine')
plt.xlabel('Fascia di Decine')
plt.ylabel('Frequenza')
plt.xticks(rotation=45)
plt.grid(axis='y')

# Mostra il grafico
plt.tight_layout()
plt.show()
