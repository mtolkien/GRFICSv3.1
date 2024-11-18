# Overview

The scripts in this folder are related to the implementation of the Siamese Network. Each script serves a specific purpose in the workflow of data preprocessing, model training, and evaluation. Below are the detailed descriptions of each script:

## Scripts Overview

### Script 1: `generate_pairs.py`

This script is responsible for generating balanced pairs of data suitable for training a Siamese Network.

- **Function**: `generate_balanced_siamese_pairs(data, labels, num_pairs)`
  - **Parameters**:
    - `data`: The input data from which pairs are generated.
    - `labels`: Corresponding labels for the input data.
    - `num_pairs`: The total number of pairs to generate (split into positive and negative).
  - **Output**: Returns two NumPy arrays: one for the pairs and one for the pair labels (1 for positive pairs, 0 for negative pairs).
  - **Key Features**:
    - Generates both positive pairs (same class) and negative pairs (different classes).
    - Utilizes shuffling from `sklearn.utils` for randomness.
    - Tracks duplicate pairs to ensure uniqueness.
    - Provides detailed print statements for debugging and tracking the number of generated pairs and attempts.

### Script 2: `preprocessing.py`

This script handles data loading and preprocessing, including splitting the dataset into training, validation, and test sets.

- **Function**: `load_and_preprocess_data(csv_file, test_size=0.2, val_size=0.2)`
  - **Parameters**:
    - `csv_file`: Path to the CSV file containing the dataset.
    - `test_size`: Proportion of the dataset to include in the test split.
    - `val_size`: Proportion of the training set to include in the validation split.
  - **Output**: Returns processed training, validation, and test sets along with the scaler and label encoder used.
  - **Key Features**:
    - Removes unnecessary columns (like 'Source IP' and 'Destination IP').
    - Ensures no overlap between training, validation, and test sets using assertions.
    - Scales features using `StandardScaler` and encodes categorical labels using `LabelEncoder`.

### Script 3: `save_components.py`

This script is responsible for saving and loading model components, specifically the trained model and preprocessing components.

- **Function**: 
  - `load_components(preprocessing_path)`: Loads preprocessing components (scaler and label encoder) from a specified path.
  - `save_components(model, scaler, le, results_path)`: Saves the trained model and preprocessing components to the specified path.
- **Parameters**:
  - `preprocessing_path`: Directory where the preprocessing components are stored.
  - `model`: The trained model to save.
  - `scaler`: The scaler object used for feature scaling.
  - `le`: The label encoder object used for encoding labels.
  - `results_path`: Directory where results should be saved.
- **Output**: None (the function saves files directly to the filesystem).

### Script 4: `siamese_net.py`

This script defines the architecture of the Siamese Network using Keras.

- **Class**: `SiameseNet`
  - **Constructor**: Initializes the network architecture with convolutional layers, inputs, and the loss function.
  - **Methods**:
    - `get()`: Returns the compiled Siamese model.
    - `euclidean_distance(vectors)`: Computes the Euclidean distance between two vectors.
    - `contrastive_loss(y_true, y_pred)`: Implements the contrastive loss function for training.
    - `load_saved_model(file_name)`: Loads a previously saved model for evaluation or further training.
- **Key Features**:
  - The network uses convolutional layers to extract features from input data.
  - Implements custom loss functions and metrics for training the Siamese architecture.

### Script 5: `main.py`

This is the main script that orchestrates the workflow, including data loading, preprocessing, pair generation, model training, and evaluation.

- **Function**: `train_siamese_network(csv_file, path_results, train, num_pairs)`
  - **Parameters**:
    - `csv_file`: Path to the dataset CSV file.
    - `path_results`: Directory for saving results and model components.
    - `train`: Boolean indicating whether to train the model or evaluate it.
    - `num_pairs`: List specifying the number of pairs to generate for training, validation, and testing.
  - **Key Features**:
    - If training, it loads and preprocesses the dataset, generates pairs, reshapes them for the model, and trains the Siamese Network.
    - If evaluating, it loads the pre-trained model and preprocessed components, generates test pairs, and evaluates the model's performance on the test set.
    - Includes detailed logging for each step, including checking for identical pairs.

## Usage Instructions

1. Ensure all dependencies are installed (TensorFlow, Keras, scikit-learn, pandas, numpy, matplotlib).
2. Prepare your dataset in CSV format, ensuring it contains the necessary features and labels.
3. Adjust the path variables in `main.py` to point to your dataset and desired results directory.
4. Run `main.py` to start the training or evaluation process.
