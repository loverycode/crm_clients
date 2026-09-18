from clients import (
    Client,
    add_client,
    filter_clients_by_status,
    find_client,
    sort_clients,
    update_status,
)


def test_client_creation():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    assert client.id == 1
    assert client.name == "Иван Петров"
    assert client.status == "Новый"


def test_client_str():
    client = Client(1, "Иван Петров", "+7-999-123-45-67", "В работе")
    text = str(client)
    assert "Иван Петров" in text
    assert "В работе" in text


def test_client_update_status_method():
    client = Client(1, "Анна Смирнова", "anna@email.com")
    client.update_status("Завершено")
    assert client.status == "Завершено"


def test_add_client():
    clients = []
    add_client(clients, "Иван Петров", "+7-999-123-45-67")
    assert len(clients) == 1
    assert isinstance(clients[0], Client)
    assert clients[0].name == "Иван Петров"


def test_add_client_empty_name_raises():
    clients = []
    try:
        add_client(clients, "   ", "+7-999-123-45-67")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_find_client():
    clients = []
    add_client(clients, "Иван Петров", "+7-999-123-45-67")
    assert find_client(clients, "иван")


def test_update_status_function():
    clients = []
    client = add_client(clients, "Анна Смирнова", "anna@email.com")
    assert update_status(clients, client.id, "В работе")
    assert clients[0].status == "В работе"


def test_filter_and_sort_clients():
    clients = []
    add_client(clients, "Борис", "boris@mail.ru", "Новый")
    add_client(clients, "Анна", "anna@mail.ru", "В работе")
    assert len(filter_clients_by_status(clients, "Новый")) == 1
    ordered = sort_clients(clients, by="name")
    assert ordered[0].name == "Анна"
