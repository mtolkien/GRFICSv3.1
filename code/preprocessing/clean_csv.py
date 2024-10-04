import os
import pandas as pd
import numpy as np

def clean_csv(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                df = pd.read_csv(file_path, low_memory=False)
                file_name = os.path.basename(file_path)

                print(f'Sto lavorando su questo file: {file_name}\n')
                original_row_count = df.shape[0]

                # Gestione dei valori mancanti in base alla colonna

                # Converti i valori in stringa e filtra solo quelli numerici e senza parte decimale
                df = df[df['Protocol'].astype(str).str.replace('.', '', regex=False).str.isnumeric()]
                df['Protocol'] = df['Protocol'].astype(np.int32)

                df['Packet Frequency'] = df['Packet Frequency'].fillna(df['Packet Frequency'].mean()).astype(np.float32)  # Media per Packet Frequency
                df['TTL'] = df['TTL'].fillna(64).astype(np.int32)  # Valore comune per il TTL è 64
                df['Source Port'] = df['Source Port'].fillna('N/A')
                df['Destination Port'] = df['Destination Port'].fillna('N/A')
                df['TCP Sequence Number'] = df['TCP Sequence Number'].fillna(0).astype(np.int32)  # Valore sicuro 0
                df['TCP Acknowledgment Number'] = df['TCP Acknowledgment Number'].fillna(0).astype(np.int32)

                # Sostituisci NaN con 0, poi convertili in int
                df['Frame Length'] = df['Frame Length'].fillna(0).astype(np.int32)
                df['IP Length'] = df['IP Length'].fillna(0).astype(np.int32)

                # Conversione delle colonne dei flag in binari (con valori int32 e sostituzione NaN con 0)
                flag_columns = ['SYN Flag', 'ACK Flag', 'FIN Flag', 'RST Flag', 'PSH Flag', 'URG Flag']
                for flag in flag_columns:
                    df[flag] = df[flag].map({True: 1, False: 0}).fillna(0).astype(np.int32)

                # Rimuove righe con valori nulli nelle colonne IP
                df.dropna(subset=['Source IP', 'Destination IP'], inplace=True)

                deleted_row_count = original_row_count - df.shape[0]
                print(f"Righe eliminate: {deleted_row_count}\n")

                # Salva il DataFrame modificato sovrascrivendo il file originale
                df.to_csv(file_path, index=False)


directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv'
clean_csv(directory_path)
