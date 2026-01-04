from config.messages import MESSAGES

def get_message(lang: str, key: str, mode: str = "text") -> str:
    msg = MESSAGES[lang][key]
    return msg.get(mode) or msg.get("text")
