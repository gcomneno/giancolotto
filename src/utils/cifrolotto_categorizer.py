import os
import subprocess
import re

# Funzione per eseguire uno script sh principale e catturarne l'output
def run_get_all_script(script_path):
    """
    Esegue lo script 'get_all.sh' nella directory 'scripts' e restituisce l'output.
    """
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

def categorize_numbers(extraction, cifrolotto):
    """
    Categorizza i numeri dell'estrazione in base alla classifica CIFROLOTTO.
    
    Args:
    extraction (dict): Dizionario con chiavi 'ruota' e 'numeri' per l'estrazione.
    cifrolotto (dict): Dizionario con classifica cifre lotto.

    Returns:
    dict: Dizionario contenente la ruota, i numeri estratti e le loro categorie con conteggio.

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
    # MD  => MIDDLEFIELD Numerico (Posizione 5 e 6)
    """
    if extraction is None:
        return None  # Gestisci il caso di estrazione non valida

    ruota = extraction['ruota']
    numeri = extraction['numeri']
    category_counts = {}

    for numero in numeri:
        cifre = [int(c) for c in str(numero)]
        if len(cifre) < 2:
            continue  # Salta numeri con meno di due cifre

        # Posizioni delle cifre nella classifica CIFROLOTTO
        pos1, pos2 = cifrolotto.get(str(cifre[0]), -1), cifrolotto.get(str(cifre[1]), -1)

        # Definisci le categorie
        categories = []
        if pos1 in range(1, 6) and pos2 in range(1, 6):
            categories.extend(["TSS" if pos1 < pos2 else "TSG", "TCS" if pos1 < pos2 else "TCG"])
        elif pos1 in range(6, 11) and pos2 in range(6, 11):
            categories.extend(["BSS" if pos1 < pos2 else "BSG", "BCS" if pos1 < pos2 else "BCG"])
        if pos1 == pos2:
            categories.append("GT" if pos1 <= 5 else "GB")
        if pos1 == 1 and pos2 == 10:
            categories.append("TD")
        if pos1 == 10 and pos2 == 1:
            categories.append("DT")
        if (pos1 == 1 and pos2 == 2) or (pos1 == 10 and pos2 == 9):
            categories.append("T2")

        # Conta le categorie
        for category in categories:
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

    # Formatta le categorie con il loro conteggio
    formatted_categories = [f"{count}|{category}" for category, count in category_counts.items()]

    return {"ruota": ruota, "numeri": numeri, "categorie": formatted_categories}

def save_to_dataset(data, filename="./dataset/cifrolotto.data"):
    """
    Salva i dati categorizzati nel dataset. Accetta un singolo dizionario per i dati.
    
    Args:
    data (dict): Dizionario contenente i dati da salvare.
    filename (str): Nome del file in cui salvare i dati.
    """
    wheel_map = {
        "Bari": "BA", "Cagliari": "CA", "Firenze": "FI", "Genova": "GE",
        "Milano": "MI", "Napoli": "NA", "Palermo": "PA", "Roma": "RM",
        "Torino": "TO", "Venezia": "VE"
    }

    try:
        with open(filename, 'a') as file:
            if data:  # Verifica che data non sia None
                wheel_abbreviation = wheel_map[data['ruota']]
                line = f"{wheel_abbreviation}\t{data['categorie']}\n"
                file.write(line)
    except Exception as e:
        print(f"Errore durante il salvataggio: {e}")

def parse_singleroute_extraction(output, start_index):
    """
    Estrae i numeri delle estrazioni dalla ruota specificata, utilizzando espressioni regolari.
    """
    # Trova la fine della prima riga di dati dopo l'intestazione
    end_index = output.find('\n', start_index)
    if end_index == -1:
        end_index = len(output)  # Se non c'è un a capo, prendi tutto fino alla fine della stringa

    # Estrai il blocco di testo per questa ruota, che corrisponde alla prima riga di dati
    block = output[start_index:end_index]

    # Trova il nome della ruota utilizzando una regex che cattura parole alfanumeriche
    ruota_name = re.search(r"\b[A-Za-z]+\b", block).group(0)

    # Utilizza un'espressione regolare per trovare tutti i numeri nella riga
    pattern = re.escape(ruota_name) + r"\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})"
    matches = re.findall(pattern, block)

    # Converti i risultati in un dizionario
    if matches:
        numeri = list(map(int, matches[0]))  # Assumi che ci sia solo una riga di numeri
        return {'ruota': ruota_name, 'numeri': numeri}
    else:
        return None  # Nessuna estrazione valida trovata

def parse_singleroute_cifrolotto(output, start_index):
    """
    Estrae la classifica CIFROLOTTO per una specifica ruota utilizzando regex per gestire spazi multipli o tabulazioni.

    Args:
    output (str): Output completo dello script.
    start_index (int): Indice di inizio delle estrazioni per la ruota specifica.

    Returns:
    dict: Dizionario con la cifra come chiave e il suo ranking come valore.
    """
    # Pattern regex che identifica la sezione iniziale di CIFROLOTTO
    cifrolotto_start_regex = re.compile(r"Cifra\s+Pres\.", re.IGNORECASE)
    cifrolotto_end_regex = re.compile(r"={5,}")

    # Trova l'inizio e la fine del blocco CIFROLOTTO utilizzando regex
    start_match = cifrolotto_start_regex.search(output, start_index)
    if not start_match:
        print("Start of CIFROLOTTO block not found.")
        return {}
    
    end_match = cifrolotto_end_regex.search(output, start_match.end())
    if not end_match:
        print("End of CIFROLOTTO block not found.")
        return {}
    
    # Estrai il blocco CIFROLOTTO
    cifrolotto_data = output[start_match.end():end_match.start()]
    cifrolotto = {}
    for line in cifrolotto_data.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            cifra, pres = parts[0], int(parts[1])
            cifrolotto[cifra] = pres

    return cifrolotto

def main():
    script_path = os.path.join(os.path.dirname(__file__), "../../scripts/get_all.sh")
    script_path = os.path.abspath(script_path)

    ruote = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

    print(f"Esecuzione dello script principale {script_path}, in corso...")
    output = run_get_all_script(script_path)
    print("Output del script recuperato. Categorizzazione per ruota, in corso...")

    for ruota_name in ruote:
        start_index = output.find(ruota_name)
        if start_index == -1:
            print(f"Ruota {ruota_name} non trovata nell'output.")
            continue

        extraction = parse_singleroute_extraction(output, start_index)
        cifrolotto = parse_singleroute_cifrolotto(output, start_index)

        print(f"Estrazione per {ruota_name}: {extraction}")
        print(f"Classifica CIFROLOTTO per {ruota_name}: {cifrolotto}")

        if extraction:
            categorized_data = categorize_numbers(extraction, cifrolotto)
            save_to_dataset(categorized_data)
            print(f"Dati salvati per {ruota_name}.")

if __name__ == "__main__":
    main()
