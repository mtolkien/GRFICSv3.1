import os
import pandas as pd


def get_file_categories(file_path, chunk_size=30000):
    categories = set()
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        categories.update(chunk['Type of connection'].unique())
    return list(categories)


def process_category(file_path, category, num_rows_per_category, exclude_df, chunk_size=10000):
    sampled_rows = pd.DataFrame()
    total_rows = 0

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        category_filtered = chunk[chunk['Type of connection'] == category]

        if not category_filtered.empty:
            # Filtro per escludere righe già presenti nel DataFrame di esclusione
            merged = category_filtered.merge(exclude_df, how='left', indicator=True)
            category_filtered = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

            sampled_rows = pd.concat([sampled_rows, category_filtered], ignore_index=True)
            total_rows += len(category_filtered)

        # Se hai raggiunto o superato il numero richiesto di righe, interrompi
        if total_rows >= num_rows_per_category:
            break

    if not sampled_rows.empty:
        return sampled_rows.sample(n=min(total_rows, num_rows_per_category), random_state=1)
    return pd.DataFrame()


def merge_files(directory_path, num_rows_per_category, benign_file_path, exclude_file_path, output_file,
                chunk_size=10000):
    if os.path.exists(output_file):
        os.remove(output_file)

    # Leggi il CSV di esclusione in un DataFrame
    exclude_df = pd.read_csv(exclude_file_path)

    categories_found = set()

    # Trova tutte le categorie presenti nei file CSV
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and os.path.join(root, file) != benign_file_path:
                file_path = os.path.join(root, file)
                categories_found.update(get_file_categories(file_path))

    categories_found.discard('Benign')

    print(f"Categorie di attacco trovate: {categories_found}")

    for category in categories_found:
        category_rows_sampled = pd.DataFrame()

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.csv') and os.path.join(root, file) != benign_file_path:
                    file_path = os.path.join(root, file)

                    sampled_rows = process_category(file_path, category, num_rows_per_category, exclude_df, chunk_size)
                    if not sampled_rows.empty:
                        sampled_rows['Type of connection'] = category
                        category_rows_sampled = pd.concat([category_rows_sampled, sampled_rows], ignore_index=True)

        if not category_rows_sampled.empty:
            final_sampled_rows = category_rows_sampled.sample(n=min(len(category_rows_sampled), num_rows_per_category),
                                                              random_state=1)
            final_sampled_rows.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

    # Processa il file benigno
    if os.path.exists(benign_file_path):
        print(f"Processing: {os.path.basename(benign_file_path)}")
        idle_filtered_rows = pd.DataFrame()
        total_idle_rows = 0

        for chunk in pd.read_csv(benign_file_path, chunksize=chunk_size):
            idle_filtered = chunk[chunk['Type of connection'] == 'Benign']
            idle_filtered_merged = idle_filtered.merge(exclude_df, how='left', indicator=True)
            idle_filtered = idle_filtered_merged[idle_filtered_merged['_merge'] == 'left_only'].drop(columns=['_merge'])
            idle_filtered_rows = pd.concat([idle_filtered_rows, idle_filtered], ignore_index=True)
            total_idle_rows += len(idle_filtered)

            if total_idle_rows >= num_rows_per_category:
                break

        final_idle_filtered = idle_filtered_rows.sample(n=min(len(idle_filtered_rows), num_rows_per_category),
                                                        random_state=1)
        final_idle_filtered['Type of connection'] = 'Benign'
        final_idle_filtered.to_csv(output_file, mode='a', header=False, index=False)

    # Mescola e salva il file finale
    final_data = pd.read_csv(output_file)
    final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True)
    final_data.to_csv(output_file, index=False)

    print(f'Numero totale di righe nel dataset finale: {final_data.shape[0]}')

    # Mostra il conteggio delle righe per ogni categoria
    category_counts = final_data['Type of connection'].value_counts()
    for category, count in category_counts.items():
        print(f'Numero di righe per la categoria "{category}": {count}')

    print('Dataset finale creato!\n')


# Esempio di utilizzo
directory = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/dataset mio/csv with connections_multiclass'
num_rows_per_category = 30000
benign_file_path = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/dataset mio/csv with connections_multiclass/idle.csv'
exclude_file_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/4 attacchi + 1 benign/Dataset_Multiclass.csv'
output_file = '/home/alessandro/Scrivania/Dataset_Multiclass_mio2.csv'

merge_files(directory, num_rows_per_category, benign_file_path, exclude_file_path, output_file)
