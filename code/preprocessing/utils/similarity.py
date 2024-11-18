import pandas as pd

def count_common_rows(file1, file2):
    # Read the two CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Merge the two DataFrames to find the common rows
    common_rows = pd.merge(df1, df2, how='inner')

    # Count the number of common rows
    common_count = common_rows.shape[0]

    return common_count

# Paths of the CSV files
file1_path = '/home/alessandro/Scrivania/Dataset_Multiclass_mio2.csv'
file2_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/4 attacchi + 1 benign/Dataset_Multiclass.csv'

# Function call and print the result
common_rows_count = count_common_rows(file1_path, file2_path)
print(f'Number of common rows: {common_rows_count}')