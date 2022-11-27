import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Escuchando...")
    r.adjust_for_ambient_noise(source, duration = 0.3)
    r.pause_threshold = 5
    audio = r.listen(source)
    query = r.recognize_google(audio, language='es-MX')
    print(f"Usted dijo: {query}\n")
with open("gerardo.wav", "wb") as f:
    f.write(audio.get_wav_data())
    f.close() 


#clip = "C:/Users/e-gm9/56/Códigos/voice_assistant-1/chunked/bencomo_9.wav"

""" #Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Audio file as source
# listening the audio file and store in audio_text variable

with sr.AudioFile(clip) as source:
    audio_text = r.record(source)

text = r.recognize_google(audio_text)
print(text) """