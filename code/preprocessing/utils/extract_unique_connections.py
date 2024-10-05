import csv
def extract_unique_connection(file_csv, file_txt):
    connessioni_uniche = set()

    # Leggi il file CSV
    with open(file_csv, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Estrae Source IP e Destination IP
            source_ip = row['Source IP'].strip()
            destination_ip = row['Destination IP'].strip()

            # Crea una tupla ordinata per garantire l'unicità
            connessione = tuple(sorted([source_ip, destination_ip]))
            connessioni_uniche.add(connessione)

    # Salva le connessioni uniche nel file di output
    with open(file_txt, mode='w', newline='') as outputfile:
        for connessione in sorted(connessioni_uniche):
            outputfile.write(f"{connessione[0]}, {connessione[1]}\n")


connessioni_uniche = extract_unique_connection('/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv after cleaning/idle.csv',
                                                     '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/connessioni_uniche.txt')

