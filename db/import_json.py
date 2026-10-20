import json
from db.database import get_connection

CLIENTS_FILE = "data/clients.json"
MANAGERS_FILE = "data/managers.json"
CONTACTS_FILE = "data/contacts.json"
DEALS_FILE = "data/deals.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def import_clients(conn):
    clients = load_json(CLIENTS_FILE)
    conn.executemany(
        "INSERT INTO clients (id, name, status, created) VALUES (?, ?, ?, ?)",
        [(c["id"], c["name"], c["status"], c.get("created", ""))
         for c in clients],
    )


def import_managers(conn):
    managers = load_json(MANAGERS_FILE)
    conn.executemany(
        "INSERT INTO managers (id, name, email) VALUES (?, ?, ?)",
        [(m["id"], m["name"], m["email"]) for m in managers],
    )


def import_contacts(conn):
    contacts = load_json(CONTACTS_FILE)
    conn.executemany(
        "INSERT INTO contacts (id, client_id, name, phone, position) VALUES (?, ?, ?, ?, ?)",
        [(c["id"], c["client_id"], c["name"], c["phone"], c.get("position", ""))
         for c in contacts],
    )


def import_deals(conn):
    deals = load_json(DEALS_FILE)
    conn.executemany(
        "INSERT INTO deals (id, client_id, manager_id, contact_id, amount, title, stage) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (d["id"], d["client_id"], d["manager_id"], d.get("contact_id"),
             d["amount"], d.get("title", ""), d.get("stage", "Открыта"))
            for d in deals
        ],
    )


def main():
    conn = get_connection()
    try:
        import_clients(conn)
        import_managers(conn)
        import_contacts(conn)
        import_deals(conn)
        conn.commit()
        print("Импорт завершён успешно")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
