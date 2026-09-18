from datetime import date


class Client:

    def __init__(
        self,
        client_id: int,
        name: str,
        contact: str,
        status: str = "Новый",
        created: str | None = None,
    ) -> None:
        self.id = client_id
        self.name = name
        self.contact = contact
        self.status = status
        self.created = created or str(date.today())

    @staticmethod
    def is_valid_contact(contact: str) -> bool:
        return bool(contact.strip())

    @classmethod
    def from_data(cls, data: dict) -> "Client":
        return cls(
            client_id=data["id"],
            name=data["name"],
            contact=data["contact"],
            status=data["status"],
            created=data.get("created"),
        )

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    def __str__(self) -> str:
        return (
            f"ID: {self.id}, Имя: {self.name}, "
            f"Контакт: {self.contact}, Статус: {self.status}"
        )


def add_client(
    clients: list[Client],
    name: str,
    contact: str,
    status: str = "Новый",
) -> Client:
    if not name.strip():
        raise ValueError("Имя клиента не может быть пустым")
    if not Client.is_valid_contact(contact):
        raise ValueError("Контакт клиента не может быть пустым")

    next_id = max((c.id for c in clients), default=0) + 1
    client = Client(
        client_id=next_id,
        name=name.strip().title(),
        contact=contact.strip(),
        status=status,
    )
    clients.append(client)
    return client


def find_client(clients: list[Client], query: str) -> list[Client]:
    query_lower = query.lower()
    return [
        c for c in clients
        if query_lower in c.name.lower()
        or query_lower in c.contact.lower()
    ]


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
