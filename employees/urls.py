from django.urls import path
from . import views


app_name = "employees"

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("dashboard/", views.EmployeeDashboardView.as_view(), name="dashboard"),
    path("lunch/", views.TodaysLunchView.as_view(), name="lunch"),
]
