class SimpleRestaurantBot:
    def __init__(self):
        self.rules = [
            (["öffungszeit", "öffnungszeiten","öffnen", "geöffnet", "offen"],"Unser Restaurant ist täglich von 12:00 bis 23:00 Uhr geöffnet."),
            (["speisekarte", "menü", "essen"],"Unsere Speisekarte finden Sie auf unserer Website unter www.beispielrestaurant.de/speisekarte.")
        ]
    def respond_to_user_input(self,user_input: str):
        input_lower = user_input.lower()
        for keywords, response in self.rules:
            if any(keyword in input_lower for keyword in keywords):
                return response
        return "Entschuldigung, das habe ich nicht verstanden"

bot = SimpleRestaurantBot()
print(f"Öffnungszeit mit geöffnet: {bot.respond_to_user_input("Wann habt ihr geöffnet?")}")
print(f"Öffnungszeit mit offen: {bot.respond_to_user_input("Wann hat euer Laden offen")}")
print(f"Öffnungszeit mit Öffnungszeiten: {bot.respond_to_user_input("Wie sind eure Öffnungszeiten")}")
print(f"Speisekarte mit Essen: {bot.respond_to_user_input("Was gibt es heute zu Essen?")}")
print(f"Speisekarte mit Speisekarte: {bot.respond_to_user_input("Wo finde ich eure Speisekarte?")}")
print(f"QuickQuack Blib Blobb: {bot.respond_to_user_input("QuickQuack Blib Blobb")}")
