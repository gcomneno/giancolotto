import re
import argparse
from collections import Counter
import os

# Determina il percorso assoluto del file di dataset rispetto alla directory dello script
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../../dataset/cifrolotto.data")

# Categorie conosciute
KNOWN_CATEGORIES = {
    "TSG", "TCG", "TSS", "TCS", "BSG", "BCG", "BSS", "BCS",
    "GT", "GB", "TD", "DT", "TPA", "ATP", "BMA", "ABM", "MD"
}

def category_count(dataset):
    """
    Conta le categorie presenti nel dataset con la possibilità di 
    escludere quelle racchiuse tra parentesi tonde ('equivalenze').

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
    semplici = {k: v for k, v in category_counter.items() if k.startswith("TS") or k.startswith("BS")}
    concatenate = {k: v for k, v in category_counter.items() if k.startswith("TC") or k.startswith("BC")}
    salire = {k: v for k, v in category_counter.items() if "S" in k[2:]}
    scendere = {k: v for k, v in category_counter.items() if "G" in k[2:]}
    altre = {k: v for k, v in category_counter.items() if k in ['GT', 'GB', 'MD', 'TD', 'DT', 'TPA', 'BMA', 'ATP', 'ABM']}
    
    # Stampa dei risultati per ogni gruppo
    print("\nSuddivisione per Semplici:")
    totale_semplici = sum(semplici.values())
    for categoria, conteggio in semplici.items():
        print(f"{categoria}: {conteggio}")
    print(f"Totale Semplici: {totale_semplici}")

    print("\nSuddivisione per Concatenate:")
    totale_concatenate = sum(concatenate.values())
    for categoria, conteggio in concatenate.items():
        print(f"{categoria}: {conteggio}")
    print(f"Totale Concatenate: {totale_concatenate}")

    print("\nMovimento a Salire:")
    totale_sali = sum(salire.values())
    for categoria, conteggio in salire.items():
        print(f"{categoria}: {conteggio}")
    print(f"Totale Salire: {totale_sali}")

    print("\nMovimento a Scendere:")
    totale_scendi = sum(scendere.values())
    for categoria, conteggio in scendere.items():
        print(f"{categoria}: {conteggio}")
    print(f"Totale Scendere: {totale_scendi}")

    print("\nAltre Categorie:")
    totale_altre = sum(altre.values())
    for categoria, conteggio in altre.items():
        print(f"{categoria}: {conteggio}")
    print(f"Totale Altre: {totale_altre}")

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
