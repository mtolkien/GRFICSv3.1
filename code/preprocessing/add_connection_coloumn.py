import csv
import os
import glob


def load_unique_connections(txt_file):
    unique_connections = set()

    # Leggi il file input contenente le coppie di connessioni uniche
    with open(txt_file, mode='r') as file:
        for line in file:
            # Estrai Source IP e Destination IP
            source_ip, destination_ip = line.strip().split(', ')
            connection = tuple(sorted([source_ip, destination_ip]))
            unique_connections.add(connection)

    return unique_connections


def extract_attack_label(csv_filename):
    # Estrai il nome del file senza il percorso
    base_name = os.path.basename(csv_filename)
    # Ottengo l'etichetta dell'attacco
    attack_label = base_name.split('_')[0].lower()
    return attack_label


def add_connection_column(csv_input_file, csv_output_file, unique_connections, attack_label, process_type):
    # Leggi il file CSV in input e creane uno nuovo con una colonna aggiuntiva "Type of connection"
    with open(csv_input_file, mode='r', newline='') as csvfile_input:
        reader = csv.DictReader(csvfile_input)
        # Aggiungi la nuova colonna
        fieldnames = reader.fieldnames + ['Type of connection']

        with open(csv_output_file, mode='w', newline='') as csvfile_output:
            writer = csv.DictWriter(csvfile_output, fieldnames=fieldnames)
            writer.writeheader()

            # Per ciascuna riga del file di input CSV, controlla se la connessione è legittima
            for row in reader:
                source_ip = row['Source IP'].strip()
                destination_ip = row['Destination IP'].strip()

                connection = tuple(sorted([source_ip, destination_ip]))

                # Assegna il valore per "Type of connection"
                if process_type == 'Multiclass':
                    row['Type of connection'] = "Benign" if connection in unique_connections else attack_label
                elif process_type == 'Binary':
                    row['Type of connection'] = "0" if connection in unique_connections else "1"

                writer.writerow(row)


def process_directory(directory_path, txt_unique_connections, process_type):
    """
    Cerca ed elabora tutti i file CSV all'interno della cartella specificata e delle sottocartelle.

    :param directory_path: Percorso della cartella principale da elaborare.
    :param txt_unique_connections: Percorso del file contenente le connessioni uniche.
    :param process_type: Tipo di processo ('Multiclass' o 'Binary').
    """
    # Carica le coppie di connessioni uniche una volta sola
    unique_connections = load_unique_connections(txt_unique_connections)

    # Cammina attraverso la cartella e tutte le sottocartelle
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Considera solo i file con estensione .csv
            if file.endswith(".csv"):
                csv_input_file = os.path.join(root, file)
                csv_output_file = os.path.join(root, file.replace('.csv', '_' + process_type.lower() + '.csv'))

                attack_label = extract_attack_label(csv_input_file)
                add_connection_column(csv_input_file, csv_output_file, unique_connections, attack_label, process_type)
                os.remove(csv_input_file)
                print(f"File originale eliminato: {csv_input_file}")


# Esegui lo script specificando la directory contenente i CSV e il file delle connessioni uniche
process_directory('/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv',
                  '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv/connessioni_uniche.txt', process_type='Binary')
# DA FARE MULTICLASS
