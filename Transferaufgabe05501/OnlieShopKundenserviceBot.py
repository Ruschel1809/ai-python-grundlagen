import random
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from simpletransformers.classification import ClassificationModel
import pandas as pd

# Templates mit Synonymen
templates = {
    "produkt": [
        ["Ich", "Ich hätte gern", "Könnten Sie mir"],
        ["mehr Informationen", "Details", "eine Beschreibung"],
        ["zu", "über"],
        ["diesem Produkt", "dem Artikel", "dem Produkt"]
    ],
    "versand": [
        ["Wie lange", "Wann", "In welchem Zeitraum"],
        ["kommt", "erhalte ich", "wird geliefert"],
        ["meine Bestellung", "mein Paket", "die Ware"]
    ],
    "rücksendung": [
        ["Wie kann ich", "Was muss ich tun, um", "Ist es möglich"],
        ["eine Rücksendung", "eine Retoure", "den Artikel zurückzuschicken"],
        ["durchzuführen", "anzumelden", "zu machen"]
    ]
}


# Satzgenerator
def generate_sentence(template_parts):
    return " ".join(random.choice(part) for part in template_parts) + "?"


# Dialog-Generator
def generate_dialogs(num_dialogs=100):
    dialogs = []
    categories = list(templates.keys())

    for _ in range(num_dialogs):
        category = random.choice(categories)
        user_input = generate_sentence(templates[category])
        bot_response = f"[Antwort auf {category}-Frage]"  # Platzhalter
        dialogs.append({
            "category": category,
            "dialog": [
                {"role": "user", "content": user_input},
                {"role": "bot", "content": bot_response}
            ]
        })
    return dialogs


def evaluate_data(dialogs):
    total_dialogs = len(dialogs)

    # 1. Vollständigkeit prüfen
    incomplete = [d for d in dialogs if len(d["dialog"]) != 2]
    completeness = 100 * (1 - len(incomplete) / total_dialogs)

    # 2. Klassenverteilung zählen
    category_counts = Counter(d["category"] for d in dialogs)

    # 3. Formulierungsvielfalt
    unique_user_inputs = set(d["dialog"][0]["content"] for d in dialogs)
    diversity = len(unique_user_inputs)

    # Bericht ausgeben
    print("Datenqualitätsbericht")
    print("------------------------")
    print(f"Anzahl der Dialoge: {total_dialogs}")
    print(f"Vollständige Dialoge: {completeness:.1f}%")
    print("\nKlassenverteilung:")
    for category, count in category_counts.items():
        print(f"  - {category}: {count} Dialoge")
    print(f"\nEinzigartige Benutzerfragen: {diversity}")


# Funktion zum Trainieren & Bewerten
def train_and_evaluate(C_value=1.0, max_features=1000):
    print(f"\nTraining mit C={C_value}, max_features={max_features}")

    # Textvektorisierung
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Modell
    model = LogisticRegression(C=C_value, max_iter=200)
    model.fit(X_train_vec, y_train)

    # Vorhersage & Bewertung
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Genauigkeit: {acc:.2f}")
    print("Klassifikationsbericht:")
    print(classification_report(y_test, y_pred))

    return model, vectorizer


# Generierung starten
dialogs = generate_dialogs(100)

# Optional: Beispielausgabe
for i in range(3):
    print(f"Dialog {i + 1}:")
    for turn in dialogs[i]['dialog']:
        print(f"{turn['role']}: {turn['content']}")
    print()

evaluate_data(dialogs)

#   Trainingsdaten vorbereiten
X = [d["dialog"][0]["content"] for d in dialogs]  # Eingaben (Texte)
y = [d["category"] for d in dialogs]  # Labels (Kategorien)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardparameter
model1, vec1 = train_and_evaluate(C_value=1.0, max_features=1000)

# Alternativer Versuch (stärkere Regularisierung & weniger Features)
model2, vec2 = train_and_evaluate(C_value=0.3, max_features=500)

# Daten vorbereiten im DataFrame-Format
train_data = pd.DataFrame({
    "text": [d["dialog"][0]["content"] for d in dialogs[:80]],
    "labels": [0 if d["category"] == "produkt" else 1 if d["category"] == "versand" else 2 for d in dialogs[:80]]
})

eval_data = pd.DataFrame({
    "text": [d["dialog"][0]["content"] for d in dialogs[80:]],
    "labels": [0 if d["category"] == "produkt" else 1 if d["category"] == "versand" else 2 for d in dialogs[80:]]
})

# Modell initialisieren (DistilBERT)
model = ClassificationModel(
    "distilbert",
    "distilbert-base-uncased",
    num_labels=3,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 3,
        "train_batch_size": 8,
        "eval_batch_size": 8,
        "evaluate_during_training": True,
        "use_multiprocessing": False,
        "logging_steps": 10,
        "output_dir": "./outputs/",
    }
)

# Trainieren
model.train_model(train_data, eval_df=eval_data)

# Evaluation
result, model_outputs, wrong_predictions = model.eval_model(eval_data)

print(f"Evaluation Accuracy: {result['eval_accuracy']:.2f}")
