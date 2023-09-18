from django.shortcuts import render
from django.http.request import HttpRequest


async def index(request: HttpRequest):
    return render(request, 'power_plants/index.html')