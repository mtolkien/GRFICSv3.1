from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report
from generate_pairs import *
from preprocessing import *
from siamese_net import SiameseNet
from save_components import *

def train_siamese_network(csv_file, path_results, train, num_pairs):
    if train:
        print("\n================= [STEP 1.0] Load and preprocess the datasets =================")

        df_original = pd.read_csv(csv_file, sep=",")
        print("Number of columns in the original dataset:", df_original.shape[1])
        print("Original columns:", df_original.columns.tolist())

        # Preprocessing
        X_train, y_train, X_val, y_val, X_test, y_test, scaler, label_encoder = load_and_preprocess_data(
            csv_file, test_size=0.2, val_size=0.2
        )
        print("Data are preprocessed!")

        print("\n================= [STEP 2.0] Generation of pairs =================")
        # Generation of pairs
        train_pairs, train_labels = generate_balanced_siamese_pairs(X_train, y_train, num_pairs=num_pairs[0])
        val_pairs, val_labels = generate_balanced_siamese_pairs(X_val, y_val, num_pairs=num_pairs[1])
        test_pairs, test_labels = generate_balanced_siamese_pairs(X_test, y_test, num_pairs=num_pairs[2])
        print("Pairs are generated!")

        # Check for duplicate pairs
        print("\n================= [STEP 2.1] Check for duplicate pairs =================")
        train_identic_count = np.sum(
            np.all(train_pairs[:, 0] == train_pairs[:, 1], axis=tuple(range(1, train_pairs[:, 0].ndim))))
        val_identic_count = np.sum(
            np.all(val_pairs[:, 0] == val_pairs[:, 1], axis=tuple(range(1, val_pairs[:, 0].ndim))))
        test_identic_count = np.sum(
            np.all(test_pairs[:, 0] == test_pairs[:, 1], axis=tuple(range(1, test_pairs[:, 0].ndim))))

        print(f"Number of identical pairs TRAIN SET: {train_identic_count}/{len(train_pairs)}")
        print(f"Number of identical pairs VAL SET: {val_identic_count}/{len(val_pairs)}")
        print(f"Number of identical pairs TEST SET: {test_identic_count}/{len(test_pairs)}")

        print("\n================= [STEP 2.2] Reshape pairs =================")
        train_a = train_pairs[:, 0]
        train_b = train_pairs[:, 1]
        val_a = val_pairs[:, 0]
        val_b = val_pairs[:, 1]
        test_a = test_pairs[:, 0]
        test_b = test_pairs[:, 1]

        # Reshape for the neural network
        train_a = train_a.reshape(-1, 15, 1, 1)
        train_b = train_b.reshape(-1, 15, 1, 1)
        val_a = val_a.reshape(-1, 15, 1, 1)
        val_b = val_b.reshape(-1, 15, 1, 1)
        test_a = test_a.reshape(-1, 15, 1, 1)
        test_b = test_b.reshape(-1, 15, 1, 1)

        print("Pairs are reshaped!")

        print("\n================= [STEP 3.0] Training Phase =================")
        # Create Siamese model
        siamese_model = SiameseNet(input_shape=(15, 1, 1)).get()

        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        # Train the model
        history = siamese_model.fit(
            [train_a, train_b], train_labels,
            validation_data=([val_a, val_b], val_labels),
            batch_size=256,
            epochs=100,
            callbacks=[early_stopping]
        )

        # Save components
        save_components(siamese_model, scaler, label_encoder, path_results)

        # Plot training history
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Loss during Training')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig(path_results + "training_loss.png")
        plt.show()

        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Accuracy during Training')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.savefig(path_results + "training_acc.png")
        plt.show()

    else:
        print("\n================= [STEP 1.0] Load and preprocess the datasets =================")
        df = pd.read_csv(csv_file, sep=",")
        scaler, label_encoder = load_components(path_results)
        X_test, y_test, _, _ = preprocess_dataset(df, train=False, scaler=scaler, label_encoder=label_encoder)
        print("Data are preprocessed!\n")

        print("================= [STEP 2.0] Generation of pairs =================")
        test_pairs, test_labels = generate_balanced_siamese_pairs(X_test, y_test, num_pairs=num_pairs[2])
        print("Pairs are generated!")

        print("\n================= [STEP 2.1] Check for duplicate pairs =================")
        test_identic_count = np.sum(
            np.all(test_pairs[:, 0] == test_pairs[:, 1], axis=tuple(range(1, test_pairs[:, 0].ndim))))
        print(f"Number of identical pairs TEST SET: {test_identic_count}/{len(test_pairs)}")

        print("\n================= [STEP 2.2] Reshape pairs in (x, 18, 1, 1) =================")
        test_a = test_pairs[:, 0].reshape(-1, 15, 1, 1)
        test_b = test_pairs[:, 1].reshape(-1, 15, 1, 1)
        print("Pairs are reshaped!")

        print("\n================= [STEP 3.0] Load Model =================")
        siamese_model = SiameseNet(input_shape=(15, 1, 1)).load_saved_model(path_results + "siamese_model.h5")
        print(f"Model loaded from {path_results}")

    print("\n================= [STEP 4.0] Evaluate Model =================")
    test_loss, test_accuracy = siamese_model.evaluate([test_a, test_b], test_labels)
    print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

    predictions = siamese_model.predict([test_a, test_b]).ravel()
    predicted_labels = (predictions < 0.5).astype(int)

    print(classification_report(test_labels, predicted_labels))

if __name__ == "__main__":
    csv_file = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/Dataset unito/Dataset.csv'
    result_path = "/home/alessandro/Scrivania/UNISA - Magistrale/Tesi/dataset/Multiclasse/4 attacchi + 1 benign/500k - 500k - 50k/"
    train = False

    num_pairs = [500000, 500000, 50000]

    train_siamese_network(csv_file, result_path, train, num_pairs)