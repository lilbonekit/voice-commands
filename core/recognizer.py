
import os
os.environ["VOSK_LOG_LEVEL"] = "-1"

import json

# Disable internal Vosk logging
import vosk                      
vosk.SetLogLevel(-1)

from vosk import Model, KaldiRecognizer


from config.languages import LANGUAGES, DEFAULT_LANGUAGE

class VoiceRecognizer:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.current_language = DEFAULT_LANGUAGE
        self.model = None
        self.rec = None
        self.load_language(self.current_language)

    def load_language(self, lang_code: str):
        cfg = LANGUAGES[lang_code]
        print(f"🌍 Loading language: {lang_code}")

        self.model = Model(cfg["model_path"])
        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self.current_language = lang_code

    def switch_language(self, lang_code: str):
        if lang_code == self.current_language:
            return
        if lang_code not in LANGUAGES:
            raise ValueError(f"Unknown language: {lang_code}")

        self.load_language(lang_code)

    def process(self, audio_bytes: bytes) -> str | None:
        if self.rec.AcceptWaveform(audio_bytes):
            result = json.loads(self.rec.Result())
            return result.get("text", "").lower().strip()
        return None
