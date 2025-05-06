import librosa
import numpy as np
import soundfile as sf
from pystoi.stoi import stoi

def load_audio(file_path):
    audio, sr = librosa.load(file_path)
    return audio

def pad_audio(audio1, audio2):
    len1, len2 = len(audio1), len(audio2)
    
    if len1 > len2:
        audio2 = np.pad(audio2, (0, len1 - len2), mode='constant')
    elif len2 > len1:
        audio1 = np.pad(audio1, (0, len2 - len1), mode='constant')
    
    return audio1, audio2

def calculate_stoi(reference_file, test_file):
    # Load both audio files
    ref_audio = load_audio(reference_file)
    test_audio = load_audio(test_file)  # Ensure same SR

    # Pad both audio signals to match in length
    ref_audio, test_audio = pad_audio(ref_audio, test_audio)

    # Compute STOI 
    try:
        stoi_score = stoi(ref_audio, test_audio, 16000, extended=False)
    except Exception as e:
        stoi_score = None
        print(f"Error calculating STOI: {e}")

    if stoi_score is None:
        stoi_score = 'N/A'

    return stoi_score


def STOI(file1, file2):
    stoi_score = calculate_stoi(file1, file2)
    return stoi_score

