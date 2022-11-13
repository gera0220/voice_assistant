import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import sqlite3
import platform
import os
import librosa
import numpy as np
import joblib
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Se deshace de warnings por no usar CUDA
warnings.simplefilter(action='ignore', category=FutureWarning)

from keras.models import load_model
voice_detection = load_model('models/voice_detection.h5')

ss = joblib.load('scaler.save')

wikipedia.set_lang('es')
db = sqlite3.connect('db/test.db')
cur = db.cursor()

def propiedades_voz(sys):
    global engine
    if sys == 'Linux':
        engine = pyttsx3.init('espeak')
        voice = engine.getProperty('voices')
        engine.setProperty('voice', voice[20].id)
    elif sys == 'Windows':
        engine = pyttsx3.init('sapi5')
        voice = engine.getProperty('voices')
        engine.setProperty('voice', voice[0].id)

def mostrar_menu():
    print("""
    ¿Qué quieres actualizar?
    1. Género
    2. Navegador
    3. Correo
    4. Idioma
    0. Salir
    """)

def actualizar_datos(persona):
    mostrar_menu()
    option = int(input('Elige tu opción: '))
    if (option == 1):
        actualizar_genero(persona)
    elif (option == 2):
        actualizar_navegador(persona)
    elif (option == 3):
        actualizar_correo(persona)
    elif (option == 0):
        pass
    else:
        print('Opción inválida. Intenta de nuevo')
        actualizar_datos()

def actualizar_genero(persona):
    speak('¿Cuál es tu género?')
    print("""
    ¿Cuál es tu género?
    0. Maculino
    1. Femenino
    """)
    genero = input('Elige tu opción: ')
    sql = """
        UPDATE personas_verdad
        SET genero = ?
        WHERE id_persona = ?;
    """
    cur.execute(sql, genero, [persona])
    db.commit()

def actualizar_navegador(persona):
    speak('¿Cuál es tu navegador?')
    print("""
    ¿Cuál es tu navegador?
    1. Firefox
    2. Chrome
    """)
    option = int(input('Elige tu opción: '))
    if option == 1:
        navegador = 'firefox'
    elif option == 2:
        navegador = 'chrome'
    sql = """
        UPDATE personass
        SET navegador = ?
        WHERE id_persona = ?;
    """
    cur.execute(sql, [navegador], [persona])
    db.commit()

def actualizar_correo(persona):
    speak('¿Cuál es tu correo?')
    correo = input('¿Cuál es tu correo?\n')
    sql = """
        UPDATE personas_verdad
        SET correo = (?)
        WHERE id_persona = ?;
    """
    cur.execute(sql, [correo], [persona])
    db.commit()

def detectar_sistema():
    sistema = platform.system()
    return sistema

def reconocer_persona(audio):
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    X, _ = librosa.load("microphone-results.wav", res_type='kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(X, n_mfcc=40).T,axis=0)
    mfccs = mfccs.reshape(-1, mfccs.shape[0])
    mfccs = ss.transform(mfccs)
    preds = voice_detection.predict(mfccs, verbose = 0)
    pos = np.argmax(preds)
    id = asociar_id(pos)
    return id

def takeAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source, duration = 0.2)
        #r.pause_threshold = 1
        audio = r.listen(source)
    return audio

def takeCommand():
    r = sr.Recognizer()
    while True:
        try:
            audio = takeAudio()
            persona = reconocer_persona(audio)
            print("Reconociendo...")    
            query = r.recognize_google(audio, language='es-MX')
            print(f"Usted dijo: {query}\n")
            return query, persona
        except:
            print("No entendí, ¿podrías repetirlo?...")
            continue

def asociar_id(pos):
    sql = "SELECT id_persona FROM personas"
    cur.execute(sql)
    ids = cur.fetchall()
    ids = np.concatenate(ids)
    return ids[pos]

def speak(audio):
    engine.say(audio)    
    engine.runAndWait()

def abrir_youtube(sys):
    if(sys == 'Linux'):
        firefox_path = '/usr/bin/firefox %s'
    else:
        firefox_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(firefox_path).open("youtube.com") 

def buscar_wikipedia():
    query = "no funciona"
    while query == 'no funciona':
        print('entre')
        query, _ = takeCommand().lower()
        if query != 'no funciona':
            break
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("De acuerdo a wikipedia")
        print(results)
        speak(results) 
    except wikipedia.DisambiguationError as e:
        speak('Múltiples resultados. ¿Cuál buscas?')
        num = 1
        for opcion in e.options:
            print(f'{num}. {opcion}')
            num += 1
        buscar_wikipedia()

def abrir_google(sys):
    if(sys == 'Linux'):
        firefox_path = '/usr/bin/firefox %s'
    else:
        firefox_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(firefox_path).open("google.com") 
 
def username():
    speak("¿Cómo debería llamarlo, amo?")
    uname, _ = takeCommand()
    speak(f"Bienvenido, {uname}")
    #speak(uname)
    print("Bienvenido", uname)

    speak("¿Como podría ayudarle?")
    print("¿Cómo podría ayudarle?")

def presentacion_powerpoint():
    speak("Abriendo powerpoint")
    power = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/PowerPoint.lnk"
    os.startfile(power)

def word():
    speak("Abriendo word")
    dragon = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Word.lnk"
    os.startfile(dragon)

def saludo(persona):
    sql = "SELECT nombre FROM personas WHERE id_persona = ?"
    cur.execute(sql, [persona])
    nombre = cur.fetchall()
    speak(f"Hola, {nombre[0][0]}. ¿Qué puedo hacer por ti?")
