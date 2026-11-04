from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, Q, F
from django.core.paginator import Paginator
from .models import Deal
from clients.models import Client, Manager


def deals_list(request):
    deals = Deal.objects.annotate(
        client_name=F("client__name"),
        manager_name=F("manager__name")
    ).values(
        "id", "title", "amount", "stage", "client_name", "manager_name"
    )

    stage = request.GET.get('stage', '').strip()
    if stage:
        deals = deals.filter(stage=stage)

    client_id = request.GET.get('client', '').strip()
    if client_id and client_id.isdigit():
        deals = deals.filter(client_id=int(client_id))

    sort = request.GET.get('sort', 'id')
    if sort in ['id', '-id', 'amount', '-amount', 'stage']:
        deals = deals.order_by(sort)

    paginator = Paginator(deals, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'deals': page_obj,
        'page_obj': page_obj,
        'stage': stage,
        'client_id': client_id,
        'sort': sort,
        'clients': Client.objects.all(),
        'stages': Deal.Stage.choices,
    }
    return render(request, "deals/deal_list.html", context)


def deal_detail(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.select_related('client', 'manager', 'contact'),
        pk=deal_id
    )

    open_count = deal.manager.deals.filter(stage=Deal.Stage.OPEN).count()
    manager_available = open_count < 5

    context = {"deal": deal, "manager_available": manager_available}
    return render(request, "deals/deal_detail.html", context)


def statistics(request):
    by_client = Client.objects.annotate(
        deals_count=Count('deals'),
        total_amount=Sum('deals__amount')
    ).order_by('-deals_count', 'name')

    by_manager = Manager.objects.annotate(
        deals_count=Count('deals', filter=Q(deals__stage=Deal.Stage.OPEN)),
        total_amount=Sum('deals__amount', filter=Q(deals__amount__gt=0))
    ).order_by('-deals_count', 'name')

    total_stats = Deal.objects.aggregate(
        total_count=Count('id'),
        total_amount=Sum('amount')
    )

    context = {
        "by_client": by_client,
        "by_manager": by_manager,
        "total_count": total_stats['total_count'] or 0,
        "total_amount": total_stats['total_amount'] or 0,
    }
    return render(request, "deals/statistics.html", context)
