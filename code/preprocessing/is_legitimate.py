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
    # Suddividi il nome del file in base agli underscore (_) e ottieni il primo elemento come etichetta dell'attacco
    attack_label = base_name.split('_')[0].lower()
    return attack_label


def add_is_legitimate_column(csv_input_file, csv_output_file, unique_connections, attack_label):
    # Leggi il file CSV in input e creane uno nuovo con una colonna aggiuntiva "is_legitimate"
    with open(csv_input_file, mode='r', newline='') as csvfile_input:
        reader = csv.DictReader(csvfile_input)
        # Aggiungi la nuova colonna
        fieldnames = reader.fieldnames + ['Connection']

        with open(csv_output_file, mode='w', newline='') as csvfile_output:
            writer = csv.DictWriter(csvfile_output, fieldnames=fieldnames)
            writer.writeheader()

            # Per ciascuna riga del file di input CSV, controlla se la connessione è legittima
            for row in reader:
                source_ip = row['Source IP'].strip()
                destination_ip = row['Destination IP'].strip()

                connection = tuple(sorted([source_ip, destination_ip]))

                # Cambia la logica per l'inserimento dei valori: 'Benign' o il nome dell'attacco
                row['is_legitimate'] = "Benign" if connection in unique_connections else attack_label

                writer.writerow(row)


def process_directory(directory_path, txt_unique_connections):
    # Carica le coppie di connessioni uniche una volta sola
    unique_connections = load_unique_connections(txt_unique_connections)

    # Trova tutti i file CSV nella directory specificata
    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

    # Itera su ciascun file CSV
    for csv_file in csv_files:
        # Estrai l'etichetta dell'attacco dal nome del file
        attack_label = extract_attack_label(csv_file)

        # Crea il percorso del file di output aggiungendo "_legitimate" prima dell'estensione .csv
        csv_output_file = csv_file.replace('.csv', '_with_attackstype.csv')

        print(f"Processing: {csv_file} -> {csv_output_file} with label '{attack_label}'")
        add_is_legitimate_column(csv_file, csv_output_file, unique_connections, attack_label)



# Esegui lo script specificando la directory contenente i CSV e il file delle connessioni uniche
process_directory('/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks',
                  '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks/connessioni_uniche.txt')
