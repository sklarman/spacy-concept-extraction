import spacy
import csv
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import re
import string
from flask import Flask
from flask import Response
from flask import request
import json

nlp = spacy.load('en_core_web_sm') 
matcher = PhraseMatcher(nlp.vocab)

concept_ids = {}
concept_labels = {}
concept_source = {}
concept_spacy_ids = {}
stopwords=[]

def normalise_white_space(word):
    word = word.rstrip()
    word = word.lstrip()
    word = re.sub(' +',' ', word)
    return word
    
def shallow_clean(label):
    label = normalise_white_space(label).lower()
    for char in string.punctuation:
        label = label.replace(char, ' ')
    label = normalise_white_space(label)
    return label

def add_to_matcher(label, i):
    if label not in concept_spacy_ids:
        word_list = []
        word_list.append(label)
        concept_pattern = [nlp(text) for text in word_list]
        matcher.add(i, None, *concept_pattern)
        concept_spacy_ids[label]=[i]
    else:
        concept_spacy_ids[label].append(i)

def load_concepts():
    print("\n\nLoading concepts...")

    with open('sources.json') as f:
        sources = json.load(f)

    concept_list = csv.DictReader(open("labels.csv", encoding="utf8"), delimiter=",")

    i = 1
    for concept in concept_list:
        if len(concept["label"]) < 30:
            label = concept["label"].lower()
            add_to_matcher(label, i)
            concept_ids[i]=concept["id"]
            concept_labels[i]=concept["label"]
            plural = ""
            if not label.endswith("s"):
                if label.endswith("y"):
                    plural = concept["label"].lower()[:-1] + "ies"
                else:
                    plural = concept["label"].lower() + "s"
                add_to_matcher(plural, i)
            for source in sources:
                if source in concept["id"]:
                    concept_source[i] = source
        i += 1
        if i > 0 and i % 1000 == 0: 
            print(i / 1000)

    print("\n\nLoading stopwords...")

    stopword_records = csv.DictReader(open("stopwords.csv", encoding="utf8"), delimiter=",")
    for word in stopword_records:
        stopwords.append(word['label'])

def update_matches(start, end, match_id, current_matches):
    label = concept_labels[match_id].lower()
    returned_matches = []
    returned_matches.extend(current_matches)
    if not (label in stopwords):
        for match in current_matches:
            if match['start']<=start and match['end']>=end and label in match['label'] and not (match['label'] in label) and concept_source[match_id] in match['url']:
               return returned_matches
            if match['start']>=start and match['end']<=end and match['label'] in label and not (label in match['label']) and concept_source[match_id] in match['url']:
                returned_matches.remove(match)
        new_match = {'url': concept_ids[match_id], 'label': label, 'start': start, 'end': end}
        returned_matches.append(new_match)
    return returned_matches

def extract_concepts(input):
    text = shallow_clean(input)
    final_matches = []
    doc = nlp(text)
    matches = matcher(doc)
    int_matches = []
    for match_id, start, end in matches:
        for match_all_id in concept_spacy_ids[concept_labels[match_id]]:
            int_matches = update_matches(start, end, match_all_id, int_matches)
    for match in int_matches:
        final_matches.append(match)
    return {"text": text, "matches": final_matches}

load_concepts()

app = Flask(__name__)

@app.route("/", methods=['POST'])
def main():
    input_text = request.get_json()["text"]
    print(input_text)
    resp = Response(json.dumps(extract_concepts(input_text)), mimetype='application/json')
    return resp

app.run(host="0.0.0.0", port=5000)
