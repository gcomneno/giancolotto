# Probabilità condizionale: rappresenta la percentuale di volte che un valore basso è seguito da un valore alto, espressa in percentuale.
# Probabilità complessiva: indica la percentuale di valori alti nella lista.

# Lista dei numeri forniti
#./go.sh | awk '{num = substr($10, 2); if (num ~ /^[0-9]+$/) printf "%s, ", num}' | sed 's/, $//'
numeri = [6, 1, 2, 6, 5, 0, 2, 8, 6, 7, 0, 9, 0, 9, 7, 6, 8, 4, 4, 5, 8, 0, 9, 7, 9, 9, 1, 2, 4, 2, 4, 3, 0, 0, 3, 1, 1, 8, 0, 8, 9, 5, 2, 7, 4, 3, 0, 4, 9, 6, 1, 7, 5, 4, 7, 3, 7, 1, 4, 4, 3, 7, 9, 3, 6, 1, 3, 7, 5, 3, 5, 4, 6, 9, 9, 8, 3, 2, 4, 9, 7, 1, 8, 8, 3, 1, 1, 1, 0, 6, 6, 8, 7, 0, 2, 3, 8, 6, 3, 5, 0, 9, 2, 7, 3, 6, 2, 7, 9, 3, 3, 8, 5, 1, 4, 7, 6, 2, 4, 8, 5, 8, 9, 8, 4, 9, 9, 0, 0, 9, 7, 1, 3, 2, 4, 7, 3, 0, 7, 0, 0, 0, 3, 8, 3, 0, 8, 9,
6, 8, 0, 1, 9, 4, 2, 2, 9, 9, 6, 2, 8, 0, 3, 5, 7, 4, 4, 4, 2, 7, 6, 5, 2, 1, 5, 1, 0, 8, 6, 0, 7, 5, 4, 7, 3, 4, 1, 3, 1, 8, 3, 2, 3, 3, 0, 2, 5, 6, 4, 1, 3, 5, 7, 4, 4, 3, 2, 7, 7, 4, 1, 0, 9, 5, 6, 0, 5, 3, 1, 4, 8, 1, 4, 1, 0, 5, 9, 1, 4, 6, 0, 2, 9, 2, 4, 2, 8, 8, 5, 5, 2, 8, 8, 1, 7, 6, 7, 7, 1, 8, 0, 2, 2, 3, 3, 5, 0, 6, 4, 3, 5, 4, 4, 4, 6, 1, 4, 7, 5, 5, 6, 0, 3, 3, 0, 5, 5, 6, 6, 3, 4, 4, 0, 0, 8, 3, 8, 2, 9, 7, 0, 3, 9, 8, 0, 6,
5, 3, 5, 0, 7, 5, 9, 1, 1, 7, 3, 4, 0, 8, 6, 9, 7, 9, 9, 8, 3, 0, 5, 9, 1, 8, 5, 1, 6, 3, 5, 1, 4, 3, 5, 9, 3, 9, 8, 0, 3, 8, 5, 1, 9, 6, 4, 2, 0, 8, 3, 0, 5, 7, 7, 0, 5, 9, 2, 3, 6, 1, 2, 3, 8, 8, 7, 3, 0, 2, 2, 9, 5, 4, 5, 1, 8, 8, 3, 7, 2, 0, 4, 3, 3, 0, 2, 9, 2, 5, 3, 3, 1, 1, 5, 4, 8, 3, 7, 3, 5, 3, 8, 5, 4, 9, 1, 4, 1, 0, 6, 0, 0, 6, 6, 9, 8, 0, 1, 0, 8, 7, 5, 2, 1, 5, 2, 8, 7, 8, 8, 6, 6, 8, 7, 0, 3, 7, 3, 7, 3, 3, 6, 2, 0, 1, 6, 4,
1, 2, 4, 1, 1, 3, 3, 5, 7, 3, 3, 1, 9, 1, 8, 8, 0, 5, 0, 0, 7, 8, 4, 9, 6, 4, 3, 2, 4, 4, 3, 0, 9, 8, 6, 1, 5, 7, 7, 6, 8, 7, 7, 1, 4, 5, 1, 6, 3, 0, 5, 4, 3, 3, 5, 5, 4, 2, 5, 4, 9, 3, 3, 8, 8, 2, 5, 0, 6, 5, 8, 2, 5, 0, 3, 6, 6, 4, 6, 8, 9, 0, 5, 9, 6, 7, 3, 3, 3, 5, 5, 4, 9, 2, 4, 2, 8, 7, 3, 5, 0, 4, 5, 0, 6, 1, 7, 7, 3, 0, 6, 0, 3, 1, 5, 7, 7, 0, 8, 5, 5, 0, 7, 5, 5, 3, 3, 4, 0, 7, 0, 0, 6, 4, 6, 8, 9, 0, 9, 2, 9, 3, 9, 2, 2, 2, 1, 4,
3, 9, 9, 6, 5, 0, 4, 8, 5, 1, 8, 6, 0, 7, 4, 4, 6, 1, 5, 4, 8, 0, 1, 7, 1, 8, 2, 4, 7, 6, 2, 6, 3, 1, 5, 9, 1, 2, 4, 1, 0, 2, 0, 2, 2, 8, 9, 7, 6, 5, 6, 2, 7, 2, 5, 7, 7, 4, 5, 1, 9, 5, 8, 4, 7, 1, 4, 6, 1, 1, 1, 3, 9, 8, 8, 0, 0, 6, 3, 5, 0, 6, 1, 3, 8, 7, 4, 8, 5, 3, 0, 1, 2, 0, 6, 3, 6, 2, 8, 1, 0, 3, 3, 8, 4, 5, 4, 3, 3, 6, 9, 9, 3, 7, 7, 1, 2, 5, 7, 5, 7, 9, 1, 2, 1, 5, 9, 3, 7, 3, 8, 6, 9, 0, 4, 4, 8, 9, 4, 4, 5, 2, 1, 4, 5, 6, 5, 1,
7, 4, 1, 9, 8, 9, 3, 3, 4, 2, 0, 1, 8, 4, 4, 5, 3, 2, 0, 4, 8, 9, 8, 0, 4, 7, 6, 4, 0, 0, 7, 5, 7, 9, 2, 2, 0, 0, 8, 9, 4, 7, 8, 3, 8, 0, 4, 6, 7, 0, 1, 3, 5, 8, 9, 4, 4, 4, 8, 9, 7, 1, 4, 0, 2, 7, 4, 3, 9, 1, 7, 0, 9, 0, 2, 1, 5, 6, 7, 1, 0, 8, 4, 5, 1, 1, 2, 5, 4, 0, 7, 9, 8, 1, 6, 0, 9, 1, 4, 6, 5, 9, 2, 1, 9, 3, 0, 7, 7, 9, 6, 2, 7, 0, 5, 2, 1, 8, 6, 8, 1, 0, 2, 9, 4, 1, 1, 1, 9, 5, 2, 3, 2, 0, 2, 3, 0, 4, 1, 6, 5, 1, 9, 3, 7, 0, 9, 1,
5, 6, 2, 5, 2, 0, 1, 8, 1, 0, 9, 2, 8, 0, 0, 1, 4, 3, 8, 4, 4, 9, 2, 7, 6, 6, 8, 4, 0, 5, 4, 1, 5, 6, 4, 0, 7, 0, 8, 7, 5, 6, 9, 5, 2, 5, 4, 8, 3, 5, 3, 6, 6, 1, 4, 6, 4, 9, 3, 3, 7, 8, 2, 0, 0, 7, 3, 2, 2, 0, 4, 0, 3, 5, 7, 6, 7, 0, 0, 6, 8, 5, 2, 0, 0, 0, 2, 7, 7, 8, 1, 1, 8, 4, 2, 3, 1, 7, 2, 9, 3, 8, 6, 1, 8, 1, 6, 9, 3, 8, 5, 2, 6, 2, 7, 1, 7, 3, 1, 5, 9, 3, 3, 5, 7, 9, 8, 4, 5, 9, 9, 2, 1, 2, 0, 8, 8, 7, 5, 4, 4, 8, 7, 2, 3, 9, 8, 0,
2, 7, 0, 5, 9, 5, 3, 1, 2, 3, 3, 8, 6, 5, 5, 8, 5, 9, 4, 8, 2, 2, 6, 0, 1, 3, 5, 2, 3, 1, 4, 1, 7, 8, 1, 4, 5, 1, 8, 0, 3, 4, 7, 4, 8, 5, 6, 4, 0, 8, 8, 1, 1, 6, 3, 7, 7, 2, 4, 6, 6, 3, 4, 1, 1, 0, 5, 6, 9, 3, 9, 3, 7, 9, 8, 5, 2, 0, 4, 3, 4, 0, 9, 8, 8, 7, 7, 9, 0, 4, 4, 1, 0, 6, 5, 8, 1, 2, 7, 3, 7, 6, 3, 9, 6, 5, 8, 3, 8, 5, 4, 2, 9, 6, 6, 3, 1, 2, 2, 1, 3, 2, 9, 7, 7, 4, 7, 8, 6, 9, 4, 1, 0, 3, 9, 5, 0, 2, 0, 5, 1, 6, 5, 2, 3, 3, 3, 4,
3, 6, 8, 1, 5, 8, 6, 1, 5, 0, 9, 8, 5, 1, 5, 1, 3, 4, 7, 7, 4, 0, 3, 1, 7, 0, 6, 7, 2, 9, 8, 7, 5, 2, 0, 9, 5, 7, 7, 1, 2, 2, 4, 8, 8, 6, 1, 1, 5, 2, 4, 9, 2, 4, 1, 4, 0, 7, 0, 8, 6, 4, 7, 1, 5, 2, 3, 5, 2, 4, 8, 4, 9, 8, 1, 8, 8, 9, 8, 6, 8, 2, 3, 5, 4, 3, 3, 7, 1, 5, 3, 3, 3, 1, 8, 8, 5, 2, 9, 4, 3, 4, 7, 7, 5, 3, 8, 4, 5, 8, 3, 9, 1, 0, 9, 2, 9, 3, 2, 5, 7, 3, 7, 5, 4, 4, 9, 9, 6, 7, 9, 1, 3, 2, 5, 4, 6, 1, 6, 1, 6, 3, 3, 5, 3, 0, 8, 4,
9, 1, 2, 5, 8, 2, 6, 7, 2, 4, 8, 9, 3, 9, 8, 6, 3, 4, 6, 8, 9, 0, 2, 8, 4, 8, 5, 6, 0, 0, 5, 6, 6, 1, 5, 0, 3, 4, 5, 0, 0, 8, 7, 4, 5, 8, 5, 6, 8, 4, 6, 6, 1, 7, 4, 8, 7, 4, 8, 2, 8, 5, 5, 9, 1, 7, 0, 5, 8, 5, 2, 8, 3, 9, 0, 5, 4, 4, 1, 8, 9, 6, 1, 6, 7, 8, 9, 7, 4, 7, 0, 2, 0, 5, 3, 9, 6, 0, 1, 0, 4, 2, 9, 7, 3, 8, 4, 8, 4, 9, 2, 5, 1, 9, 9, 1, 4, 9, 0, 9, 4, 7, 6, 1, 3, 6, 9, 4, 3, 6, 0, 4, 3, 2, 8, 3, 4, 8, 5, 1, 4, 7, 2, 0, 8, 6, 3, 5,
7, 4, 8, 9, 6, 2, 1, 2, 5, 4, 2, 4, 9, 6, 8, 5, 7, 9, 5, 7, 6, 3, 3, 3, 8, 8, 8, 2, 1, 3, 5, 9, 3, 9, 1, 4, 4, 4, 9, 0, 1, 0, 0, 9, 6, 4, 3, 4, 5, 3, 9, 9, 5, 6, 6, 2, 1, 1, 7, 7, 1, 9, 6, 2, 8, 3, 7, 8, 8, 2, 5, 3, 1, 0, 9, 4, 3, 2, 0, 1, 7, 4, 9, 4, 7, 0, 0, 1, 9, 8, 4, 0, 8, 4, 6, 8, 2, 9, 1, 1]

# Definizione delle soglie
soglia_bassa = 3
soglia_alta = 7

# Inizializzazione delle variabili
valori_bassi = 0
valori_bassi_seguiti_da_alti = 0

# Iteriamo per trovare le coppie dove un valore basso è seguito da un valore alto
for i in range(len(numeri) - 1):
    if numeri[i] <= soglia_bassa:  # Valore basso
        valori_bassi += 1
        if numeri[i + 1] >= soglia_alta:  # Valore alto dopo
            valori_bassi_seguiti_da_alti += 1

# Calcoliamo la probabilità condizionale
probabilita_condizionale = valori_bassi_seguiti_da_alti / valori_bassi if valori_bassi > 0 else 0

# Calcoliamo anche la probabilità complessiva di estrarre un numero alto (≥7) nella sequenza
valori_alti = sum(1 for num in numeri if num >= soglia_alta)
probabilita_complessiva_alto = valori_alti / len(numeri)

# Stampa dei risultati
print("Valori bassi:", valori_bassi)
print("Valori bassi seguiti da valori alti:", valori_bassi_seguiti_da_alti)
print(f"Probabilità condizionale: {probabilita_condizionale:.3f}%")
print(f"Probabilità complessiva di estrarre un numero alto: {probabilita_complessiva_alto:.3f}%")