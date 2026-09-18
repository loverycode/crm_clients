from datetime import date


def add_client(
    clients: list[dict],
    name: str,
    contact: str,
    status: str = "Новый",
) -> dict:
    if not name.strip():
        raise ValueError("Имя клиента не может быть пустым")
    if not contact.strip():
        raise ValueError("Контакт клиента не может быть пустым")

    next_id = max((c["id"] for c in clients), default=0) + 1
    client = {
        "id": next_id,
        "name": name.strip().title(),
        "contact": contact.strip(),
        "status": status,
        "created": str(date.today()),
    }
    clients.append(client)
    return client


def find_client(clients: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [
        c for c in clients
        if query_lower in c["name"].lower()
        or query_lower in c["contact"].lower()
    ]


def update_status(
    clients: list[dict],
    client_id: int,
    new_status: str,
) -> bool:
    for c in clients:
        if c["id"] == client_id:
            c["status"] = new_status
            return True
    return False


def filter_clients_by_status(clients: list[dict], status: str) -> list[dict]:
    return [c for c in clients if c["status"] == status]


def sort_clients(clients: list[dict], by: str = "name") -> list[dict]:
    if by not in ("name", "status", "created"):
        raise ValueError(f"Недопустимое поле сортировки: {by}")
    return sorted(clients, key=lambda c: c[by])
