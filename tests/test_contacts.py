"""Автоматизированные тесты класса Contact и функций работы с ним."""
from models.clients import Client
from models.contacts import add_contact, contacts_for_client, find_contact


def test_contact_creation_linked_to_client():
    client = Client(1, "ООО Ромашка")
    contacts = []
    contact = add_contact(contacts, client, "Сергей Волков", "+7-900-1")
    assert contact.client is client
    assert "ООО Ромашка" in str(contact)


def test_add_contact_empty_phone_raises():
    client = Client(1, "ООО Ромашка")
    contacts = []
    try:
        add_contact(contacts, client, "Сергей Волков", "   ")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_find_contact():
    client = Client(1, "ООО Ромашка")
    contacts = []
    add_contact(contacts, client, "Сергей Волков", "+7-900-1")
    assert find_contact(contacts, "волков")


def test_contacts_for_client():
    client_1 = Client(1, "ООО Ромашка")
    client_2 = Client(2, "ИП Иванов")
    contacts = []
    add_contact(contacts, client_1, "Сергей Волков", "+7-900-1")
    add_contact(contacts, client_2, "Мария Орлова", "+7-900-2")
    result = contacts_for_client(contacts, client_1)
    assert len(result) == 1
    assert result[0].name == "Сергей Волков"
