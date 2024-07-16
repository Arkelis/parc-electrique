from django.urls import path
from django.urls import include
from django.conf import settings

urlpatterns = [
    path("", include('power_plants.urls'))
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns.extend(debug_toolbar_urls())