"""Функции сохранения и загрузки данных проекта в JSON-файлах."""
import json
from pathlib import Path

from models.clients import Client
from models.contacts import Contact
from models.deals import Deal
from models.managers import Manager


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
    return [Client.from_data(item) for item in _load_raw(filename)]


def save_clients(filename: str, clients: list[Client]) -> None:
    data = [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "created": c.created,
        }
        for c in clients
    ]
    _save_raw(filename, data)


def load_managers(filename: str) -> list[Manager]:
    return [Manager.from_data(item) for item in _load_raw(filename)]


def save_managers(filename: str, managers: list[Manager]) -> None:
    data = [
        {"id": m.id, "name": m.name, "email": m.email}
        for m in managers
    ]
    _save_raw(filename, data)


def load_contacts(filename: str, clients: list[Client]) -> list[Contact]:
    contacts = []
    for item in _load_raw(filename):
        client = next(
            (c for c in clients if c.id == item["client_id"]), None
        )
        if client is None:
            print(
                f"Клиент с ID {item['client_id']} не найден, "
                f"контакт {item['id']} пропущен"
            )
            continue
        contacts.append(
            Contact(
                contact_id=item["id"],
                client=client,
                name=item["name"],
                phone=item["phone"],
                position=item.get("position", ""),
            )
        )
    return contacts


def save_contacts(filename: str, contacts: list[Contact]) -> None:
    data = [
        {
            "id": c.id,
            "client_id": c.client.id,
            "name": c.name,
            "phone": c.phone,
            "position": c.position,
        }
        for c in contacts
    ]
    _save_raw(filename, data)


def load_deals(
    filename: str,
    clients: list[Client],
    managers: list[Manager],
    contacts: list[Contact],
) -> list[Deal]:
    deals = []
    for item in _load_raw(filename):
        client = next(
            (c for c in clients if c.id == item["client_id"]), None
        )
        manager = next(
            (m for m in managers if m.id == item["manager_id"]), None
        )
        if client is None or manager is None:
            print(
                f"Сделка {item['id']} пропущена: "
                f"не найден клиент или менеджер"
            )
            continue
        contact = None
        contact_id = item.get("contact_id")
        if contact_id is not None:
            contact = next(
                (c for c in contacts if c.id == contact_id), None
            )
        deals.append(
            Deal(
                deal_id=item["id"],
                client=client,
                manager=manager,
                amount=item["amount"],
                title=item.get("title", ""),
                contact=contact,
                stage=item.get("stage", "Открыта"),
            )
        )
    return deals


def save_deals(filename: str, deals: list[Deal]) -> None:
    data = [
        {
            "id": d.id,
            "client_id": d.client.id,
            "manager_id": d.manager.id,
            "contact_id": d.contact.id if d.contact else None,
            "amount": d.amount,
            "title": d.title,
            "stage": d.stage,
        }
        for d in deals
    ]
    _save_raw(filename, data)
