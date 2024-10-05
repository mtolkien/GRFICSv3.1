import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, OneHotEncoder
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

    # Identifica le feature categoriali e le feature numeriche
    categorical_features = ['Protocol']
    numeric_features = X.columns.difference(categorical_features)

    # Crea un ColumnTransformer per applicare trasformazioni diverse su categoriali e numeriche
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])

    # Suddivisione in training set e test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Applica il preprocessing
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, y_train, X_test, y_test

def train_svm(dataset_path):
    X_train, y_train, X_test, y_test = load_and_preprocess_data(dataset_path, test_size=0.2)

    # Inizializza il classificatore SVM
    svm_classifier = SVC(kernel='rbf')  # Puoi cambiare kernel se necessario
    svm_classifier.fit(X_train, y_train)

    # Valuta sul set di test
    y_pred = svm_classifier.predict(X_test)

    # Calcola le metriche di valutazione sul test
    test_accuracy = accuracy_score(y_test, y_pred)
    test_precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    test_recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    test_f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

    # Stampa i risultati sul test
    print("\nRisultati sul Test con SVM:")
    print(f"Accuracy del Test: {test_accuracy:.4f}")
    print(f"Precisione del Test: {test_precision:.4f}")
    print(f"Recall del Test: {test_recall:.4f}")
    print(f"F1 Score del Test: {test_f1:.4f}")

    # Calcola e visualizza la matrice di confusione sul test
    cmatrix = confusion_matrix(y_test, y_pred, labels=[0, 1])
    print("\nMatrice di Confusione sul Test:")
    print(cmatrix)

dataset_path = 'path_to_your_csv_file.csv'
train_svm(dataset_path)
