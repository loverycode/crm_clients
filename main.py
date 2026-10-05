"""Точка запуска CRM-приложения: клиенты, менеджеры, контакты, сделки."""
from models.clients import (
    Client,
    add_client,
    filter_clients_by_status,
    find_client,
    find_client_by_id,
    sort_clients,
    update_status,
)
from models.contacts import (
    Contact,
    add_contact,
    contacts_for_client,
    find_contact,
)
from models.deals import (
    Deal,
    close_deal,
    create_deal,
    filter_deals_by_stage,
    sort_deals_by_amount,
)
from models.managers import (
    Manager,
    add_manager,
    find_manager,
    find_manager_by_id,
)
from storage import (
    load_clients,
    load_contacts,
    load_deals,
    load_managers,
    save_clients,
    save_contacts,
    save_deals,
    save_managers,
)
from utils import input_float, input_int, input_nonempty

CLIENTS_FILE = "data/clients.json"
MANAGERS_FILE = "data/managers.json"
CONTACTS_FILE = "data/contacts.json"
DEALS_FILE = "data/deals.json"


def show_list(items: list) -> None:
    if not items:
        print("Список пуст")
        return
    print()
    for item in items:
        print(item)
    print()


def print_menu() -> None:
    print("=== CRM: клиенты, менеджеры, контакты, сделки ===")
    print("--- Клиенты ---")
    print(" 1. Показать клиентов")
    print(" 2. Добавить клиента")
    print(" 3. Найти клиента")
    print(" 4. Изменить статус клиента")
    print(" 5. Отфильтровать клиентов по статусу")
    print(" 6. Отсортировать клиентов по имени")
    print("--- Менеджеры ---")
    print(" 7. Показать менеджеров")
    print(" 8. Добавить менеджера")
    print(" 9. Найти менеджера")
    print("--- Контакты ---")
    print("10. Показать контакты клиента")
    print("11. Добавить контакт")
    print("12. Найти контакт")
    print("--- Сделки ---")
    print("13. Показать сделки")
    print("14. Создать сделку")
    print("15. Закрыть сделку")
    print("16. Отфильтровать сделки по стадии")
    print("17. Отсортировать сделки по сумме")
    print(" 0. Выход")


def create_new_contact(contacts: list[Contact], clients: list[Client]) -> None:
    client_id = input_int("ID клиента: ")
    client = find_client_by_id(clients, client_id)
    if client is None:
        print(f"Клиент с ID {client_id} не найден")
        return
    name = input_nonempty("Имя контакта: ")
    phone = input_nonempty("Телефон: ")
    position = input("Должность (необязательно): ").strip()
    try:
        contact = add_contact(contacts, client, name, phone, position)
        print(f"Контакт '{contact.name}' добавлен (ID: {contact.id})")
        save_contacts(CONTACTS_FILE, contacts)
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def create_new_deal(
    deals: list[Deal],
    clients: list[Client],
    managers: list[Manager],
    contacts: list[Contact],
) -> None:
    client_id = input_int("ID клиента: ")
    client = find_client_by_id(clients, client_id)
    if client is None:
        print(f"Клиент с ID {client_id} не найден")
        return

    manager_id = input_int("ID менеджера: ")
    manager = find_manager_by_id(managers, manager_id)
    if manager is None:
        print(f"Менеджер с ID {manager_id} не найден")
        return

    contact_id_raw = input(
        "ID контакта (необязательно, Enter — пропустить): "
    ).strip()
    contact = None
    if contact_id_raw:
        contact = next(
            (c for c in contacts if c.id == int(contact_id_raw)), None
        )
        if contact is None:
            print("Контакт с таким ID не найден, сделка без контакта")

    amount = input_float("Сумма сделки: ")
    title = input_nonempty("Тема сделки: ")
    try:
        deal = create_deal(deals, client, manager, amount, title, contact)
        print(f"Сделка создана (ID: {deal.id})")
        save_deals(DEALS_FILE, deals)
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def main() -> None:
    clients = load_clients(CLIENTS_FILE)
    managers = load_managers(MANAGERS_FILE)
    contacts = load_contacts(CONTACTS_FILE, clients)
    deals = load_deals(DEALS_FILE, clients, managers, contacts)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_list(clients)

        elif choice == "2":
            name = input_nonempty("Название клиента: ")
            try:
                client = add_client(clients, name)
                print(f"Клиент '{client.name}' добавлен (ID: {client.id})")
                save_clients(CLIENTS_FILE, clients)
            except ValueError as exc:
                print(f"Ошибка: {exc}")

        elif choice == "3":
            query = input_nonempty("Название для поиска: ")
            found_clients = find_client(clients, query)
            show_list(found_clients) if found_clients else print(
                f"Клиент '{query}' не найден"
            )

        elif choice == "4":
            client_id = input_int("ID клиента: ")
            new_status = input_nonempty("Новый статус: ")
            if update_status(clients, client_id, new_status):
                print("Статус обновлён")
                save_clients(CLIENTS_FILE, clients)
            else:
                print(f"Клиент с ID {client_id} не найден")

        elif choice == "5":
            status = input_nonempty("Статус для фильтра: ")
            show_list(filter_clients_by_status(clients, status))

        elif choice == "6":
            show_list(sort_clients(clients, by="name"))

        elif choice == "7":
            show_list(managers)

        elif choice == "8":
            name = input_nonempty("Имя менеджера: ")
            email = input_nonempty("Email менеджера: ")
            try:
                manager = add_manager(managers, name, email)
                print(
                    f"Менеджер '{manager.name}' добавлен "
                    f"(ID: {manager.id})"
                )
                save_managers(MANAGERS_FILE, managers)
            except ValueError as exc:
                print(f"Ошибка: {exc}")

        elif choice == "9":
            query = input_nonempty("Имя или email для поиска: ")
            found_managers = find_manager(managers, query)
            show_list(found_managers) if found_managers else print(
                f"Менеджер '{query}' не найден"
            )

        elif choice == "10":
            client_id = input_int("ID клиента: ")
            contact_owner = find_client_by_id(clients, client_id)
            if contact_owner is None:
                print(f"Клиент с ID {client_id} не найден")
            else:
                show_list(contacts_for_client(contacts, contact_owner))

        elif choice == "11":
            create_new_contact(contacts, clients)

        elif choice == "12":
            query = input_nonempty("Имя или телефон для поиска: ")
            found_contacts = find_contact(contacts, query)
            show_list(found_contacts) if found_contacts else print(
                f"Контакт '{query}' не найден"
            )

        elif choice == "13":
            show_list(deals)

        elif choice == "14":
            create_new_deal(deals, clients, managers, contacts)

        elif choice == "15":
            deal_id = input_int("ID сделки: ")
            outcome = input_nonempty(
                "Исход (Выиграна / Проиграна / Отменена): "
            )
            try:
                if close_deal(deals, deal_id, outcome):
                    print("Сделка закрыта")
                    save_deals(DEALS_FILE, deals)
                else:
                    print(f"Сделка с ID {deal_id} не найдена")
            except ValueError as exc:
                print(f"Ошибка: {exc}")

        elif choice == "16":
            stage = input_nonempty("Стадия для фильтра: ")
            show_list(filter_deals_by_stage(deals, stage))

        elif choice == "17":
            show_list(sort_deals_by_amount(deals))

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный пункт меню, попробуйте снова")


if __name__ == "__main__":
    main()
