class SimpleChatbot:
    def __init__(self):
        self.greetings = ["hallo", "hi", "guten tag", "hey"]
        self.cities = ["berlin", "münchen", "hamburg", "köln"]

    def process_input(self, user_input):
        user_input_lower = user_input.lower()

        # Schritt 1: Regelbasierte Begrüßung
        if self.is_greeting(user_input_lower):
            return self.respond_to_greeting()

        # Schritt 2: Intent-Erkennung "Wetter"
        elif self.is_weather_question(user_input_lower):
            return self.respond_to_weather(user_input_lower)

        # Schritt 3: Unbekannte Eingabe
        else:
            return "Das habe ich leider nicht verstanden. Können Sie das anders formulieren?"

    def is_greeting(self, text):
        return any(greeting in text for greeting in self.greetings)

    def respond_to_greeting(self):
        return "Hallo! Wie kann ich Ihnen helfen?"

    def is_weather_question(self, text):
        return "wetter" in text and any(city in text for city in self.cities)

    def respond_to_weather(self, text):
        for city in self.cities:
            if city in text:
                return f"In {city.capitalize()} ist es heute sonnig."
        return "Für diese Stadt habe ich leider keine Wetterinformationen."

# Chatbot erstellen
bot = SimpleChatbot()

# Testfälle
eingaben = [
    "Hallo",
    "Guten Tag",
    "Wie ist das Wetter in Berlin?",
    "Sag mir das Wetter für Köln",
    "Was kannst du?",
    "Wie ist das Wetter in Zürich?"  # Stadt nicht in Liste
]

# Chatbot ausführen
for eingabe in eingaben:
    antwort = bot.process_input(eingabe)
    print(f"Nutzer: {eingabe}")
    print(f"Bot: {antwort}")
    print("-" * 30)
