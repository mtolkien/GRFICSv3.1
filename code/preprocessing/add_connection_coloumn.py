import csv
import os


def load_unique_connections(txt_file):
    unique_connections = set()
    with open(txt_file, mode='r') as file:
        for line in file:
            source_ip, destination_ip = line.strip().split(', ')
            connection = tuple(sorted([source_ip, destination_ip]))
            unique_connections.add(connection)
    return unique_connections


def determine_attack_category(filename, directory_path):
    """
    Determine the attack category based on the directory path as it is.
    """
    # Check against the exact strings
    if 'Flooding attack' in directory_path:
        return "Denial of Service"
    elif 'Port Scan' in directory_path or 'OS Scan' in directory_path or 'Host Discovery' in directory_path:
        return "Network Scanning"
    elif 'OpenVAS_scan' in filename:
        return "Vulnerability Scanning"
    else:
        return "Benign"  # Default category


def add_connection_column(csv_input_file, csv_output_file, unique_connections, attack_category, process_type):
    with open(csv_input_file, mode='r', newline='') as csvfile_input:
        reader = csv.DictReader(csvfile_input)
        fieldnames = reader.fieldnames + ['Type of connection']

        with open(csv_output_file, mode='w', newline='') as csvfile_output:
            writer = csv.DictWriter(csvfile_output, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                source_ip = row['Source IP'].strip()
                destination_ip = row['Destination IP'].strip()

                connection = tuple(sorted([source_ip, destination_ip]))

                # Assign the "Type of connection" value
                if process_type == 'Multiclass':
                    row['Type of connection'] = "Benign" if connection in unique_connections else attack_category
                elif process_type == 'Binary':
                    row['Type of connection'] = "0" if connection in unique_connections else "1"

                writer.writerow(row)


def process_directory(directory_path, txt_unique_connections, process_type):
    """
    Process all CSV files within the specified directory and subdirectories to add the "Type of connection" column.

    :param directory_path: Path to the main directory containing the CSV files.
    :param txt_unique_connections: Path to the file containing the unique connections.
    :param process_type: Process type ('Multiclass' or 'Binary').
    """
    unique_connections = load_unique_connections(txt_unique_connections)

    # Iterate through all files in the directory and subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                csv_input_file = os.path.join(root, file)
                csv_output_file = os.path.join(root, file.replace('.csv', f'_{process_type.lower()}.csv'))

                # Determine attack category based on directory structure
                attack_category = determine_attack_category(root, csv_input_file)

                add_connection_column(csv_input_file, csv_output_file, unique_connections, attack_category, process_type)
                os.remove(csv_input_file)
                print(f"Processed file: {csv_input_file} into {csv_output_file}\n")


# Execute the script by specifying the directory containing the CSV files and the file with unique connections
process_directory('/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv',
                  '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv/connessioni_uniche.txt', process_type='Binary')
