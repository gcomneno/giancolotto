import re
import argparse
from collections import Counter
import os

# Determina il percorso assoluto del file di dataset rispetto alla directory dello script
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../../dataset/cifrolotto.data")

# Legenda delle categorie:
# TSG => Formazioni Area TOP Semplici a Scendere Giù  
# BSG => Formazioni Area BOTTOM Semplici a Scendere Giù  
# TCG => Formazioni Area TOP Concatenate a Scendere Giù 
# BCG => Formazioni Area BOTTOM Concatenate a Scendere Giù 
# TSS => Formazioni Area TOP Semplici a Salire Sù 
# BSS => Formazioni Area BOTTOM Semplici a Salire Sù 
# TCS => Formazioni Area TOP Concatenate a Salire Sù
# BCS => Formazioni Area BOTTOM Concatenate a Salire Sù 
# GT  => Gemello sulla cifra TOP
# GB  => Gemello sulla cifra BOTTOM
# TD  => TOPDOWN!
# T2  => TOPDOWN Numerico (2 cifre)

def category_count(dataset, exclude_parentheses=False):
    """
    Conta le categorie presenti nel dataset con la possibilità di 
    escludere quelle racchiuse tra parentesi tonde ('equivalenze').

    Parametri:
    ----------
    dataset : str
        Stringa che rappresenta il dataset da analizzare.
    exclude_parentheses : bool
        Se True, esclude le categorie tra parentesi tonde dal conteggio.
    """
    # Rimuove i prefissi delle ruote (es. "BA:", "CA:")
    cleaned_text = re.sub(r'^[A-Z]{2}:\s*', '', dataset, flags=re.MULTILINE)

    # Se richiesto, rimuove le categorie tra parentesi tonde
    if exclude_parentheses:
        cleaned_text = re.sub(r'\([^)]+\)', '', cleaned_text)

    # Trova categorie e moltiplicatori
    categories = re.findall(r'(\d*)([A-Z]+)', cleaned_text)
    category_counter = Counter()

    # Conta le categorie
    for multiplier, category in categories:
        multiplier = int(multiplier) if multiplier else 1
        category_counter[category] += multiplier

    # Categorie con lunghezza maggiore di 2 (classificabili come Semplici/Concatenate e Direzione Movimento)
    semplici = {k: v for k, v in category_counter.items() if len(k) > 2 and k[1] == 'S'}
    concatenate = {k: v for k, v in category_counter.items() if len(k) > 2 and k[1] == 'C'}
    salire = {k: v for k, v in category_counter.items() if len(k) > 2 and k[2] == 'S'}
    scendere = {k: v for k, v in category_counter.items() if len(k) > 2 and k[2] == 'G'}

    # Categorie di lunghezza 2 (altre categorie)
    altre = {k: v for k, v in category_counter.items() if len(k) == 2}

    # Stampa dei risultati per ogni gruppo
    print("\nSuddivisione per Semplici:")
    totale_semplici = 0
    for categoria, conteggio in semplici.items():
        print(f"{categoria}: {conteggio}")
        totale_semplici += conteggio
    print(f"Totale Semplici: {totale_semplici}")

    print("\nSuddivisione per Concatenate:")
    totale_concatenate = 0
    for categoria, conteggio in concatenate.items():
        print(f"{categoria}: {conteggio}")
        totale_concatenate += conteggio
    print(f"Totale Concatenate: {totale_concatenate}")

    print("\nMovimento a Salire:")
    totale_sali = 0
    for categoria, conteggio in salire.items():
        print(f"{categoria}: {conteggio}")
        totale_sali += conteggio
    print(f"Totale Salire: {totale_sali}")

    print("\nMovimento a Scendere:")
    totale_scendi = 0
    for categoria, conteggio in scendere.items():
        print(f"{categoria}: {conteggio}")
        totale_scendi += conteggio
    print(f"Totale Scendere: {totale_scendi}")

    print("\nAltre Categorie:")
    totale_altre = 0
    for categoria, conteggio in altre.items():
        print(f"{categoria}: {conteggio}")
        totale_altre += conteggio
    print(f"Totale Altre: {totale_altre}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Conta le categorie nel dataset e fornisce una suddivisione dettagliata.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-e", "--exclude",
        action="store_true",
        help="Escludi le categorie tra parentesi tonde dal conteggio"
    )
    args = parser.parse_args()

    try:
        # Legge il dataset dal file cifrolotto.data
        with open(dataset_path, "r", encoding="utf-8") as file:
            dataset = file.read()

        # Esegue la funzione principale
        category_count(dataset, exclude_parentheses=args.exclude)

    except FileNotFoundError:
        print("Errore: il file 'cifrolotto.data' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
