from lotto_extractor import LottoExtractor

if __name__ == "__main__":

    lotto_extractor = LottoExtractor()

    # Stampa le collezioni presenti nel database
    collections = lotto_extractor.get_collections()
    if collections:
        print("Collezioni presenti nel database:")
        for collection_name in collections:
            print(collection_name)
    else:
        print("Nessuna collezione presente nel database.")    

    # Imposta il numero di estrazioni da recuperare. Default = 1
    try:
        num_estr = int(lotto_extractor.config['Scraping'].get('num_estr', 1))
    except ValueError:
        num_estr = 1

    # Imposta il tipo di evidenziamento (numeri oppure cifre). Default = numeri
    filtro = lotto_extractor.config.get('Filtering', 'filtro', fallback='numeri')

    # Verifica che il tipo di evidenziamento sia valido
    if filtro not in ['numeri', 'cifre']:
        filtro = 'numeri'

    try:
        for estr in range(num_estr):
            refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estr + 1)

            if filtro == 'numeri':
                lotto_extractor.print_results_numeri(refs, nomi_ruote, numeri_per_ruota, estr + 1)
            elif filtro == 'cifre':
                lotto_extractor.print_results_cifre(refs, nomi_ruote, numeri_per_ruota, estr + 1)

            lotto_extractor.salva_su_mongodb(refs, numeri_per_ruota)

        print()
    except Exception as e:
        print(f"Errore: {e}")