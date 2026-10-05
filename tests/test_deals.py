"""Автоматизированные тесты класса Deal и функций работы с ним."""
from models.clients import Client
from models.deals import (
    close_deal,
    create_deal,
    filter_deals_by_stage,
    is_manager_available,
    sort_deals_by_amount,
)
from managers import Manager


def test_deal_creation():
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deals = []
    deal = create_deal(deals, client, manager, 150000, "Поставка")
    assert deal.client is client
    assert deal.manager is manager
    assert deal.is_open()
    assert deal.stage == "Открыта"


def test_deal_close_method():
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deals = []
    deal = create_deal(deals, client, manager, 150000, "Поставка")
    deal.close("Выиграна")
    assert deal.stage == "Выиграна"
    assert not deal.is_open()


def test_deal_close_invalid_outcome_raises():
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deal = create_deal([], client, manager, 150000, "Поставка")
    try:
        deal.close("Что-то не то")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_manager_availability_limit():
    """У менеджера не может быть больше max_open_deals открытых сделок."""
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deals = []
    for _ in range(2):
        create_deal(deals, client, manager, 1000, max_open_deals=2)

    assert not is_manager_available(deals, manager, max_open_deals=2)
    try:
        create_deal(deals, client, manager, 1000, max_open_deals=2)
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_closed_deal_frees_manager_slot():
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deals = []
    deal = create_deal(deals, client, manager, 1000, max_open_deals=1)

    assert not is_manager_available(deals, manager, max_open_deals=1)
    assert close_deal(deals, deal.id, "Выиграна")
    assert is_manager_available(deals, manager, max_open_deals=1)


def test_filter_and_sort_deals():
    client = Client(1, "ООО Ромашка")
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    deals = []
    create_deal(deals, client, manager, 1000, "Мелкая сделка")
    create_deal(deals, client, manager, 5000, "Крупная сделка")

    assert len(filter_deals_by_stage(deals, "Открыта")) == 2
    ordered = sort_deals_by_amount(deals)
    assert ordered[0].amount == 5000
