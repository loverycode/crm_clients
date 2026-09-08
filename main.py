from datetime import date

clients_db = []
next_id = 1
#Добавление нового клиента с указанием имени, контактов и статуса
def add_client(name, contact, status="Новый"):
    global next_id
    client = {
        "id": next_id,
        "name": name.strip().title(),
        "contact": contact.strip(),
        "status": status,
        "created": str(date.today())
    }
    clients_db.append(client)
    next_id += 1
    print(f"Клиент '{client['name']}' добавлен (ID: {client['id']})")

#Просмотр списка всех клиентов
def show_clients():
    if not clients_db:
        print("Список клиентов пуст")
        return
    print("\n--- ВСЕ КЛИЕНТЫ ---")
    for c in clients_db:
        print(f"ID: {c['id']}, Имя: {c['name']}, Контакт: {c['contact']}, Статус: {c['status']}")
    print("--------------------\n")

# Функция 3: Поиск клиента по имени или контакту
def find_client(search):
    found = False
    search_lower = search.lower()
    for c in clients_db:
        if search_lower in c['name'].lower() or search_lower in c['contact'].lower():
            print(f"🔍 Найден: ID {c['id']}, Имя: {c['name']}, Контакт: {c['contact']}, Статус: {c['status']}")
            found = True
    if not found:
        print(f"Клиент '{search}' не найден")

# Функция 4: Изменение статуса клиента
def update_status(client_id, new_status):
    for c in clients_db:
        if c['id'] == client_id:
            old = c['status']
            c['status'] = new_status
            print(f"🔄 Статус клиента '{c['name']}' изменён с '{old}' на '{new_status}'")
            return
    print(f" Клиент с ID {client_id} не найден")

if __name__ == "__main__":
    print("=== СИСТЕМА УЧЁТА КЛИЕНТОВ ===\n")
    
    add_client("Иван Петров", "+7-999-123-45-67")
    add_client("ООО Ромашка", "info@romashka.ru", "В работе")
    add_client("Анна Смирнова", "anna@email.com", "Завершено")
    
    show_clients()
    
    find_client("иван")
    find_client("+7-999")
    
    update_status(1, "В работе")
    show_clients()