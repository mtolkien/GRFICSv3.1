import os
import subprocess
import pandas as pd

def map_protocol_to_number(protocol):
    """
    Mappa il protocollo da una stringa a un numero personalizzato.

    :param protocol: Nome del protocollo (es. 'TCP', 'UDP').
    :return: Numero corrispondente al protocollo.
    """
    protocol_mapping = {
        'TCP': 1,
        'UDP': 2,
        'ICMP': 3,
        'HTTP': 4,
        'HTTPS': 5,
        'DNS': 6,
        'DHCP': 7,
        'ARP': 8,
        'TLS': 9,
        'FTP': 10,
        'SSH': 11,
        'SMTP': 12,
        'SNMP': 13,
        'Modbus': 14,
        'SMB': 15,
    }

    return protocol_mapping.get(protocol, 0)


def preprocess_frame_time_delta(df):
    """
    Elabora la colonna 'frame.time_delta' per calcolare la frequenza dei pacchetti.

    :param df: DataFrame contenente il dataset con la colonna 'frame.time_delta'.
    :return: DataFrame aggiornato con la frequenza.
    """
    if 'frame.time_delta' in df.columns:
        df['frame.time_delta'] = pd.to_numeric(df['frame.time_delta'], errors='coerce')
        df['Packet Frequency'] = 1 / df['frame.time_delta'].replace(0, pd.NA)  # Calcola la frequenza
        df.drop(columns=['frame.time_delta'], inplace=True)
    return df


def process_pcapng(input_file, output_file):
    """
    Esegue il comando tshark per elaborare un file pcapng e salvare i risultati in formato CSV.

    :param input_file: Percorso del file pcapng da elaborare.
    :param output_file: Percorso del file CSV di output.
    """
    command = [
        "tshark",
        "-r", input_file,
        "-T", "fields",
        "-e", "frame.time_delta",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "_ws.col.Protocol",  # Campo del protocollo testuale, non numerico
        "-e", "frame.len",
        "-e", "ip.ttl",
        "-e", "ip.len",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "tcp.seq",
        "-e", "tcp.ack",
        "-e", "tcp.flags.syn",
        "-e", "tcp.flags.ack",
        "-e", "tcp.flags.fin",
        "-e", "tcp.flags.reset",
        "-e", "tcp.flags.push",
        "-e", "tcp.flags.urg",
        "-E", "header=y",
        "-E", "separator=;",
    ]

    with open(output_file, 'w') as outfile:
        process = subprocess.Popen(command, stdout=outfile, stderr=subprocess.PIPE)
        _, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Errore durante l'elaborazione di {input_file}: {stderr.decode('utf-8')}")
        else:
            print(f"Elaborazione completata: {output_file}")
            rename_and_modify_csv(output_file, custom_labels)

        try:
            os.remove(input_file)
            print(f"File .pcapng eliminato: {input_file}\n")
        except Exception as e:
            print(f"Errore durante l'eliminazione del file {input_file}: {e}\n")


def rename_and_modify_csv(output_file, custom_labels):
    """
    Rinomina le etichette di un file CSV esistente utilizzando le etichette personalizzate.

    :param output_file: Percorso del file CSV da modificare.
    :param custom_labels: Lista di etichette personalizzate.
    """
    try:
        # Carica il file CSV in un DataFrame di pandas
        df = pd.read_csv(output_file, sep=';', low_memory=False)

        # Sostituisci le etichette delle colonne con quelle personalizzate
        df.columns = custom_labels

        # Elabora 'frame.time_delta' per calcolare la frequenza
        df = preprocess_frame_time_delta(df)

        # Converte il protocollo umano in numero
        df['Protocol'] = df['Protocol'].apply(map_protocol_to_number)

        # Salva il DataFrame modificato nel file CSV
        df.to_csv(output_file, index=False)
        print(f"Intestazioni del CSV aggiornate per: {output_file}\n")
    except Exception as e:
        print(f"Errore durante la modifica delle etichette per {output_file}: {e}\n")


def process_folder(folder_path):
    """
    Cerca ed elabora tutti i file pcapng all'interno della cartella specificata e delle sottocartelle.

    :param folder_path: Percorso della cartella principale da elaborare.
    """
    # Cammina attraverso la cartella e tutte le sottocartelle
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Considera solo i file con estensione .pcapng
            if file.endswith(".pcapng"):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, file.replace(".pcapng", ".csv"))

                # Elabora il file pcapng
                process_pcapng(input_file, output_file)


custom_labels = [
    "Packet Frequency", "Source IP", "Destination IP", "Protocol", 
    "Frame Length", "TTL", "IP Length", "Source Port", "Destination Port",
    "TCP Sequence Number", "TCP Acknowledgment Number", "SYN Flag", "ACK Flag",
    "FIN Flag", "RST Flag", "PSH Flag", "URG Flag"
]


# Avvia il processo per l'intera cartellag
process_folder("/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/pcapng")
