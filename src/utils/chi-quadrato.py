import pandas as pd
import numpy as np
from scipy.stats import chisquare

# Frequenze osservate (ottenute precedentemente)
frequenze_osservate = [94, 82, 76, 18, 0, 0, 0, 0]

# Definizione delle frequenze attese
# Supponiamo una distribuzione uniforme
num_fasce = len(frequenze_osservate)
frequenze_attese = [sum(frequenze_osservate) / num_fasce] * num_fasce

# Esegui il test del chi-quadrato
chi2_stat, p_value = chisquare(frequenze_osservate, frequenze_attese)

# Stampa i risultati
print(f"Statistiche del Chi-quadrato: {chi2_stat}")
print(f"P-value: {p_value}")

# Interpreta il risultato
alpha = 0.05
if p_value < alpha:
    print("Rifiutiamo l'ipotesi nulla: ci sono differenze significative nelle frequenze.")
else:
    print("Non possiamo rifiutare l'ipotesi nulla: non ci sono differenze significative nelle frequenze.")
