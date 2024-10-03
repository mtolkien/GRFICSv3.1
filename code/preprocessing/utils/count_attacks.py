import os
import pandas as pd

def count_attacks(directory):
    output_file = "count_attacks_total.txt"

    with open(output_file, "w") as f_output:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".csv"):
                    csv_file_path = os.path.join(root, file)
                    df = pd.read_csv(csv_file_path)
                    file_name = os.path.basename(csv_file_path)

                    if 'Type of connection' in df.columns:
                        attacks_count = df[(df['type of connection'] != 'Benign') & (df['type of connection'] != '0')].shape[0]
                        f_output.write(f"File: {file_name} -> Righe non Benign: {attacks_count}\n")
                    else:
                        f_output.write(f"File: {file_name} -> Colonna 'Type of connection' non trovata\n")


directory = "/percorso/alla/directory"
count_attacks(directory)
