import sys
import io

from lotto_extractor import LottoExtractor
from collections import Counter

if __name__ == "__main__":

    # Forza l'uso di UTF-8 come encoding di output
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    lotto_extractor = LottoExtractor()

    # 1) Lettura dei parametri di configurazione
    try:
        num_estr = int(lotto_extractor.config['Scraping'].get('num_estr', 1))
    except ValueError:
        num_estr = 1

    try:
        offset_estr = int(lotto_extractor.config['Scraping'].get('offset_estr', 0))
    except ValueError:
        offset_estr = 0

    filtro = lotto_extractor.config.get('Filtering', 'filtro', fallback='numeri')
    if filtro not in ['numeri', 'cifre']:
        filtro = 'numeri'

    previsionale = lotto_extractor.config.getboolean('Stats', 'previsionale', fallback=False)

    # 2) Gestione contatori e statistiche (solo per 'cifre')
    cifre_statistiche = Counter()

    # 3) Calcoliamo il “range” di estrazioni da prelevare, in base anche al valore di "previsionale"
    start_id = offset_estr + 1           # Le estrazioni ufficiali iniziano da 1
    end_id = offset_estr + num_estr      # Fine range ufficiale

    # Se previsionale=True, saltiamo la più recente
    if previsionale and num_estr > 0:
        end_id -= 1

    # 4) Loop principale sulle estrazioni
    #    Se previsionale=True, l'ultima iterazione non verrà inclusa in range(...)
    estrazione_count = 0
    try:
        # Loop inverso: da end_id a start_id (incluso), decrementando di 1
        for estr_id in range(end_id, start_id - 1, -1):
            # Richiama extraction per ottenere i dati dell'estrazione
            refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estr_id)

            # Se la chiamata non restituisce dati validi, ignoriamo e passiamo all'iterazione successiva
            if refs is None or nomi_ruote is None or numeri_per_ruota is None:
                #print(f"[DEBUG] Nessun dato valido per estrazione ID={estr_id}, ignoro.")
                continue

            # Stampa l'header solo nella prima iterazione
            printHeader = (estrazione_count == 0)

            # Stampa dei risultati in base al filtro
            if filtro == 'numeri':
                lotto_extractor.print_results_numeri(
                    refs,
                    nomi_ruote,
                    numeri_per_ruota,
                    printHeader,
                    estrazione_count
                )
            else:  # filtro == 'cifre'
                lotto_extractor.print_results_cifre(
                    refs,
                    nomi_ruote,
                    numeri_per_ruota,
                    printHeader,
                    estrazione_count
                )

                # Aggiorna le statistiche per cifre
                if not previsionale or (previsionale and not printHeader):
                    presenze_estr = lotto_extractor.calcola_statistiche_cifre(numeri_per_ruota)
                    cifre_statistiche.update(dict(presenze_estr))

            estrazione_count += 1

        # 5) Fine loop: riga vuota per separare
        print()

        # 6) Se stiamo analizzando cifre, stampa le statistiche finali
        if filtro == 'cifre':
            print("=====================")
            print(" C I F R O L O T T O ")
            print("=====================")
            print("Cifra\t\tPres.")
            for cifra, presenze in cifre_statistiche.most_common():
                print(f"{cifra}\t\t{presenze}")
            print()

            # Richiama extraction() per ottenere i dati dell'ultima estrazione (ignorata quando previsionale=True)
            if previsionale:
                refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estrazione_count + 1)
                pairings = lotto_extractor.generate_pairings(cifre_statistiche, numeri_per_ruota)
                formatted_pairings = lotto_extractor.format_pairings(pairings)

                for ruota, assoc_list in formatted_pairings.items():
                    print(" ".join("|".join(pair) for pair in zip(*[iter(assoc_list)]*2)))
                    print()

    except Exception as e:
        print(f"Errore nel loop principale: {e}")
