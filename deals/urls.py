from django.urls import path
from . import views

urlpatterns = [path("", views.deals_list, name="deals_list"),
               path("<int:deal_id>/", views.deal_detail, name="deal_detail")]
