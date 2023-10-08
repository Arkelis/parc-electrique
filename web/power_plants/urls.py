from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plant/<int:osm_id>", views.plant, name="plant"),
]
