# Evaluation-of-Audio-Quality-and-Speech-Intelligibility-Using-PESQ-MSE-STOI-WER-and-CER-Metrics
This project compares audio quality and intelligibility using standardized metrics: PESQ, MSE, STOI, WER, and CER. It evaluates the impact of audio processing techniques like noise removal and enhancement, providing insights for improving speech quality in applications like VoIP and speech recognition systems.

## 📁 Project Structure

- `home.py` – Main script to launch the application and display audio details.
- `preprocessingAudio.py` – Handles preprocessing of audio files.
- `extractSpeech.py` – Extracts speech segments and logs relevant parameters.
- `MSE.py` – Calculates Mean Squared Error; handles cases when score can't be computed.
- `PESQ.py` – Computes PESQ (Perceptual Evaluation of Speech Quality) scores.
- `STOI.py` – Computes Short-Time Objective Intelligibility.
- `WER_CER.py` – Calculates Word Error Rate (WER) and Character Error Rate (CER).
- `convertCSVtoSTR.py` – Converts CSV files to string format.
- `requirements.txt` – List of all dependencies needed to run the project.

## 🚀 How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/Akshay99264/SoundSync.git
   cd SoundSync
2. pip install -r requirements.txt
3. python home.py

