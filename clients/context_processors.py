from .models import Client


def crm_context(request):
    return {
        "site_name": "CRM Система",
        "clients_count": Client.objects.count(),
    }
