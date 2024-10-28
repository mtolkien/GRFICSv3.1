import os
import subprocess
import pandas as pd


def map_protocol_to_number(protocol):
    protocol_mapping = {
        'TCP': 1, 'UDP': 2, 'ICMP': 3, 'HTTP': 4,
        'HTTPS': 5, 'DNS': 6, 'DHCP': 7, 'ARP': 8,
        'TLS': 9, 'FTP': 10, 'SSH': 11, 'SMTP': 12,
        'SNMP': 13, 'Modbus/TCP': 14, 'SMB': 15,
        'POP3': 16, 'IMAP': 17, 'NTP': 18, 'BGP': 19,
        'RDP': 20, 'LDAP': 21, 'Telnet': 22, 'SIP': 23,
        'LLDP': 24, 'MPLS': 25
    }
    return protocol_mapping.get(protocol, 0)


def preprocess_frame_time_delta(df):
    if 'frame.time_delta' in df.columns:
        df['frame.time_delta'] = pd.to_numeric(df['frame.time_delta'], errors='coerce')
        df['Packet Frequency'] = 1 / df['frame.time_delta'].replace(0, pd.NA)
        df.drop(columns=['frame.time_delta'], inplace=True)
    return df


def process_pcapng(input_file, output_file, extract_sample, max_lines):
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

    line_count = 0

    with open(output_file, 'w') as outfile:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            while True:
                output = process.stdout.readline()
                if output == b"" and process.poll() is not None:
                    break
                if output:
                    outfile.write(output.decode())
                    line_count += 1
                    # Termina il campionamento se richiesto
                    if extract_sample and line_count >= max_lines:
                        break

        except Exception as e:
            print(f"Error during line reading: {e}")
        finally:
            process.kill()
            process.wait()

    # Chiama la funzione per modificare le intestazioni del CSV
    rename_and_modify_csv(output_file, custom_labels)


def rename_and_modify_csv(output_file, custom_labels):
    try:
        df = pd.read_csv(output_file, sep=',', low_memory=False)

        # Modifica le intestazioni e i protocolli
        df.columns = custom_labels
        df = preprocess_frame_time_delta(df)
        df['Protocol'] = df['Protocol'].apply(map_protocol_to_number)
        df.to_csv(output_file, index=False)
        print(f"Updated CSV headers for: {output_file}\n")

    except pd.errors.EmptyDataError:
        print(f"No data found in the file: {output_file}\n")
    except Exception as e:
        print(f"Error when editing labels for {output_file}: {e}\n")


def process_folder(input_folder_path, output_folder_path, extract_sample, max_lines):
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith(".pcap"):
                input_file = os.path.join(root, file)

                relative_path = os.path.relpath(root, input_folder_path)
                output_dir = os.path.join(output_folder_path, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                output_file = os.path.join(output_dir, file.replace(".pcap", ".csv"))

                process_pcapng(input_file, output_file, extract_sample, max_lines)


custom_labels = [
    "Packet Frequency", "Source IP", "Destination IP", "Protocol",
    "Frame Length", "TTL", "IP Length", "Source Port", "Destination Port",
    "TCP Sequence Number", "TCP Acknowledgment Number", "SYN Flag", "ACK Flag",
    "FIN Flag", "RST Flag", "PSH Flag", "URG Flag"
]

input_folder_path = "/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/CIC2017/pcap/friday"
output_folder_path = "/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/CIC2017/pcap/friday csv"
extract_sample = False
max_lines = 5000000
process_folder(input_folder_path, output_folder_path, extract_sample, max_lines)