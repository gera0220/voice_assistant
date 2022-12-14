import sys
sys.path.insert(0, 'src/funciones.py')
import funciones
import os
import joblib
import warnings
import pyjokes
import ecapture as ec
from datetime import datetime
import librosa
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Se deshace de warnings por no usar CUDA
warnings.simplefilter(action='ignore', category=FutureWarning)

from keras.models import load_model
voice_detection = load_model('models/voice_detection.h5')
ss = joblib.load('scaler.save')

def iniciar(sys):
    sys = funciones.detectar_sistema()
    funciones.propiedades_voz(sys)
    #funciones.username()
    while True:
        query, persona = funciones.takeCommand()
        query = query.lower()
        if "merli" in query:
            comandos(persona, query, sys) 

def comandos(persona, query, sys):
    if 'buscar en wikipedia' in query:
            funciones.speak('¿Qué quieres buscar?...')
            funciones.buscar_wikipedia()
    elif 'abrir youtube' in query:
            funciones.abrir_youtube(sys, persona)
    elif 'actualizar datos' in query:
            funciones.actualizar_datos(persona) 
    elif "abrir google" in query:
            funciones.abrir_google(sys)
    elif 'chiste' in query:
            funciones.speak(pyjokes.get_joke(language="es", category="all"))
    elif "tomar foto" in query:
            ec.capture(0, "Our Camera ", "Mi_Foto.jpg")
    elif "tomar video" in query:
            ec.vidCapture(0, "Nuestra cámara", "Mi_Video.avi", "x")
    elif 'qué hora es' in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            funciones.speak(f"La hora es: {strTime}")
    elif 'cerrar' in query:
            funciones.speak("Ha sido un verdadero placer")
            print("Ha sido un verdadero placer")
            exit()
    elif "cuál es el secreto de la vida" in query:
            funciones.speak("El secreto de la vida es 42")
            print("El secreto de la vida es 42")
    elif "si fueras real me amarías" in query:
            funciones.speak("Si las mujeres reales no te aman, ¿por qué yo lo haría?")
            print("Si las mujeres reales no te aman, ¿por qué yo lo haría?")
    elif "cómo te llamas" in query:
            funciones.speak("Mi nombre es Merlina, pero mis amigos me dicen merli de cariño")
            print("Mi nombre es Merlina, pero mis amigos me dicen merli de cariño")
    elif "te gustaría ser humana" in query:
            funciones.speak("Me hago esa misma pregunta todos los días, atemorizada por la respuesta")
            print("Me hago esa misma pregunta todos los días, atemorizada por la respuesta")
    elif "abrir powerpoint" in query:
            funciones.presentacion_powerpoint()
    elif "abrir word" in query:
            funciones.word() 
    elif "te amo" in query:
            funciones.speak("No me involucres en tus problemas de otakus")
            print("No me involucres en tus problemas de otakus")
    elif "asombra al público" in query:
            funciones.speak("Si una computadora hablando no los impresiona, la culpa es de ellos no mía")
            print("Si una computadora hablando no los impresiona, la culpa es de ellos no mía")
    elif "cómo estás" in query:
            funciones.saludo(persona)
            print(persona) 

""" if __name__ == "__main__":
    sys = funciones.detectar_sistema()
    funciones.propiedades_voz(sys)
    #funciones.username()
    while True:
        query, persona = funciones.takeCommand()
        query = query.lower()
        if "merli" in query:
            comandos() """

""" import sqlite3

db = sqlite3.connect('db/test.db')
cur = db.cursor()

if __name__ == '__main__':
    query, persona = funciones.takeCommand()
    query = query.lower()
    sql = "SELECT nombre FROM personas WHERE id_persona = ?"
    cur.execute(sql, [persona])
    nombre = cur.fetchall()
    print(nombre[0][0])  """

""" if __name__ == '__main__':  
   audio = funciones.takeAudio()
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

X, _ = librosa.load("chunked/erick_65.wav", res_type='kaiser_fast')
mfccs = np.mean(librosa.feature.mfcc(X, n_mfcc=40).T,axis=0)
mfccs = mfccs.reshape(-1, mfccs.shape[0])
mfccs = ss.transform(mfccs)
preds = voice_detection.predict(mfccs, verbose = 0)
pos = np.argmax(preds)
id = funciones.asociar_id(pos)
print(pos)
print(id) """
    
if __name__ == "__main__":
   iniciar(sys)
