import os
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np

def load_and_preprocess_data(csv_file):
    data = pd.read_csv(csv_file)

    # Remove IP addresses
    data = data.drop(columns=['Source IP', 'Destination IP'])

    # Separate features (X) and target (y)
    X = data.drop(columns=['Type of connection'])
    y = data['Type of connection']

    # Encode labels into numbers
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    numeric_features = X.columns
    preprocessor = ColumnTransformer(transformers=[('num', MinMaxScaler(), numeric_features)])

    # Apply preprocessing
    X = preprocessor.fit_transform(X)

    return X, y, label_encoder, preprocessor

def evaluate_model(y_true, y_pred, dataset_type, file_path, label_encoder):
    num_classes = len(set(y_true))

    if num_classes == 2:
        average_type = 'binary'
        pos_label = 1
    else:
        average_type = 'macro'
        pos_label = None

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, average=average_type, zero_division=0, pos_label=pos_label)
    f1 = f1_score(y_true, y_pred, average=average_type, zero_division=0, pos_label=pos_label)

    cmatrix = confusion_matrix(y_true, y_pred)

    # Ensure the file directory exists and create it if necessary
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a") as f:
        f.write(f"\nResults on {dataset_type}:\n")
        f.write(f"Accuracy for {dataset_type}: {accuracy:.4f}\n")
        f.write(f"Recall for {dataset_type}: {recall:.4f}\n")
        f.write(f"F1 Score for {dataset_type}: {f1:.4f}\n")
        f.write(f"\nConfusion Matrix for {dataset_type}:\n")
        f.write(f"{cmatrix}\n")

        # Add the classification report
        report = classification_report(y_true, y_pred, target_names=label_encoder.classes_)
        f.write(f"\nClassification Report for {dataset_type}:\n")
        f.write(f"{report}\n")

def train_knn_kfold(dataset_path, result_file, model_path, k_folds=10):
    if os.path.exists(result_file):
        os.remove(result_file)

    print("Preprocessing data..")
    X, y, label_encoder, preprocessor = load_and_preprocess_data(dataset_path)

    # Initialize KFold
    kfold = KFold(n_splits=k_folds, shuffle=True, random_state=1)

    accuracy_scores = []
    recall_scores = []
    f1_scores = []

    best_model = None
    best_accuracy = 0  # Variable to track the best accuracy
    best_fold = 0  # Track the fold with the best accuracy

    fold_idx = 1
    for train_index, test_index in kfold.split(X):
        print(f"Fold {fold_idx}/{k_folds}")

        # Split the dataset into training and test sets for the current fold
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Initialize the KNN classifier
        knn_classifier = KNeighborsClassifier(n_neighbors=7)
        knn_classifier.fit(X_train, y_train)

        # Predictions on the test set
        y_pred = knn_classifier.predict(X_test)

        # Evaluate the current fold
        accuracy = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

        # Add metrics for this fold
        accuracy_scores.append(accuracy)
        recall_scores.append(recall)
        f1_scores.append(f1)

        # Save results for the current fold, including the classification report
        evaluate_model(y_test, y_pred, dataset_type=f'Fold {fold_idx}', file_path=result_file, label_encoder=label_encoder)

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

    # Calculate the averages of the metrics
    with open(result_file, "a") as f:
        f.write("\nAverage results across all folds:\n")
        f.write(f"Average Accuracy: {np.mean(accuracy_scores):.4f}\n")
        f.write(f"Average Recall: {np.mean(recall_scores):.4f}\n")
        f.write(f"Average F1 Score: {np.mean(f1_scores):.4f}\n")

# Dataset and output file paths
dataset_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/3 attacchi + 1 benign/Dataset_Multiclass.csv'
output_file = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/3 attacchi + 1 benign/KNN_KFold_Results.txt'
model_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/3 attacchi + 1 benign/best_knn_model.pkl'
train_knn_kfold(dataset_path, output_file, model_path, k_folds=10)