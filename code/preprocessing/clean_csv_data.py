import os
import pandas as pd

def clean_csv(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                df = pd.read_csv(file_path, low_memory=False)

                print(f'Sto lavorando su questo file: {file_path}')
                original_row_count = df.shape[0]

                # Gestione dei valori mancanti in base alla colonna

                # Converti i valori in stringa e filtra solo quelli numerici e senza parte decimale
                df = df[df['Protocol'].astype(str).str.replace('.', '', regex=False).str.isnumeric()]
                df['Protocol'] = df['Protocol'].astype(int)

                df['Packet Frequency'] = df['Packet Frequency'].fillna(df['Packet Frequency'].mean()).astype(float)  # Media per Packet Frequency
                df['TTL'] = df['TTL'].fillna(64).astype(int)  # Valore comune per il TTL potrebbe essere 64
                df['Source Port'] = df['Source Port'].fillna(-1).astype(int)  #  -1 per porte mancanti
                df['Destination Port'] = df['Destination Port'].fillna(-1).astype(int)
                df['TCP Sequence Number'] = df['TCP Sequence Number'].fillna(0).astype(int)  #  0 come valore sicuro
                df['TCP Acknowledgment Number'] = df['TCP Acknowledgment Number'].fillna(0).astype(int)

                # Nuova gestione per Frame Length e IP Length
                df['Frame Length'] = df['Frame Length'].fillna(0).astype(int)  # Sostituisci NaN con 0, poi convertili in int
                df['IP Length'] = df['IP Length'].fillna(0).astype(int)  # Stessa cosa per IP Length

                # Conversione delle colonne dei flag in binari
                flag_columns = ['SYN Flag', 'ACK Flag', 'FIN Flag', 'RST Flag', 'PSH Flag', 'URG Flag']
                for flag in flag_columns:
                    df[flag] = df[flag].map({True: 1, False: 0}).fillna(-1).replace('', -1)

                # Rimuove righe con valori nulli nelle colonne IP
                df.dropna(subset=['Source IP', 'Destination IP'], inplace=True)

                deleted_row_count = original_row_count - df.shape[0]
                print(f"Righe eliminate: {deleted_row_count}")

                new_file_path = os.path.join(root, f"{os.path.splitext(file)[0]}_cleared.csv")
                df.to_csv(new_file_path, index=False)


# Utilizzo
directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv'
clean_csv(directory_path)
