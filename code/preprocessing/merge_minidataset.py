import os
import pandas as pd


def get_filtered_rows(file_path, num_rows, connection_type, chunk_size=10000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    total_filtered_rows = []

    check = 0 if connection_type == 'Binary' else 'Benign'

    for chunk in chunks:
        filtered_chunk = chunk[(chunk['Type of connection'] != check)]
        total_filtered_rows.append(filtered_chunk)

        if sum(len(f) for f in total_filtered_rows) >= num_rows:
            break

    final_filtered = pd.concat(total_filtered_rows, ignore_index=True)

    if not final_filtered.empty:
        return final_filtered.sample(n=min(num_rows, len(final_filtered)), random_state=1)
    return pd.DataFrame()

def merge_files(directory_path, target_count, process_type, chunk_size=10000):
    output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/merged_output_binary.csv'

    # Elimina il file di output se esiste già
    if os.path.exists(output_file):
        os.remove(output_file)

    first_write = True
    total_attack_rows = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and file != 'idle.csv':
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                filtered_rows = get_filtered_rows(file_path, target_count, process_type, chunk_size)

                if not filtered_rows.empty:
                    filtered_rows.to_csv(output_file, mode='a', header=first_write, index=False)
                    first_write = False
                    total_attack_rows += len(filtered_rows)

    # Elaborazione di idle.csv per abbinare il numero totale di righe filtrate
    idle_file = os.path.join(directory_path, 'idle.csv')
    if os.path.exists(idle_file):
        print(f"Processing: {idle_file}")
        idle_filtered_rows = []

        for chunk in pd.read_csv(idle_file, chunksize=chunk_size):
            idle_filtered_rows.append(chunk)
            if sum(len(f) for f in idle_filtered_rows) >= total_attack_rows:
                break

        final_idle_filtered = pd.concat(idle_filtered_rows, ignore_index=True)

        if not final_idle_filtered.empty:
            final_idle_filtered.sample(n=total_attack_rows, random_state=1).to_csv(output_file, mode='a', header=first_write, index=False)

    final_data = pd.read_csv(output_file)
    total_bad_rows = total_attack_rows
    total_good_rows = final_data.shape[0] - total_bad_rows

    final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True)
    final_data.to_csv(output_file, index=False)

    # Stampa dei risultati
    print(f'\nNumero di righe di attacchi nel dataset finale: {total_bad_rows}')
    print(f'Numero di righe corrette nel dataset finale: {total_good_rows}')
    print(f'Numero totale di righe nel dataset finale: {final_data.shape[0]}')
    print('Dataset finale creato!\n')

directory = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_binary'
num_rows = 1000
process_type = 'Binary'

merge_files(directory, num_rows, process_type)