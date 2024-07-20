from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView(), name="index"),
    path("a-propos", views.AboutView(), name="about"),
    path("<str:region_slug>", views.RegionView(), name="region"),
    path("centrale/<osm_id>", views.PlantView(), name="plant"),
]
