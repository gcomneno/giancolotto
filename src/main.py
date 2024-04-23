from lotto_extractor import LottoExtractor
from collections import Counter

if __name__ == "__main__":

    lotto_extractor = LottoExtractor()

    # Stampa le collezioni eventualmente già presenti nel db
    lotto_extractor.stampa_collezioni()

    # Imposta il numero di estrazioni da recuperare. Default = 1
    try:
        num_estr = int(lotto_extractor.config['Scraping'].get('num_estr', 1))
    except ValueError:
        num_estr = 1

    # Imposta l'offset di estrazioni da saltare. Default = 0
    try:
        offset_estr = int(lotto_extractor.config['Scraping'].get('offset_estr', 0))
    except ValueError:
        offset_estr = 0

    # Imposta il tipo di evidenziamento (numeri oppure cifre). Default = numeri
    filtro = lotto_extractor.config.get('Filtering', 'filtro', fallback='numeri')

    # Verifica che il tipo di evidenziamento sia valido
    if filtro not in ['numeri', 'cifre']:
        filtro = 'numeri'

    try:
        cifre_statistiche = Counter()

        for estr in range(offset_estr, offset_estr + num_estr):
            refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estr + 1)

            if estr == offset_estr:
                 prima_estrazione = numeri_per_ruota

            printHeader = estr == offset_estr
            if filtro == 'numeri':
                lotto_extractor.print_results_numeri(refs, nomi_ruote, numeri_per_ruota, printHeader)
            elif filtro == 'cifre':
                lotto_extractor.print_results_cifre(refs, nomi_ruote, numeri_per_ruota, printHeader)

            lotto_extractor.salva_su_mongodb('ESTR', refs, numeri_per_ruota)

            # Previsionale ? (Ignora l'ultimissima estrazione)
            previsionale = lotto_extractor.config.getboolean('Stats', 'previsionale')

            if (previsionale and not printHeader) or not previsionale:
                # Calcola le statistiche delle presenze per ogni cifra            
                presenze_estr = lotto_extractor.calcola_statistiche_cifre(numeri_per_ruota)

                # Aggiorna le statistiche delle cifre con quelle dell'estratto corrente
                cifre_statistiche.update(dict(presenze_estr))
                
        print()

        # Stampa le statistiche finali
        print("Statistica delle cifre alla estraz.-1:")
        print("Presenze\tCifra")
        for cifra, presenze in cifre_statistiche.most_common():
            print(f"{presenze}\t\t{cifra}")

        print()

        # Genera le accopiamenti di presenza delle cifre in base alla classifica corrente
        associations = lotto_extractor.generate_associations(cifre_statistiche, prima_estrazione)

        # Sala le associazioni appena generate
        lotto_extractor.salva_su_mongodb('ASSO', refs, associations, is_association=True)

        # Formatta le associazioni per l'output a video
        formatted_associations = lotto_extractor.format_associations(associations)

        # Stampa tutte le coppie relazionate su una singola riga
        for ruota, assoc_list in formatted_associations.items():
            print("|".join("".join(pair) for pair in zip(*[iter(assoc_list)]*2)))

        print()

        # Chiamata alla funzione per caricare e calcolare la classifica delle associazioni da DB
        # ruota_specifica = lotto_extractor.ottieni_ruota_specifica()
        # risultati_associazioni = lotto_extractor.carica_associazioni_da_mongodb(ruota_specifica)
        # print(risultati_associazioni)

        # Generazione e stampa della classifica delle associazioni
        # classifica = LottoExtractor.calcola_classifica_associazioni(risultati_associazioni)
        # print("Classifica delle coppie di presenze più presenti:")
        # for coppia, presenze in classifica:
        #     print(f"{coppia}: {presenze} volte")

    except Exception as e:
        print(f"Errore: {e}")
