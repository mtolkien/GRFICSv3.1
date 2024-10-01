import random
import numpy as np
import pandas as pd
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.layers import Input, Dense, Lambda, Dropout, Conv1D, Flatten, MaxPooling1D
from tensorflow.keras.models import Model

def initialize_bias(shape):
    return np.random.normal(loc=0.5, scale=1e-2, size=shape)

def last_layer(encoded_l, encoded_r):
    L2_layer = Lambda(lambda tensors: (tensors[0] - tensors[1]) ** 2 / (tensors[0] + tensors[1]))
    L2_distance = L2_layer([encoded_l, encoded_r])
    add_dens = Dense(512, activation='relu', bias_initializer=initialize_bias)(L2_distance)
    drp_lyr = Dropout(0.25)(add_dens)
    prediction = Dense(1, activation='sigmoid', bias_initializer=initialize_bias)(drp_lyr)
    return prediction

def make_oneshot_task(genes_len, x_test, class_test_ind, N):
    X = x_test.values
    class_test_dic = class_test_ind
    list_N_samples = random.sample(list(class_test_dic.keys()), N)
    true_category = list_N_samples[0]
    out_ind = np.array([random.sample(class_test_dic[j], 2) for j in list_N_samples])
    indices = out_ind[:, 1]
    ex1 = out_ind[0, 0]
    test_image = np.asarray([X[ex1]] * N).reshape(N, genes_len, 1)
    support_set = X[indices].reshape(N, genes_len, 1)
    targets = np.zeros((N,))
    targets[0] = 1
    targets, test_image, support_set, list_N_samples = shuffle(targets, test_image, support_set, list_N_samples)
    pairs = [test_image, support_set]
    return pairs, targets, true_category, list_N_samples

def test_oneshot(model, genes_len, x_test, class_test_ind, N, k):
    n_correct = 0
    for i in range(k):
        inputs, targets, true_category, list_N_samples = make_oneshot_task(genes_len, x_test, class_test_ind, N)
        probs = model.predict(inputs, verbose=0)
        if np.argmax(probs) == np.argmax(targets):
            n_correct += 1
    percent_correct = (100.0 * n_correct / k)
    return percent_correct

def get_batch(batch_size, x_train, class_train_ind, genes_len):
    categories = random.sample(list(class_train_ind.keys()), len(class_train_ind.keys()))
    n_classes = len(class_train_ind.keys())
    pairs = [np.zeros((batch_size, genes_len, 1)) for _ in range(2)]
    targets = np.zeros((batch_size,))
    targets[batch_size // 2:] = 1
    j = 0
    for i in range(batch_size):
        if j > n_classes - 1:
            categories = random.sample(list(class_train_ind.keys()), len(class_train_ind.keys()))
            j = 0
        category = categories[j]
        idx_1 = random.sample(class_train_ind[category], 1)[0]
        pairs[0][i, :, :] = x_train.values[idx_1].reshape(genes_len, 1)
        if i >= batch_size // 2:
            idx_2 = random.sample(class_train_ind[category], 1)[0]
            pairs[1][i, :, :] = x_train.values[idx_2].reshape(genes_len, 1)
        else:
            ind_pop = list(categories).index(category)
            copy_list = categories.copy()
            copy_list.pop(ind_pop)
            category_2 = random.sample(copy_list, 1)[0]
            idx_2 = random.sample(class_train_ind[category_2], 1)[0]
            pairs[1][i, :, :] = x_train.values[idx_2].reshape(genes_len, 1)
        j += 1
    return pairs, targets

def indices_save(dataset, label_column):
    class_map = {}
    for index, label in dataset[label_column].items():
        if label in class_map:
            class_map[label].append(index)
        else:
            class_map[label] = [index]
    return class_map

def get_siamese_model(input_shape):
    left_input = Input(input_shape)
    right_input = Input(input_shape)

    siamese_model = Sequential()
    siamese_model.add(Conv1D(filters=256, kernel_size=50, strides=1, activation='relu', padding='same', input_shape=input_shape))
    siamese_model.add(Conv1D(filters=128, kernel_size=10, strides=1, activation='relu', padding='same'))
    siamese_model.add(MaxPooling1D(pool_size=2))
    siamese_model.add(Conv1D(filters=128, kernel_size=5, strides=1, activation='sigmoid', padding='same'))
    siamese_model.add(MaxPooling1D(pool_size=2))
    siamese_model.add(Conv1D(filters=64, kernel_size=3, strides=1, activation='sigmoid', padding='same'))
    siamese_model.add(MaxPooling1D(pool_size=2))
    siamese_model.add(Conv1D(filters=32, kernel_size=3, strides=1, activation='sigmoid', padding='same'))
    siamese_model.add(MaxPooling1D(pool_size=2))
    siamese_model.add(Flatten())

    encoded_l = siamese_model(left_input)
    encoded_r = siamese_model(right_input)

    siamese_net = Model(inputs=[left_input, right_input], outputs=last_layer(encoded_l, encoded_r), name="siamese-network")
    return siamese_net

def siamese_network(siamese_path, risultati_siamese, dataset_genes, label_column):
    input_shape = (dataset_genes.shape[1] - 1, 1)  # Assumendo che l'ultima colonna sia la label
    genes_len = input_shape[0]
    siamese_model = get_siamese_model(input_shape)
    siamese_model.summary()

    optimizer = Adam(learning_rate=0.000005)
    siamese_model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=['accuracy'])

    class_labels = dataset_genes[label_column].unique()
    dataset_genes = pd.concat([dataset_genes], axis=1)

    x_train, x_test = train_test_split(dataset_genes, test_size=0.20, stratify=dataset_genes[label_column], random_state=42)

    class_train_ind = indices_save(x_train, label_column)
    class_test_ind = indices_save(x_test, label_column)

    x_train = x_train.drop(label_column, axis=1)
    x_test = x_test.drop(label_column, axis=1)

    evaluate_every = 200
    batch_size = 256
    n_iter = 1000000
    N_way = len(class_labels)
    n_val = 1000
    best = -1

    for i in range(1, n_iter + 1):
        (inputs, targets) = get_batch(batch_size, x_train, class_train_ind, genes_len)
        loss = siamese_model.train_on_batch(inputs, targets)

        if i % evaluate_every == 0:
            val_acc = test_oneshot(siamese_model, genes_len, x_test, class_test_ind, N_way, n_val)
            if val_acc >= best:
                best = val_acc
                siamese_model.save(siamese_path + "siamese_model.keras")
                with open(risultati_siamese, 'a') as file:
                    file.write("Epoca: {0}, Current best: {1}\n".format(i, val_acc))
