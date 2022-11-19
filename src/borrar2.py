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
import pickle
import warnings
#from keras.models import load_model

def haz_algo():
    ss = pickle.load(open('scaler.pkl','rb'))
