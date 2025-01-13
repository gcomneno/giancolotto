import os
import requests
import re
import configparser
import pymongo

from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from collections import Counter

class LottoExtractor:
    def __init__(self, config_file='config.ini'):
        """
        Inizializza l'istanza della classe LottoExtractor, caricando il file di configurazione,
        i numeri e cifre evidenziate, e i dati delle estrazioni.

        Parametri:
        -----------
        config_file : str
            Percorso del file di configurazione (default: 'config.ini').
        """

        # Inizializza Colorama per la gestione dei colori nella stampa
        init()

        # Determina i percorsi rilevanti
        self.project_root = self.get_project_root()
        self.config_path = os.path.join(self.project_root, config_file)

        # Legge il file di configurazione
        self.config = self.read_config(self.config_path)

        # Imposta l'URL di scraping
        self.url = self.config.get('Scraping', 'url')

        # Carica i numeri e le cifre evidenziate
        self.numeri_evidenziati = self.get_highlighted_numbers()
        self.cifre_evidenziate = self.get_highlighted_digits()

        # Recupera e analizza i dati di scraping
        self.response = self.fetch_data()
        self.extractions = self.parse_data()

    def get_project_root(self):
        """
        Determina la root del progetto in base al percorso dello script corrente.

        Ritorna:
        --------
        str : Percorso assoluto della root del progetto.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(script_dir, '..'))

    def read_config(self, config_file_path):
        """
        Reads the configuration file.

        Parameters:
        -----------
        config_file_path : str
            Path to the configuration file.

        Returns:
        --------
        configparser.ConfigParser : The configuration object.
        """
        config = configparser.ConfigParser()
        config.read(config_file_path)
        return config

    def get_persistence_options(self):
        """
        Retrieves persistence configuration options from the configuration file.

        Returns:
        --------
        tuple : A tuple containing the host, port, and database name.
        """
        host = self.config.get('Persistence', 'host')
        port = self.config.getint('Persistence', 'porta')
        database_name = self.config.get('Persistence', 'database')
        return host, port, database_name

    def get_mongodb_connection(self):
        """
        Establishes a MongoDB connection based on the configuration file.

        Returns:
        --------
        tuple : A tuple containing the MongoDB client and the selected database.
        """
        host, port, database_name = self.get_persistence_options()
        client = pymongo.MongoClient(host, port)
        return client, client[database_name]

    def get_specific_wheel(self):
        """
        Retrieves the specific wheel name from the configuration file.

        Returns:
        --------
        str : The name of the specific wheel or 'All' if none is specified.
        """
        specific_wheel = self.config['Scraping']['ruota']
        return specific_wheel if specific_wheel else 'All'

    def get_highlighted_numbers(self):
        """
        Retrieves the highlighted numbers from the configuration file.

        Returns:
        --------
        set : A set of highlighted numbers.
        """
        try:
            numbers_str = self.config['Filtering']['numeri']
            numbers = {int(number) for number in numbers_str.split(',')}
            return numbers
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return set()

    def get_highlighted_digits(self):
        """
        Retrieves the highlighted digits from the configuration file.

        Returns:
        --------
        set : A set of highlighted digits.
        """
        try:
            digits_str = self.config['Filtering']['cifre']
            digits = {int(digit) for digit in digits_str.split(',')}
            return digits
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return set()

    def fetch_data(self):
        """
        Fetches the HTML content from the configured URL.

        Returns:
        --------
        requests.Response : The HTTP response object containing the HTML content.

        Raises:
        -------
        Exception : If the page cannot be retrieved successfully.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Impossibile recuperare la pagina. Errore: {e}")

    def parse_data(self):
        """
        Parses the HTML content and extracts the relevant table(s) containing lottery data.

        Returns:
        --------
        list : A list of BeautifulSoup objects representing the extracted tables.

        Raises:
        -------
        ValueError : If no valid extraction tables are found.
        """
        soup = BeautifulSoup(self.response.text, 'html.parser')

        # Retrieve all tables matching the class name
        extractions = soup.find_all('table', class_='tabellaEstrazioni-arch')

        # Fall-back logic for alternative URL structure
        if not extractions and 'ultime-estrazioni-lotto' in self.url:
            extractions = soup.find_all('article')

        if not extractions:
            raise ValueError("Nessuna estrazione trovata!")

        return extractions

    def extraction(self, target_id=None):
        """
        Recupera i dati dell'estrazione con l'ID ufficiale target_id.
        
        Parametri:
        -----------
        target_id : int
            L'ID ufficiale dell'estrazione che si desidera recuperare.
        
        Ritorna:
        --------
        main_references : list of int
            Lista dei primi 9 interi trovati nel testo del blocco (per retrocompatibilità).
        nomi_ruote : list of str
            Lista dei nomi delle ruote per questa estrazione.
        numeri_per_ruota : dict
            Dizionario associando ad ogni ruota i 5 numeri estratti.
            Se l'ID non è valido o non si trova, restituisce (None, None, None).
        """
        # Verifica che target_id sia un numero intero positivo
        if not isinstance(target_id, int) or target_id <= 0:
            print(f"[Errore] ID estrazione non valido: {target_id}")
            return None, None, None

        # Cerca il blocco corrispondente
        matching_block = None
        for block in self.extractions:
            id_tag = block.find("td", class_="estr-n-arch")
            if id_tag:
                text_id = id_tag.get_text(strip=True)
                match_id = re.search(r'\d+', text_id)
                if match_id and int(match_id.group()) == target_id:
                    matching_block = block
                    break

        # Se non viene trovato alcun blocco corrispondente, restituisce valori di errore
        if not matching_block:
            print(f"[Errore] Estrazione con ID {target_id} non trovata.")
            return None, None, None

        # Recupera tutti i numeri dal testo del blocco
        all_numbers = re.findall(r'\d+', matching_block.text)

        # I primi 9 numeri sono considerati riferimenti principali
        main_references = [int(x) for x in all_numbers[:9]]

        # I rimanenti corrispondono ai numeri estratti per le varie ruote
        all_numbers = all_numbers[9:]

        # Trova tutti gli elementi <td> che indicano i nomi delle ruote
        ruote_elements = matching_block.find_all('td', class_='nomeRuota-arch estratto-arch')
        nomi_ruote = [ruota.text.strip() for ruota in ruote_elements]

        # Controllo di validità: ci devono essere abbastanza numeri per ogni ruota
        if len(all_numbers) < len(nomi_ruote) * 5:
            print(f"[Errore] Numero insufficiente di estratti per le ruote.")
            return None, None, None

        # Associa a ciascuna ruota i 5 numeri corrispondenti
        numeri_per_ruota = {
            ruota: [int(n) for n in all_numbers[i*5:(i+1)*5]]
            for i, ruota in enumerate(nomi_ruote)
        }

        return main_references, nomi_ruote, numeri_per_ruota

    def get_last_extraction(self):
        """
        Recupera i dati relativi all'ultima estrazione disponibile (la più recente).
        
        Ritorna:
        --------
        main_references : list of int
            Lista dei primi 9 interi trovati nel testo del blocco (per retrocompatibilità).
        nomi_ruote : list of str
            Lista dei nomi delle ruote per questa estrazione.
        numeri_per_ruota : dict
            Dizionario associando ad ogni ruota i 5 numeri estratti.
            Se non ci sono estrazioni disponibili, restituisce (None, None, None).
        """
        # Controlla se ci sono estrazioni disponibili
        if not self.extractions or len(self.extractions) == 0:
            print("[Errore] Nessuna estrazione disponibile.")
            return None, None, None

        # Recupera il primo blocco (ultima estrazione)
        latest_block = self.extractions[0]

        # Recupera tutti i numeri dal testo del blocco
        all_numbers = re.findall(r'\d+', latest_block.text)

        # I primi 9 numeri sono considerati riferimenti principali
        main_references = [int(x) for x in all_numbers[:9]]

        # I rimanenti corrispondono ai numeri estratti per le varie ruote
        all_numbers = all_numbers[9:]

        # Trova tutti gli elementi <td> che indicano i nomi delle ruote
        ruote_elements = latest_block.find_all('td', class_='nomeRuota-arch estratto-arch')
        nomi_ruote = [ruota.text.strip() for ruota in ruote_elements]

        # Controllo di validità: ci devono essere abbastanza numeri per ogni ruota
        if len(all_numbers) < len(nomi_ruote) * 5:
            print(f"[Errore] Numero insufficiente di estratti per le ruote.")
            return None, None, None

        # Associa a ciascuna ruota i 5 numeri corrispondenti
        numeri_per_ruota = {
            ruota: [int(n) for n in all_numbers[i*5:(i+1)*5]]
            for i, ruota in enumerate(nomi_ruote)
        }

        return main_references, nomi_ruote, numeri_per_ruota

    def _print_header(self, num_columns, is_cifre):
        """
        Stampa l'intestazione della tabella dei risultati.

        Parametri:
        -----------
        num_columns : int
            Numero di colonne per i numeri/cifre per ruota.
        is_cifre : bool
            Indica se il risultato riguarda le cifre (True) o i numeri (False).
        """

        print("=" * 80)
        headers = "\t".join([f"{i}o" for i in range(1, num_columns + 1)])
        print(f"Estrazione\t\tRUOTA\t\t{headers}")
        print("=" * 80)

    def print_results_numbers(self, refs, ruote, numeri_ruote, show_header, extraction_index):
        """
        Stampa i risultati per i numeri estratti.

        Parametri:
        -----------
        refs : list
            Informazioni sull'estrazione (ID, data, ecc.).
        ruote : list
            Nomi delle ruote.
        numeri_ruote : dict
            Numeri estratti per ogni ruota.
        show_header : bool
            Indica se stampare l'intestazione.
        extraction_index : int
            Indice cardinale dell'estrazione (0 = ultima estrazione).
        """
        specific_wheel = self.config['Scraping'].get('ruota', '')

        if show_header:
            self._print_header(len(numeri_ruote[ruote[0]]), is_cifre=False)

        for ruota, numeri in numeri_ruote.items():
            if not specific_wheel or ruota == specific_wheel:
                print(f"n. {refs[0]:03d} del {refs[3]:04d}/{refs[2]:02d}/{refs[1]:02d}\t{ruota.ljust(9)}\t", end="")
                red_count = 0

                for numero in numeri:
                    if numero in self.numeri_evidenziati:
                        print(Fore.RED + f"{numero:02d}", end="\t")
                        red_count += 1
                    else:
                        print(Fore.WHITE + f"{numero:02d}", end="\t")

                print(Style.RESET_ALL + f"\t<{red_count}>\t[{extraction_index if extraction_index > 0 else 'U'}]")

    def print_results_digits(self, refs, ruote, numeri_ruote, show_header, extraction_index):
        """
        Stampa i risultati per le cifre dei numeri estratti.

        Parametri:
        -----------
        refs : list
            Informazioni sull'estrazione (ID, data, ecc.).
        ruote : list
            Nomi delle ruote.
        numeri_ruote : dict
            Numeri estratti per ogni ruota.
        show_header : bool
            Indica se stampare l'intestazione.
        extraction_index : int
            Indice cardinale dell'estrazione (0 = ultima estrazione).
        """
        specific_wheel = self.config['Scraping'].get('ruota', '')

        if show_header:
            self._print_header(len(numeri_ruote[ruote[0]]), is_cifre=True)

        for ruota, numeri in numeri_ruote.items():
            if not specific_wheel or ruota == specific_wheel:
                print(f"n. {refs[0]:03d} del {refs[3]:04d}/{refs[2]:02d}/{refs[1]:02d}\t{ruota.ljust(9)}\t", end="")
                red_count = 0
                consecutive_reds = 0

                for numero in numeri:
                    digits = [0, numero] if numero < 10 else [int(c) for c in str(numero)]
                    was_previous_red = False

                    for digit in digits:
                        if digit in self.cifre_evidenziate:
                            print(Fore.RED + str(digit), end="")
                            red_count += 1
                            if was_previous_red:
                                consecutive_reds += 1
                            was_previous_red = True
                        else:
                            print(Fore.WHITE + str(digit), end="")
                            was_previous_red = False

                    print("\t", end="")
                
                print(Style.RESET_ALL + f"\t#{red_count} <{consecutive_reds}>\t[{extraction_index if extraction_index > 0 else 'U'}]")

    def calculate_digit_statistics(self, numbers_per_wheel):
        """
        Calcola le statistiche delle cifre presenti nei numeri estratti.

        Parametri:
        -----------
        numbers_per_wheel : dict
            Dizionario che associa a ciascuna ruota i numeri estratti.

        Ritorna:
        --------
        list of tuple
            Lista di tuple ordinate per cifra, contenente ciascuna cifra e il numero di presenze.
        """
        digit_counts = Counter()
        specific_wheel = self.config['Scraping'].get('ruota', '')

        # Conta le cifre per la ruota specifica o tutte
        for wheel, numbers in numbers_per_wheel.items():
            if not specific_wheel or wheel == specific_wheel:
                for number in numbers:
                    # Aggiorna il conteggio delle cifre (aggiungi zeri iniziali se necessario)
                    digit_counts.update(str(number).zfill(2))

        # Assicurati che tutte le cifre da 0 a 9 siano presenti (anche con conteggio 0)
        all_digits = {str(i) for i in range(10)}
        digit_counts.update({digit: 0 for digit in all_digits - digit_counts.keys()})

        # Ordina le statistiche per cifra
        sorted_statistics = sorted(digit_counts.items(), key=lambda x: x[0])
        
        return sorted_statistics

    def generate_pairings(self, digit_statistics, extraction):
        """
        Genera le associazioni basate sulle cifre dei numeri estratti.

        Parametri:
        -----------
        digit_statistics : dict
            Dizionario che mappa ogni cifra con il numero di presenze.
        extraction : dict
            Dizionario che associa a ogni ruota i numeri estratti.

        Ritorna:
        --------
        list of dict
            Lista di associazioni con la ruota specifica come chiave e coppie di valori come lista.
        """
        pairings = []
        specific_wheel = self.get_specific_wheel()

        # Estrai i numeri della ruota selezionata (o tutte)
        wheel_numbers = extraction.get(specific_wheel, [])

        # Aggiungi zeri iniziali ai numeri minori di 10
        formatted_numbers = [str(number).zfill(2) for number in wheel_numbers]

        # Genera associazioni per ciascun numero
        for number in formatted_numbers:
            number_str = str(number)
            pairings_for_number = []

            for digit in number_str:
                pairings_for_number.append(str(digit_statistics.get(digit, 0)))

                # Quando si accumulano due cifre, crea una coppia
                if len(pairings_for_number) == 2:
                    try:
                        pairings.append({specific_wheel: pairings_for_number.copy()})
                    except Exception as e:
                        print(f"Errore nell'aggiunta di associazioni: {e}")

                    # Resetta la lista dopo ogni coppia
                    pairings_for_number = []

        return pairings

    def format_pairings(self, pairings):
        """
        Formatta le associazioni in un dizionario con il nome della ruota come chiave
        e una lista di coppie come valore.

        Parametri:
        -----------
        pairings : list of dict
            Lista di associazioni con ruote come chiavi e coppie come valori.

        Ritorna:
        --------
        dict
            Dizionario formattato come {'ruota': ['xx', 'xx', ...]}.
        """
        formatted_pairings = {}
        for association in pairings:
            wheel_name = list(association.keys())[0]
            pair_list = association[wheel_name]
            formatted_pairings.setdefault(wheel_name, []).extend(pair_list)

        return formatted_pairings
