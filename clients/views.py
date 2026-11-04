from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Client, Manager


def clients_list(request):
    clients = Client.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        clients = clients.filter(name__icontains=query)

    status = request.GET.get('status', '').strip()
    if status:
        clients = clients.filter(status=status)

    sort = request.GET.get('sort', 'name')
    if sort in ['name', '-name', 'created', '-created']:
        clients = clients.order_by(sort)

    paginator = Paginator(clients, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'clients': page_obj,
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'sort': sort
    }
    return render(request, "clients/client_list.html", context)


def client_detail(request, client_id):
    client = get_object_or_404(
        Client.objects.prefetch_related('contacts'), pk=client_id)

    context = {"client": client}
    return render(request, "clients/client_detail.html", context)


def managers_load(request):
    managers = Manager.objects.annotate(
        open_count=Count('deals', filter=Q(deals__stage='Открыта'))
    ).filter(open_count__lt=5).order_by('open_count', 'name')

    return render(request, "clients/managers_load.html", {"managers": managers})
