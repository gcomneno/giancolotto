import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import argparse

def load_data(file_path, offset=0, limit=None):
    """Carica i dati dal file, applicando offset e limit."""
    data = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # Validazione dei parametri rispetto al numero di righe disponibili
            if offset < 0:
                offset = max(0, len(lines) + offset)  # Offset negativo dal fondo
            if offset >= len(lines):
                raise ValueError(f"Offset troppo alto: il file contiene solo {len(lines)} righe.")
            if limit is not None and limit <= 0:
                raise ValueError("Il parametro 'limit' deve essere maggiore di zero.")

            # Applica l'offset e il limit
            lines = lines[offset:]
            if limit is not None:
                lines = lines[:limit]

            for line in lines:
                try:
                    # Converti la riga in una lista di numeri interi
                    numbers = list(map(int, line.strip().split(',')))
                    data.append(numbers)
                except ValueError:
                    print(f"Riga non valida trovata nel file: {line.strip()}")
        if not data:
            raise ValueError("Il file non contiene dati validi dopo l'applicazione di offset e limit.")
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non esiste.")
        raise
    except Exception as e:
        print(f"Errore durante il caricamento del file: {e}")
        raise
    return data

def count_occurrences(data):
    """Conta le occorrenze di ogni numero."""
    return Counter(number for row in data for number in row)

def count_decades(data, decade_ranges):
    """Conta le presenze per fasce di decine."""
    decade_counts = Counter()
    for row in data:
        for number in row:
            for low, high in decade_ranges:
                if low <= number <= high:
                    decade_counts[f"{low:02}-{high:02}"] += 1
                    break
    return decade_counts

def display_text(sorted_presence, df_decades):
    """Mostra i dati calcolati in modalità testuale."""
    print("\nPresenze dei Numeri:")
    for number, count in sorted_presence:
        print(f"Numero {number:02}: {count} presenze")

    print("\nFrequenza per Fascia di Decine:")
    df_decades["Percentuale"] = df_decades["Percentuale"].apply(lambda x: f"{x:.2f}%")
    print(df_decades.to_string(index=False))

def plot_data(sorted_presence, df_decades):
    """Crea e visualizza i grafici."""
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Primo grafico: Presenze dei numeri
    axs[0].bar([str(number) for number, _ in sorted_presence],
               [count for _, count in sorted_presence], color='salmon')
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

    plt.tight_layout()

    # Imposta la finestra in full-screen
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Per Windows
    except AttributeError:
        try:
            mng.full_screen_toggle()  # Per altri sistemi
        except AttributeError:
            pass

    plt.show()

def parse_arguments():
    """Analizza gli argomenti della riga di comando."""
    parser = argparse.ArgumentParser(
        description="Calcola le presenze per valori uguali di un dataset.",
        epilog="Usage examples:\n"
               "  python frequenze.py --mode text\n"
               "  python frequenze.py --offset -10 --limit 20 --mode graphic",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--offset", type=int, default=0, 
                        help="Numero di estrazioni da cui partire (offset). Può essere negativo. Default: 0")
    parser.add_argument("--limit", type=int, default=None, 
                        help="Numero di estrazioni da elaborare (limit). Deve essere maggiore di zero. Default: tutte le righe.")
    parser.add_argument("--mode", type=str, choices=["text", "graphic"], default="text", 
                        help="Modalità di output: 'text' (testo) o 'graphic' (grafici). Default: text.")
    return parser.parse_args()

def main():
    # Parametri di configurazione
    file_path = '../dataset/database.2025.md'
    decade_ranges = [(i, i + 9) for i in range(0, 80, 10)]

    # Analizza gli argomenti della riga di comando
    args = parse_arguments()
    offset = args.offset
    limit = args.limit
    mode = args.mode

    try:
        # Carica i dati
        data = load_data(file_path, offset=offset, limit=limit)

        # Conta le presenze
        presence_count = Counter(number for row in data for number in row)

        # Ordina per presenze decrescenti
        sorted_presence = sorted(presence_count.items(), key=lambda x: x[1], reverse=True)

        # Conta le fasce di decine
        decade_counts = Counter()
        for row in data:
            for number in row:
                for low, high in decade_ranges:
                    if low <= number <= high:
                        decade_counts[f"{low:02}-{high:02}"] += 1
                        break

        # Crea un DataFrame per le fasce di decine
        df_decades = pd.DataFrame(list(decade_counts.items()), columns=["Fascia di Decine", "Frequenza"])
        df_decades.sort_values(by="Frequenza", ascending=False, inplace=True)

        # Calcola la percentuale delle frequenze
        total_count = df_decades["Frequenza"].sum()
        df_decades["Percentuale"] = (df_decades["Frequenza"] / total_count) * 100

        # Modalità di output
        if mode == "text":
            display_text(sorted_presence, df_decades)
        elif mode == "graphic":
            plot_data(sorted_presence, df_decades)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
