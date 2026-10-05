from django.http import HttpResponse

from homepage.views import page
from models.clients import find_client_by_id
from models.contacts import contacts_for_client
from storage import load_clients, load_contacts


def clients_list(request):
    items = ""
    for client in load_clients("data/clients.json"):
        badge = "bg-success" if client.status == "В работе" else "bg-secondary"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/clients/{client.id}/">{client.name}</a>
            <span class="badge {badge}">{client.status}</span>
        </li>
        """
    content = f"""
    <h1>Клиенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("CRM – клиенты", content))


def client_detail(request, client_id):
    clients_data = load_clients("data/clients.json")
    client = find_client_by_id(clients_data, client_id)

    if client is None:
        content = """
        <h1 class="text-danger">Клиент не найден</h1>
        <a href="/clients/" class="btn btn-outline-secondary">
            &larr; к списку клиентов
        </a>
        """
        return HttpResponse(page("Клиент не найден", content), status=404)

    contacts_data = load_contacts("data/contacts.json", clients_data)
    client_contacts = contacts_for_client(contacts_data, client)

    contacts_html = ""
    for contact in client_contacts:
        position = f", {contact.position}" if contact.position else ""
        contacts_html += f"""
        <li class="list-group-item">
            {contact.name}{position} &mdash; {contact.phone}
        </li>
        """
    if not contacts_html:
        contacts_html = (
            '<li class="list-group-item text-muted">Контактов пока нет</li>'
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{client.name}</h5>
            <p class="card-text"><strong>ID:</strong> {client.id}</p>
            <p class="card-text"><strong>Статус:</strong> {client.status}</p>
            <p class="card-text">
                <strong>Клиент с:</strong> {client.created}
            </p>
            <h6 class="mt-4">Контакты</h6>
            <ul class="list-group mb-3">{contacts_html}</ul>
            <a href="/clients/" class="btn btn-outline-secondary">
                &larr; к списку клиентов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(client.name, content), status=200)
