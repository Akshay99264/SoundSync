import os
import csv
import re
from jiwer import wer
import numpy as np
def interpret_quality(score):
    if score <= 0.05:
        return "Excellent"
    elif score <= 0.15:
        return "Good"
    elif score <= 0.30:
        return "Fair"
    elif score <= 0.50:
        return "Poor"
    else:
        return "Unusable"

def WER(file1, file2):
    word_error = min(1.0, max(0.0, wer(file1, file2)))

    # Quality based on WER
    quality = interpret_quality(word_error)
    return word_error, quality
