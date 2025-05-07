import os
import csv
import re
from jiwer import wer
import numpy as np
def levenshtein_distance(ref, hyp):
    m, n = len(ref), len(hyp)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]
                )
    return dp[m][n]

def CER(str_1, str_2):
    ref_chars = str_1.replace(" ", "")
    hyp_chars = str_2.replace(" ", "")
    raw_cer = levenshtein_distance(ref_chars, hyp_chars) / max(1, len(ref_chars))
    cer = min(1.0, max(0.0, raw_cer))
    return cer



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