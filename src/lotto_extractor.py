import requests
from bs4 import BeautifulSoup
import re
import configparser
import pymongo
from collections import Counter

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

    def ottieni_opzioni_configurazione(self):
        host = self.config.get('Persistence', 'host')
        porta = self.config.getint('Persistence', 'porta')
        database_nome = self.config.get('Persistence', 'database')
        return host, porta, database_nome

    def ottieni_connessione_mongodb(self):
        host, porta, database_nome = self.ottieni_opzioni_configurazione()        
        client = pymongo.MongoClient(host, porta)
        return client, client[database_nome]

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

    def print_results_numeri(self, refs, nomi_ruote, numeri_per_ruota, printHeader):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or printHeader:
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

    def print_results_cifre(self, refs, nomi_ruote, numeri_per_ruota, printHeader):
        ruota_specifica = self.config['Scraping']['ruota']
        if not ruota_specifica or printHeader:
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

    def stampa_collezioni(self):
        # Verifica se è abilitata la persistenza
        if self.config.getboolean('Persistence', 'attiva'):
            try:
                # Ottieni la connessione a MongoDB
                client, db = self.ottieni_connessione_mongodb()

                # Ottieni le collezioni presenti nel database
                collections = db.list_collection_names()

                if collections:
                    print("Collezioni presenti nel database:")
                    for collection_name in collections:
                        print(collection_name)
                else:
                    print("Nessuna collezione presente nel database.")

                # Chiudi la connessione solo dopo aver completato tutte le operazioni
                client.close()

            except Exception as e:
                print(f"Errore durante la visualizzazione delle collezioni nel database: {e}")

    def carica_associazioni_da_mongodb(self, ruota_specifica='Tutte'):
        # Ottieni la connessione a MongoDB
        client, db = self.ottieni_connessione_mongodb()

        # Ottieni le collezioni che iniziano con "ASSO" dal database
        collections = [collezione for collezione in db.list_collection_names() if collezione.startswith("ASSO")]

        # Dizionario per tenere traccia delle presenze delle coppie
        coppie_presenze = {}

        # Itera attraverso le collezioni
        for collezione_nome in collections:
            # Estrai la ruota dal nome della collezione
            ruota_collezione = collezione_nome.replace("ASSO", "")
            
            # Carica le associazioni solo se la ruota corrisponde a quella specificata o è "Tutte"
            if ruota_specifica == 'Tutte' or ruota_specifica == ruota_collezione:
                collezione_associazioni = db[collezione_nome]

                # Itera attraverso i documenti nella collezione
                for documento in collezione_associazioni.find():
                    risultati_associazioni = documento.get("associazioni", [])

                    # Itera attraverso le associazioni nel documento
                    for risultato in risultati_associazioni:
                        cifre = risultato.split('|')

                        # Itera attraverso le cifre in coppia
                        for cifra in cifre:
                            coppie_presenze[cifra] = coppie_presenze.get(cifra, 0) + 1

        # Ordina le coppie in base alle presenze (da più a meno presenti)
        coppie_ordinate = sorted(coppie_presenze.items(), key=lambda x: x[1], reverse=True)

        client.close()

        return coppie_ordinate

    def salva_su_mongodb(self, prefisso_collezione, refs, data, is_association=False):
        # Verifica se è abilitato il salvataggio su MongoDB
        if self.config.getboolean('Persistence', 'attiva'):
            try:
                # Ottieni la connessione a MongoDB
                client, db = self.ottieni_connessione_mongodb()

                # Ottieni la ruota specifica
                ruota_specifica = self.ottieni_ruota_specifica()

                # Il nome della collection in DB è prefisso+anno+num_estr+ruota
                collezione_nome = f"{prefisso_collezione}{refs[3]}{refs[0]}{ruota_specifica}"
                collezione = db[collezione_nome]

                # Crea un documento da inserire nel database
                if is_association:
                    documento = {
                        "estrazione": refs[0],
                        "data": f"{refs[1]}/{refs[2]}/{refs[3]}",
                        "associazioni": data
                    }
                else:
                    documento = {
                        "estrazione": refs[0],
                        "data": f"{refs[1]}/{refs[2]}/{refs[3]}",
                        "ruote": []
                    }

                    # Aggiungi le informazioni di ogni ruota al documento
                    for ruota, numeri in data.items():
                        documento_ruota = {
                            "nome_ruota": ruota,
                            "numeri": numeri
                        }
                        documento["ruote"].append(documento_ruota)

                # Inserisci il documento nella collezione
                collezione.insert_one(documento)

                print(f"Dati salvati nella collection: {collezione_nome}")
                print()

                # Chiudi la connessione solo dopo aver completato tutte le operazioni
                client.close()
                
            except Exception as e:
                print(f"Errore durante il salvataggio su MongoDB: {e}")

    def get_collections(self):
        try:
            # Connetti al server MongoDB
            host = self.config.get('Persistence', 'host')
            porta = self.config.getint('Persistence', 'porta')

            client = pymongo.MongoClient(host, porta)
            
            # Scegli il database
            db = client[self.config.get('Persistence', 'database')]

            # Ottieni una lista di tutte le collection nel database
            collections_list = db.list_collection_names()

            purge = self.config['Persistence'].get('purga')
            if purge:
                # Pulizia di ogni collezione
                for collection_name in collections_list:
                    collection = db[collection_name]
                    collection.drop()

            # Chiudi la connessione al server MongoDB
            client.close()

            # Restituisci la lista delle collection
            return collections_list
        except Exception as e:
            print(f"Errore durante il recupero delle collection: {e}")
            return []

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

    def generate_associations(self, cifre_statistiche, estrazione):
        associations = []

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
            associations_for_num = []

            for cifra in num_str:
                associations_for_num.append(str(cifre_statistiche.get(cifra, 0)))

                # Aggiungi la coppia alla lista se ne hai accumulate due
                if len(associations_for_num) == 2:
                    try:
                        associations.append({ruota_specifica: associations_for_num.copy()})
                    except Exception as e:
                        print(f"Errore nell'aggiunta di associazioni: {e}")

                    # Resetta la lista dopo ogni coppia
                    associations_for_num = []

        return associations

    def format_associations(self, associations):
        """
        Formatta le associazioni in un dizionario con il nome della ruota come chiave
        e una lista di coppie come valore.

        :param associations: Lista di associazioni
        :return: Dizionario formattato {'ruota': ['xx', 'xx', ...]}
        """
        formatted_dict = {}
        for association in associations:
            ruota_name = list(association.keys())[0]
            pairs_list = association[ruota_name]
            formatted_dict.setdefault(ruota_name, []).extend(pairs_list)

        return formatted_dict

    def calcola_classifica_associazioni(self, risultati_associazioni):

        # Esempio dei risultati delle associazioni (da cancellare)
        risultati_associazioni = [
            "31|31|01|10|40",
            "10|31|44|11|32",
            "44|03|41|44|40",
            "54|11|21|23|55",
            "31|03|04|50|00",
            "31|22|21|22|22",
            "32|00|11|11|02",
            "33|32|22|23|30",
            "23|24|33|32|02",
            "23|32|22|12|11"
        ]

        # Dizionario per tenere traccia delle presenze delle coppie
        coppie_presenze = {}

        # Itera attraverso i risultati delle associazioni
        for risultato in risultati_associazioni:
            # Separa le cifre nella coppia
            cifre = risultato.split('|')

            # Itera attraverso le cifre in coppia
            for cifra in cifre:
                # Aggiorna il conteggio delle presenze della coppia nel dizionario
                coppie_presenze[cifra] = coppie_presenze.get(cifra, 0) + 1

        # Ordina le coppie in base alle presenze (da più a meno presenti)
        coppie_ordinate = sorted(coppie_presenze.items(), key=lambda x: x[1], reverse=True)

        return coppie_ordinate
