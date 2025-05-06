import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pesq import pesq
from scipy.signal import resample_poly
import csv
def calculate_mse(y1, y2, sr1, sr2, target_sr):
    y1_resampled = resample_poly(y1, target_sr, sr1)
    y2_resampled = resample_poly(y2, target_sr, sr2)
    max_length = max(len(y1_resampled), len(y2_resampled))
    y1_padded = np.pad(y1_resampled, (0, max_length - len(y1_resampled)), 'constant')
    y2_padded = np.pad(y2_resampled, (0, max_length - len(y2_resampled)), 'constant')
    S1 = np.abs(librosa.stft(y1_padded))
    S2 = np.abs(librosa.stft(y2_padded))
    S1_db = librosa.amplitude_to_db(S1, ref=np.max)
    S2_db = librosa.amplitude_to_db(S2, ref=np.max)
    min_freq = 100
    max_freq = 4000
    frequencies = librosa.fft_frequencies(sr=sr1)
    freq_indices = np.where((frequencies >= min_freq) & (frequencies <= max_freq))[0]
    S1_db_voice = S1_db[freq_indices, :]
    S2_db_voice = S2_db[freq_indices, :]
    if S1_db_voice.shape != S2_db_voice.shape:
        scale_factor = S2_db_voice.shape[1] / S1_db_voice.shape[1]
        S1_db_voice = zoom(S1_db_voice, (1, scale_factor), order=1)
    mse = np.mean((S1_db_voice - S2_db_voice) ** 2)

    return mse

def MSE(file1, file2):
    y1, sr1 = librosa.load(file1, sr=None)
    y2, sr2 = librosa.load(file2, sr=None)
    target_sr = 16000
    mse = calculate_mse(y1, y2, sr1, sr2, target_sr)
    if mse is None:
        mse = 'N/A'
    
    return mse