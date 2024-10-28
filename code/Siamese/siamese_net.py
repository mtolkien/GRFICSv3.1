from keras.models import Model, Sequential
from keras.optimizers import Adam
from tensorflow.keras.layers import Input, Lambda, MaxPooling2D, Conv2D, Flatten
from keras.models import load_model
import tensorflow as tf
from tensorflow.keras import backend as K  # Importa il backend da tensorflow

class SiameseNet:
    def __init__(self, input_shape, verbose=True):
        # Definizione degli input per le due ramificazioni della rete Siamese
        self.left_input = Input(input_shape)
        self.right_input = Input(input_shape)
        self.convnet = Sequential()

        lr = 0.0001

        # Aggiunta di livelli convoluzionali
        self.convnet.add(Conv2D(filters=256, kernel_size=(50, 1), strides=(1, 1), activation='relu', padding='same', input_shape=input_shape))
        self.convnet.add(Conv2D(filters=128, kernel_size=(10, 1), strides=(1, 1), activation='relu', padding='same'))
        self.convnet.add(MaxPooling2D(pool_size=(2, 1)))

        self.convnet.add(Conv2D(filters=128, kernel_size=(5, 1), strides=(1, 1), activation='sigmoid', padding='same'))
        self.convnet.add(MaxPooling2D(pool_size=(2, 1)))

        #######################################################################################
        # Due ulteriori livelli
        self.convnet.add(Conv2D(filters=64, kernel_size=(3, 1), strides=(1, 1), activation='sigmoid', padding='same'))
        self.convnet.add(MaxPooling2D(pool_size=(2, 1)))

        self.convnet.add(Conv2D(filters=32, kernel_size=(3, 1), strides=(1, 1), activation='sigmoid', padding='same'))
        self.convnet.add(MaxPooling2D(pool_size=(1, 1)))
        #######################################################################################

        # Appiattimento dell'output
        self.convnet.add(Flatten())

        # Applica il modello convoluzionale ai due input
        self.encoded_l = self.convnet(self.left_input)
        self.encoded_r = self.convnet(self.right_input)

        # Livello per calcolare la distanza euclidea tra i due input codificati
        self.L1_layer = Lambda(self.euclidean_distance, output_shape=self.eucl_dist_output_shape)

        # Calcola la distanza L1 tra le due codifiche
        self.L1_distance = self.L1_layer([self.encoded_l, self.encoded_r])
        self.siamese_net = Model(inputs=[self.left_input, self.right_input], outputs=self.L1_distance)

        # Compilazione del modello
        self.optimizer = Adam(lr)
        self.siamese_net.compile(loss=self.contrastive_loss, optimizer=self.optimizer, metrics=[self.accuracy])

        if verbose:
            print('Rete Siamese Creata:\n')
            self.siamese_net.summary()

    def get(self):
        return self.siamese_net

    def euclidean_distance(self, vectors):
        x, y = vectors
        sum_square = tf.reduce_sum(tf.square(x - y), axis=1, keepdims=True)
        return tf.sqrt(sum_square)

    def eucl_dist_output_shape(self, shapes):
        shape1, shape2 = shapes
        return (shape1[0], 1)

    def contrastive_loss(self, y_true, y_pred):
        '''Funzione di perdita contrastiva da Hadsell-et-al.'06'''
        margin = 1
        y_true = K.cast(y_true, 'float32')  # Usa tf.keras.backend qui
        square_pred = K.square(y_pred)
        margin_square = K.square(K.maximum(margin - y_pred, 0))
        return K.mean(y_true * square_pred + (1 - y_true) * margin_square)

    def accuracy(self, y_true, y_pred):
        '''Calcola l'accuratezza con una soglia fissa sulle distanze.'''
        return K.mean(K.equal(y_true, K.cast(y_pred < 0.5, y_true.dtype)))

    def load_saved_model(self, file_name):
        self.siamese_net = load_model(file_name, custom_objects={
            'contrastive_loss': self.contrastive_loss,
            'accuracy': self.accuracy,
            'euclidean_distance': self.euclidean_distance,
            'eucl_dist_output_shape': self.eucl_dist_output_shape
        })
        return self.siamese_net
