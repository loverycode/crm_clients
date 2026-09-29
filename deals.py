"""Класс Deal и функции для работы с коллекцией сделок."""
from clients import Client
from contacts import Contact
from managers import Manager

OUTCOMES = ("Выиграна", "Проиграна", "Отменена")


class Deal:

    def __init__(
        self,
        deal_id: int,
        client: Client,
        manager: Manager,
        amount: float,
        title: str = "",
        contact: Contact | None = None,
        stage: str = "Открыта",
    ) -> None:
        self.id = deal_id
        self.client = client
        self.manager = manager
        self.contact = contact
        self.amount = amount
        self.title = title
        self.stage = stage

    def is_open(self) -> bool:
        return self.stage == "Открыта"

    def close(self, outcome: str) -> None:
        if outcome not in OUTCOMES:
            raise ValueError(f"Недопустимый исход сделки: {outcome}")
        self.stage = outcome

    def __str__(self) -> str:
        contact_part = (
            f", Контакт: {self.contact.name}" if self.contact else ""
        )
        return (
            f"ID: {self.id}, Клиент: {self.client.name}, "
            f"Менеджер: {self.manager.name}{contact_part}, "
            f"Сумма: {self.amount}, Тема: {self.title}, "
            f"Стадия: {self.stage}"
        )


def is_manager_available(
    deals: list[Deal],
    manager: Manager,
    max_open_deals: int = 5,
) -> bool:
    open_count = sum(
        1 for d in deals if d.manager.id == manager.id and d.is_open()
    )
    return open_count < max_open_deals


def create_deal(
    deals: list[Deal],
    client: Client,
    manager: Manager,
    amount: float,
    title: str = "",
    contact: Contact | None = None,
    max_open_deals: int = 5,
) -> Deal:
    if not is_manager_available(deals, manager, max_open_deals):
        raise ValueError(
            f"У менеджера {manager.name} уже {max_open_deals} "
            f"открытых сделок"
        )

    next_id = max((d.id for d in deals), default=0) + 1
    deal = Deal(
        deal_id=next_id,
        client=client,
        manager=manager,
        amount=amount,
        title=title,
        contact=contact,
    )
    deals.append(deal)
    return deal


def close_deal(deals: list[Deal], deal_id: int, outcome: str) -> bool:
    for d in deals:
        if d.id == deal_id:
            d.close(outcome)
            return True
    return False


def find_deal_by_id(deals: list[Deal], deal_id: int) -> Deal | None:
    for d in deals:
        if d.id == deal_id:
            return d
    return None


def filter_deals_by_stage(deals: list[Deal], stage: str) -> list[Deal]:
    return [d for d in deals if d.stage == stage]


def sort_deals_by_amount(
    deals: list[Deal],
    descending: bool = True,
) -> list[Deal]:
    return sorted(deals, key=lambda d: d.amount, reverse=descending)
