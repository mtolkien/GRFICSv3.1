import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(csv_file, test_size=0.2, val_size=0.2):
    df = pd.read_csv(csv_file, sep=",")

    # Remove the 'Source IP' and 'Destination IP' columns
    df = df.drop(columns=['Source IP', 'Destination IP'])

    print("Columns in DataFrame after removing 'Source IP' and 'Destination IP':", df.columns.tolist())
    print("Unique values in 'Type of connection' column:", df['Type of connection'].unique())

    # Split the dataset into train, validation, and test sets
    train_val_df, test_df = train_test_split(df, test_size=test_size, stratify=df['Type of connection'], shuffle=True)

    # Split train_val_df into train and val
    train_df, val_df = train_test_split(train_val_df, test_size=val_size, stratify=train_val_df['Type of connection'],
                                        shuffle=True)

    # Check for overlap between train, val, and test
    train_indices = set(train_df.index)
    val_indices = set(val_df.index)
    test_indices = set(test_df.index)

    assert train_indices.isdisjoint(val_indices), "Training and validation sets overlap!"
    assert train_indices.isdisjoint(test_indices), "Training and test sets overlap!"
    assert val_indices.isdisjoint(test_indices), "Validation and test sets overlap!"

    # Reset indices
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    # Preprocessing the datasets
    X_train, y_train, scaler, label_encoder = preprocess_dataset(train_df, train=True)
    X_val, y_val, _, _ = preprocess_dataset(val_df, train=False, scaler=scaler, label_encoder=label_encoder)
    X_test, y_test, _, _ = preprocess_dataset(test_df, train=False, scaler=scaler, label_encoder=label_encoder)

    print(f"Size of the training set: {len(train_df)}")
    print(f"Size of the validation set: {len(val_df)}")
    print(f"Size of the test set: {len(test_df)}")

    return X_train, y_train, X_val, y_val, X_test, y_test, scaler, label_encoder


def preprocess_dataset(df, train=True, scaler=None, label_encoder=None):

    df = df.drop(columns=['Source IP', 'Destination IP'])
    # Extract the target column 'Type of connection'
    y = df['Type of connection'].values

    # Remove the target column from the dataset
    X = df.drop(columns=['Type of connection'])

    # Convert all columns of the DataFrame to float
    X = X.astype(float)

    if train:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)  # Scale data during training
    else:
        X = scaler.transform(X)  # Use existing scaler to transform data

    return X, y, scaler, label_encoder