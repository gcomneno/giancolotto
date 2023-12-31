import requests
from bs4 import BeautifulSoup
import re
import configparser

class LottoExtractor:
    def __init__(self, config_file='config.ini'):
        self.config = self.read_config(config_file)
        self.url = self.config.get('Scraping', 'url')
        self.response = self.fetch_data()

    def read_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Impossibile recuperare la pagina. Codice di stato: {response.status_code}")

    def parse_data(self, num_estr=None):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        extraction_articles = soup.find_all('article', class_='tabellaEstrazioni-arch')
        extraction_article = extraction_articles[num_estr]        
        ruote_elements = extraction_article.find_all('td', class_='nomeRuota-arch estratto-arch')
        nomi_ruote = [ruota.text.strip()[:9] for ruota in ruote_elements]

        numbers = re.findall(r'\d+', extraction_article.text)
        numeri_per_ruota = {}

        for i, ruota in enumerate(nomi_ruote):
            start_index = 9 + i * 5
            end_index = start_index + 5
            numeri_per_ruota[ruota] = numbers[start_index:end_index]

        return numbers, nomi_ruote, numeri_per_ruota

    def print_results(self, numbers, nomi_ruote, numeri_per_ruota):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica:
            print(f"\nEstrazione n. {numbers[0]} del {numbers[1]}/{numbers[2]}/{numbers[3]}")
            print("\nRUOTA\t\t" + "\t".join([f"{i}o" for i in range(1, len(numeri_per_ruota[nomi_ruote[0]]) + 1)]))
            print("===================================================")
        for ruota, numeri in numeri_per_ruota.items():
            if not ruota_specifica or ruota_specifica in ruota:
                numeri_formattati = [int(numero) for numero in numeri]
                print(f"{ruota.ljust(9)}\t{numeri_formattati[0]:02d}\t{numeri_formattati[1]:02d}\t{numeri_formattati[2]:02d}\t{numeri_formattati[3]:02d}\t{numeri_formattati[4]:02d}")
