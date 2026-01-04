# 🎙 Voice Command Control (Local, Offline)

Lightweight local voice-command system using Python + Vosk.
It listens to your microphone, recognizes speech offline and runs configured actions.

No cloud. No accounts. Full local control.

**This README is a practical quick-start — see the code for extensibility.**

---

**Quick summary**

- Entry point: `main.py` (not `listen.py`)
- Offline recognition: Vosk models located under `models/` (per-language)
- Language switching: supported (configurable phrases in `config/languages.py`)
- TTS and a short cooldown are used to avoid recognizing the assistant's own speech

---

**Requirements (macOS tested)**

- Python 3.10+ (use virtualenv)
- `portaudio` (install via Homebrew)

Install system deps:

```bash
brew install python portaudio
```

Python env:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

**Vosk models**
Place models under `models/<lang>/...` and point `config/languages.py` to the model path. Example project already includes `models/ru/...` and `models/en/...` directories.

Download example model (if needed):

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
unzip vosk-model-small-ru-0.22.zip -d models/ru
```

---

**Run**

```bash
source .venv/bin/activate
python main.py
```

You should see a startup message and then live `➡️ recognized: '...'` lines as the recognizer produces text.

---

**Language switching**

- Phrases that trigger a language switch live in `config/languages.py` under `switch_phrases` for each language.
- The app matches recognized text against those phrases and attempts to infer the target language. If automatic detection fails, an interactive `choose_language()` prompt will appear in the console.

To add/change phrases, edit `config/languages.py`.

---

**TTS & echo protection**

- The app uses a short TTS cooldown after speaking to avoid the microphone picking up assistant speech and retriggering commands.
- If you still get echo-trigger loops, increase `speech_cooldown` in `core/processor.py`.

---

**Configuration & Commands**

- Commands are defined in `config/commands.py` and actions in `core/actions.py`.
- Intents live in `config/intents.py` and matching is implemented in `core/intents.py`.

---

**Troubleshooting**

- If you see Python exceptions from the audio callback, restart the process and verify your virtualenv and `sounddevice`/`portaudio` are installed correctly.
- If language switching doesn't work, check the recognized text printed to console (lines prefixed with `➡️ recognized:`) and update `switch_phrases` or keywords in `config/languages.py`.
- If TTS is being recognized as speech, increase `speech_cooldown` in `core/processor.py` or route TTS to a separate audio device.

---

**Development notes**

- The microphone callback runs in a native audio thread — keep it minimal and non-blocking.
- Use `main.py`'s `sd.RawInputStream` settings (`SAMPLE_RATE` and `BLOCK_SIZE`) to tune latency vs CPU.

---

**License**
MIT — do whatever you want. Hack responsibly.
