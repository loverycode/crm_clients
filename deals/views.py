from django.http import HttpResponse

from homepage.views import page
from models.deals import find_deal_by_id, is_manager_available
from storage import load_clients, load_contacts, load_deals, load_managers

STAGE_BADGES = {
    "Открыта": "bg-primary",
    "Выиграна": "bg-success",
    "Проиграна": "bg-danger",
    "Отменена": "bg-secondary",
}


def _load_all():
    clients = load_clients("data/clients.json")
    managers = load_managers("data/managers.json")
    contacts = load_contacts("data/contacts.json", clients)
    deals = load_deals("data/deals.json", clients, managers, contacts)
    return clients, managers, contacts, deals


def deals_list(request):
    _, _, _, deals = _load_all()

    items = ""
    for deal in deals:
        badge = STAGE_BADGES.get(deal.stage, "bg-secondary")
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/deals/{deal.id}/">
                {deal.title or "Сделка №" + str(deal.id)}
                &mdash; {deal.client.name}
            </a>
            <span class="badge {badge}">{deal.stage}</span>
        </li>
        """
    content = f"""
    <h1>Сделки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("CRM – сделки", content))


def deal_detail(request, deal_id):
    _, _, _, deals = _load_all()
    deal = find_deal_by_id(deals, deal_id)

    if deal is None:
        content = """
        <h1 class="text-danger">Сделка не найдена</h1>
        <a href="/deals/" class="btn btn-outline-secondary">
            &larr; к списку сделок
        </a>
        """
        return HttpResponse(page("Сделка не найдена", content), status=404)

    badge = STAGE_BADGES.get(deal.stage, "bg-secondary")
    contact_line = ""
    if deal.contact is not None:
        contact_line = f"""
        <p class="card-text">
            <strong>Контакт:</strong> {deal.contact.name}
        </p>
        """

    available = is_manager_available(deals, deal.manager)
    load_status = "доступен" if available else "загружен"
    load_badge = "bg-success" if available else "bg-warning text-dark"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                {deal.title or "Сделка №" + str(deal.id)}
            </h5>
            <p class="card-text">
                <strong>Клиент:</strong> {deal.client.name}
            </p>
            <p class="card-text">
                <strong>Менеджер:</strong> {deal.manager.name}
                <span class="badge {load_badge}">{load_status}</span>
            </p>
            {contact_line}
            <p class="card-text"><strong>Сумма:</strong> {deal.amount}</p>
            <p class="card-text">
                <strong>Стадия:</strong>
                <span class="badge {badge}">{deal.stage}</span>
            </p>
            <a href="/deals/" class="btn btn-outline-secondary">
                &larr; к списку сделок
            </a>
        </div>
    </div>
    """
    title = deal.title or f"Сделка №{deal.id}"
    return HttpResponse(page(title, content), status=200)
