"""wars URL Configuration"""
from django.urls import path
from . import views


app_name = "wars"

urlpatterns = [
    path("participate/", views.Participate.as_view(), name="participate"),
    path("create-menu/", views.MenuCreateView.as_view(), name="create-menu"),
    path("menu/<int:pk>/", views.MenuDetailView.as_view(), name="menu-detail"),
    path("add-to-menu/", views.AddToMenuView.as_view(), name="add-to-menu"),
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),
]
