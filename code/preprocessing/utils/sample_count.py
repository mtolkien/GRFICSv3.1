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

    # Calculate the total number of files
    num_file = len(attack_rows)

    # Calculate the common number of rows to sample
    common = max_samples // num_file if num_file > 0 else 0

    # Initialize a dictionary for the samples to pick
    sample_to_pick = {}
    total_sum = 0

    # Calculate the samples to pick for each file
    for file, rows in attack_rows.items():
        if common > rows:
            sample_to_pick[file] = rows
        else:
            sample_to_pick[file] = common
        total_sum += sample_to_pick[file]

    print(f"Common number of samples to take for each file: {common}")
    print(f"Total sum of samples to take: {total_sum}")

file_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/count_attacks_total.txt'
sample_count(file_path)