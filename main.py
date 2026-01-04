import threading
import time
import sounddevice as sd

from core.processor import VoiceProcessor
from core.recognizer import VoiceRecognizer
from core.messages import get_message
from core.tts import speak
from core.actions import AVAILABLE_ACTIONS

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

exit_event = threading.Event()

recognizer = VoiceRecognizer(SAMPLE_RATE)

processor = VoiceProcessor(
    recognizer=recognizer,
    actions=AVAILABLE_ACTIONS,
    speak=speak,
    get_message=get_message,
)

def callback(indata, frames, time_info, status):
    # Ignore input while TTS is actively running or during short cooldown
    if processor.is_speaking or (time.time() - getattr(processor, "last_spoken_at", 0)) < getattr(processor, "speech_cooldown", 0):
        return

    text = recognizer.process(bytes(indata))
    if not text:
        return

    processor.process_text(text)

    if processor.should_exit():
        exit_event.set()



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
            sd.sleep(2_000) # sleep for TTS speaking and processing
except KeyboardInterrupt:
    print("\n🛑 Interrupted by user")
finally:
    print("✅ Exit")
