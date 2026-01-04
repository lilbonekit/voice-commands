from config.intents import INTENTS

def detect_intent(text: str, lang: str) -> str | None:
    for intent, langs in INTENTS.items():
        phrases = langs.get(lang, [])
        for phrase in phrases:
            if phrase in text:
                return intent
    return None
