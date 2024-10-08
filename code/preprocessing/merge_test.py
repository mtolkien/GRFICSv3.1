import os
import pandas as pd

def get_file_categories(file_path, chunk_size=30000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    categories = set()
    for chunk in chunks:
        categories.update(chunk['Type of connection'].unique())
    return list(categories)


def get_filtered_rows(file_path, rows_per_file, category, process_type, chunk_size=10000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    filtered_rows = []
    check = 0 if process_type == 'Binary' else 'Benign'

    for chunk in chunks:
        if process_type == 'Multiclass':
            category_filtered = chunk[chunk['Type of connection'] == category]
        elif process_type == 'Binary':
            category_filtered = chunk[chunk['Type of connection'] != check]

        filtered_rows.append(category_filtered)
        # Controlla se sono state accumulate abbastanza righe
        if sum(len(rows) for rows in filtered_rows) >= rows_per_file:
            break

    combined_rows = pd.concat(filtered_rows, ignore_index=True) if filtered_rows else pd.DataFrame()

    if len(combined_rows) < rows_per_file:
        return combined_rows
    else:
        return combined_rows.sample(n=rows_per_file, random_state=1)


def merge_files(directory_path, num_rows, process_type, chunk_size=10000):
    output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Dataset_' + process_type + '.csv'

    if os.path.exists(output_file):
        os.remove(output_file)

    first_write = True
    total_attack_rows = 0
    remaining_rows = 0

    if process_type == 'Multiclass':
        total_files_per_category = {
            'Denial of Service': 0,
            'Network Scanning': 0,
            'Vulnerability Scanning': 0,
            'Modbus Attack': 0
        }

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.csv') and file != 'idle.csv':
                    file_path = os.path.join(root, file)
                    categories = get_file_categories(file_path)
                    for category in categories:
                        if category in total_files_per_category:
                            total_files_per_category[category] += 1

        print(f"Numero di file per categoria: {total_files_per_category}")

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv') and file != 'idle.csv':
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                print(f"Processing: {file_name}")

                if process_type == 'Multiclass':
                    categories = get_file_categories(file_path)
                    for category in categories:
                        if category in total_files_per_category and total_files_per_category[category] > 0:
                            rows_per_file = num_rows // total_files_per_category[category]

                            # Filtra le righe dal file corrente
                            filtered_rows = get_filtered_rows(file_path, rows_per_file, category, process_type,
                                                              chunk_size)

                            # Se non ci sono abbastanza righe nel file corrente
                            if len(filtered_rows) < rows_per_file:
                                remaining_rows_needed = rows_per_file - len(filtered_rows)

                                # Cerca di riempire le righe rimanenti con altri file della stessa categoria
                                for other_file in files:
                                    if other_file != file and other_file.endswith('.csv') and other_file != 'idle.csv':
                                        other_file_path = os.path.join(root, other_file)
                                        other_filtered_rows = get_filtered_rows(other_file_path, remaining_rows_needed,
                                                                                category, process_type, chunk_size)

                                        # Aggiungi righe solo se ci sono
                                        if not other_filtered_rows.empty:
                                            filtered_rows = pd.concat([filtered_rows, other_filtered_rows],
                                                                      ignore_index=True)

                                        # Se abbiamo raggiunto il numero richiesto, esci dal ciclo
                                        if len(filtered_rows) >= rows_per_file:
                                            break

                            # Se ci sono righe sufficienti, campiona solo quelle richieste
                            if len(filtered_rows) >= rows_per_file:
                                filtered_rows = filtered_rows.sample(n=rows_per_file,
                                                                     random_state=1)  # Assicurati di prendere solo il numero richiesto

                            if not filtered_rows.empty:
                                filtered_rows.to_csv(output_file, mode='a', header=first_write, index=False)
                                first_write = False
                                total_attack_rows += len(filtered_rows)

    # Elaborazione di idle.csv per abbinare il numero totale di righe filtrate
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

    final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True)
    final_data.to_csv(output_file, index=False)

    print(f'\nNumero di righe di attacchi nel dataset finale: {total_attack_rows}')
    print(f'Numero di righe benigne nel dataset finale: {total_good_rows}')
    print(f'Numero totale di righe nel dataset finale: {final_data.shape[0]}')

    if process_type == 'Multiclass':
        category_counts = final_data['Type of connection'].value_counts()
        for category, count in category_counts.items():
            print(f'Numero di righe per la categoria "{category}": {count}')

        # Check for any category that does not meet the required number of rows
        for category in total_files_per_category.keys():
            required_rows = num_rows // len(total_files_per_category)
            if category_counts.get(category, 0) < required_rows:
                print(f"Category '{category}' has insufficient rows: {category_counts.get(category, 0)} < {required_rows}. Reprocessing...")

                # Reprocess for this specific category
                while category_counts.get(category, 0) < required_rows:
                    rows_per_file = required_rows - category_counts.get(category, 0)
                    filtered_rows = get_filtered_rows(file_path, rows_per_file, category, process_type, chunk_size)

                    if not filtered_rows.empty:
                        filtered_rows.to_csv(output_file, mode='a', header=False, index=False)
                        total_attack_rows += len(filtered_rows)
                        category_counts[category] += len(filtered_rows)

    print('Dataset finale creato!\n')


directory = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections_multiclass'
num_rows = 25000
process_type = 'Multiclass'

merge_files(directory, num_rows, process_type)