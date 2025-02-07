import re
import argparse
from collections import Counter
import os

# Determina il percorso assoluto del file di dataset rispetto alla directory dello script
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../../dataset/cifrolotto.data")

# Categorie conosciute
KNOWN_CATEGORIES = {
    "AA", "AB", "BA", "BB",
#    "GT", "GB", "TD", "DT", "MD", "DM"
}

def category_count(dataset):
    """
    Conta le categorie presenti nel dataset

    Parametri:
    ----------
    dataset : str
        Stringa che rappresenta il dataset da analizzare.
    """
    # Rimuove i prefissi delle ruote (es. "BA\t", "CA\t")
    cleaned_text = re.sub(r'^[A-Z]{2}\t', '', dataset, flags=re.MULTILINE)

    # Trova categorie e moltiplicatori
    categories = re.findall(r'(\d*)\|([A-Z]+)', cleaned_text)
    category_counter = Counter()

    # Conta le categorie
    for multiplier, category in categories:
        if category in KNOWN_CATEGORIES:
            multiplier = int(multiplier) if multiplier else 1
            category_counter[category] += multiplier

    # Suddividi le categorie in base ai criteri
    altre = {k: v for k, v in category_counter.items() if k in ['AA', 'AB', 'BA', 'BB']}

    # Ordina le categorie per conteggio decrescente
    sorted_categories = sorted(altre.items(), key=lambda x: x[1], reverse=True)

    # Stampa dei risultati
    totale_categorie = 0
    for categoria, conteggio in sorted_categories:
        print(f"[INFO] {categoria}: {conteggio}")
        totale_categorie += conteggio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Conta le categorie nel dataset e fornisce una suddivisione dettagliata.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    args = parser.parse_args()

    try:
        # Legge il dataset dal file cifrolotto.data
        with open(dataset_path, "r", encoding="utf-8") as file:
            dataset = file.read()

        # Esegue la funzione principale
        category_count(dataset)

    except FileNotFoundError:
        print("Errore: il file 'cifrolotto.data' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
