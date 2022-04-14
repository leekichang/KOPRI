import os
import librosa
import warnings
import numpy as np
import soundfile as sf
from config import *
from multiprocessing import Pool

warnings.filterwarnings(action='ignore')

def select_data(file):
    if not file.startswith('.') and file.endswith('.wav'):
        return True
    else:
        return False

def save_segments(file_name, new):
    print(file_name)
    sf.write(file_name, new, sampling_rate)

def segment_audio(file):
    data, sr = librosa.load(data_path+file, sampling_rate)
    for idx in range(n_segment):
        new = data[n_points*idx:n_points*(idx+1)]
        save_segments(save_path+(file.split('.')[0])+f'_{idx+1}.wav', new)

if __name__ == '__main__':
    files = [f for f in os.listdir(data_path) if select_data(f)]
    for file in files:
        segment_audio(file)
    # with Pool(30) as p:
    #     p.map(segment_audio, files)
        