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
import joblib
import keras_tuner as kt

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

print(X_train.shape), print(y_train.shape)
print(X_val.shape), print(y_val.shape)
print(X_test.shape), print(y_test.shape)

ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_val = ss.transform(X_val)
X_test = ss.transform(X_test)

def build_model(tuner):

    model = Sequential()
    model.add(Dense(tuner.Int("fc",  min_value=X.shape[1], max_value=90000, step=1000)))
    model.add(Activation("relu"))
    model.add(Dropout(tuner.Choice("dropout_1", values=list(np.array(range(0, 0.6, 0.02))))))
    model.add(Dense(y.shape[1]))
    model.add(Activation("softmax"))
    optimizer = tuner.Choice(name="optimizer", values=["rmsprop", "adam", "nadam", "adamaz"])
    model.compile(optimizer=optimizer,
    loss="categorical_crossentropy",
    metrics=["accuracy"])
    return model

early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=1, mode='auto')

tuner = kt.Hyperband(build_model, max_epochs=50, overwrite=True)

tuner.search(X_train, y_train, validation_data=(X_val, y_val), batch_size=256, 
callbacks=[early_stop], epochs= 50)

best_hp = tuner.get_best_hyperparameters(num_trials=1)
