from django.urls import path
from . import views

app_name= "encyclopedia"
urlpatterns=[
    path("", views.index, name = "index"),
    path("encyclopedia/<str:title>", views.entry, name="entry"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("encyclopedia/<str:title>/edit", views.edit, name= "edit"),
    path("search", views.search, name= "search"),
    path("random_pages", views.random_pages, name = "random_pages")
]
