import json
from pathlib import Path

from clients import Client
from meetings import Meeting


def _load_raw(filename: str) -> list[dict]:
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


def _save_raw(filename: str, data: list[dict]) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Не удалось сохранить файл {filename}: {exc}")


def load_clients(filename: str) -> list[Client]:
    raw = _load_raw(filename)
    return [Client.from_data(item) for item in raw]


def save_clients(filename: str, clients: list[Client]) -> None:
    data = [
        {
            "id": c.id,
            "name": c.name,
            "contact": c.contact,
            "status": c.status,
            "created": c.created,
        }
        for c in clients
    ]
    _save_raw(filename, data)


def load_meetings(filename: str, clients: list[Client]) -> list[Meeting]:
    raw = _load_raw(filename)
    meetings = []
    for item in raw:
        client = next(
            (c for c in clients if c.id == item["client_id"]),
            None,
        )
        if client is None:
            print(
                f"Клиент с ID {item['client_id']} не найден, "
                f"встреча {item['id']} пропущена"
            )
            continue
        meetings.append(
            Meeting(
                meeting_id=item["id"],
                client=client,
                meeting_date=item["meeting_date"],
                topic=item.get("topic", ""),
                is_cancelled=item.get("is_cancelled", False),
            )
        )
    return meetings


def save_meetings(filename: str, meetings: list[Meeting]) -> None:
    data = [
        {
            "id": m.id,
            "client_id": m.client.id,
            "meeting_date": m.meeting_date,
            "topic": m.topic,
            "is_cancelled": m.is_cancelled,
        }
        for m in meetings
    ]
    _save_raw(filename, data)
