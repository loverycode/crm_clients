from django.urls import path

from . import views

app_name = "deals"

urlpatterns = [
    path("", views.deals_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:deal_id>/", views.deal_detail, name="detail"),
]
