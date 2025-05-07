import os
import csv
import re

def convertToString(filename):
    with open(filename, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        words = [row[0].strip() for row in reader if row]
    raw_text = ' '.join(words)
    clean_text = re.sub(r'[^A-Za-z ]+', '', raw_text)
    return clean_text