from lotto_extractor import LottoExtractor

if __name__ == "__main__":

    lotto_extractor = LottoExtractor()

    # Imposta il numero di estrazioni da recuperare. Default = 1
    try:
        num_estr = int(lotto_extractor.config['Scraping'].get('num_estr', 1))
    except ValueError:
        num_estr = 1

    try:
        for estr in range(num_estr):
            numbers, nomi_ruote, numeri_per_ruota = lotto_extractor.extraction(estr + 1)
            lotto_extractor.print_results(numbers, nomi_ruote, numeri_per_ruota, estr + 1)
        print()
    except Exception as e:
        print(f"Errore: {e}")
