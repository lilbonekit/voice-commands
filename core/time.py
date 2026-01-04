import re


def _words_to_int(tokens: list[str]) -> int:
    units = {
        "ноль": 0, "нуль": 0,
        "один": 1, "одна": 1, "одно": 1,
        "два": 2, "две": 2,
        "три": 3, "четыре": 4, "пять": 5, "шесть": 6,
        "семь": 7, "восемь": 8, "девять": 9,
        "десять": 10, "одиннадцать": 11, "двенадцать": 12,
        "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15,
        "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18,
        "девятнадцать": 19,
    }
    tens = {
        "двадцать": 20, "тридцать": 30, "сорок": 40,
        "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70,
        "восемьдесят": 80, "девяносто": 90,
    }
    hundreds = {
        "сто": 100, "двести": 200, "триста": 300, "четыреста": 400,
        "пятьсот": 500, "шестьсот": 600, "семьсот": 700, "восемьсот": 800,
        "девятьсот": 900,
    }

    value = 0
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in hundreds:
            value += hundreds[token]
            i += 1
            continue
        if token in tens:
            value += tens[token]
            # possible composite like 'двадцать три'
            if i + 1 < len(tokens) and tokens[i + 1] in units:
                value += units[tokens[i + 1]]
                i += 2
            else:
                i += 1
            continue
        if token in units:
            value += units[token]
            i += 1
            continue
        # skip filler words
        i += 1

    return value


def parse_minutes(text: str) -> int | None:
    """Parse minutes from text. Accepts digits or Russian number words.

    Returns integer minutes (1..720) or None if not found/invalid.
    """
    if not text:
        return None

    # try digits first
    m = re.search(r"\b(\d{1,3})\b", text)
    if m:
        minutes = int(m.group(1))
        if 1 <= minutes <= 720:
            return minutes

    # normalize and split into tokens
    txt = re.sub(r"[^\w\sа-яёА-ЯЁ-]", " ", text.lower())
    # replace hyphens with spaces to split composite words
    txt = txt.replace("-", " ")
    tokens = [t for t in txt.split() if t]
    if not tokens:
        return None

    # attempt to parse contiguous number-word spans
    # find runs that contain number words
    number_words = set(
        [
            "ноль","нуль","один","одна","одно","два","две","три","четыре",
            "пять","шесть","семь","восемь","девять","десять","одиннадцать",
            "двенадцать","тринадцать","четырнадцать","пятнадцать","шестнадцать",
            "семнадцать","восемнадцать","девятнадцать","двадцать","тридцать",
            "сорок","пятьдесят","шестьдесят","семьдесят","восемьдесят",
            "девяносто","сто","двести","триста","четыреста","пятьсот",
            "шестьсот","семьсот","восемьсот","девятьсот",
        ]
    )

    runs = []
    cur = []
    for tok in tokens:
        if tok in number_words:
            cur.append(tok)
        else:
            if cur:
                runs.append(list(cur))
                cur = []
    if cur:
        runs.append(list(cur))

    # parse each run and pick the first valid minutes in range
    for run in runs:
        val = _words_to_int(run)
        if 1 <= val <= 720:
            return val

    return None
