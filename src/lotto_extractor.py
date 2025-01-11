import os
import requests
from bs4 import BeautifulSoup
import re
import configparser
import pymongo
from collections import Counter
from colorama import init, Fore, Style

class LottoExtractor:
    def __init__(self, config_file='config.ini'):
        # Initialize Colorama
        init()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, '..'))

        # Percorso assoluto del file di configurazione
        config_file = os.path.join(project_root, 'config.ini')

        self.config = self.read_config(config_file)
        self.url = self.config.get('Scraping', 'url')
        
        self.numeri_evidenziati = self.get_numeri_evidenziati()
        self.cifre_evidenziate = self.get_cifre_evidenziate()

        self.response = self.fetch_data()
        self.extractions = self.parse_data()

    def read_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def ottieni_opzioni_configurazione(self):
        host = self.config.get('Persistence', 'host')
        porta = self.config.getint('Persistence', 'porta')
        database_nome = self.config.get('Persistence', 'database')
        return host, porta, database_nome

    def ottieni_connessione_mongodb(self):
        host, porta, nome_database = self.ottieni_opzioni_configurazione()        
        client = pymongo.MongoClient(host, porta)
        return client, client[nome_database]

    def ottieni_ruota_specifica(self):
        ruota_specifica = self.config['Scraping']['ruota']
        return ruota_specifica if ruota_specifica else 'Tutte'

    def get_numeri_evidenziati(self):
        try:
            numeri_str = self.config['Filtering']['numeri']
            numeri = [int(numero) for numero in numeri_str.split(',')]
            return set(numeri)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return set()

    def get_cifre_evidenziate(self):
        try:
            cifre_str = self.config['Filtering']['cifre']
            cifre = [int(cifra) for cifra in cifre_str.split(',')]
            return set(cifre)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return set()
        
    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Impossibile recuperare la pagina. Codice di stato: {response.status_code}")

    def parse_data(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        extractions = soup.find_all('table', class_='tabellaEstrazioni-arch')
        # NOTA:
        # per l'url di scraping 'https://www.estrazionedellotto.it/ultime-estrazioni-lotto' invece,
        # in lotto_extractor.py alla linea 68 il primo parametro alla find_all deve essere 'article'

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

    def print_results_numeri(self, refs, nomi_ruote, numeri_per_ruota, printHeader, estrazione_count):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or printHeader:
            print("\nEstrazione\t\tRUOTA\t\t" + "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)]))
            print("=" * 80)

        for ruota, numeri in numeri_per_ruota.items():

            if not ruota_specifica or ruota == ruota_specifica:
                print(f"n. {int(refs[0]):03d} del {int(refs[3]):04d}/{int(refs[2]):02d}/{int(refs[1]):02d}", end="\t")
                print(f"{ruota.ljust(9)}", end="\t")

                # Inizializza il contatore per i numeri evidenziati in rosso
                numeri_rossi_count = 0
            
                for numero in numeri:
                    # Verifica se il numero è tra quelli da evidenziare
                    if numero in self.numeri_evidenziati:
                        try:
                            # Evidenzia il numero con un colore rosso
                            print(Fore.RED + f"{numero:02d}", end="\t")          
                        except OSError as e:
                            print(f"{numero:02d}", end="\t")
                            pass
              
                        # Incrementa il contatore dei numeri evidenziati in rosso
                        numeri_rossi_count += 1  
                    else:
                        try:
                            print(Fore.WHITE + f"{numero:02d}", end="\t")                       
                        except OSError as e:
                            print(f"{numero:02d}", end="\t")
                            pass

                # Stampa il conteggio dei numeri evidenziati in rosso per questa riga
                print(Style.RESET_ALL + f"\t<{numeri_rossi_count}>", end="\t")

                # Stampa il numero cardinale dell'estrazione
                print(f"[{estrazione_count}]" if estrazione_count > 0 else "[U]")

    def print_results_cifre(self, refs, nomi_ruote, numeri_per_ruota, printHeader, estrazione_count):
        ruota_specifica = self.config['Scraping'].get('ruota')
        
        if not ruota_specifica or printHeader:
            headers = "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)])
            print(f"\nEstrazione\t\tRUOTA\t\t{headers}")
            print("=" * 80)
        
        consecutive_reds_count = 0
        
        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota == ruota_specifica:
                rosso_count = 0
                print(f"n. {int(refs[0]):03d} del {int(refs[3]):04d}/{int(refs[2]):02d}/{int(refs[1]):02d}\t{ruota.ljust(9)}\t", end="")
                
                for numero in numeri:
                    # Crea una lista di cifre per il numero, aggiungendo uno zero iniziale se necessario.
                    cifre = [0, numero] if numero < 10 else [int(cifra) for cifra in str(numero)]
                    
                    previous_was_red = False  # Reset for each new number
                    for i, cifra in enumerate(cifre, start=1):
                        # Evidenzia la cifra se è nella lista delle cifre evidenziate.
                        if cifra in self.cifre_evidenziate:
                            try:
                                print(Fore.RED + str(cifra), end="")
                            except OSError as e:
                                print(str(cifra), end="")
                                pass
                            rosso_count += 1
                            if previous_was_red:
                                consecutive_reds_count += 1
                            previous_was_red = True
                        else:
                            try:
                                print(Fore.WHITE + str(cifra), end="")
                            except OSError as e:
                                print(str(cifra), end="")
                                pass
                            previous_was_red = False
                        
                        if i % 2 == 0:
                            print("\t", end="")
                    
                    if len(cifre) % 10 == 0:
                        print()
                    else:
                        print(" ", end="")
                
                # Stampa il conteggio delle cifre rosse e assicurati di andare a capo
                print(f"{Style.RESET_ALL}\t#{rosso_count} <{consecutive_reds_count}>", end="\t")

                 # Stampa il numero cardinale dell'estrazione
                print(f"[{estrazione_count}]" if estrazione_count > 0 else "[U]")
    
    def calcola_statistiche_cifre(self, numeri_per_ruota):
        cifre_presenti = Counter()
        ruota_specifica = self.config['Scraping']['ruota']
        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota == ruota_specifica:
                for numero in numeri:
                    cifre_presenti.update(str(numero).zfill(2))

        # Aggiungi le cifre mancanti con presenza 0
        cifre_totali = set(str(i) for i in range(10))
        cifre_presenti.update(dict.fromkeys(cifre_totali - set(cifre_presenti.keys()), 0))

        # Restituisci la lista di tuple ordinate per presenza discendente
        statistiche_ordinate = sorted(cifre_presenti.items(), key=lambda x: x[0], reverse=False)
        
        return statistiche_ordinate

    def generate_pairings(self, cifre_statistiche, estrazione):
        pairings = []

        # Individua la ruota specifica se presente
        ruota_specifica = self.ottieni_ruota_specifica()

        # Estrai i 5 numeri della ruota selezionata (o tutte)
        numeri_ruota = estrazione.get(ruota_specifica, [])

        # Aggiunge lo zero iniziale ai numeri minori di 10
        numeri_formattati = [str(numero).zfill(2) for numero in numeri_ruota]

        # Genera le associazioni per ogni numero dell'ultima estrazione
        for num in numeri_formattati:
            # Converti il numero in una stringa per poter scorrere la sua sequenza di cifre
            num_str = str(num)
            pairings_for_num = []

            for cifra in num_str:
                pairings_for_num.append(str(cifre_statistiche.get(cifra, 0)))

                # Aggiungi la coppia alla lista se ne hai accumulate due
                if len(pairings_for_num) == 2:
                    try:
                        pairings.append({ruota_specifica: pairings_for_num.copy()})
                    except Exception as e:
                        print(f"Errore nell'aggiunta di associazioni: {e}")

                    # Resetta la lista dopo ogni coppia
                    pairings_for_num = []

        return pairings

    def format_pairings(self, pairings):
        """
        Formatta le associazioni in un dizionario con il nome della ruota come chiave
        e una lista di coppie come valore.

        :param pairings: Lista di associazioni
        :return: Dizionario formattato {'ruota': ['xx', 'xx', ...]}
        """
        formatted_dict = {}
        for association in pairings:
            ruota_name = list(association.keys())[0]
            pairs_list = association[ruota_name]
            formatted_dict.setdefault(ruota_name, []).extend(pairs_list)

        return formatted_dict
