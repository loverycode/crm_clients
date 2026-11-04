import sqlite3
from datetime import date
from clients.models import Client, Manager, Contact
from deals.models import Deal

SOURCE_DB = "data/crm.sqlite"


def main():
    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        clients = conn.execute("SELECT * FROM clients").fetchall()
        managers = conn.execute("SELECT * FROM managers").fetchall()
        contacts = conn.execute("SELECT * FROM contacts").fetchall()
        deals = conn.execute("SELECT * FROM deals").fetchall()

    for row in clients:
        Client.objects.update_or_create(
            pk=row["id"],
            defaults={"name": row["name"], "status": row["status"],
                      "created": date.fromisoformat(row["created"])}
        )

    for row in managers:
        Manager.objects.update_or_create(
            pk=row["id"],
            defaults={"name": row["name"], "email": row["email"]}
        )

    for row in contacts:
        Contact.objects.update_or_create(
            pk=row["id"],
            defaults={"client_id": row["client_id"], "name": row["name"],
                      "phone": row["phone"], "position": row["position"]}
        )

    for row in deals:
        Deal.objects.update_or_create(
            pk=row["id"],
            defaults={
                "client_id": row["client_id"],
                "manager_id": row["manager_id"],
                "contact_id": row["contact_id"],
                "amount": row["amount"],
                "title": row["title"],
                "stage": row["stage"]
            }
        )

    print("Перенос данных завершен!")
    print(f"Клиентов: {Client.objects.count()}")
    print(f"Менеджеров: {Manager.objects.count()}")
    print(f"Контактов: {Contact.objects.count()}")
    print(f"Сделок: {Deal.objects.count()}")


main()
