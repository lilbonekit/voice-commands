import subprocess

def open_url(url: str):
    subprocess.run([
        "open",
        "-a",
        "Google Chrome",
        url
    ])
