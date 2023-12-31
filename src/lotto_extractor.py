import requests
from bs4 import BeautifulSoup
import re
import configparser

class LottoExtractor:
    def __init__(self, config_file='config.ini'):
        self.config = self.read_config(config_file)
        self.url = self.config.get('Scraping', 'url')
        self.numeri_evidenziati = self.get_numeri_evidenziati()
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

    def print_results(self, refs, nomi_ruote, numeri_per_ruota, curr_estr):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or curr_estr == 1:
            print("\nEstrazione\t\tRUOTA\t\t" + "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)]))
            print("===========================================================================")
        
        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota == ruota_specifica:
                print(f"n. {refs[0]} del {refs[1]}/{refs[2]}/{refs[3]}", end="\t")

                numeri_formattati = [int(numero) for numero in numeri]
                print(f"{ruota.ljust(9)}", end="\t")

                for numero in numeri_formattati:
                    # Verifica se il numero è tra quelli da evidenziare
                    if numero in self.numeri_evidenziati:
                        # Evidenzia il numero con un colore
                        print(f"\033[91m{numero:02d}\033[0m", end="\t")
                    else:
                        print(f"{numero:02d}", end="\t")

                print()