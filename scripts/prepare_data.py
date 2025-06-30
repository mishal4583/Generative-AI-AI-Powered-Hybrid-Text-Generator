import re
import json
import spacy

# Load SpaCy for sentence splitting
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    # Remove unwanted characters and extra spaces
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'[^A-Za-z0-9,.?!;:\'\" \n]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'Chapter \d+', '', text, flags=re.IGNORECASE)
    return text.strip()

def split_into_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]

# ---- Load and clean .txt files ----
with open("data/1342-0.txt", "r", encoding="utf-8") as f:
    pride_raw = f.read()
with open("data/84-0.txt", "r", encoding="utf-8") as f:
    frankenstein_raw = f.read()
with open("data/sonnets.txt", "r", encoding="utf-8") as f:
    sonnets_raw = f.read()

# Clean the text
pride_clean = clean_text(pride_raw)
frankenstein_clean = clean_text(frankenstein_raw)
sonnets_clean = clean_text(sonnets_raw)

# Split into sentences (only for pride/frankenstein)
pride_sents = split_into_sentences(pride_clean)
frankenstein_sents = split_into_sentences(frankenstein_clean)

# Save cleaned files
with open("outputs/pride_sentences.txt", "w") as f:
    f.write("\n".join(pride_sents))

with open("outputs/frankenstein_sentences.txt", "w") as f:
    f.write("\n".join(frankenstein_sents))

with open("outputs/sonnets_clean.txt", "w") as f:
    f.write(sonnets_clean)

# ---- Load moods.json ----
with open("data/moods.json", "r") as f:
    moods_data = json.load(f)

moods_list = moods_data["moods"]

# Save mood words as a text file
with open("outputs/moods_list.txt", "w") as f:
    f.write("\n".join(moods_list))

print("✅ All files cleaned and saved.")
