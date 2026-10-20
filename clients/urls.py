from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path("", views.clients_list, name="list"),
    path("managers/", views.managers_load, name="managers_load"),
    path("<int:client_id>/", views.client_detail, name="detail"),
]
