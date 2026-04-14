# pip install nltk
import nltk
# Grundlegende Ressourcen herunterladen
nltk.download('punkt')
# Tokenizer
nltk.download('stopwords')
# Stopwörter
nltk.download('averaged_perceptron_tagger')
# POS-Tagger
nltk.download('wordnet')
nltk.download('punkt_tab')
#VADER
nltk.download('vader_lexicon')
# WordNet für Lemmatisierung
# Oder alle Ressourcen (ca. 3GB)
# nltk.download('all')
# Erste Schritte mit NLTK
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
text = "NLTK ist eine mächtige Bibliothek für Natural Language Processing."
# Tokenisierung
tokens = word_tokenize(text, language='german')
sentences = sent_tokenize(text, language='german')
print("Wörter:", tokens)
print("Sätze:", sentences)
# Stopwörter entfernen
german_stopwords = set(stopwords.words('german'))
filtered_tokens = [word for word in tokens if word.lower() not in
german_stopwords]
print("Ohne Stopwörter:", filtered_tokens)