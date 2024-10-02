import os
import pandas as pd

def remove_empty_rows_in_csv(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)

                df = pd.read_csv(file_path)

                initial_row_count = len(df)
                df = df.dropna(subset=['Source IP', 'Destination IP'])

                # Riempie le altre colonne con "N/A" se "Source IP" o "Destination IP" sono presenti
                mask = df['Source IP'].notna() | df['Destination IP'].notna()
                df.loc[mask] = df.loc[mask].fillna('N/A')

                # Verifica se ci sono state modifiche
                if len(df) < initial_row_count:
                    df.to_csv(file_path, index=False)
                    print(f"File modificato: {file_path}, righe rimosse: {initial_row_count - len(df)}")
                else:
                    print(f"Nessuna riga vuota trovata in: {file_path}")


# Utilizzo
directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv'
remove_empty_rows_in_csv(directory_path)
