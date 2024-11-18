import os
import pandas as pd

def load_unique_connections(txt_file):
    unique_connections = set()
    with open(txt_file, mode='r') as file:
        for line in file:
            connection_part = line.split(':')[0]
            source_ip, destination_ip = connection_part.strip().split(', ')

            connection = tuple(sorted([source_ip, destination_ip]))
            unique_connections.add(connection)

    return unique_connections

def determine_attack_category(filename, directory_path):
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
    df['Type of connection'] = ""

    for i, row in df.iterrows():
        source_ip = row['Source IP'].strip()
        destination_ip = row['Destination IP'].strip()

        connection = tuple(sorted([source_ip, destination_ip]))

        if process_type == 'Multiclass':
            df.at[i, 'Type of connection'] = "Benign" if connection in unique_connections else attack_category
        elif process_type == 'Binary':
            df.at[i, 'Type of connection'] = "0" if connection in unique_connections else "1"

def process_directory(input_directory_path, output_directory_path, txt_unique_connections, process_type):
    unique_connections = load_unique_connections(txt_unique_connections)

    output_directory_path = f"{output_directory_path}_{process_type.lower()}"

    for root, dirs, files in os.walk(input_directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                df = pd.read_csv(file_path, low_memory=False)
                file_name = os.path.basename(file_path)

                print(f'Processing this file: {file_name}')

                attack_category = determine_attack_category(file, root)

                add_connection_column(df, unique_connections, attack_category, process_type)

                output_dir = os.path.join(output_directory_path, os.path.relpath(root, input_directory_path))
                os.makedirs(output_dir, exist_ok=True)

                output_file_path = os.path.join(output_dir, file_name)
                df.to_csv(output_file_path, index=False)
                print(f"File saved in: {output_file_path}\n")

input_directory_path = '/run/media/alessandro/TOSHIBA EXT/CIC2017/benign/cleared'
output_directory_path = '/run/media/alessandro/TOSHIBA EXT/CIC2017/benign'
txt_unique_connections = '/run/media/alessandro/TOSHIBA EXT/CIC2017/benign/connessioni_uniche.txt'
process_type = 'Multiclass'

process_directory(input_directory_path, output_directory_path, txt_unique_connections, process_type)