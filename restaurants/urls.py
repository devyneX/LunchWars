"""restaurants URL Configuration"""
from django.urls import path
from . import views


app_name = "restaurants"

urlpatterns = [
    path("create/", views.RestaurantCreateView.as_view(), name="create"),
    path("dashboard/", views.RestaurantDashboardView.as_view(), name="dashboard"),
    path("add-dish/", views.AddDishView.as_view(), name="add-dish"),
    path("dishes/", views.DishListView.as_view(), name="dishes"),
]
