from datetime import date, datetime


def input_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число")


def input_date(prompt: str) -> date:
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")


def input_nonempty(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Ошибка: значение не может быть пустым")
