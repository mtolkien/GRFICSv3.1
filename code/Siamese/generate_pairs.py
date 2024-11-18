import random
import numpy as np
from sklearn.utils import shuffle

def generate_balanced_siamese_pairs(data, labels, num_pairs):
    # Initialize pairs and labels
    pairs = []
    pair_labels = []

    # Set to keep track of generated pairs
    generated_pairs = set()

    # Counters for duplicates
    duplicate_attempts = 0

    # Get unique classes from the labels
    unique_classes = np.unique(labels)
    print(f"Classes: {len(unique_classes)}")

    # Create a dictionary to hold indices for each class
    class_indices = {label: np.where(labels == label)[0] for label in unique_classes}

    # Calculate the number of positive and negative pairs
    num_positive_pairs = num_pairs // 2
    num_negative_pairs = num_pairs - num_positive_pairs

    # Function to create a unique key for a pair
    def make_pair_key(idx1, idx2):
        return tuple(sorted((int(idx1), int(idx2))))

    # Maximum number of attempts to prevent infinite loops
    max_attempts = num_pairs * 1000  # Adjust as necessary

    # Generate positive pairs
    positive_pairs_generated = 0
    attempts = 0  # Reset attempts for positive pairs
    while positive_pairs_generated < num_positive_pairs and attempts < max_attempts:
        # Select a random class
        class_label = random.choice(unique_classes)
        # Check if there are at least 2 samples in this class
        if len(class_indices[class_label]) < 2:
            attempts += 1
            continue
        idx1, idx2 = np.random.choice(class_indices[class_label], size=2, replace=False)
        pair_key = make_pair_key(idx1, idx2)
        if pair_key in generated_pairs:
            attempts += 1
            duplicate_attempts += 1
            continue
        # Add the pair and label
        pairs.append([data[idx1], data[idx2]])
        pair_labels.append(1)  # Same class
        generated_pairs.add(pair_key)
        positive_pairs_generated += 1
        attempts = 0  # Reset attempts since we successfully added a pair

    if attempts >= max_attempts:
        print("Reached maximum attempts while generating positive pairs.")

    # Generate negative pairs
    negative_pairs_generated = 0
    attempts = 0  # Reset attempts for negative pairs
    while negative_pairs_generated < num_negative_pairs and attempts < max_attempts:
        # Select two different classes
        if len(unique_classes) < 2:
            print("Not enough classes to generate negative pairs.")
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
        # Add the pair and label
        pairs.append([data[idx1], data[idx2]])
        pair_labels.append(0)  # Different classes
        generated_pairs.add(pair_key)
        negative_pairs_generated += 1
        attempts = 0  # Reset attempts since we successfully added a pair

    if attempts >= max_attempts:
        print("Reached maximum attempts while generating negative pairs.")

    if positive_pairs_generated < num_positive_pairs or negative_pairs_generated < num_negative_pairs:
        print("Not all requested unique pairs could be generated.")
        print(f"Positive pairs generated: {positive_pairs_generated}/{num_positive_pairs}")
        print(f"Negative pairs generated: {negative_pairs_generated}/{num_negative_pairs}")

    total_pairs_generated = positive_pairs_generated + negative_pairs_generated
    print(f"Total pairs generated: {total_pairs_generated}")
    print(f"Total duplicate attempts: {duplicate_attempts}")
    print(f"Duplicates over total attempts: {duplicate_attempts}/{total_pairs_generated}\n")

    # Convert pairs to NumPy arrays
    pairs_array = np.array(pairs)
    pair_labels = np.array(pair_labels)

    # Use sklearn.utils.shuffle for advanced shuffling
    pairs_array, pair_labels = shuffle(pairs_array, pair_labels, random_state=None)

    return pairs_array, pair_labels