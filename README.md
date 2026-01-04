# 🎙 Voice Command Control Server (Local, Offline)

A local, offline voice command system built with **Python + Vosk**.
It listens to your microphone, recognizes speech in real time, and executes system or custom commands.

No cloud. No accounts. Full local control.

---

## ✨ Features

- 🎤 Real-time microphone input
- 🧠 Offline speech recognition (Vosk)
- ⚡ Low latency, low CPU usage
- 🖥 Execute local system commands

---

## 🧱 Architecture Overview

```
Microphone
   ↓
sounddevice (RawInputStream)
   ↓
Vosk (speech-to-text)
   ↓
Text → Command Logic
   ↓
System / RPC / Smart Home actions
```

---

## 🖥 Requirements

### Operating System

- macOS (tested)
- Linux (should work)
- Windows (possible, not tested)

### System dependencies (via Homebrew)

Make sure you have **Homebrew** installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install required system packages:

```bash
brew install python portaudio
```

---

## 🐍 Python Environment Setup

### 1️⃣ Create virtual environment

```bash
python3 -m venv .venv
```

### 2️⃣ Activate it

```bash
source .venv/bin/activate
```

### 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Important:
> Do **NOT** install packages globally.
> Use a virtual environment to avoid Homebrew / system conflicts.

---

## 🧠 Vosk Model Setup

Download a Vosk model (example: Russian small model):

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
unzip vosk-model-small-ru-0.22.zip
```

Project structure should look like:

```
project/
├── listen.py
├── vosk-model-small-ru-0.22/
│   ├── am/
│   ├── conf/
│   ├── graph/
│   └── ivector/
```

---

## ▶️ Running the Project

Activate virtual environment:

```bash
source .venv/bin/activate
```

Run:

```bash
python listen.py
```

You should see:

```
🎤 Speak, I am listening...
```

---

## 🗣 Example Voice Commands

- **"start"** → custom action
- **"stop"** → custom action
- **"exit"** → gracefully shutdown program
- **"a nu eb\*at let's learn English"** → opens YouTube in Chrome (example)

Commands are fully customizable in code.

---

## 🔧 Configuration

Key constants in `listen.py`:

```python
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
```

- Lower `BLOCK_SIZE` → lower latency, more CPU
- Higher `BLOCK_SIZE` → higher latency, less CPU

---

## 🧩 Extending the System

This project is designed to scale:

- 🔗 RPC server (HTTP / WebSocket)
- 🏠 Smart Home via MQTT
- 🧠 Intent parsing
- 🎛 State machine
- 🗣 Text-to-speech responses

---

## ⚠️ Notes

- The microphone callback runs in a **native audio thread**
- Avoid heavy logic inside the callback
- Always use `RawInputStream` for minimal latency
- Restart the process after changing callback logic

---

## 🧠 Why Python?

Python excels at:

- Native audio integration
- Machine learning libraries
- Rapid prototyping
- Glue code between systems

This project uses Python as a **control layer**, not a web framework.

---

## 📜 License

MIT — do whatever you want.
Hack responsibly.
