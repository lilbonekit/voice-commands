import time

from config.commands import COMMANDS
from config.languages import LANGUAGES
from core.languages import detect_language_from_text, choose_language
from core.intents import detect_intent


class VoiceProcessor:
    def __init__(self, recognizer, actions, speak, get_message):
        self.recognizer = recognizer
        self.actions = actions
        self.speak = speak
        self.get_message = get_message

        self.exit_requested = False
        self.exit_confirmation = False
        self.shutdown_confirmation = False

        self.is_speaking = False  
        # Timestamp of last moment we triggered TTS. Used to ignore immediate echoes.
        self.last_spoken_at = 0.0
        # Seconds to ignore recognizer input after speaking (adjustable)
        self.speech_cooldown = 1.2

    def should_exit(self) -> bool:
        return self.exit_requested

    def say(self, key: str):
        text = self.get_message(self.recognizer.current_language, key, "text")
        voice = self.get_message(self.recognizer.current_language, key, "voice")

        print(text)

        self.is_speaking = True
        try:
            self.speak(voice, self.recognizer.current_language)
        finally:
            # record when we spoke so we can ignore immediate microphone echo
            self.last_spoken_at = time.time()
            self.is_speaking = False

    def process_text(self, text: str):
        print(f"➡️ recognized: '{text}'")

        # If we recently spoke, ignore recognizer input for a short cooldown
        if time.time() - self.last_spoken_at < self.speech_cooldown:
            print("⏱ Ignoring input during speech cooldown")
            return

        intent = detect_intent(text, self.recognizer.current_language)
        print(f"🔍 Detected intent: {intent}")

        # ---------- INTENTS ----------
        if intent == "greeting":
            self.say("greeting")
            return

        if intent == "switch_language":
            target = detect_language_from_text(text)
            if not target:
                # fallback to interactive chooser if no language detected
                try:
                    chosen = choose_language()
                    target = chosen
                except Exception:
                    target = None

            if target and target in LANGUAGES:
                if target == self.recognizer.current_language:
                    print(f"🌍 Already on {LANGUAGES[target]['label']}")
                    return
                try:
                    self.recognizer.switch_language(target)
                    print(f"🌍 Switched to {LANGUAGES[target]['label']}")
                    # confirm in the new language
                    self.say("listening")
                except Exception as e:
                    print("⚠️ Language switch failed:", e)
                return

        if intent == "exit":
            self.say("exit_ask")
            self.exit_confirmation = True
            return

        if self.exit_confirmation:
            if intent == "confirm_yes":
                self.say("exit_confirmed")
                self.exit_requested = True
                return

            if intent == "confirm_no":
                self.say("exit_cancelled")
                self.exit_confirmation = False
                return

        if intent == "shutdown_computer":
            self.say("shutdown_ask")
            self.shutdown_confirmation = True
            return

        if self.shutdown_confirmation:
            if intent == "confirm_yes":
                self.say("shutdown_confirmed")
                self.actions["shutdown_computer"]()
                self.exit_requested = True
                return

            if intent == "confirm_no":
                self.say("shutdown_cancelled")
                self.shutdown_confirmation = False
                return

        # ---------- COMMANDS ----------

        for action, cfg in COMMANDS[self.recognizer.current_language].items():
            for phrase in cfg["triggers"]:
                if phrase in text:
                    self.is_speaking = True
                    try:
                        self.speak(cfg["voice"], self.recognizer.current_language)
                        self.actions[action]()
                    finally:
                        # mark cooldown regardless of speak() behavior
                        self.last_spoken_at = time.time()
                        self.is_speaking = False
                    return
