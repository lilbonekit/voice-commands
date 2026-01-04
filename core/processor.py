from email.mime import text
import threading
import time

from config.commands import COMMANDS
from config.languages import LANGUAGES
from core.languages import detect_language_from_text, choose_language
from core.intents import detect_intent
from core.time import parse_minutes

DEFAULT_SPEECH_COOLDOWN = 1.2
TTS_CHARS_PER_SECOND = 12.0

class VoiceProcessor:
    def __init__(self, recognizer, actions, speak, get_message):
        self.recognizer = recognizer
        self.actions = actions
        self.speak = speak
        self.get_message = get_message

        # ---------- EXIT / SHUTDOWN ----------
        self.exit_requested = False
        self.exit_confirmation = False
        self.shutdown_confirmation = False

        # ---------- SPEECH CONTROL ----------
        self.is_speaking = False
        self.last_spoken_at = 0.0
        self.speech_cooldown = DEFAULT_SPEECH_COOLDOWN

        # ---------- SHUTDOWN TIMER ----------
        self.shutdown_timer_waiting_minutes = False
        self.shutdown_timer_confirmation = False
        self.pending_shutdown_minutes: int | None = None
        self.shutdown_timer: threading.Timer | None = None

    def _apply_dynamic_cooldown(self, spoken_text: str):
        char_count = len(spoken_text)
        estimated_seconds = char_count / TTS_CHARS_PER_SECOND
        self.speech_cooldown = max(DEFAULT_SPEECH_COOLDOWN, estimated_seconds)

    # ---------- PUBLIC API ----------
    def should_exit(self) -> bool:
        return self.exit_requested

    # ---------- INTERNAL HELPERS ----------
    def cancel_shutdown_timer(self):
        if self.shutdown_timer:
            self.shutdown_timer.cancel()
            self.shutdown_timer = None

    def say_dynamic(self, key: str, **kwargs):
        text_tpl = self.get_message(self.recognizer.current_language, key, "text")
        voice_tpl = self.get_message(self.recognizer.current_language, key, "voice")

        text = text_tpl.format(**kwargs)
        voice = voice_tpl.format(**kwargs)

        print(text)
        self.is_speaking = True
        try:
            self.speak(voice, self.recognizer.current_language)
        finally:
            self._apply_dynamic_cooldown(voice)
            self.last_spoken_at = time.time()
            self.is_speaking = False

    def say(self, key: str):
        text = self.get_message(self.recognizer.current_language, key, "text")
        voice = self.get_message(self.recognizer.current_language, key, "voice")

        print(text)

        self.is_speaking = True
        try:
            self.speak(voice, self.recognizer.current_language)
        finally:
            self._apply_dynamic_cooldown(voice)
            self.last_spoken_at = time.time()
            self.is_speaking = False

    # ---------- MAIN LOGIC ----------
    def process_text(self, text: str):
        print(f"➡️ recognized: '{text}'")

        # Ignore mic echo after TTS
        if time.time() - self.last_spoken_at < self.speech_cooldown:
            print("⏱ Ignoring input during speech cooldown")
            return

        intent = detect_intent(text, self.recognizer.current_language)
        print(f"🔍 Detected intent: {intent}")

        # ---------- BASIC INTENTS ----------
        if intent == "greeting":
            self.say("greeting")
            return

        if intent == "switch_language":
            target = detect_language_from_text(text)
            if not target:
                try:
                    target = choose_language()
                except Exception:
                    target = None

            if target and target in LANGUAGES:
                if target == self.recognizer.current_language:
                    print(f"🌍 Already on {LANGUAGES[target]['label']}")
                    return
                try:
                    self.recognizer.switch_language(target)
                    print(f"🌍 Switched to {LANGUAGES[target]['label']}")
                    self.say("listening")
                except Exception as e:
                    print("⚠️ Language switch failed:", e)
            return

        # ---------- EXIT FLOW ----------
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

        # ---------- IMMEDIATE SHUTDOWN ----------
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

        # ---------- SHUTDOWN TIMER FLOW ----------
        if intent == "shutdown_timer":
            self.pending_shutdown_minutes = None
            self.shutdown_timer_waiting_minutes = True
            self.shutdown_timer_confirmation = False

            self.say("shutdown_timer_ask_minutes")
            return

        if self.shutdown_timer_waiting_minutes:
            minutes = parse_minutes(text)
            if minutes is None:
                self.say("shutdown_timer_bad_minutes")
                return

            self.pending_shutdown_minutes = minutes
            self.shutdown_timer_waiting_minutes = False
            self.shutdown_timer_confirmation = True

            self.say_dynamic(
               "shutdown_timer_confirm",
                minutes=minutes
            )
            return        

        if self.shutdown_timer_confirmation:
            if intent == "confirm_yes":
                minutes = self.pending_shutdown_minutes or 0

                self.cancel_shutdown_timer()

                self.shutdown_timer = threading.Timer(
                    minutes * 60,
                    self.actions["shutdown_computer"],
                )
                self.shutdown_timer.daemon = True
                self.shutdown_timer.start()

                self.pending_shutdown_minutes = None
                self.shutdown_timer_confirmation = False

                self.say_dynamic(
                    "shutdown_timer_started",
                    minutes=minutes
                )
                return

            if intent == "confirm_no":
                self.pending_shutdown_minutes = None
                self.shutdown_timer_confirmation = False
                self.say("shutdown_timer_cancelled")
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
                        self.last_spoken_at = time.time()
                        self.is_speaking = False
                    return

    