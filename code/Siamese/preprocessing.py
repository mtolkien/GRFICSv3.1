import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# ==========================================================
#  Carica e preprocessa il dataset
# ==========================================================
def load_and_preprocess_data(csv_file, test_size=0.2, val_size=0.2):
    df = pd.read_csv(csv_file, sep=",")

    # Rimozione delle colonne 'Source IP' e 'Destination IP'
    df = df.drop(columns=['Source IP', 'Destination IP'])

    print("Colonne nel DataFrame dopo la rimozione di 'Source IP' e 'Destination IP':", df.columns.tolist())
    print("Valori unici nella colonna 'Type of connection':", df['Type of connection'].unique())

    # Divisione del dataset in train, validation e test set
    train_val_df, test_df = train_test_split(df, test_size=test_size, stratify=df['Type of connection'], shuffle=True)

    # Split train_val_df in train e val
    train_df, val_df = train_test_split(train_val_df, test_size=val_size, stratify=train_val_df['Type of connection'],
                                        shuffle=True)

    # Verifica sovrapposizione tra train, val e test
    train_indices = set(train_df.index)
    val_indices = set(val_df.index)
    test_indices = set(test_df.index)

    assert train_indices.isdisjoint(val_indices), "Le set di addestramento e validazione si sovrappongono!"
    assert train_indices.isdisjoint(test_indices), "Le set di addestramento e test si sovrappongono!"
    assert val_indices.isdisjoint(test_indices), "Le set di validazione e test si sovrappongono!"

    # Reset degli indici
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    # Preprocessing dei dataset
    X_train, y_train, scaler, label_encoder = preprocess_dataset(train_df, train=True)
    X_val, y_val, _, _ = preprocess_dataset(val_df, train=False, scaler=scaler, label_encoder=label_encoder)
    X_test, y_test, _, _ = preprocess_dataset(test_df, train=False, scaler=scaler, label_encoder=label_encoder)

    print(f"Dimensione del set di addestramento: {len(train_df)}")
    print(f"Dimensione del set di validazione: {len(val_df)}")
    print(f"Dimensione del set di test: {len(test_df)}")

    return X_train, y_train, X_val, y_val, X_test, y_test, scaler, label_encoder


def preprocess_dataset(df, train=True, scaler=None, label_encoder=None):

    df = df.drop(columns=['Source IP', 'Destination IP'])
    # Estrai la colonna target 'Type of connection'
    y = df['Type of connection'].values

    # Rimuovi la colonna target dal dataset
    X = df.drop(columns=['Type of connection'])

    # Converte tutte le colonne del DataFrame in float
    X = X.astype(float)

    if train:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)  # Scala i dati in fase di addestramento
    else:
        X = scaler.transform(X)  # Usa lo scaler esistente per trasformare i dati

    return X, y, scaler, label_encoder
