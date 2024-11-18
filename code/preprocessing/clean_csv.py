import os
import pandas as pd
import numpy as np

def clean_csv(input_directory_path, output_directory_path):
    for root, dirs, files in os.walk(input_directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                df = pd.read_csv(file_path, low_memory=False)
                file_name = os.path.basename(file_path)

                print(f'Processing this file: {file_name}')
                original_row_count = df.shape[0]

                # Handle missing values based on the column
                df = df[df['Protocol'].astype(str).str.replace('.', '', regex=False).str.isnumeric()]
                df['Protocol'] = df['Protocol'].astype(np.int32)

                df['Packet Frequency'] = df['Packet Frequency'].fillna(df['Packet Frequency'].mean()).astype(np.float32)  # Mean for Packet Frequency

                df = df[df['TTL'].astype(str).str.replace('.', '', regex=False).str.isnumeric()]
                df['TTL'] = pd.to_numeric(df['TTL'], errors='coerce').fillna(64).astype(np.int32)

                df['Source Port'] = df['Source Port'].fillna(0).astype(np.int32)
                df['Destination Port'] = df['Destination Port'].fillna(0).astype(np.int32)
                df['TCP Sequence Number'] = df['TCP Sequence Number'].fillna(0).astype(np.int32)  # Safe value 0
                df['TCP Acknowledgment Number'] = df['TCP Acknowledgment Number'].fillna(0).astype(np.int32)

                df['Frame Length'] = df['Frame Length'].fillna(0).astype(np.int32)
                df['IP Length'] = df['IP Length'].fillna(0).astype(np.int32)

                # Convert flag columns to binary
                flag_columns = ['SYN Flag', 'ACK Flag', 'FIN Flag', 'RST Flag', 'PSH Flag', 'URG Flag']
                for flag in flag_columns:
                    df[flag] = df[flag].map({True: 1, False: 0}).fillna(0).astype(np.int32)

                # Remove rows with null values in IP columns
                df.dropna(subset=['Source IP', 'Destination IP'], inplace=True)

                deleted_row_count = original_row_count - df.shape[0]
                print(f"Deleted rows: {deleted_row_count}\n")

                output_dir = os.path.join(output_directory_path, os.path.relpath(root, input_directory_path))
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, file_name)
                df.to_csv(output_file_path, index=False)

input_directory_path = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/CIC2017/pcap/friday csv'
output_directory_path = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/CIC2017/pcap/friday csv cleared'

clean_csv(input_directory_path, output_directory_path)