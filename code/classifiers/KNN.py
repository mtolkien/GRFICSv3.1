import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, shuffle=True)

    # Applica il preprocessing
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, y_train, X_test, y_test

def evaluate_model(y_true, y_pred, dataset_type, file_path):
    num_classes = len(set(y_true))

    if num_classes == 2:
        average_type = 'binary'
        pos_label = 1
    else:
        average_type = 'macro'
        pos_label = None

    # Calcola le metriche di valutazione
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average=average_type, zero_division=0, pos_label=pos_label)
    recall = recall_score(y_true, y_pred, average=average_type, zero_division=0, pos_label=pos_label)
    f1 = f1_score(y_true, y_pred, average=average_type, zero_division=0, pos_label=pos_label)

    cmatrix = confusion_matrix(y_true, y_pred)

    with open(file_path, "a") as f:
        f.write(f"\nRisultati sul {dataset_type}:\n")
        f.write(f"Accuracy del {dataset_type}: {accuracy:.4f}\n")
        f.write(f"Precisione del {dataset_type}: {precision:.4f}\n")
        f.write(f"Recall del {dataset_type}: {recall:.4f}\n")
        f.write(f"F1 Score del {dataset_type}: {f1:.4f}\n")
        f.write(f"\nMatrice di Confusione sul {dataset_type}:\n")
        f.write(f"{cmatrix}\n")

def train_knn(dataset_path, result_file):
    if os.path.exists(result_file):
        os.remove(result_file)

    print("Preprocessing data..")
    X_train, y_train, X_test, y_test = load_and_preprocess_data(dataset_path, test_size=0.2)

    print("Distribuzione classi nel test set:", pd.Series(y_test).value_counts())

    # Inizializza il classificatore KNN
    print("Training..")
    knn_classifier = KNeighborsClassifier(n_neighbors=7)
    knn_classifier.fit(X_train, y_train)

    # Predizioni sul training set
    print("Predicting on training set..")
    y_train_pred = knn_classifier.predict(X_train)

    # Valuta sul set di training
    evaluate_model(y_train, y_train_pred, dataset_type='Training', file_path=result_file)

    # Valuta sul set di test
    print("Predict..")
    y_pred = knn_classifier.predict(X_test)

    # Valuta sul set di test
    evaluate_model(y_test, y_pred, dataset_type='Test', file_path=result_file)

dataset_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Dataset_Binary.csv'
output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Binario/KNN_Results.txt'
train_knn(dataset_path, output_file)