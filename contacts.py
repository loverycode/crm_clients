"""Класс Contact и функции для работы с коллекцией контактов."""
from clients import Client


class Contact:

    def __init__(
        self,
        contact_id: int,
        client: Client,
        name: str,
        phone: str,
        position: str = "",
    ) -> None:
        self.id = contact_id
        self.client = client
        self.name = name
        self.phone = phone
        self.position = position

    def __str__(self) -> str:
        position_part = f", {self.position}" if self.position else ""
        return (
            f"ID: {self.id}, {self.name}{position_part} "
            f"({self.client.name}), Тел: {self.phone}"
        )


def add_contact(
    contacts: list[Contact],
    client: Client,
    name: str,
    phone: str,
    position: str = "",
) -> Contact:
    if not name.strip():
        raise ValueError("Имя контакта не может быть пустым")
    if not phone.strip():
        raise ValueError("Телефон контакта не может быть пустым")

    next_id = max((c.id for c in contacts), default=0) + 1
    contact = Contact(
        contact_id=next_id,
        client=client,
        name=name.strip(),
        phone=phone.strip(),
        position=position.strip(),
    )
    contacts.append(contact)
    return contact


def find_contact(contacts: list[Contact], query: str) -> list[Contact]:
    query_lower = query.lower()
    return [
        c for c in contacts
        if query_lower in c.name.lower() or query_lower in c.phone.lower()
    ]


def find_contact_by_id(
    contacts: list[Contact],
    contact_id: int,
) -> Contact | None:
    for c in contacts:
        if c.id == contact_id:
            return c
    return None


def contacts_for_client(
    contacts: list[Contact],
    client: Client,
) -> list[Contact]:
    return [c for c in contacts if c.client.id == client.id]
