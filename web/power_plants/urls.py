from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("a-propos", views.about, name="about"),
    path("<str:region_slug>", views.region, name="region"),
    path("centrale/<int:osm_id>", views.plant, name="plant"),
]
