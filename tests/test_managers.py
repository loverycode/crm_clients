"""Автоматизированные тесты класса Manager и функций работы с ним."""
from models.managers import Manager, add_manager, find_manager


def test_manager_creation():
    manager = Manager(1, "Анна Смирнова", "anna@company.ru")
    assert manager.id == 1
    assert manager.email == "anna@company.ru"


def test_is_valid_email():
    assert Manager.is_valid_email("anna@company.ru")
    assert not Manager.is_valid_email("anna.company.ru")
    assert not Manager.is_valid_email("   ")


def test_add_manager_invalid_email_raises():
    managers = []
    try:
        add_manager(managers, "Анна Смирнова", "не email")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_find_manager():
    managers = []
    add_manager(managers, "Анна Смирнова", "anna@company.ru")
    assert find_manager(managers, "анна")
    assert find_manager(managers, "company.ru")
