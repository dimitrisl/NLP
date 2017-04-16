import spacy
from spacy.cli import download

try:
    spacy.load('en')
except Exception as e:
    print(e)
    download('en')
