from lotto_extractor import LottoExtractor

if __name__ == "__main__":
    lotto_extractor = LottoExtractor()

    try:
        numbers, nomi_ruote, numeri_per_ruota = lotto_extractor.parse_data()
        lotto_extractor.print_results(numbers, nomi_ruote, numeri_per_ruota)
    except Exception as e:
        print(f"Errore: {e}")

    # Attendere l'input dell'utente prima di terminare il programma
    input("Premi Invio per uscire...")
