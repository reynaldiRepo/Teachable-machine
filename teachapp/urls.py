from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainapp, name="mainapp"),
    path("pagetry", views.pagetry, name="mainapp"),
    path("starttrain", views.starttrain, name="starttrain"),
]