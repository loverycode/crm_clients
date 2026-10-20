from django.shortcuts import render

from db.database import get_connection


def clients_list(request):
    conn = get_connection()
    try:
        clients = conn.execute(
            "SELECT id, name, status, created FROM clients ORDER BY name"
        ).fetchall()
    finally:
        conn.close()
    return render(request, "clients/client_list.html", {"clients": clients})


def client_detail(request, client_id):
    conn = get_connection()
    try:
        client = conn.execute(
            "SELECT id, name, status, created FROM clients WHERE id = ?",
            (client_id,),
        ).fetchone()

        contacts = []
        if client is not None:
            contacts = conn.execute(
                "SELECT id, name, phone, position "
                "FROM contacts WHERE client_id = ? ORDER BY name",
                (client_id,),
            ).fetchall()
    finally:
        conn.close()

    context = {"client": client, "contacts": contacts}
    return render(
        request,
        "clients/client_detail.html",
        context,
        status=404 if client is None else 200,
    )


def managers_load(request):
    conn = get_connection()
    try:
        managers = conn.execute(
            """
            SELECT
                managers.id,
                managers.name,
                managers.email,
                COUNT(deals.id) AS open_count
            FROM managers
            LEFT JOIN deals
                ON managers.id = deals.manager_id
                AND deals.stage = 'Открыта'
            GROUP BY managers.id, managers.name, managers.email
            HAVING COUNT(deals.id) < 5
            ORDER BY open_count, managers.name
            """
        ).fetchall()
    finally:
        conn.close()
    return render(
        request,
        "clients/managers_load.html",
        {"managers": managers},
    )
