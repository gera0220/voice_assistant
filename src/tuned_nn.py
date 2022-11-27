import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import StandardScaler
from tensorflow.python.keras.layers import Activation
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sqlite3
import pandas as pd
from keras_tuner import RandomSearch
import time

LOG_DIR = f'{int(time.time())}'

# Cargar datos
db = sqlite3.connect("db/test.db")
cur = db.cursor()
cur.execute("SELECT * FROM audio_features")
features = cur.fetchall()

# Escoger columnas de características
features = pd.DataFrame(features)
features = np.array(features.iloc[:, 1:]) 

# Red Neuronal
train_size = int(features.shape[0] * 0.8)

X = features[:,1:]
y = features[:,0]

lb = LabelEncoder()
y = to_categorical(lb.fit_transform(y))

X_train, X_rem, y_train, y_rem = train_test_split(X, y, train_size=0.8, stratify = y)
X_val, X_test, y_val, y_test = train_test_split(X_rem, y_rem, test_size=0.5, stratify = y_rem)

#print(X_train.shape), print(y_train.shape)
#print(X_val.shape), print(y_val.shape)
#print(X_test.shape), print(y_test.shape)

ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_val = ss.transform(X_val)
X_test = ss.transform(X_test)

def build_model(hp):

    model = Sequential()
    model.add(Dense(hp.Int('input_units', min_value = 8, max_value = 64, step = 8), input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(Dropout(hp.Float('dropout_input', min_value = 0, max_value = 0.5, step = 0.05))) 

    for i in range(hp.Int("n_layers", 1, 5)):
        model.add(Dense(hp.Int(f'layer_{i}_units', min_value = 128, max_value = 512, step = 32)))
        model.add(Activation(hp.Choice(f'activacion_{i}', values = ['selu', 'elu','relu'])))
        model.add(Dropout(hp.Float(f'dropout_layer_{i}', min_value = 0, max_value = 0.5, step = 0.05))) 

    model.add(Dense(y.shape[1], activation = hp.Choice('final_layer', values = ['softmax', 'softplus', 'softsign'])))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=hp.Choice('optimizador', values = ['nadam', 'adam', 'rmsprop']))

    return model

tuner = RandomSearch(
    build_model,
    objective = 'val_accuracy',
    max_trials = 40,
    executions_per_trial = 1,
    directory = LOG_DIR
)

tuner.search(x = X_train,
    y = y_train,
    epochs = 4,
    batch_size = 512,
    validation_data = (X_val, y_val)
    )