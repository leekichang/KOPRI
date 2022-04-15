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
    #s1  = time.time()
    data, sr = librosa.load('../segmented_audio(10sec)/'+file, 32768)
    #s2  = time.time()
    #print(f'data loading took {s2-s1:.4f} sec')
    spectrogram = get_spectrogram(data)
    #s3 = time.time()
    #print(f'spectrogram took {s3-s2:.4f} sec')
    save_spectrogram(spectrogram, file)
    #s4 = time.time()
    #print(f'saving took {s4-s3:.4f} sec')

if __name__ == '__main__':
    chunk_size = 1000
    args = parse_args()
    start = time.time()
    files = os.listdir('../segmented_audio(10sec)/')
    files = files[args.set*chunk_size:(args.set+1)*chunk_size]
    with Pool(6) as p:
        p.map(mp_get_spectrogram, files)
    end = time.time()
    print(f'{args.set+1}/513 done in {end-start} sec')



'''
1000개 처리 속도 비교
naive : 51.53179430961609 (sec)
mp 4  : 21.0592942237854  (sec)  
mp 5  : 16.247143983840942(sec)
mp 6  : 14.058369636535645(sec)
mp 7  : 14.659644365310669(sec)
mp 30 : 49.77599549293518
mp6 하나
4/15 03:26 시작
4/15 03:30 3700개
4/15 03:35 9200개

chunk 8개로 나눠서 시작
4/15 03:42 시작
4/15 03:45 5000개

shell script 작업
4/15 03:57 시작
4/15 04:07 10000개
4/15 04:25 24000개
4/15 04:35 28000개
'''

