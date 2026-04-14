# deutsches Sprachmodell herunterladen
# python -m spacy download de_core_news_sm
# Kleines Modell
# python -m spacy download de_core_news_lg # Großes Modell mit Word Vectors
# spaCy folgt einer anderen Philosophie und lädt Sprachmodelle als separate Pakete
import spacy
# Deutsches Sprachmodell laden
nlp = spacy.load('de_core_news_sm')
# Text verarbeiten
text = "spaCy macht NLP-Pipelines einfach und effizient."
doc = nlp(text)
# Alle Informationen in einem Durchgang
for token in doc:
    print(f"{token.text} | {token.lemma_} | {token.pos_} | {token.is_stop}")
# Named Entity Recognition
for ent in doc.ents:
    print(f"{ent.text} ({ent.label_})")