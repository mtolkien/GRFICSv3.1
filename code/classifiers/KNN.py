import os
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np

def load_and_preprocess_data(csv_file):
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

    # Applica il preprocessing
    X = preprocessor.fit_transform(X)

    return X, y, label_encoder, preprocessor

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

    # Verifica che la directory del file esista e creala se necessario
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a") as f:
        f.write(f"\nRisultati sul {dataset_type}:\n")
        f.write(f"Accuracy del {dataset_type}: {accuracy:.4f}\n")
        f.write(f"Precisione del {dataset_type}: {precision:.4f}\n")
        f.write(f"Recall del {dataset_type}: {recall:.4f}\n")
        f.write(f"F1 Score del {dataset_type}: {f1:.4f}\n")
        f.write(f"\nMatrice di Confusione sul {dataset_type}:\n")
        f.write(f"{cmatrix}\n")

def train_knn_kfold(dataset_path, result_file, model_path, k_folds=10):
    if os.path.exists(result_file):
        os.remove(result_file)

    print("Preprocessing data..")
    X, y, label_encoder, preprocessor = load_and_preprocess_data(dataset_path)

    # Inizializza KFold
    kfold = KFold(n_splits=k_folds, shuffle=True, random_state=1)

    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []

    best_model = None
    best_accuracy = 0  # Variabile per tracciare la migliore accuracy
    best_fold = 0  # Traccia il fold con la migliore accuracy

    fold_idx = 1
    for train_index, test_index in kfold.split(X):
        print(f"Fold {fold_idx}/{k_folds}")

        # Divisione del dataset in training e test set per il fold corrente
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Inizializza il classificatore KNN
        knn_classifier = KNeighborsClassifier(n_neighbors=7)
        knn_classifier.fit(X_train, y_train)

        # Predizioni sul test set
        y_pred = knn_classifier.predict(X_test)

        # Valutazione sul fold corrente
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
        recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

        # Aggiungi le metriche per questo fold
        accuracy_scores.append(accuracy)
        precision_scores.append(precision)
        recall_scores.append(recall)
        f1_scores.append(f1)

        # Salva i risultati per il fold corrente
        evaluate_model(y_test, y_pred, dataset_type=f'Fold {fold_idx}', file_path=result_file)

        # Calcola e salva l'accuracy per ciascuna classe
        report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
        with open(result_file, "a") as f:
            f.write(f"\nReport di classificazione per {dataset_type}:\n")
            f.write(f"{classification_report(y_test, y_pred, target_names=label_encoder.classes_)}\n")

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = knn_classifier
            best_fold = fold_idx

        fold_idx += 1

    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': best_model,
            'label_encoder': label_encoder,
            'preprocessor': preprocessor
        }, f)

    # Calcola le medie delle metriche
    with open(result_file, "a") as f:
        f.write("\nRisultati medi su tutti i fold:\n")
        f.write(f"Accuracy media: {np.mean(accuracy_scores):.4f}\n")
        f.write(f"Precisione media: {np.mean(precision_scores):.4f}\n")
        f.write(f"Recall medio: {np.mean(recall_scores):.4f}\n")
        f.write(f"F1 Score medio: {np.mean(f1_scores):.4f}\n")

dataset_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/Dataset_Multiclass.csv'
output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/KNN_KFold_Results.txt'
model_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/best_knn_model.pkl'
train_knn_kfold(dataset_path, output_file, model_path, k_folds=10)