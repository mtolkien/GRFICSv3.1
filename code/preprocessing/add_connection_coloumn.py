import os
import csv
import pandas as pd


def load_unique_connections(txt_file):
    """
    Carica le connessioni uniche da un file di testo.
    """
    unique_connections = set()
    with open(txt_file, mode='r') as file:
        for line in file:
            source_ip, destination_ip = line.strip().split(', ')
            connection = tuple(sorted([source_ip, destination_ip]))
            unique_connections.add(connection)
    return unique_connections


def determine_attack_category(filename, directory_path):
    """
    Determina la categoria di attacco in base alla struttura della directory o al nome del file.
    """
    if 'Flooding attack' in directory_path:
        return "Denial of Service"
    elif 'Port scan' in directory_path or 'OS scan' in directory_path or 'Host Discovery' in directory_path:
        return "Network Scanning"
    elif 'OpenVAS_scan' in filename:
        return "Vulnerability Scanning"
    elif 'Modbus' in directory_path:
        return "Modbus Attack"
    else:
        return "Benign"


def add_connection_column(df, unique_connections, attack_category, process_type):
    """
    Aggiunge la colonna "Type of connection" al DataFrame in base alle connessioni uniche.
    """
    df['Type of connection'] = ""

    for i, row in df.iterrows():
        source_ip = row['Source IP'].strip()
        destination_ip = row['Destination IP'].strip()

        connection = tuple(sorted([source_ip, destination_ip]))

        # Assegna il valore corretto alla colonna "Type of connection"
        if process_type == 'Multiclass':
            df.at[i, 'Type of connection'] = "Benign" if connection in unique_connections else attack_category
        elif process_type == 'Binary':
            df.at[i, 'Type of connection'] = "0" if connection in unique_connections else "1"


def process_directory(input_directory_path, output_directory_path, txt_unique_connections, process_type):
    """
    Elabora tutti i file CSV nella directory di input aggiungendo la colonna "Type of connection" e salva
    i file modificati nella directory di output mantenendo la stessa struttura delle directory.

    :param input_directory_path: Path della directory dei file CSV di input.
    :param output_directory_path: Path della directory in cui salvare i file CSV di output.
    :param txt_unique_connections: Path del file con le connessioni uniche.
    :param process_type: Tipo di processo ('Multiclass' o 'Binary').
    """
    unique_connections = load_unique_connections(txt_unique_connections)

    output_directory_path = f"{output_directory_path}_{process_type.lower()}"

    # Itera attraverso tutti i file CSV nella directory
    for root, dirs, files in os.walk(input_directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                # Leggi il file CSV
                df = pd.read_csv(file_path, low_memory=False)
                file_name = os.path.basename(file_path)

                print(f'Sto lavorando su questo file: {file_name}')

                # Determina la categoria di attacco
                attack_category = determine_attack_category(file, root)

                # Aggiungi la colonna "Type of connection"
                add_connection_column(df, unique_connections, attack_category, process_type)

                # Crea la directory di output mantenendo la struttura delle directory di input
                output_dir = os.path.join(output_directory_path, os.path.relpath(root, input_directory_path))
                os.makedirs(output_dir, exist_ok=True)

                # Salva il file CSV modificato
                output_file_path = os.path.join(output_dir, file_name)
                df.to_csv(output_file_path, index=False)
                print(f"File salvato in: {output_file_path}\n")


input_directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv after cleaning'
output_directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv with connections'
txt_unique_connections = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/connessioni_uniche.txt'
process_type = 'Multiclass'

process_directory(input_directory_path, output_directory_path, txt_unique_connections, process_type)