import threading
from time import sleep
import sounddevice as sd

from core.recognizer import VoiceRecognizer
from core.intents import detect_intent
from core.messages import get_message
from core.tts import speak
from config.commands import COMMANDS
from core.actions import AVAILABLE_ACTIONS

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

exit_event = threading.Event()
exit_confirmation = False

shutdown_confirmation = False

recognizer = VoiceRecognizer(SAMPLE_RATE)

def say(key: str):
    """
    Helper: print + speak message correctly
    """
    text = get_message(recognizer.current_language, key, "text")
    voice = get_message(recognizer.current_language, key, "voice")
    print(text)
    speak(voice, recognizer.current_language)


def callback(indata, frames, time, status):
    global exit_confirmation
    global shutdown_confirmation

    if status:
        print("⚠️", status)

    text = recognizer.process(bytes(indata))
    if not text:
        return

    print("➡️", text)

    # ---------- INTENTS (system / dialog) ----------
    intent = detect_intent(text, recognizer.current_language)

    if intent == "greeting":
        say("greeting")
        return

    if intent == "switch_language":
        if recognizer.current_language == "ru":
            recognizer.switch_language("en")
        else:
            recognizer.switch_language("ru")

        say("startup")
        return

    if intent == "exit":
        say("exit_ask")
        exit_confirmation = True
        return

    if exit_confirmation:
        if intent == "confirm_yes":
            say("exit_confirmed")
            exit_event.set()
            return

        if intent == "confirm_no":
            say("exit_cancelled")
            exit_confirmation = False
            return
    
    # --- shutdown intent ---
    if intent == "shutdown_computer":
        say("shutdown_ask")
        shutdown_confirmation = True
        return

    # --- confirmation ---
    if shutdown_confirmation:
        if intent == "confirm_yes":
            say("shutdown_confirmed")
            sleep(1_000)  # wait for TTS to finish
            AVAILABLE_ACTIONS["shutdown_computer"]()
            exit_event.set()
            return

        if intent == "confirm_no":
            say("shutdown_cancelled")
            shutdown_confirmation = False
            return

    # ---------- COMMANDS (actions) ----------
    lang_cmds = COMMANDS.get(recognizer.current_language, {})

    for action_name, cfg in lang_cmds.items():
        for phrase in cfg["triggers"]:
            if phrase in text:
               print(cfg["text"])
               speak(cfg["voice"], recognizer.current_language)
               AVAILABLE_ACTIONS[action_name]()
               return


# ---------- ENTRYPOINT ----------
startup_text = get_message(recognizer.current_language, "startup", "text")
startup_voice = get_message(recognizer.current_language, "startup", "voice")
listening_text = get_message(recognizer.current_language, "listening", "text")

print(startup_text)
print(listening_text)

speak(startup_voice, recognizer.current_language)

try:
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while not exit_event.is_set():
            sd.sleep(100)
except KeyboardInterrupt:
    print("\n🛑 Interrupted by user")
finally:
    print("✅ Exit")
