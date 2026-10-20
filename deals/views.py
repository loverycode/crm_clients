from django.shortcuts import render

from db.database import get_connection


DEALS_QUERY = """
    SELECT
        deals.id,
        deals.title,
        deals.amount,
        deals.stage,
        deals.manager_id,
        clients.name  AS client_name,
        managers.name AS manager_name,
        contacts.name AS contact_name
    FROM deals
    JOIN clients  ON deals.client_id  = clients.id
    JOIN managers ON deals.manager_id = managers.id
    LEFT JOIN contacts ON deals.contact_id = contacts.id
"""


def deals_list(request):
    conn = get_connection()
    try:
        deals = conn.execute(
            DEALS_QUERY + " ORDER BY deals.id"
        ).fetchall()
    finally:
        conn.close()
    return render(request, "deals/deal_list.html", {"deals": deals})


def deal_detail(request, deal_id):
    conn = get_connection()
    try:
        deal = conn.execute(
            DEALS_QUERY + " WHERE deals.id = ?",
            (deal_id,),
        ).fetchone()

        manager_available = None
        if deal is not None:
            open_count = conn.execute(
                "SELECT COUNT(*) FROM deals "
                "WHERE manager_id = ? AND stage = 'Открыта'",
                (deal["manager_id"],),
            ).fetchone()[0]
            manager_available = open_count < 5
    finally:
        conn.close()

    context = {"deal": deal, "manager_available": manager_available}
    return render(
        request,
        "deals/deal_detail.html",
        context,
        status=404 if deal is None else 200,
    )


def statistics(request):
    conn = get_connection()
    try:
        by_client = conn.execute(
            """
            SELECT
                clients.name      AS client_name,
                COUNT(deals.id)   AS deals_count,
                COALESCE(SUM(deals.amount), 0) AS total_amount
            FROM clients
            LEFT JOIN deals ON clients.id = deals.client_id
            GROUP BY clients.id, clients.name
            ORDER BY deals_count DESC, client_name
            """
        ).fetchall()

        by_manager = conn.execute(
            """
            SELECT
                managers.name     AS manager_name,
                COUNT(deals.id)   AS deals_count
            FROM managers
            LEFT JOIN deals ON managers.id = deals.manager_id
            GROUP BY managers.id, managers.name
            ORDER BY deals_count DESC, manager_name
            """
        ).fetchall()

        total = conn.execute(
            "SELECT COUNT(*) AS cnt, COALESCE(SUM(amount), 0) AS total "
            "FROM deals"
        ).fetchone()
    finally:
        conn.close()

    context = {
        "by_client": by_client,
        "by_manager": by_manager,
        "total_count": total["cnt"],
        "total_amount": total["total"],
    }
    return render(request, "deals/statistics.html", context)
