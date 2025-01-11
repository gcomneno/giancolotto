import os
import subprocess

# Funzione per eseguire ./get_all.sh e catturare l'output
def run_get_all_script():
    """
    Esegue lo script 'get_all.sh' nella directory 'scripts' e restituisce l'output.
    """
    script_path = os.path.join(os.path.dirname(__file__), "../../scripts/get_all.sh")
    script_path = os.path.abspath(script_path)

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Lo script {script_path} non esiste.")

    # Usa 'bash' per eseguire lo script su Windows
    try:
        result = subprocess.run(
            ["bash", script_path],
            check=True,
            text=True,
            capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione dello script {script_path}:")
        print("Uscita standard:", e.stdout)
        print("Errore standard:", e.stderr)
        raise

# Funzione per categorizzare i numeri
def categorize_numbers(extractions, cifrolotto):
    """
    Categorizza i numeri delle estrazioni in base alla classifica CIFROLOTTO.
    """
    categorized_data = []

    for extraction in extractions:
        ruota = extraction['ruota']
        numeri = extraction['numeri']
        categories = []

        for numero in numeri:
            cifre = [int(c) for c in str(numero)]
            if len(cifre) < 2:
                continue

            # Posizioni delle cifre nella classifica CIFROLOTTO
            pos1, pos2 = cifrolotto.get(str(cifre[0]), -1), cifrolotto.get(str(cifre[1]), -1)

            # TOP/BOTTOM
            if pos1 in range(1, 6) and pos2 in range(1, 6):
                # Semplici a Salire/Scendere
                if pos1 < pos2:
                    categories.append("TSS")
                elif pos1 > pos2:
                    categories.append("TSG")

                # Concatenate a Salire/Scendere
                categories.append("TCS" if pos1 < pos2 else "TCG")

            elif pos1 in range(6, 11) and pos2 in range(6, 11):
                # Semplici a Salire/Scendere
                if pos1 < pos2:
                    categories.append("BSS")
                elif pos1 > pos2:
                    categories.append("BSG")

                # Concatenate a Salire/Scendere
                categories.append("BCS" if pos1 < pos2 else "BCG")

            # Gemelli (GT e GB)
            if pos1 == pos2:
                categories.append("GT" if pos1 <= 5 else "GB")

            # TOPDOWN (TD)
            if pos1 == 1 and pos2 == 10:
                categories.append("TD")

            # DT (TOPDOWN inverso)
            if pos1 == 10 and pos2 == 1:
                categories.append("DT")

            # T2 (Accoppiamenti Specifici)
            if pos1 == 1 and pos2 == 2:
                categories.append("T2")
            elif pos1 == 10 and pos2 == 9:
                categories.append("T2")

        categorized_data.append({"ruota": ruota, "numeri": numeri, "categorie": categories})

    return categorized_data

# Funzione per salvare nel file cifrolotto.data
def save_to_dataset(data, filename="cifrolotto.data"):
    """
    Salva i dati categorizzati nel dataset.
    """
    try:
        with open(filename, 'a') as file:
            for entry in data:
                line = f"{entry['ruota']} | {entry['numeri']} | {entry['categorie']}\n"
                file.write(line)
        print(f"Dati salvati correttamente in {filename}.")
    except Exception as e:
        print(f"Errore durante il salvataggio: {e}")

# Main Script
def main():
    # Esegui ./get_all.sh e ottieni le estrazioni
    extractions = run_get_all_script()
    
    if extractions:
        # Classifica CIFROLOTTO (ipotizziamo che venga generata da ./get_all.sh)
        cifrolotto = {
            "0": 1, "1": 2, "2": 3, "3": 4, "4": 5,
            "5": 6, "6": 7, "7": 8, "8": 9, "9": 10
        }

        # Categorizza i numeri
        categorized_data = categorize_numbers(extractions, cifrolotto)

        # Salva il risultato nel dataset
        save_to_dataset(categorized_data)

if __name__ == "__main__":
    main()
