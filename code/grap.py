import pandas as pd
import torch
from torch_geometric.data import Data
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import os

def preprocess_gnn(dataset_path: str, output_dir: str, legitimate_connections: list):
    # Carica il dataset
    df = pd.read_csv(dataset_path)

    # Verifica che le colonne necessarie esistano
    required_columns = ['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 'tcp.seq', 'tcp.ack']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Il dataset manca di una o più colonne richieste: {required_columns}")

    # Creazione della colonna 'legitimate' in base alla lista di connessioni lecite
    df['legitimate'] = df.apply(lambda row: 0 if (row['ip.src'], row['ip.dst']) in legitimate_connections else 1, axis=1)

    # Estrai le colonne rilevanti per la creazione dei nodi e degli archi
    ip_src = df['ip.src'].dropna().astype(str)
    ip_dst = df['ip.dst'].dropna().astype(str)
    edges = list(zip(ip_src, ip_dst))

    # Codifica gli indirizzi IP come ID unici dei nodi
    node_encoder = LabelEncoder()
    all_ips = pd.concat([ip_src, ip_dst]).drop_duplicates().astype(str).values
    node_encoder.fit(all_ips)
    node_indices = node_encoder.transform(all_ips)

    # Crea la mappatura dagli indirizzi IP agli indici dei nodi
    ip_to_index = dict(zip(all_ips, node_indices))

    # Estrai le coppie di indici dei nodi per gli archi
    edge_index = torch.tensor([[ip_to_index[src], ip_to_index[dst]] for src, dst in edges], dtype=torch.long).t().contiguous()

    # Estrai le feature degli archi (inclusa la nuova colonna 'legitimate')
    edge_features = df[['tcp.srcport', 'tcp.dstport', 'tcp.seq', 'tcp.ack', 'legitimate']].fillna(0)

    # Preprocessing delle feature: normalizzazione delle colonne numeriche con MinMaxScaler
    scaler = MinMaxScaler()
    numeric_features = ['tcp.srcport', 'tcp.dstport', 'tcp.seq', 'tcp.ack']
    edge_features[numeric_features] = scaler.fit_transform(edge_features[numeric_features])

    # Converte le feature degli archi in un tensor
    edge_attr = torch.tensor(edge_features.values, dtype=torch.float)

    # Crea l'oggetto di dati del grafo
    data = Data(x=None, edge_index=edge_index, edge_attr=edge_attr)

    # Dividi il dataset in train, validation e test set
    train_df, val_df = train_test_split(df, test_size=0.2, shuffle=True, random_state=42)
    train_df, test_df = train_test_split(train_df, test_size=0.25, shuffle=True, random_state=42)

    # Salva i dataset suddivisi
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)
    test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)

    # Creazione del set di dati per la classificazione binaria
    df['label'] = df['legitimate'].apply(lambda x: 1 if x != 0 else 0)
    train_binary, val_binary = train_test_split(df, test_size=0.2, shuffle=True, random_state=42)
    train_binary, test_binary = train_test_split(train_binary, test_size=0.25, shuffle=True, random_state=42)

    # Salva i dataset per la classificazione binaria
    train_binary.to_csv(os.path.join(output_dir, 'train-binary.csv'), index=False)
    val_binary.to_csv(os.path.join(output_dir, 'val-binary.csv'), index=False)
    test_binary.to_csv(os.path.join(output_dir, 'test-binary.csv'), index=False)

    # Salva l'oggetto dati del grafo elaborato
    torch.save(data, os.path.join(output_dir, 'processed_graph_data.pt'))
    print(f"I dati del grafo sono stati salvati in '{os.path.join(output_dir, 'processed_graph_data.pt')}'")

if __name__ == '__main__':
    # Esempio di lista di connessioni lecite
    legitimate_connections = [
        ('192.168.1.1', '192.168.1.2'),
        ('10.0.0.1', '10.0.0.2')
        # Aggiungi tutte le altre connessioni lecite qui
    ]

    preprocess_gnn('/home/alessandro/Scrivania/output2.csv', 'dataset/elaborati', legitimate_connections)
