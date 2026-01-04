from config.languages import LANGUAGES, DEFAULT_LANGUAGE


def choose_language():
    print("🌍 Choose language:")

    languages = list(LANGUAGES.keys())

    for idx, lang in enumerate(languages, start=1):
        label = LANGUAGES[lang].get("label", lang)
        default_mark = " (default)" if lang == DEFAULT_LANGUAGE else ""
        print(f"{idx} — {label}{default_mark}")

    while True:
        choice = input("> ").strip()

        if choice == "":
            return DEFAULT_LANGUAGE

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(languages):
                return languages[index]

        print("❌ Invalid choice. Try again.")


def detect_language_from_text(text: str) -> str | None:
    """Return language code if `text` contains any configured switch phrase.

    Matching is case-insensitive and looks for any `switch_phrases` defined
    in `config/languages.py`.
    """
    txt = text.lower()

    # try direct phrase match first (legacy config)
    for code, cfg in LANGUAGES.items():
        for phrase in cfg.get("switch_phrases", []):
            if phrase.lower() in txt:
                # attempt to infer the *target* language from the phrase/text
                # by looking for known language keywords (English/Russian).
                # This handles configs where switch_phrases are written in the
                keywords = {
                    "en": ["english", "англ", "англий"],
                    "ru": ["russian", "рус", "русск"]
                }
                # search matched phrase + original text for language keywords
                combined = (phrase + " " + text).lower()
                for target_code, kws in keywords.items():
                    for kw in kws:
                        if kw in combined:
                            return target_code
                # fallback: return the code of the config entry (best-effort)
                return code

    # fallback: detect by scanning text for language name keywords
    keywords = {
        "en": ["english", "англ", "англий"],
        "ru": ["russian", "рус", "русск"],
    }
    for target_code, kws in keywords.items():
        for kw in kws:
            if kw in txt:
                return target_code

    return None
