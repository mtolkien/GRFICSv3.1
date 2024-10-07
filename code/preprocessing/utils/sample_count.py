def sample_count(file_path):
    max_samples = 4100000

    attack_rows = {}

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(" -> ")
            if len(parts) == 2:
                file_name = parts[0].replace("File: ", "").strip()
                rows = int(parts[1].replace("Righe di attacchi: ", "").strip())
                attack_rows[file_name] = rows

    # Calcola il numero totale di file
    num_file = len(attack_rows)

    # Calcola il numero comune di rows da prelevare
    common = max_samples // num_file if num_file > 0 else 0

    # Inizializza un dizionario per i samples da prelevare
    sample_to_pick = {}
    sum = 0

    # Calcola i samples da prelevare per ciascun file
    for file, rows in attack_rows.items():
        if common > rows:
            sample_to_pick[file] = rows
        else:
            sample_to_pick[file] = common
        sum += sample_to_pick[file]

    print(f"Numero comune di campioni da prelevare per ciascun file: {common}")
    print(f"Somma totale di samples da prelevare: {sum}")

file_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/count_attacks_total.txt'
sample_count(file_path)
