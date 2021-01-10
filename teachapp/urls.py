from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainapp, name="mainapp"),
    path("starttrain", views.starttrain, name="starttrain"),
    path("testing/<int:machineid>", views.testing, name="testing"),
]