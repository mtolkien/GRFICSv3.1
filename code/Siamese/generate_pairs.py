import random
import numpy as np
from sklearn.utils import shuffle

# ==========================================================
#  Genera coppie bilanciate di Siamese per multiclass
# ==========================================================
def generate_balanced_siamese_pairs(data, labels, num_pairs):
    # Inizializza coppie e etichette
    pairs = []
    pair_labels = []

    # Insieme per tenere traccia delle coppie generate
    generated_pairs = set()

    # Contatori per i duplicati
    duplicate_attempts = 0

    # Ottieni classi uniche dalle etichette
    unique_classes = np.unique(labels)
    print(f"Classi: {len(unique_classes)}")

    # Crea un dizionario per tenere gli indici per ogni classe
    class_indices = {label: np.where(labels == label)[0] for label in unique_classes}

    # Calcola il numero di coppie positive e negative
    num_positive_pairs = num_pairs // 2
    num_negative_pairs = num_pairs - num_positive_pairs

    # Funzione per creare una chiave unica per una coppia
    def make_pair_key(idx1, idx2):
        return tuple(sorted((int(idx1), int(idx2))))

    # Numero massimo di tentativi per prevenire cicli infiniti
    max_attempts = num_pairs * 1000  # Regola come necessario

    # Genera coppie positive
    positive_pairs_generated = 0
    attempts = 0  # Resetta i tentativi per le coppie positive
    while positive_pairs_generated < num_positive_pairs and attempts < max_attempts:
        # Seleziona una classe casuale
        class_label = random.choice(unique_classes)
        # Controlla se ci sono almeno 2 campioni in questa classe
        if len(class_indices[class_label]) < 2:
            attempts += 1
            continue
        idx1, idx2 = np.random.choice(class_indices[class_label], size=2, replace=False)
        pair_key = make_pair_key(idx1, idx2)
        if pair_key in generated_pairs:
            attempts += 1
            duplicate_attempts += 1
            continue
        # Aggiungi la coppia e l'etichetta
        pairs.append([data[idx1], data[idx2]])
        pair_labels.append(1)  # Stessa classe
        generated_pairs.add(pair_key)
        positive_pairs_generated += 1
        attempts = 0  # Resetta i tentativi poiché abbiamo aggiunto con successo una coppia

    if attempts >= max_attempts:
        print("Raggiunto il numero massimo di tentativi mentre si generavano coppie positive.")

    # Genera coppie negative
    negative_pairs_generated = 0
    attempts = 0  # Resetta i tentativi per le coppie negative
    while negative_pairs_generated < num_negative_pairs and attempts < max_attempts:
        # Seleziona due classi diverse
        if len(unique_classes) < 2:
            print("Non ci sono abbastanza classi per generare coppie negative.")
            break
        class_label1, class_label2 = random.sample(list(unique_classes), 2)
        if len(class_indices[class_label1]) == 0 or len(class_indices[class_label2]) == 0:
            attempts += 1
            continue
        idx1 = np.random.choice(class_indices[class_label1])
        idx2 = np.random.choice(class_indices[class_label2])
        pair_key = make_pair_key(idx1, idx2)
        if pair_key in generated_pairs:
            attempts += 1
            duplicate_attempts += 1
            continue
        # Aggiungi la coppia e l'etichetta
        pairs.append([data[idx1], data[idx2]])
        pair_labels.append(0)  # Classi diverse
        generated_pairs.add(pair_key)
        negative_pairs_generated += 1
        attempts = 0  # Resetta i tentativi poiché abbiamo aggiunto con successo una coppia

    if attempts >= max_attempts:
        print("Raggiunto il numero massimo di tentativi mentre si generavano coppie negative.")

    if positive_pairs_generated < num_positive_pairs or negative_pairs_generated < num_negative_pairs:
        print("Non è stato possibile generare tutte le coppie uniche richieste.")
        print(f"Coppie positive generate: {positive_pairs_generated}/{num_positive_pairs}")
        print(f"Coppie negative generate: {negative_pairs_generated}/{num_negative_pairs}")

    total_pairs_generated = positive_pairs_generated + negative_pairs_generated
    print(f"Coppie totali generate: {total_pairs_generated}")
    print(f"Totale tentativi di duplicati: {duplicate_attempts}")
    print(f"Duplichi su tentativi totali: {duplicate_attempts}/{total_pairs_generated}\n")

    # Converti le coppie in array NumPy
    pairs_array = np.array(pairs)
    pair_labels = np.array(pair_labels)

    # Utilizza sklearn.utils.shuffle per uno shuffle più avanzato
    pairs_array, pair_labels = shuffle(pairs_array, pair_labels, random_state=None)

    return pairs_array, pair_labels
