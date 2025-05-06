import librosa
import numpy as np
import soundfile as sf
from pystoi.stoi import stoi

def load_audio(file_path, target_sr=16000):
    audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
    return audio, sr

def pad_audio(audio1, audio2):
    len1, len2 = len(audio1), len(audio2)
    
    if len1 > len2:
        audio2 = np.pad(audio2, (0, len1 - len2), mode='constant')
    elif len2 > len1:
        audio1 = np.pad(audio1, (0, len2 - len1), mode='constant')
    
    return audio1, audio2

def calculate_stoi(reference_file, test_file):
    # Load both audio files
    ref_audio, sr_ref = load_audio(reference_file)
    test_audio, sr_test = load_audio(test_file, target_sr=sr_ref)  # Ensure same SR

    # Pad both audio signals to match in length
    ref_audio, test_audio = pad_audio(ref_audio, test_audio)

    # Compute STOI score
    stoi_score = stoi(ref_audio, test_audio, sr_ref, extended=False)
    print(f"STOI Score: {stoi_score:.4f}")
    return stoi_score


def STOI(file1, file2):
    stoi_score = calculate_stoi(file1, file2)
    return stoi_score

