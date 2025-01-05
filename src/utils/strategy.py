def strategy(number: int, min_consecutive: int, max_attempts: int):
    # Carica i dati dal dataset
    data = []
    with open('../dataset/database.2025.md', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            # parts[0] = "Palermo" 
            numeri_str = parts[1:]  # ignore ruota

            numbers = list(map(int, numeri_str))
            data.append(numbers)

    consecutive_presences = 0
    ng = 0
    ok_count = 0  # Contatore OK
    ko_count = 0  # Contatore KO
    results = []
    in_game = False  # Flag per tenere traccia se siamo in gioco

    for extraction_number in range(1, len(data) + 1):
        # Verifica se il numero è presente nell'estrazione
        if number in data[extraction_number - 1]:
            consecutive_presences += 1

            # Se le presenze consecutive raggiungono il limite per giocare
            if consecutive_presences >= min_consecutive:
                if in_game:
                    ng += 1  # Incrementiamo il numero di giocate consecutive
                    results.append((number, extraction_number, consecutive_presences, "Si", "OK", ng))
                    ok_count += 1  # Incrementa il contatore OK

                    # Controlla se abbiamo raggiunto il numero massimo di giocate consecutive
                    if ng >= max_attempts:
                        results.append((number, extraction_number, consecutive_presences, "Esco", "", ""))
                        in_game = False  # Non siamo più in gioco
                        ng = 0  # Resetta il contatore NG
                else:
                    results.append((number, extraction_number, consecutive_presences, "Entro", "", ""))
                    in_game = True  # Siamo ora in gioco
            else:
                results.append((number, extraction_number, consecutive_presences, "No", "", ""))
        else:
            # Se il numero non esce e siamo in gioco, esito KO
            if in_game:
                ng += 1  # Incrementiamo NG anche per i tentativi con KO
                results.append((number, extraction_number, 0, "Si", "KO", ng))  # Mantieni "Si" e mostra "KO"
                ko_count += 1  # Incrementa il contatore KO
                results.append((number, extraction_number, 0, "Esco", "", ""))  # Forza l'uscita dopo "KO"
                in_game = False  # Uscita immediata dal gioco
                ng = 0  # Resetta NG dopo "Esco"
            else:
                results.append((number, extraction_number, 0, "No", "", ""))

            # Azzeramento del contatore delle presenze
            consecutive_presences = 0

    # Calcolo del rapporto OK/KO
    if ko_count > 0:  # Evita divisioni per zero
        rapporto = ok_count / ko_count
    else:
        rapporto = "Inf"  # Nessun KO significa un rapporto infinito

    return results, ok_count, ko_count, rapporto

# Esegui la strategia
if __name__ == "__main__":
    import sys
    
    # Verifica se ci sono abbastanza argomenti
    if len(sys.argv) != 4:
        print("Utilizzo: python strategy.py <numero> <min_consecutive> <max_tentativi>")
        sys.exit(1)

    number = int(sys.argv[1])
    min_consecutive = int(sys.argv[2])
    max_attempts = int(sys.argv[3])
    
    output, ok_count, ko_count, rapporto = strategy(number, min_consecutive, max_attempts)
    print(f"Num.  Estr. Pres.   Gioco?   Esito   NG")
    for line in output:
        print(f"[{line[0]}]  {line[1]:02d}    {line[2]}       {line[3]}       {line[4]}      {line[5]}")

    # Stampa il rapporto finale
    print(f"\n[{int(line[0]):02d}] Rapporto di Successo: {ok_count} OK / {ko_count} KO = {rapporto}")
