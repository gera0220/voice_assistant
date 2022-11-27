from pydub import AudioSegment 
from pydub.utils import make_chunks
import os

#os.chdir('data/raw')

def process_audio(file_name):
    myaudio = AudioSegment.from_file(file_name, "wav") 
    chunk_length_ms = 5000 # pydub calculates in millisec 
    chunks = make_chunks(myaudio, chunk_length_ms) 
    for i, chunk in enumerate(chunks): 
        #chunk_name = './chunked/' + file_name + "_{0}.wav".format(i) 
        chunk_name = './chunked/' + file_name.split('.')[0] + "_{0}.wav".format(i) 
        print ("exporting", chunk_name) 
        chunk.export(chunk_name, format="wav") 

all_file_names = os.listdir()

try:
    os.makedirs('chunked') 
except:
    pass
for each_file in all_file_names:
    if ('.wav' in each_file):
        process_audio(each_file)