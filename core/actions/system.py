import os
import platform
import subprocess

def shutdown_computer():
    system = platform.system()

    if system == "Darwin":
        subprocess.run([
            "osascript",
            "-e",
            'tell application "System Events" to shut down'
        ])
    elif system == "Linux":
        raise NotImplementedError("Shutdown not implemented for Linux yet.")
        # os.system("shutdown -h now")
    elif system == "Windows":
        raise NotImplementedError("Shutdown not implemented for Windows yet.")
        # os.system("shutdown /s /t 0")
