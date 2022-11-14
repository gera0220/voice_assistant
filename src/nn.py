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
import joblib

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

joblib.dump(ss, 'scaler.save')

model = Sequential()

model.add(Dense(X.shape[1], input_shape=(X.shape[1],), activation = 'relu'))
model.add(Dropout(0.1))

model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.25))  

model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.5))

model.add(Dense(y.shape[1], activation = 'softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=1, mode='auto')

history = model.fit(X_train, y_train, batch_size=256, epochs=50, 
                    validation_data=(X_val, y_val),
                    callbacks=[early_stop])

train_accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']

# Set figure size.
plt.figure(figsize=(12, 8))

# Generate line plot of training, testing loss over epochs.
plt.plot(train_accuracy, label='Training Accuracy', color='#185fad')
plt.plot(val_accuracy, label='Validation Accuracy', color='orange')

# Set title
plt.title('Training and Validation Accuracy by Epoch', fontsize = 25)
plt.xlabel('Epoch', fontsize = 18)
plt.ylabel('Categorical Crossentropy', fontsize = 18)
plt.xticks(range(0,20,1), range(0,20,1))

plt.legend(fontsize = 18)
plt.show()

preds = model.predict(X_test)
preds = np.around(preds)

accuracy_score(y_test, preds)

# Save model
model.save('models/voice_detection.h5')

from sklearn.metrics import multilabel_confusion_matrix
multilabel_confusion_matrix(y_test, preds)