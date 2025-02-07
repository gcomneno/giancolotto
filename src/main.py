import sys
import io
from lotto_extractor import LottoExtractor
from collections import Counter

def configure_output():
    """Configura l'output del terminale per UTF-8."""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_config_values(lotto_extractor):
    """Recupera e valida i valori di configurazione."""
    try:
        offset_estr = int(lotto_extractor.config['Scraping'].get('offset_estr', 0))
    except ValueError:
        offset_estr = 0

    try:
        num_estr = int(lotto_extractor.config['Scraping'].get('num_estr', 1))
    except ValueError:
        num_estr = 1

    filtro = lotto_extractor.config.get('Filtering', 'filtro', fallback='numeri')
    if filtro not in ['numeri', 'cifre']:
        filtro = 'numeri'

    previsionale = lotto_extractor.config.getboolean('Stats', 'previsionale', fallback=False)

    return offset_estr, num_estr, filtro, previsionale

def calculate_extraction_range(offset, num_estr):
    """
    Calcola il range di estrazioni da processare.
    """
    start_id = offset + 1  # Le estrazioni iniziano da 1
    end_id = offset + num_estr

    return start_id, end_id

def process_extractions(lotto_extractor, start_id, end_id, filtro, previsionale):
    """
    Processa le estrazioni nel range specificato e stampa i risultati.
    """
    cifre_statistiche = Counter()

    # Mappa delle funzioni per i filtri
    filter_functions = {
        'numeri': lotto_extractor.print_results_numbers,
        'cifre': lotto_extractor.print_results_digits,
    }

    estrazione_count = 0
    for estr_id in range(end_id, start_id - 1, -1):
        refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estr_id)
        if refs is None or nomi_ruote is None or numeri_per_ruota is None:
            continue

        print_header = (estrazione_count == 0)

        # Ottieni la funzione di stampa corretta dal filtro
        print_function = filter_functions.get(filtro)

        if print_function:
            print_function(
                refs,
                nomi_ruote,
                numeri_per_ruota,
                print_header,
                estrazione_count,
            )
        else:
            print(f"[Errore] Filtro non valido: {filtro}")
            break

        # Calcola le statistiche se il filtro è 'cifre'
        if filtro == 'cifre' and (not previsionale or (previsionale and not print_header)):
            presenze_estr = lotto_extractor.calculate_digit_statistics(numeri_per_ruota)
            cifre_statistiche.update(dict(presenze_estr))

        estrazione_count += 1

    return cifre_statistiche, estrazione_count

def print_cifrolotto_statistics(cifre_statistiche):
    """Stampa le statistiche finali delle cifre."""
    print("=====================")
    print(" C I F R O L O T T O ")
    print("=====================")
    print("Cifra\t\tPres.")
    for cifra, presenze in cifre_statistiche.most_common():
        print(f"{cifra}\t\t{presenze}")
    print()

def main():
    configure_output()
    lotto_extractor = LottoExtractor()

    # Lettura e validazione dei parametri di configurazione
    offset_estr, num_estr, filtro, previsionale = get_config_values(lotto_extractor)

    # Ottieni l'ultima estrazione se richiesto
    if num_estr == 999:
        refs, _, _ = lotto_extractor.get_last_extraction()
        if refs:
            num_estr = refs[0]
        else:
            print("[DEBUG] Impossibile recuperare l'ultima estrazione.")
            sys.exit(1)

    # Calcolo del range di estrazioni
    start_id, end_id = calculate_extraction_range(offset_estr, num_estr)

    try:
        # Processamento delle estrazioni
        cifre_statistiche, estrazione_count = process_extractions(
            lotto_extractor, start_id, end_id, filtro, previsionale
        )

        # Stampa delle statistiche finali per il filtro "cifre"
        if filtro == 'cifre' and estrazione_count > 1:
            print_cifrolotto_statistics(cifre_statistiche)

            if previsionale and end_id > 1:
                refs, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(end_id)
                pairings = lotto_extractor.generate_pairings(cifre_statistiche, numeri_per_ruota)
                formatted_pairings = lotto_extractor.format_pairings(pairings)

                for ruota, assoc_list in formatted_pairings.items():
                    print(" ".join("|".join(pair) for pair in zip(*[iter(assoc_list)] * 2)))

    except Exception as e:
        print(f"Errore nel loop principale: {e}")

if __name__ == "__main__":
    main()
