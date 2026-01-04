import subprocess

import os
import platform

ENGLISH_VIDEO_URL = "https://youtu.be/scJciUkC-F4?si=cS24t1RQkSl4pOHx&t=14"
SPIDER_MAN_VIDEO_URL = "https://www.youtube.com/watch?v=OBpXq0XVyCw"

# TODO: Replace with actual Supernatural URL
SUPERNATURAL_VIDEO_URL = SPIDER_MAN_VIDEO_URL

def open_english():
    open_url(ENGLISH_VIDEO_URL)

def open_spiderman():
    open_url(SPIDER_MAN_VIDEO_URL)

def shutdown_computer():
    system = platform.system()

    if system == "Darwin":  # macOS
        # os.system("sudo shutdown -h now")
      subprocess.run([
          "osascript",
          "-e",
          'tell application "System Events" to shut down'
      ])
    elif system == "Linux":
        os.system("shutdown -h now")
    elif system == "Windows":
        os.system("shutdown /s /t 0")

def open_supernatural():
    open_url(SUPERNATURAL_VIDEO_URL)


def open_url(url: str):
    subprocess.run([
        "open",
        "-a",
        "Google Chrome",
        url
    ])

AVAILABLE_ACTIONS = {
    "open_english": open_english,
    "open_spiderman": open_spiderman,
    "shutdown_computer": shutdown_computer,
    "open_supernatural": open_supernatural,
} 
