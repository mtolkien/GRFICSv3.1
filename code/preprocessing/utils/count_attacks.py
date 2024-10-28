import os
import pandas as pd

def count_attacks(directory, dataset_type):
    output_file = "/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/count_attacks_total.txt"

    if dataset_type == 'Binary':
        benign_value = 0
    else:
        benign_value = 'Benign'

    with open(output_file, "w") as f_output:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".csv"):
                    csv_file_path = os.path.join(root, file)
                    df = pd.read_csv(csv_file_path)
                    file_name = os.path.basename(csv_file_path)
                    print(f"Check sul file: {file_name}")

                    if 'Type of connection' in df.columns:
                        # Se il dataset è multiclasse, trattiamo 'Type of connection' come stringa
                        if dataset_type == 'Multiclass':
                            df['Type of connection'] = df['Type of connection'].astype(str).str.strip()

                        attacks_count = df[df['Type of connection'] != benign_value].shape[0]

                        f_output.write(f"File: {file_name} -> Righe di attacchi: {attacks_count}\n")
                    else:
                        f_output.write(f"File: {file_name} -> Colonna 'Type of connection' non trovata\n")

directory = "/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse"
count_attacks(directory, "Multiclass")