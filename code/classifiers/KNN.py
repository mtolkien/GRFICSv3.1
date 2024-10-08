import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def load_and_preprocess_data(csv_file, test_size=0.2):
    data = pd.read_csv(csv_file)

    # Rimuovi gli indirizzi IP
    data = data.drop(columns=['Source IP', 'Destination IP'])

    # Separazione delle feature (X) e del target (y)
    X = data.drop(columns=['Type of connection'])
    y = data['Type of connection']

    # Codifica le etichette in numeri
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    numeric_features = X.columns
    preprocessor = ColumnTransformer(transformers=[('num', MinMaxScaler(), numeric_features)])

    # Suddivisione in training set e test set con stratificazione
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=42)

    # Applica il preprocessing
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, y_train, X_test, y_test

def train_knn(dataset_path):
    print("Preprocessing data..")
    X_train, y_train, X_test, y_test = load_and_preprocess_data(dataset_path, test_size=0.2)

    print("Distribuzione classi nel test set:", pd.Series(y_test).value_counts())

    # Inizializza il classificatore KNN
    print("Training..")
    knn_classifier = KNeighborsClassifier(n_neighbors=7)
    knn_classifier.fit(X_train, y_train)

    # Valuta sul set di test
    print("Predict..")
    y_pred = knn_classifier.predict(X_test)

    # Calcola le metriche di valutazione sul test
    test_accuracy = accuracy_score(y_test, y_pred)
    test_precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    test_recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    test_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # Stampa i risultati sul test
    print("\nRisultati sul Test con KNN:")
    print(f"Accuracy del Test: {test_accuracy:.4f}")
    print(f"Precisione del Test: {test_precision:.4f}")
    print(f"Recall del Test: {test_recall:.4f}")
    print(f"F1 Score del Test: {test_f1:.4f}")

    # Calcola e visualizza la matrice di confusione sul test
    cmatrix = confusion_matrix(y_test, y_pred)
    print("\nMatrice di Confusione sul Test:")
    print(cmatrix)

dataset_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/merged_output_binary.csv'
data = pd.read_csv(dataset_path)

count_type_0 = data[data['Type of connection'] == 0].shape[0]
count_type_1 = data[data['Type of connection'] == 1].shape[0]
print(f"Numero di righe con 'Type of connection' 0: {count_type_0}")
print(f"Numero di righe con 'Type of connection' 1: {count_type_1}")

train_knn(dataset_path)
