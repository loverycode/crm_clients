import json
from pathlib import Path


def _load(filename: str) -> list[dict]:
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены")
        return []
    except OSError as exc:
        print(f"Не удалось прочитать файл {filename}: {exc}")
        return []


def _save(filename: str, data: list[dict]) -> None:

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Не удалось сохранить файл {filename}: {exc}")


def load_clients(filename: str) -> list[dict]:
    return _load(filename)


def save_clients(filename: str, clients: list[dict]) -> None:
    _save(filename, clients)


def load_meetings(filename: str) -> list[dict]:
    return _load(filename)


def save_meetings(filename: str, meetings: list[dict]) -> None:
    _save(filename, meetings)
