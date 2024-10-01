import pyshark
import pandas as pd
from tqdm import tqdm

# Leggi il file PCAPNG
capture = pyshark.FileCapture('/home/alessandro/Scrivania/PHS_flood_chemicalplant_10.pcapng')

# Conta il numero totale di pacchetti per visualizzare meglio il progresso
total_packets = sum(1 for _ in capture)  # Conta il numero totale di pacchetti

# Riapri la cattura per analizzare (perché l'iterazione precedente ha esaurito i pacchetti)
capture.close()
capture = pyshark.FileCapture('/home/alessandro/Scrivania/PHS_flood_chemicalplant_10.pcapng')

# Crea un elenco per memorizzare i dati
data = []

# Estrazione delle feature da ogni pacchetto con tqdm per il progresso
for packet in tqdm(capture, total=total_packets, desc="Elaborazione pacchetti"):
    if 'IP' in packet and 'TCP' in packet:
        try:
            # Estrai le feature chiave
            timestamp = packet.sniff_time
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            protocol = packet.highest_layer
            length = packet.length

            # Estrai le flag TCP
            tcp_flags = packet.tcp.flags_str  # Stringa delle flag (es: S, A, P)
            syn_flag = 1 if 'S' in tcp_flags else 0
            ack_flag = 1 if 'A' in tcp_flags else 0
            fin_flag = 1 if 'F' in tcp_flags else 0
            rst_flag = 1 if 'R' in tcp_flags else 0
            psh_flag = 1 if 'P' in tcp_flags else 0
            urg_flag = 1 if 'U' in tcp_flags else 0

            info = {
                'Timestamp': timestamp,
                'Source IP': src_ip,
                'Destination IP': dst_ip,
                'Protocol': protocol,
                'Length': length,
                'TCP SYN': syn_flag,
                'TCP ACK': ack_flag,
                'TCP FIN': fin_flag,
                'TCP RST': rst_flag,
                'TCP PSH': psh_flag,
                'TCP URG': urg_flag
            }
            data.append(info)
        except AttributeError:
            pass

# Converti in DataFrame per analisi successive
df = pd.DataFrame(data)

# Salva il dataset come file CSV
df.to_csv('/home/alessandro/Scrivania/dataset_with_tcp_flags.csv', index=False)

print(df.head())
