from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("centrale/<str:osm_id>", views.plant, name="plant"),
    path("a-propos", views.about, name="about"),
]
