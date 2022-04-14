import os
import librosa, librosa.display
import numpy as np
from numba import njit, prange
import warnings
from multiprocessing import Pool
import argparse
import time
warnings.filterwarnings(action='ignore')

def parse_args():
    parser = argparse.ArgumentParser(description='preprocessing KOPRI data')
    
    parser.add_argument('--set', default = 0, type = int)
    args = parser.parse_args()    
    return args

def get_spectrogram(data, sr = 32768, hop_length = 256, n_fft = 1023):
    hop_length_duration = float(hop_length) / sr
    n_fft_duration = float(n_fft) / sr
    stft = librosa.stft(data, n_fft=n_fft, hop_length=hop_length)
    magnitude = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(magnitude)
    return log_spectrogram

def save_spectrogram(log_spectrogram, file_name):
    np.save(f'../spectrogram/{file_name}.npy', log_spectrogram,)    

def mp_get_spectrogram(file):
    data, sr = librosa.load('../segmented_audio(10sec)/'+file, 32768)
    save_spectrogram(get_spectrogram(data), file)

if __name__ == '__main__':
    chunk_size = 513000
    args = parse_args()
    files = os.listdir('../segmented_audio(10sec)/')
    start = time.time()
    with Pool(6) as p:
        p.map(mp_get_spectrogram, files[args.set*chunk_size:(args.set+1)*chunk_size])
    end = time.time()
    print(end-start)



'''
1000개 처리 속도 비교
naive : 51.53179430961609
mp 4  : 21.0592942237854
mp 5  : 16.247143983840942
mp 6  : 14.058369636535645
mp 7  : 14.659644365310669
mp 8  : 
mp 30 : 49.77599549293518
4/15 03:11 3:10 2200개

'''

