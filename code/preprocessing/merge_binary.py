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

def merge_files(directory_path, num_rows, benign_file_path, output_file, chunk_size=10000):
    # Remove the output file if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    first_write = True
    total_attack_rows = 0

    # Process each CSV file in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and os.path.join(root, file) != benign_file_path:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                print(f"Processing: {file_name}")

                filtered_rows = get_filtered_rows(file_path, num_rows, chunk_size)

                if not filtered_rows.empty:
                    filtered_rows.to_csv(output_file, mode='a', header=first_write, index=False)
                    first_write = False
                    total_attack_rows += len(filtered_rows)

    # Process the benign file to match the total number of attack rows
    if os.path.exists(benign_file_path):
        print(f"Processing: {os.path.basename(benign_file_path)}")
        benign_filtered_rows = []

        for chunk in pd.read_csv(benign_file_path, chunksize=chunk_size):
            benign_filtered_rows.append(chunk)
            if sum(len(f) for f in benign_filtered_rows) >= total_attack_rows:
                break

        final_benign_filtered = pd.concat(benign_filtered_rows, ignore_index=True)

        if not final_benign_filtered.empty:
            final_benign_filtered.sample(n=total_attack_rows, random_state=1).to_csv(output_file, mode='a', header=first_write, index=False)

    # Read the final dataset
    final_data = pd.read_csv(output_file)
    total_good_rows = final_data.shape[0] - total_attack_rows

    # Final shuffle of the dataset
    final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True)
    final_data.to_csv(output_file, index=False)

    print(f'\nNumber of attack rows in the final dataset: {total_attack_rows}')
    print(f'Number of benign rows in the final dataset: {total_good_rows}')
    print(f'Total number of rows in the final dataset: {final_data.shape[0]}')

    print('Final dataset created!\n')

directory = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_binary'
num_rows = 1000
benign_file_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_binary/idle.csv'
output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Dataset_Binary.csv'

merge_files(directory, num_rows, benign_file_path, output_file)