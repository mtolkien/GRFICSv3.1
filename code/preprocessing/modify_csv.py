import os
import pandas as pd

def modify_csv_files(directory, replacement_string):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            if 'Type of Connection' in df.columns:
                df['Type of connection'] = df['Type of Connection'].apply(
                    lambda x: replacement_string if x != 'Benign' else x
                )
                print('fatto')

                # Salva il CSV modificato
                df.to_csv(file_path, index=False)


directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv/csv con multiclasse da sistemare/Multiple Hosts/Host Discovery/PA'
replacement_string = 'Host Discovery'
modify_csv_files(directory_path, replacement_string)
