import asyncio

import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator


text = """
Ich liebe es, im Herbst spazieren zu gehen, das ist hammer.
Pfff, es regnet schon wieder, wie deprimierend.
Wow, heute ist ein großartiger Tag!
Ich gehe einkaufen.
Ich wasche Wäsche.
Der Hund frisst Hundefutter.
"""

# a) Verwende spaCy, um einen deutschen Text zu tokenisieren und die Tokens auszugeben. Wähle einen kurzen Text deiner Wahl.
nlp = spacy.load("de_core_news_sm")

doc = nlp(text)
print("Lemmatisierte Wörter:")
for token in doc:
    if not token.is_punct and not token.is_space:
        print(f"{token.text} --> {token.lemma_}")

# b) Führe eine einfache Sentiment-Analyse mit einem vorgegebenen Satz durch, indem du NLTK’s VADER-Modul verwendest. Da VADER primär für englische Texte entwickelt wurde, übersetze den deutschen Satz zuerst ins Englische.
# Beispiel mit einem vereinfachten Sentiment-Lexikon
sia = SentimentIntensityAnalyzer()

# Erweiterung des vaderLexikons
new_words = {"wow" : 2.5,
             "pfff" : -3.0,
             "pfft" : -3.0}
sia.lexicon.update(new_words)

async def translate(text: str) -> str:
    translator = Translator()
    trans = await translator.translate(text, src = 'de', dest='en')
    return trans.text

translated = asyncio.run(translate(text))
print(translated)

# Sentiment-Analyse
score = sia.polarity_scores(translated)
print(score)

compound = score['compound']
if compound >= 0.05:
    sentiment = "positiv"
elif compound <= -0.05:
    sentiment = "negativ"
else:
    sentiment = "neutral"
print("Die Stimmung ist: ", sentiment)
