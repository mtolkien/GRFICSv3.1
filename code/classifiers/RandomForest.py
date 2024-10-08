import pandas as pd
from sklearn.ensemble import RandomForestClassifier
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

    # Suddivisione in training set e test set con stratificazione e shuffle
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=42, shuffle=True)

    # Applica il preprocessing
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, y_train, X_test, y_test

def evaluate_model(y_true, y_pred, dataset_type='Test'):
    # Calcola le metriche di valutazione
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)

    # Stampa i risultati
    print(f"\nRisultati sul {dataset_type}:")
    print(f"Accuracy del {dataset_type}: {accuracy:.4f}")
    print(f"Precisione del {dataset_type}: {precision:.4f}")
    print(f"Recall del {dataset_type}: {recall:.4f}")
    print(f"F1 Score del {dataset_type}: {f1:.4f}")

    # Calcola e visualizza la matrice di confusione
    cmatrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    print(f"\nMatrice di Confusione sul {dataset_type}:")
    print(cmatrix)

def train_rf(dataset_path):
    print("Preprocessing data..")
    X_train, y_train, X_test, y_test = load_and_preprocess_data(dataset_path, test_size=0.2)

    print("Distribuzione classi nel test set:", pd.Series(y_test).value_counts())

    # Inizializza il classificatore Random Forest
    print("Training..")
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    # Predizioni sul training set
    print("Predicting on training set..")
    y_train_pred = rf_classifier.predict(X_train)

    # Valuta sul set di training
    evaluate_model(y_train, y_train_pred, dataset_type='Training')

    # Valuta sul set di test
    print("Predict..")
    y_pred = rf_classifier.predict(X_test)

    # Valuta sul set di test
    evaluate_model(y_test, y_pred, dataset_type='Test')

dataset_path = '/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/merged_output_binary.csv'
train_rf(dataset_path)