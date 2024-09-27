import subprocess
import pandas as pd


def extract_unique_connections(input_file):
    """
    Estrae le coppie uniche di connessioni (source IP e destination IP) da un file pcapng
    e le salva in un insieme.

    :param input_file: Il file pcapng da analizzare.
    :return: Un insieme di tuple contenenti le coppie uniche di connessioni (source IP, destination IP).
    """
    # Comando tshark per estrarre solo source IP e destination IP
    command = [
        "tshark",
        "-r", input_file,
        "-T", "fields",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-E", "separator=;"
    ]

    # Esegui il comando tshark e cattura l'output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Errore durante l'elaborazione di {input_file}: {stderr}")
        return None

    # Insieme per contenere le coppie uniche di connessioni
    unique_connections = set()

    # Processa l'output di tshark riga per riga
    for line in stdout.splitlines():
        fields = line.split(';')
        if len(fields) == 2:
            src_ip = fields[0].strip()
            dst_ip = fields[1].strip()

            # Aggiungi la coppia (source IP, destination IP) all'insieme
            if src_ip and dst_ip:
                unique_connections.add((src_ip, dst_ip))

    return unique_connections


def compare_with_csv(unique_connections, input_csv, output_csv):
    """
    Confronta le coppie uniche di connessioni con quelle presenti in un file CSV e aggiunge una colonna binaria
    che indica se la connessione è lecita (0) o non lecita (1).

    :param unique_connections: Insieme delle coppie uniche di connessioni.
    :param input_csv: Il file CSV da confrontare.
    :param output_csv: Il file CSV risultante con la colonna aggiuntiva.
    """
    try:
        # Carica il CSV in un DataFrame di pandas
        df = pd.read_csv(input_csv)

        # Assicurati che il file CSV abbia colonne per IP sorgente e destinazione
        if 'Source IP' not in df.columns or 'Destination IP' not in df.columns:
            print("Errore: il file CSV deve contenere colonne 'Source IP' e 'Destination IP'.")
            return

        # Crea una colonna binaria 'is_legit' che ha valore 0 se la coppia è presente nell'insieme, altrimenti 1
        df['is_legit'] = df.apply(
            lambda row: 0 if (row['Source IP'], row['Destination IP']) in unique_connections else 1, axis=1)

        # Salva il DataFrame aggiornato nel file CSV di output
        df.to_csv(output_csv, index=False)
        print(f"Confronto completato. Risultato salvato in: {output_csv}")

    except Exception as e:
        print(f"Errore durante il confronto con il file CSV: {e}")


# Percorso del file pcapng da analizzare (comportamento normale)
pcapng_file = "path/to/your/normal_behavior.pcapng"  # Sostituisci con il percorso del tuo file pcapng

# Percorso del file CSV da confrontare
input_csv = "path/to/your/input.csv"  # Sostituisci con il percorso del tuo file CSV

# Percorso del file CSV risultante
output_csv = "output_with_legit_column.csv"  # Sostituisci con il percorso desiderato per il file CSV di output

# Estrai le coppie uniche di connessioni dal file pcapng
unique_connections = extract_unique_connections(pcapng_file)

if unique_connections is not None:
    # Confronta le coppie uniche con il file CSV e aggiungi la colonna binaria
    compare_with_csv(unique_connections, input_csv, output_csv)
