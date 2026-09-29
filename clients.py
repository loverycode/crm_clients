"""Класс Client и функции для работы с коллекцией клиентов."""
from datetime import date


class Client:

    def __init__(
        self,
        client_id: int,
        name: str,
        status: str = "Новый",
        created: str | None = None,
    ) -> None:
        self.id = client_id
        self.name = name
        self.status = status
        self.created = created or str(date.today())

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    @classmethod
    def from_data(cls, data: dict) -> "Client":
        return cls(
            client_id=data["id"],
            name=data["name"],
            status=data["status"],
            created=data.get("created"),
        )

    def __str__(self) -> str:
        return f"ID: {self.id}, Название: {self.name}, Статус: {self.status}"


def add_client(
    clients: list[Client],
    name: str,
    status: str = "Новый",
) -> Client:
    if not name.strip():
        raise ValueError("Название клиента не может быть пустым")

    next_id = max((c.id for c in clients), default=0) + 1
    client = Client(client_id=next_id, name=name.strip(), status=status)
    clients.append(client)
    return client


def find_client(clients: list[Client], query: str) -> list[Client]:
    query_lower = query.lower()
    return [c for c in clients if query_lower in c.name.lower()]


def find_client_by_id(
    clients: list[Client],
    client_id: int,
) -> Client | None:
    for c in clients:
        if c.id == client_id:
            return c
    return None


def update_status(
    clients: list[Client],
    client_id: int,
    new_status: str,
) -> bool:
    client = find_client_by_id(clients, client_id)
    if client is None:
        return False
    client.update_status(new_status)
    return True


def filter_clients_by_status(
    clients: list[Client],
    status: str,
) -> list[Client]:
    return [c for c in clients if c.status == status]


def sort_clients(clients: list[Client], by: str = "name") -> list[Client]:
    if by not in ("name", "status", "created"):
        raise ValueError(f"Недопустимое поле сортировки: {by}")
    return sorted(clients, key=lambda c: getattr(c, by))
