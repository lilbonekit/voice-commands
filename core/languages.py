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
