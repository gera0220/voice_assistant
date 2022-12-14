import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sqlite3
import pandas as pd
import pickle

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

#pickle.dump(ss, open('scaler.pkl','wb'))

model = Sequential()

model.add(Dense(X.shape[1], input_shape=(X.shape[1],), activation = 'relu'))
model.add(Dropout(0.15)) 

model.add(Dense(1024, activation = 'relu'))
model.add(Dropout(0.2))  

model.add(Dense(512, activation = 'relu'))
model.add(Dropout(0.3))  

model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.3))  

model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.4))

model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))

model.add(Dense(y.shape[1], activation = 'softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='nadam')

early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=40, verbose=1, mode='auto')

history = model.fit(X_train, y_train, batch_size=512, epochs=40, 
                    validation_data=(X_val, y_val),
                    callbacks=[early_stop])

train_accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']

# Set figure size.
plt.figure(figsize=(12, 8))

# Generate line plot of training, testing loss over epochs.
plt.plot(train_accuracy, label='Conjunto de entrenamiento', color='#185fad')
plt.plot(val_accuracy, label='Conjunto de validación', color='orange')

# Set title
plt.title('Precisión de entrenamiento y validación por época', fontsize = 25)
plt.xlabel('Época', fontsize = 18)
plt.ylabel('Precisión', fontsize = 18)
plt.xticks(range(0,41,5), range(0,41,5))

plt.legend(fontsize = 18)
plt.show()

preds = model.predict(X_test)
preds = np.around(preds)

accuracy_score(y_test, preds)

# Save model
#model.save('models/voice_detection.h5')

from sklearn.metrics import multilabel_confusion_matrix
multilabel_confusion_matrix(y_test, preds)