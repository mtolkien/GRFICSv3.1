import os
import pandas as pd


def remove_empty_rows_in_csv(directory):
    # Cerca tutti i file CSV all'interno della directory e delle sottocartelle
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)

                # Leggi il CSV
                df = pd.read_csv(file_path)

                # Controlla se ci sono righe con valori vuoti
                initial_row_count = len(df)
                df = df.dropna()  # Rimuove le righe con valori NaN

                # Verifica se ci sono state modifiche
                if len(df) < initial_row_count:
                    df.to_csv(file_path, index=False)
                    print(f"File modificato: {file_path}, righe rimosse: {initial_row_count - len(df)}")
                else:
                    print(f"Nessuna riga vuota trovata in: {file_path}")


# Utilizzo
directory_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/Attacks csv'
remove_empty_rows_in_csv(directory_path)
