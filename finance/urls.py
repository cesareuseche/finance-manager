from django.urls import path
from . import views

"""
URL patterns for the finance app
This includes the main dashboard view and entry management views
The dashboard view displays a summary of financial entries
"""
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("add/", views.EntryCreateView.as_view(), name="entry-add"),
    path("delete/<int:pk>/", views.EntryDeleteView.as_view(), name="entry-delete"),
]