from clients import (
    Client,
    add_client,
    filter_clients_by_status,
    find_client,
    find_client_by_id,
    sort_clients,
    update_status,
)
from meetings import (
    Meeting,
    cancel_meeting,
    create_meeting,
    get_meeting_status,
    is_slot_available,
)
from storage import (
    load_clients,
    load_meetings,
    save_clients,
    save_meetings,
)
from utils import input_date, input_int, input_nonempty

CLIENTS_FILE = "data/clients.json"
MEETINGS_FILE = "data/meetings.json"


def show_clients(clients: list[Client]) -> None:
    if not clients:
        print("Список клиентов пуст")
        return
    print("\n--- КЛИЕНТЫ ---")
    for c in clients:
        print(c)
    print("---------------\n")


def show_meetings(meetings: list[Meeting]) -> None:
    if not meetings:
        print("Список встреч пуст")
        return
    print("\n--- ВСТРЕЧИ ---")
    for m in meetings:
        print(m)
    print("---------------\n")


def print_menu() -> None:
    print("=== СИСТЕМА УЧЁТА КЛИЕНТОВ (ClientFlow) ===")
    print(" 1. Показать клиентов")
    print(" 2. Добавить клиента")
    print(" 3. Найти клиента")
    print(" 4. Изменить статус клиента")
    print(" 5. Отфильтровать клиентов по статусу")
    print(" 6. Отсортировать клиентов по имени")
    print(" 7. Показать встречи")
    print(" 8. Проверить доступность клиента на дату")
    print(" 9. Назначить встречу")
    print("10. Отменить встречу")
    print(" 0. Выход")


def create_new_meeting(
    meetings: list[Meeting],
    clients: list[Client],
) -> None:
    client_id = input_int("ID клиента: ")
    client = find_client_by_id(clients, client_id)
    if client is None:
        print(f"Клиент с ID {client_id} не найден")
        return

    meeting_date = input_date("Дата встречи (ДД.ММ.ГГГГ): ")
    topic = input_nonempty("Тема встречи: ")
    try:
        meeting = create_meeting(meetings, client, meeting_date, topic)
        print(f"Встреча назначена (ID: {meeting.id})")
        save_meetings(MEETINGS_FILE, meetings)
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def main() -> None:
    clients = load_clients(CLIENTS_FILE)
    meetings = load_meetings(MEETINGS_FILE, clients)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_clients(clients)

        elif choice == "2":
            name = input_nonempty("Имя клиента: ")
            contact = input_nonempty("Контакт: ")
            try:
                client = add_client(clients, name, contact)
                print(f"Клиент '{client.name}' добавлен (ID: {client.id})")
                save_clients(CLIENTS_FILE, clients)
            except ValueError as exc:
                print(f"Ошибка: {exc}")

        elif choice == "3":
            query = input_nonempty("Имя или контакт для поиска: ")
            found = find_client(clients, query)
            if found:
                for c in found:
                    print(f"Найден: {c}")
            else:
                print(f"Клиент '{query}' не найден")

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
            show_clients(filter_clients_by_status(clients, status))

        elif choice == "6":
            show_clients(sort_clients(clients, by="name"))

        elif choice == "7":
            show_meetings(meetings)

        elif choice == "8":
            client_id = input_int("ID клиента: ")
            client = find_client_by_id(clients, client_id)
            if client is None:
                print(f"Клиент с ID {client_id} не найден")
            else:
                meeting_date = input_date("Дата (ДД.ММ.ГГГГ): ")
                available = is_slot_available(meetings, client, meeting_date)
                print(get_meeting_status(available))

        elif choice == "9":
            create_new_meeting(meetings, clients)

        elif choice == "10":
            meeting_id = input_int("ID встречи: ")
            if cancel_meeting(meetings, meeting_id):
                print("Встреча отменена")
                save_meetings(MEETINGS_FILE, meetings)
            else:
                print(f"Встреча с ID {meeting_id} не найдена")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный пункт меню, попробуйте снова")


if __name__ == "__main__":
    main()
