from django.urls import path
from apps.core.app_index.views import index_or_category_view

app_name = "app_index"

urlpatterns = [
    # Index général
    path("", index_or_category_view, name="index"),
    # path("index/", index_or_category_view, name="index"),
    path("index/<str:letter>/", index_or_category_view, name="index_letter"),
    path("index/<str:letter>/<str:sub_letter>/", index_or_category_view, name="index_sub_letter"),

    # Index thématique
    path("category/<str:category>/", index_or_category_view, name="category_index"),
    path("category/<str:category>/<str:letter>/", index_or_category_view, name="category_index_letter"),
    path("category/<str:category>/<str:letter>/<str:sub_letter>/", index_or_category_view, name="category_index_sub_letter"),
]
