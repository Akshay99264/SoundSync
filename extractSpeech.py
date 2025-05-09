import whisper
import sys
import csv
import gc
from convertCSVtoSTR import convertToString

def extract_words_with_timestamps(model, audio_path, output_csv):

    # Enable word-level timestamps
    result = model.transcribe(audio_path, word_timestamps=True)

    words_with_timestamps = []

    for segment in result.get("segments", []):  # Use .get() to prevent KeyError
        for word_info in segment.get("words", []):  
            # Debugging: Print the entire word_info structure
            print(f"DEBUG: {word_info}")

            # Extract word information safely
            word = word_info.get("word", "UNKNOWN")  # Default to "UNKNOWN" if missing
            start_time = word_info.get("start", -1)  # Default to -1 if missing
            end_time = word_info.get("end", -1)  # Default to -1 if missing
            prob = word_info.get("probability", 0) # Default to 0 if missing

            # Only add valid entries
            if word != "UNKNOWN" and start_time != -1 and end_time != -1 and prob != -1:
                words_with_timestamps.append([word])
            else:
                print(f"Skipping due to missing values: {word_info}")

    # Write to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        writer.writerows(words_with_timestamps)

    str_text = convertToString(output_csv)
    return str_text

def extractSpeech(input_file1, input_file2):
    model = whisper.load_model("small")
    output_file1 = input_file1.split('.')[0] + '.csv'
    output_file2 = input_file2.split('.')[0] + '.csv'
    extracted_string_1 = extract_words_with_timestamps(model, input_file1, output_file1)
    extracted_string_2 = extract_words_with_timestamps(model, input_file2, output_file2)
    del model
    gc.collect()
    return extracted_string_1, extracted_string_2
