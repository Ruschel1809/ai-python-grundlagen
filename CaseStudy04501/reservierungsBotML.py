import spacy
from datetime import datetime
import re


class ReservationChatbot:
    def __init__(self):
        self.context = {}
        self.reservations = {}
        self.nlp = spacy.load("de_core_news_sm")

    def handle_message(self, user_id, message):
        if user_id not in self.context:
            self.context[user_id] = {"intent": None, "entities": {}}

        doc = self.nlp(message.lower())

        # --- Intent-Erkennung ---
        if any(tok.lemma_ in ["reservieren", "tisch"] for tok in doc):
            self.context[user_id]["intent"] = "reservation"
        elif any(tok.lemma_ in ["öffnungszeiten", "geöffnet", "zeit"] for tok in doc):
            self.context[user_id]["intent"] = "opening_hours"

        # --- Entity-Erkennung (mit Regex + NLP) ---
        date_match = re.search(r"\d{1,2}[.\-/]\d{1,2}[.\-/]\d{4}", message)
        time_match = re.search(r"\d{1,2}:\d{2}", message)
        people_match = re.search(r"(\d+)\s*(personen|gäste)", message.lower())

        if date_match:
            self.context[user_id]["entities"]["date"] = date_match.group()
        if time_match:
            self.context[user_id]["entities"]["time"] = time_match.group()
        if people_match:
            self.context[user_id]["entities"]["people"] = int(people_match.group(1))

        # --- Intelligente Antwort basierend auf Kontext ---
        intent = self.context[user_id].get("intent")
        entities = self.context[user_id]["entities"]

        if intent == "reservation":
            missing = [key for key in ["date", "time", "people"] if key not in entities]

            if not missing:
                reservation_id = self.create_reservation(user_id, entities)
                self.context[user_id] = {"intent": None, "entities": {}}  # Reset context
                return f"Reservierung erfolgreich! Ihre Reservierungsnummer ist {reservation_id}."
            else:
                missing_str = ", ".join(missing)
                return f"Könnten Sie bitte noch folgende Informationen angeben: {missing_str}?"

        elif intent == "opening_hours":
            return "Unsere Öffnungszeiten sind täglich von 10:00 bis 22:00 Uhr."

        else:
            return "Wie kann ich Ihnen helfen? Möchten Sie eine Reservierung oder unsere Öffnungszeiten wissen?"

    def create_reservation(self, user_id, entities):
        reservation_id = f"{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.reservations[reservation_id] = entities
        return reservation_id


# Beispiel zur Verwendung
if __name__ == "__main__":
    chatbot = ReservationChatbot()

    print(chatbot.handle_message("user123", "Hallo, ich möchte einen Tisch reservieren."))
    print(chatbot.handle_message("user123", "Für 4 Personen am 24.12.2025"))
    print(chatbot.handle_message("user123", "um 18:30 Uhr"))
