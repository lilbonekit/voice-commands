import pyttsx3

_engine = pyttsx3.init()

VOICE_MAP = {
    "ru": "com.apple.voice.compact.ru-RU.Milena",
    "en": "com.apple.voice.compact.en-US.Samantha",
}

def set_voice(lang: str):
    voice_id = VOICE_MAP.get(lang)
    if not voice_id:
        return

    for v in _engine.getProperty("voices"):
        if v.id == voice_id:
            _engine.setProperty("voice", v.id)
            return

def speak(text: str, lang: str | None = None):
    if lang:
        set_voice(lang)

    _engine.say(text)
    _engine.runAndWait()
