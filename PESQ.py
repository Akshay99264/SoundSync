import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pesq import pesq
from scipy.signal import resample_poly
import csv
def calculate_pesq(y1, y2):
    max_length = max(len(y1), len(y2))
    y1_padded = np.pad(y1, (0, max_length - len(y1)), 'constant')
    y2_padded = np.pad(y2, (0, max_length - len(y2)), 'constant')
    try:
        pesq_score = pesq(16000, y1_padded, y2_padded, mode='wb')
    except Exception as e:
        pesq_score = None
        print(f"Error calculating PESQ: {e}")

    return pesq_score

def PESQ(file1, file2):
    y1, sr1 = librosa.load(file1, sr=None)
    y2, sr2 = librosa.load(file2, sr=None)
    target_sr = 16000
    pesq_score = calculate_pesq(y1, y2)
    if pesq_score is None:
            pesq_score = 'N/A'
    
    return pesq_score