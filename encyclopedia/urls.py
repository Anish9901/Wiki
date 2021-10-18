from re import search
from django.urls import path

from . import views
""" app_name = "wiki" """
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index2"),
    path("wiki/<str:titles>", views.entry_page, name="display_page"),
    path("wiki/search/", views.search,name = "search_page"),
    path("wiki/newpage/",views.create_newpage,name = "new_page"),
    path("wiki/random/",views.random_page,name ="random_page"),
    path("wiki/edit/<str:page_name>",views.edit_page,name = "edit_page")
]