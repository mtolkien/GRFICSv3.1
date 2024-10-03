import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def load_and_preprocess_data(csv_file, test_size=0.2):
    data = pd.read_csv(csv_file)

    # Codifica delle colonne categoriali (come Source IP e Destination IP)
    label_encoder_ip = LabelEncoder()
    data['Source IP'] = label_encoder_ip.fit_transform(data['Source IP'])
    data['Destination IP'] = label_encoder_ip.fit_transform(data['Destination IP'])

    # Separazione delle feature (X) e del target (y)
    X = data.drop(columns=['Type of connection'])
    y = data['Type of connection']

    # Suddivisione in training set e test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Standardizzazione delle feature
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, y_train, X_test, y_test

def train_knn(dataset_path):
    X_train, y_train, X_test, y_test = load_and_preprocess_data(dataset_path, test_size=0.2)

    # Inizializza il classificatore KNN
    knn_classifier = KNeighborsClassifier(n_neighbors=5)  # Puoi cambiare il valore di n_neighbors

    knn_classifier.fit(X_train, y_train)

    # Valuta sul set di training
    y_train_pred = knn_classifier.predict(X_train)

    # Calcola le metriche di valutazione sul training
    train_accuracy = accuracy_score(y_train, y_train_pred)
    train_precision = precision_score(y_train, y_train_pred, pos_label=1, zero_division=0)
    train_recall = recall_score(y_train, y_train_pred, pos_label=1, zero_division=0)
    train_f1 = f1_score(y_train, y_train_pred, pos_label=1, zero_division=0)

    # Stampa i risultati sul training
    print("\nRisultati sul Training con KNN:")
    print(f"Accuracy del Training: {train_accuracy:.4f}")
    print(f"Precisione del Training: {train_precision:.4f}")
    print(f"Recall del Training: {train_recall:.4f}")
    print(f"F1 Score del Training: {train_f1:.4f}")

    # Valuta sul set di test
    y_pred = knn_classifier.predict(X_test)

    # Calcola le metriche di valutazione sul test
    test_accuracy = accuracy_score(y_test, y_pred)
    test_precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    test_recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    test_f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

    # Stampa i risultati sul test
    print("\nRisultati sul Test con KNN:")
    print(f"Accuracy del Test: {test_accuracy:.4f}")
    print(f"Precisione del Test: {test_precision:.4f}")
    print(f"Recall del Test: {test_recall:.4f}")
    print(f"F1 Score del Test: {test_f1:.4f}")

    # Calcola e visualizza la matrice di confusione sul test
    cmatrix = confusion_matrix(y_test, y_pred, labels=[0, 1])
    print("\nMatrice di Confusione sul Test:")
    print(cmatrix)

dataset_path = 'path_to_your_csv_file.csv'
train_knn(dataset_path)
