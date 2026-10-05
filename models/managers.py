"""Класс Manager и функции для работы с коллекцией менеджеров."""


class Manager:

    def __init__(self, manager_id: int, name: str, email: str) -> None:
        self.id = manager_id
        self.name = name
        self.email = email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email = email.strip()
        return bool(email) and "@" in email

    @classmethod
    def from_data(cls, data: dict) -> "Manager":
        return cls(
            manager_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def __str__(self) -> str:
        return f"ID: {self.id}, Имя: {self.name}, Email: {self.email}"


def add_manager(managers: list[Manager], name: str, email: str) -> Manager:
    if not name.strip():
        raise ValueError("Имя менеджера не может быть пустым")
    if not Manager.is_valid_email(email):
        raise ValueError("Некорректный email менеджера")

    next_id = max((m.id for m in managers), default=0) + 1
    manager = Manager(
        manager_id=next_id,
        name=name.strip(),
        email=email.strip(),
    )
    managers.append(manager)
    return manager


def find_manager(managers: list[Manager], query: str) -> list[Manager]:
    query_lower = query.lower()
    return [
        m for m in managers
        if query_lower in m.name.lower() or query_lower in m.email.lower()
    ]


def find_manager_by_id(
    managers: list[Manager],
    manager_id: int,
) -> Manager | None:
    for m in managers:
        if m.id == manager_id:
            return m
    return None
