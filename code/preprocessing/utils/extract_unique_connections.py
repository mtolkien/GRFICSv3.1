import csv
from collections import defaultdict

def extract_unique_connection_with_count(file_csv, file_txt):
    connessioni_count = defaultdict(int)

    with open(file_csv, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source_ip = row['Source IP'].strip()
            destination_ip = row['Destination IP'].strip()

            connessione = tuple(sorted([source_ip, destination_ip]))
            connessioni_count[connessione] += 1

    with open(file_txt, mode='w', newline='') as outputfile:
        for connessione, count in sorted(connessioni_count.items()):
            outputfile.write(f"{connessione[0]}, {connessione[1]}: {count}\n")

extract_unique_connection_with_count(
    '/run/media/alessandro/TOSHIBA EXT/CIC2017/benign/Monday-WorkingHours-cleared.csv',
    '/run/media/alessandro/TOSHIBA EXT/CIC2017/benign/connessioni_uniche.txt'
)
