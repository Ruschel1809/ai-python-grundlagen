import spacy
from nltk.tokenize import sent_tokenize, word_tokenize

nlp = spacy.load("de_core_news_sm")
# a) Text einlesen
text = """
Ich liebe es, im Herbst spazieren zu gehen.
Es regnet schon wieder, wie deprimierend.
Heute ist ein großartiger Tag!
"""

# b) Text in Sätze und Wörter tokenisieren mit NLTK
sentences = sent_tokenize(text, language='german')
print("Sätze:")
for s in sentences:
    print(s)

words = word_tokenize(text, language='german')
print("\nTokenisierte Wörter:")
print(words)

# c) Sentiment-Analyse mit einfacher Positiv-/Negativwortliste
positive_words = ['liebe', 'großartig', 'schön', 'freue', 'glücklich']
negative_words = ['deprimierend', 'hasse', 'traurig', 'schlecht', 'wütend']

positive_count = 0
negative_count = 0

for word in words:
    word_lower = word.lower()
    if word_lower in positive_words:
        positive_count += 1
    elif word_lower in negative_words:
        negative_count += 1

print("Anzahl positiver Wörter:", positive_count)
print("Anzahl negativer Wörter:", negative_count)

# d) Lemmatisierung mit spaCy
doc = nlp(text)
print("Lemmatisierte Wörter:")
for token in doc:
    if not token.is_punct and not token.is_space:
        print(f"{token.text} --> {token.lemma_}")

# e) Stimmung bestimmen
if positive_count > negative_count:
    sentiment = "Positive Stimmung"
elif negative_count > positive_count:
    sentiment = "Negative Stimmung"
else:
    sentiment = "Neutrale Stimmung"

print("\nGesamteinschätzung der Stimmung:", sentiment)

