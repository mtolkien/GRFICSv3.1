import pickle

# ==========================================================
#  Salva e carica i componenti
# ==========================================================
def load_components(preprocessing_path):
    with open(preprocessing_path + "preprocessing.pkl", 'rb') as prepro_file:
        scaler, label_encoder = pickle.load(prepro_file)
    print(f"Preprocessing caricato da {preprocessing_path}preprocessing.pkl")

    return scaler, label_encoder


def save_components(model, scaler, le, results_path):
    model.save(results_path + 'siamese_model.h5')
    model.save(results_path + 'siamese_model.keras')
    print(f"Modello salvato in {results_path}")

    with open(results_path + "preprocessing.pkl", 'wb') as file:
        pickle.dump((scaler, le), file)
    print("Preprocessing salvato!")

