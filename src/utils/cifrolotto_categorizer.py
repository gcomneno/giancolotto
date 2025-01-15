import os
import subprocess
import re

class CifrolottoCategorizer:
    MAIN_SCRIPT = "./scripts/get_all.sh"

    RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

    WHEEL_MAP = {
        "Bari": "BA", "Cagliari": "CA", "Firenze": "FI", "Genova": "GE",
        "Milano": "MI", "Napoli": "NA", "Palermo": "PA", "Roma": "RM",
        "Torino": "TO", "Venezia": "VE"
    }

    CATEGORY_RULES = {
        "GT": [(1, 1)],
        "GB": [(10, 10)],
        "TD": [(1, 10)],
        "DT": [(10, 1)],
        "MD": [(5, 6), (6, 5)],
        "TSG": [(1, 2), (3, 4)],
        "BSG": [(7, 8), (9, 10)],
        "TCG": [(1, 2), (2, 3), (3, 4)],
        "BCG": [(7, 8), (8, 9), (9, 10)],
        "TSS": [(4, 3), (2, 1)],
        "BSS": [(10, 9), (8, 7)],
        "TCS": [(4, 3), (3, 2), (2, 1)],
        "BCS": [(10, 9), (9, 8), (8, 7)],
        "TPA": [(1, 2)],
        "BMA": [(9, 10)],
        "ATP": [(2, 1)],
        "ABM": [(10, 9)],
    }

    def __init__(self):
        self.MAIN_SCRIPT = os.path.abspath(self.MAIN_SCRIPT)

    def run(self):
        print(f"Esecuzione dello script principale {self.MAIN_SCRIPT}, in corso...")
        output = self.run_script()
        print("Output del script recuperato. Categorizzazione per ruota, in corso...")

        for ruota_name in self.RUOTE:
            start_index = output.find(ruota_name)
            if start_index == -1:
                print(f"Ruota {ruota_name} non trovata nell'output.")
                continue

            extraction = self.parse_extraction(output, start_index)
            cifrolotto = self.parse_cifrolotto(output, start_index)

            print(f"Estrazione per {ruota_name}: {extraction}")
            print(f"Classifica CIFROLOTTO per {ruota_name}: {cifrolotto}")

            if extraction:
                categorized_data = self.categorize_numbers(extraction, cifrolotto)
                self.save_to_dataset(categorized_data)
                print(f"Dati salvati per {ruota_name}.")

    def run_script(self):
        if not os.path.exists(self.MAIN_SCRIPT):
            raise FileNotFoundError(f"Lo script {self.MAIN_SCRIPT} non esiste.")

        try:
            result = subprocess.run(
                ["bash", self.MAIN_SCRIPT],
                check=True,
                text=True,
                capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione dello script {self.MAIN_SCRIPT}:")
            print("Uscita standard:", e.stdout)
            print("Errore standard:", e.stderr)
            raise

    def parse_extraction(self, output, start_index):
        end_index = output.find('\n', start_index)
        if end_index == -1:
            end_index = len(output)

        block = output[start_index:end_index]
        ruota_name = re.search(r"\b[A-Za-z]+\b", block).group(0)

        pattern = re.escape(ruota_name) + r"\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})"
        matches = re.findall(pattern, block)

        if matches:
            numeri = list(map(int, matches[0]))
            return {'ruota': ruota_name, 'numeri': numeri}
        else:
            print(f"Errore: Nessun numero trovato per la ruota {ruota_name}.")
            return None

    def parse_cifrolotto(self, output, start_index):
        cifrolotto_start_regex = re.compile(r"Cifra\s+Pres\.\n", re.IGNORECASE)
        next_header_regex = re.compile(r"={5,}")

        start_match = cifrolotto_start_regex.search(output, start_index)
        if not start_match:
            print(f"[DEBUG] Start of CIFROLOTTO block not found for start_index {start_index}.")
            return {}

        end_match = next_header_regex.search(output, start_match.end())
        end_index = end_match.start() if end_match else len(output)

        cifrolotto_data = output[start_match.end():end_index]
        cifrolotto = {}
        for line in cifrolotto_data.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                cifra, pres = parts[0], int(parts[1])
                cifrolotto[cifra] = pres

        return cifrolotto

    def calculate_positions(self, cifrolotto):
        sorted_cifrolotto = sorted(cifrolotto.items(), key=lambda x: x[1], reverse=True)
        return {cifra: idx + 1 for idx, (cifra, _) in enumerate(sorted_cifrolotto)}

    def categorize_pair(self, pos1, pos2):
        categories = []
        for category, rules in self.CATEGORY_RULES.items():
            if (pos1, pos2) in rules:
                categories.append(category)
        return categories

    def categorize_numbers(self, extraction, cifrolotto):
        if not extraction or not cifrolotto:
            return None

        ruota = extraction['ruota']
        numeri = extraction['numeri']
        categories = []

        posizioni_cifre = self.calculate_positions(cifrolotto)

        for numero in numeri:
            numero_str = f"{numero:02d}"
            cifre = [int(c) for c in numero_str]

            posizione1 = posizioni_cifre.get(str(cifre[0]), -1)
            posizione2 = posizioni_cifre.get(str(cifre[1]), -1)

            if posizione1 == -1 or posizione2 == -1:
                continue

            categorie_numero = self.categorize_pair(posizione1, posizione2)
            categories.extend(categorie_numero)

            print(f"Numero: {numero}, Posizioni: {posizione1}, {posizione2}, Categorie: {categorie_numero}")

        category_counts = {cat: categories.count(cat) for cat in set(categories)}
        formatted_categories = [f"{count}|{cat}" for cat, count in category_counts.items()]

        print(f"Risultati finali per ruota {ruota}: {formatted_categories}")
        return {"ruota": ruota, "numeri": numeri, "categorie": formatted_categories}

    def save_to_dataset(self, data, filename="./dataset/cifrolotto.data"):
        try:
            with open(filename, 'a') as file:
                if data:
                    wheel_abbreviation = self.WHEEL_MAP[data['ruota']]
                    line = f"{wheel_abbreviation}\t{data['categorie']}\n"
                    file.write(line)
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")

if __name__ == "__main__":
    categorizer = CifrolottoCategorizer()
    categorizer.run()
