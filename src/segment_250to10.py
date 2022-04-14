import os
import numpy as np
from config import *
from plot import *
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import librosa
from multiprocessing import Pool
import warnings
import soundfile as sf

warnings.filterwarnings(action='ignore')

def select_data(file):
    if not file.startswith('.') and file.endswith('.WAV'):
        return True
    else:
        return False

def add_zero(data):
    data[-1] = 0
    return data

def save_segments(file_name, new):
    print(file_name)
    sf.write(file_name, new, sampling_rate)

def segment_audio(file):
    data, sr = librosa.load(data_path+file, sampling_rate)
    for idx in range(n_segment):
        new = add_zero(data[n_points*idx:n_points*(idx+1)])
        save_segments(save_path+(file.split('.')[0])+f'_{idx+1}.wav', new)
    
if __name__ == '__main__':
    files = [f for f in os.listdir(data_path) if select_data(f)]
    with Pool(30) as p:
        p.map(segment_audio, files)

