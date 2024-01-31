from django.urls import path
from . import views


app_name = "restaurants"

urlpatterns = [
    path("create/", views.RestaurantCreateView.as_view(), name="create"),
    path("dashboard/", views.RestaurantDashboardView.as_view(), name="dashboard"),
]
