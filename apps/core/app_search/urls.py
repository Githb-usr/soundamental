# apps/core/app_search/urls.py
from django.urls import path
from .views import search_view

app_name = "app_search"

urlpatterns = [
    path("", search_view, name="search"),
]
