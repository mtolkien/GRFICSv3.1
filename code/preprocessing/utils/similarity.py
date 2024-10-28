import pandas as pd

def count_common_rows(file1, file2):
    # Leggi i due file CSV in DataFrame
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Unire i due DataFrame per trovare le righe in comune
    common_rows = pd.merge(df1, df2, how='inner')

    # Contare il numero di righe comuni
    common_count = common_rows.shape[0]

    return common_count

# Percorsi dei file CSV
file1_path =  '/home/alessandro/Scrivania/Dataset_Multiclass_mio2.csv'
file2_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/4 attacchi + 1 benign/Dataset_Multiclass.csv'

# Chiamata alla funzione e stampa del risultato
common_rows_count = count_common_rows(file1_path, file2_path)
print(f'Numero di righe in comune: {common_rows_count}')
