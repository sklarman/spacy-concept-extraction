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

def addToMatcher(label, i):
    word_list = []
    word_list.append(label)
    concept_pattern = [nlp(text) for text in word_list]
    matcher.add(i, None, *concept_pattern)

def loadConcepts():
    print("\n\n\nLoading concepts...")

    with open('sources.json') as f:
        sources = json.load(f)

    concept_list = csv.DictReader(open("labels.csv", encoding="utf8"), delimiter=",")

    i = 0
    for concept in concept_list:
        if len(concept["label"]) < 30:
            addToMatcher(concept["label"].lower(), i)
            concept_ids[i]=concept["id"]
            concept_labels[i]=concept["label"]
            plural = ""
            if concept["label"].lower().endswith("y"):
                plural = concept["label"].lower()[:-1] + "ies"
            else:
                plural = concept["label"].lower() + "s"
            addToMatcher(plural, i)
            for source in sources:
                if source in concept["id"]:
                    concept_source[i] = source
        i += 1
        if i > 0 and i % 1000 == 0: 
            print(i / 1000)

    print("\n\n\nLoading stopwords...")

    stopword_records = csv.DictReader(open("stopwords.csv", encoding="utf8"), delimiter=",")
    for word in stopword_records:
        stopwords.append(word['label'])

def updateMatches(start, end, match_id, prod_matches):
    if not (concept_labels[match_id].lower() in stopwords):
        for match in prod_matches:
            if concept_labels[match_id].lower() in match['label'] and not (match['label'] in concept_labels[match_id].lower()):
                return prod_matches
            if match['label'] in concept_labels[match_id].lower() and not (concept_labels[match_id].lower() in match['label']):
                prod_matches.remove(match) 
        newMatch = {'url': concept_ids[match_id], 'label': concept_labels[match_id].lower(), 'start': start, 'end': end}
        prod_matches.append(newMatch)
    return prod_matches

def extract_concepts(input):
    text = shallow_clean(input)
    final_matches = []
    doc = nlp(text)
    matches = matcher(doc)
    int_matches = []
    for match_id, start, end in matches:
        int_matches = updateMatches(start, end, match_id, int_matches)
    for match in int_matches:
        final_matches.append(match)
    return {"text": text, "matches": final_matches}

loadConcepts()

app = Flask(__name__)

@app.route("/", methods=['POST'])
def main():
    input_text = request.get_json()["text"]
    print(input_text)
    resp = Response(json.dumps(extract_concepts(input_text)), mimetype='application/json')
    return resp

app.run(host="0.0.0.0", port=5000)
