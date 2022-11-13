import os
import pandas as pd
import librosa
import numpy as np
import uuid
import sqlite3
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Conexión a la base de datos
db = sqlite3.connect("db/test.db")
cur = db.cursor()

# Cambio de directorio
os.chdir('chunked')

# Guardar lista de audios
audio_files = os.listdir()
df = pd.DataFrame(audio_files)

df = df.rename(columns = {0: 'file'})

def extract_features(files):

    # Ubicación del archivo
    file_name = os.path.join(os.path.abspath('') + '/' + str(files.file))

    # Carga de archivo como serie de tiempo y frecuencia de sampleo
    X, sr = librosa.load(file_name, res_type='kaiser_fast') 

    X = X[0:sr]

    # Genera los coeficientes de mel a partir de la serie de tiempo
    mfccs = librosa.feature.mfcc(X, n_mfcc=40).T
    return mfccs

# Obtención de features y conversión a array
features_label = df.apply(extract_features, axis = 1)
features_label = features_label.to_numpy()

# Obtención de hablantes
speaker = []
for audio_file in range(len(df)):
    speaker.append(df['file'][audio_file].split('_')[0])

speaker_rep = np.repeat(speaker, features_label[0].shape[0])

speaker_rep = np.array(speaker_rep).reshape(-1, 1)

speakers_names = np.unique(speaker_rep)
n_speakers = len(speakers_names)

# Creación de claves únicas
n_id = []
for i in range(n_speakers):
    n_id.append(speakers_names[i])

keys = dict(zip(list(speakers_names), n_id))
all_keys = np.array([keys[str(ele[0])] for ele in speaker_rep])

keys = np.array(list(keys.items()))
keys = np.fliplr(keys) #Cambiar el orden porque se quiere primero la clave



# Concatenación de arrays
features_label = np.concatenate(features_label)

features = np.concatenate([all_keys.reshape(-1, 1), features_label], axis = 1)


#Inserción de datos
cur.executemany("""INSERT INTO audio_features VALUES(NULL, ?,
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", features)

cur.executemany("INSERT OR IGNORE INTO personas VALUES(?, ?, NULL, NULL, NULL)", keys)

db.commit()

