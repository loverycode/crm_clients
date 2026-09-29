"""Автоматизированные тесты класса Client и функций работы с ним."""
from clients import (
    Client,
    add_client,
    filter_clients_by_status,
    find_client,
    sort_clients,
    update_status,
)


def test_client_creation():
    client = Client(1, "ООО Ромашка")
    assert client.id == 1
    assert client.name == "ООО Ромашка"
    assert client.status == "Новый"


def test_client_str():
    client = Client(1, "ООО Ромашка", "В работе")
    text = str(client)
    assert "ООО Ромашка" in text
    assert "В работе" in text


def test_add_client_empty_name_raises():
    clients = []
    try:
        add_client(clients, "   ")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_find_client():
    clients = []
    add_client(clients, "ООО Ромашка")
    assert find_client(clients, "ромашка")


def test_update_status_function():
    clients = []
    client = add_client(clients, "ООО Ромашка")
    assert update_status(clients, client.id, "В работе")
    assert clients[0].status == "В работе"


def test_filter_and_sort_clients():
    clients = []
    add_client(clients, "Борис Иванов", "Новый")
    add_client(clients, "Анна Петрова", "В работе")
    assert len(filter_clients_by_status(clients, "Новый")) == 1
    ordered = sort_clients(clients, by="name")
    assert ordered[0].name == "Анна Петрова"
