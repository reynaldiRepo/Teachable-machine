from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainapp, name="mainapp"),
    path("starttrain", views.starttrain, name="starttrain"),
    path("testing/<int:machineid>", views.testing, name="testing"),
    path("downloadmodel/<int:machineid>", views.downloadModel, name="downloadModel"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("savingmodel", views.savingmodel, name="savingmodel"),
    path("usermodels", views.usermodels, name="usermodels"),
    path("about-us", views.about, name="about"),
    path("our-machine", views.ourmachine, name="ourmachine"),
]