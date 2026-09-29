"""Вспомогательные функции безопасного ввода данных."""


def input_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число")


def input_float(prompt: str) -> float:
    while True:
        raw = input(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число (например, 15000 или 15000.50)")


def input_nonempty(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Ошибка: значение не может быть пустым")
