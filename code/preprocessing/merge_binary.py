import os
import pandas as pd


def get_filtered_rows(file_path, rows_per_file, chunk_size=10000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    filtered_rows = []
    check = 0

    for chunk in chunks:
        category_filtered = chunk[chunk['Type of connection'] != check]
        filtered_rows.append(category_filtered)

        if sum(len(rows) for rows in filtered_rows) >= rows_per_file:
            break

    combined_rows = pd.concat(filtered_rows, ignore_index=True) if filtered_rows else pd.DataFrame()

    if len(combined_rows) < rows_per_file:
        return combined_rows
    else:
        return combined_rows.sample(n=rows_per_file, random_state=1)


def merge_files(directory_path, num_rows, chunk_size=10000):
    output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Dataset_Binary.csv'

    if os.path.exists(output_file):
        os.remove(output_file)

    first_write = True
    total_attack_rows = 0

    # Process each CSV file in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and file != 'idle.csv':
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                print(f"Processing: {file_name}")

                filtered_rows = get_filtered_rows(file_path, num_rows, chunk_size)

                if not filtered_rows.empty:
                    filtered_rows.to_csv(output_file, mode='a', header=first_write, index=False)
                    first_write = False
                    total_attack_rows += len(filtered_rows)

    # Process idle.csv to match the total number of filtered rows
    idle_file = os.path.join(directory_path, 'idle.csv')
    if os.path.exists(idle_file):
        print(f"Processing: {os.path.basename(idle_file)}")
        idle_filtered_rows = []

        for chunk in pd.read_csv(idle_file, chunksize=chunk_size):
            idle_filtered_rows.append(chunk)
            if sum(len(f) for f in idle_filtered_rows) >= total_attack_rows:
                break

        final_idle_filtered = pd.concat(idle_filtered_rows, ignore_index=True)

        if not final_idle_filtered.empty:
            final_idle_filtered.sample(n=total_attack_rows, random_state=1).to_csv(output_file, mode='a', header=first_write, index=False)

    final_data = pd.read_csv(output_file)
    total_good_rows = final_data.shape[0] - total_attack_rows

    final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True
    )
    final_data.to_csv(output_file, index=False)

    print(f'\nNumero di righe di attacchi nel dataset finale: {total_attack_rows}')
    print(f'Numero di righe benigne nel dataset finale: {total_good_rows}')
    print(f'Numero totale di righe nel dataset finale: {final_data.shape[0]}')

    print('Dataset finale creato!\n')


directory = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_binary'
num_rows = 1000

merge_files(directory, num_rows)