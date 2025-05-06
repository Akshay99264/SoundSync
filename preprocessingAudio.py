from pydub import AudioSegment
import scipy.io.wavfile as wavfile
import numpy as np
import os

def preprocess_audio(input_path):
    # Load the audio using pydub (supports many formats: mp3, wav, flac, etc.)
    filename = input_path.split('.')[0]
    output_path = filename + '.wav'
    audio = AudioSegment.from_file(input_path)

    # Convert to mono, 16 kHz, 16-bit PCM
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_sample_width(2)  # 2 bytes = 16 bits

    # Export to WAV (16-bit PCM)
    temp_wav_path = output_path if output_path.endswith('.wav') else output_path + '.wav'
    audio.export(temp_wav_path, format="wav")

    # Double-check: ensure it's int16 format (in case your PESQ tool is strict)
    rate, data = wavfile.read(temp_wav_path)
    if data.dtype != np.int16:
        data = (data * 32767).astype(np.int16)
        wavfile.write(temp_wav_path, rate, data)
    return output_path

# Example usage
preprocess_audio("audio1.mp3")
