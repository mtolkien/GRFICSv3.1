import os
import pandas as pd

def get_filtered_rows(file_path, n):
    df = pd.read_csv(file_path)

    # Filtra le righe che non sono 'Benign' o '0'
    filtered_df = df[(df['Type of connection'] != 'Benign') & (df['Type of connection'] != '0')]

    if len(filtered_df) >= n:
        return filtered_df.sample(n)
    else:
        return filtered_df


def merge_files(directory_path, n):
    all_rows = []
    idle_file = os.path.join(directory_path, 'idle.csv')

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and file != 'idle.csv':
                file_path = os.path.join(root, file)
                filtered_rows = get_filtered_rows(file_path, n)
                all_rows.append(filtered_rows)

    # Estrae n righe casuali anche da idle.csv
    idle_df = pd.read_csv(idle_file)
    idle_sample = idle_df.sample(n)
    all_rows.append(idle_sample)

    final_df = pd.concat(all_rows, ignore_index=True)
    final_df = final_df.sample(frac=1).reset_index(drop=True)

    # Salva il DataFrame finale in un nuovo file CSV
    final_df.to_csv('/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/merged_output.csv', index=False)

directory = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_binary'
num_rows = 131000
merge_files(directory, num_rows)