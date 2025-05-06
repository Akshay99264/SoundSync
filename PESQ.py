import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pesq import pesq
from scipy.signal import resample_poly
import csv
def calculate_pesq(y1, y2, sr1, sr2, target_sr):
    y1_resampled = resample_poly(y1, target_sr, sr1)
    y2_resampled = resample_poly(y2, target_sr, sr2)
    max_length = max(len(y1_resampled), len(y2_resampled))
    y1_padded = np.pad(y1_resampled, (0, max_length - len(y1_resampled)), 'constant')
    y2_padded = np.pad(y2_resampled, (0, max_length - len(y2_resampled)), 'constant')
    try:
        pesq_score = pesq(target_sr, y1_padded, y2_padded, mode='wb')
    except Exception as e:
        pesq_score = None
        print(f"Error calculating PESQ: {e}")

    return pesq_score

def PESQ(file1, file2):
    y1, sr1 = librosa.load(file1, sr=None)
    y2, sr2 = librosa.load(file2, sr=None)
    target_sr = 16000
    pesq_score = calculate_pesq(y1, y2, sr1, sr2, target_sr)
    if pesq_score is None:
            pesq_score = 'N/A'
    
    return pesq_score