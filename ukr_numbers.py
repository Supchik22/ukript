import re

UNITS = {
    "нуль": 0, "один": 1, "одна": 1, "два": 2, "дві": 2, "двух": 2, "три": 3, "чотири": 4, "чотирьох": 4, "п'яти": 4,
    "п’ять": 5, "шість": 6, "сім": 7, "вісім": 8, "дев’ять": 9, "дев’яти": 9
}

TEENS = {
    "десять": 10, "одинадцять": 11, "дванадцять": 12, "тринадцять": 13,
    "чотирнадцять": 14, "п’ятнадцять": 15, "шістнадцять": 16,
    "сімнадцять": 17, "вісімнадцять": 18, "дев’ятнадцять": 19
}

TENS = {
    "двадцять": 20, "тридцять": 30, "сорок": 40, "п’ятдесят": 50,
    "шістдесят": 60, "сімдесят": 70, "вісімдесят": 80, "дев’яносто": 90
}

HUNDREDS = {
    "сто": 100, "двісті": 200, "триста": 300, "чотириста": 400,
    "п’ятсот": 500, "шістсот": 600, "сімсот": 700, "вісімсот": 800, "дев’ятсот": 900
}

MULTIPLIERS = {
    "тисяча": 1_000, "тисячі": 1_000, "тисяч": 1_000, "тисячу": 1_000,
    "мільйон": 1_000_000, "мільйони": 1_000_000, "мільйонів": 1_000_000,
    "мільярд": 1_000_000_000, "мільярди": 1_000_000_000, "мільярдів": 1_000_000_000,
    "трильйон": 1_000_000_000_000, "трильйони": 1_000_000_000_000, "трильйонів": 1_000_000_000_000,
}

FRACTIONAL_ENDINGS = {
    "десятих": 10,
    "сотих": 100,
    "тисячних": 1000,
}

def parse_integer(tokens):
    total = 0
    current = 0
    for word in tokens:
        if word in UNITS:
            current += UNITS[word]
        elif word in TEENS:
            current += TEENS[word]
        elif word in TENS:
            current += TENS[word]
        elif word in HUNDREDS:
            current += HUNDREDS[word]
        elif word in MULTIPLIERS:
            multiplier = MULTIPLIERS[word]
            if current == 0:
                current = 1
            total += current * multiplier
            current = 0
        elif word == "і":
            continue
        else:
            return None
    return total + current


def parse_number(text: str) -> float:
    text = text.lower().strip()
    if not text.startswith("дробове"):
        return parse_integer(re.split(r"[\s\-]+", text))

    # Парсимо дробове число
    text = text.removeprefix("дробове").strip()
    parts = re.split(r"\bі\b", text)
    if len(parts) != 2:
        raise ValueError("Невірний формат дробового числа. Очікується: 'дробове ... цілих і ... десятих'")

    integer_part = re.split(r"[\s\-]+", parts[0].replace("ціла", "").replace("цілих", "").strip())
    fractional_part_raw = parts[1].strip()
    # Знаходимо закінчення (десятих/сотих/тисячних)
    denom = None
    for ending in FRACTIONAL_ENDINGS:
        if fractional_part_raw.endswith(ending):
            denom = FRACTIONAL_ENDINGS[ending]
            fractional_part = fractional_part_raw.removesuffix(ending).strip()
            break
    if denom is None:
        raise ValueError("Не знайдено закінчення дробової частини (десятих/сотих/тисячних)")

    fractional_tokens = re.split(r"[\s\-]+", fractional_part)
    integer_value = parse_integer(integer_part)
    fractional_value = parse_integer(fractional_tokens)

    return integer_value + fractional_value / denom


def i_to_words(number: int) -> str:
    if number == 0:
        return "нуль"

    words = []

    if number >= 1000:
        thousands = number // 1000
        number %= 1000
        if thousands == 1:
            words.append("тисяча")
        elif 2 <= thousands <= 4:
            words.append(f"{list(UNITS.keys())[list(UNITS.values()).index(thousands)]} тисячі")
        else:
            words.append(f"{i_to_words(thousands)} тисяч")

    for word, val in sorted(HUNDREDS.items(), key=lambda x: -x[1]):
        if number >= val:
            words.append(word)
            number -= val

    if 10 <= number <= 19:
        for word, val in TEENS.items():
            if number == val:
                words.append(word)
                number = 0
                break
    else:
        for word, val in sorted(TENS.items(), key=lambda x: -x[1]):
            if number >= val:
                words.append(word)
                number -= val
        for word, val in UNITS.items():
            if number == val:
                words.append(word)
                break

    return " ".join(words)
