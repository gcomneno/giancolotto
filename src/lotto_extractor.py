import requests
from bs4 import BeautifulSoup
import re
import configparser

class LottoExtractor:
    def __init__(self, config_file='config.ini'):
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
        extractions = soup.find_all('article', class_='tabellaEstrazioni-arch')

        if not extractions:
            raise ValueError("Nessuna estrazione trovata!")

        return extractions

    def extraction(self, num=None):
        extraction = self.extractions[num - 1] if num and 1 <= num <= len(self.extractions) else None

        if extraction:
            ruote_elements = extraction.find_all('td', class_='nomeRuota-arch estratto-arch')
            nomi_ruote = [ruota.text.strip() for ruota in ruote_elements]

            numbers = re.findall(r'\d+', extraction.text)

            main_references = [int(num) for num in numbers[:9]]
            numbers = numbers[9:]
            numeri_per_ruota = {ruota: [int(num) for num in numbers[i*5:(i+1)*5]] for i, ruota in enumerate(nomi_ruote)}

            return main_references, nomi_ruote, numeri_per_ruota
        else:
            print("Numero estrazione non valido.")
            return None, None, None

    def print_results_numeri(self, refs, nomi_ruote, numeri_per_ruota, curr_estr):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or curr_estr == 1:
            print("\nEstrazione\t\tRUOTA\t\t" + "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)]))
            print("===========================================================================")

        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota == ruota_specifica:
                print(f"n. {refs[0]} del {refs[1]}/{refs[2]}/{refs[3]}", end="\t")
                print(f"{ruota.ljust(9)}", end="\t")
                for numero in numeri:
                    # Verifica se il numero è tra quelli da evidenziare
                    if numero in self.numeri_evidenziati:
                        # Evidenzia il numero con un colore (ad esempio, colore rosso)
                        print("\033[91m", end="")
                        print(f"{numero:02d}", end="\t")
                        print("\033[0m", end="")
                    else:
                        print(f"{numero:02d}", end="\t")

                # Vai a capo alla fine della riga
                print()

    def print_results_cifre(self, refs, nomi_ruote, numeri_per_ruota, curr_estr):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or curr_estr == 1:
            print("\nEstrazione\t\tRUOTA\t\t" + "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)]))
            print("===========================================================================")
        
        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota == ruota_specifica:
                print(f"n. {refs[0]} del {refs[1]}/{refs[2]}/{refs[3]}", end="\t")
                print(f"{ruota.ljust(9)}", end="\t")
                for numero in numeri:
                    if numero < 10:
                        # Aggiungi uno zero davanti al numero e crea una lista di cifre
                        cifre = [0, numero]
                    else:
                        # Altrimenti, crea una lista di cifre normalmente
                        cifre = [int(cifra) for cifra in str(numero)]
                        
                    for i, cifra in enumerate(cifre, start=1):
                        # Verifica se la cifra è tra quelle da evidenziare
                        if cifra in self.cifre_evidenziate:
                            # Evidenzia la cifra con un colore (ad esempio, colore verde chiaro)
                            print("\033[92m", end="")
                            print(cifra, end="")
                            print("\033[0m", end="")
                        else:
                            print(cifra, end="")

                        # Aggiungi un tabulatore ogni due cifre
                        if i % 2 == 0:
                            print("\t", end="")

                    # Aggiungi un ritorno a capo dopo 10 cifre
                    if i % 10 == 0:
                        print()
                    else:
                        print("", end="")

                # Assicurati di andare a capo alla fine del ciclo
                print()

