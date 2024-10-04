import os
import subprocess
import pandas as pd


def map_protocol_to_number(protocol):
    protocol_mapping = {
        'TCP': 1, 'UDP': 2, 'ICMP': 3, 'HTTP': 4,
        'HTTPS': 5, 'DNS': 6, 'DHCP': 7, 'ARP': 8,
        'TLS': 9, 'FTP': 10, 'SSH': 11, 'SMTP': 12,
        'SNMP': 13, 'Modbus/TCP': 14, 'SMB': 15
    }
    return protocol_mapping.get(protocol, 0)


def preprocess_frame_time_delta(df):
    if 'frame.time_delta' in df.columns:
        df['frame.time_delta'] = pd.to_numeric(df['frame.time_delta'], errors='coerce')
        df['Packet Frequency'] = 1 / df['frame.time_delta'].replace(0, pd.NA)  # Calcola la frequenza
        df.drop(columns=['frame.time_delta'], inplace=True)
    return df


def process_pcapng(input_file, output_file):
    command = [
        "tshark",
        "-r", input_file,
        "-T", "fields",
        "-e", "frame.time_delta",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "_ws.col.Protocol",
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


def rename_and_modify_csv(output_file, custom_labels):
    try:
        df = pd.read_csv(output_file, sep=';', low_memory=False)
        df.columns = custom_labels
        df = preprocess_frame_time_delta(df)
        df['Protocol'] = df['Protocol'].apply(map_protocol_to_number)
        df.to_csv(output_file, index=False)
        print(f"Intestazioni del CSV aggiornate per: {output_file}\n")
    except Exception as e:
        print(f"Errore durante la modifica delle etichette per {output_file}: {e}\n")


def process_folder(input_folder_path, output_folder_path):
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith(".pcapng"):
                input_file = os.path.join(root, file)

                # Crea la struttura delle cartelle nel percorso di output
                relative_path = os.path.relpath(root, input_folder_path)
                output_dir = os.path.join(output_folder_path, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                output_file = os.path.join(output_dir, file.replace(".pcapng", ".csv"))

                process_pcapng(input_file, output_file)


custom_labels = [
    "Packet Frequency", "Source IP", "Destination IP", "Protocol",
    "Frame Length", "TTL", "IP Length", "Source Port", "Destination Port",
    "TCP Sequence Number", "TCP Acknowledgment Number", "SYN Flag", "ACK Flag",
    "FIN Flag", "RST Flag", "PSH Flag", "URG Flag"
]

input_folder_path = "/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/pcapng"
output_folder_path = "/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/csv before cleaning"

process_folder(input_folder_path, output_folder_path)
