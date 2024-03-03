from django.core.paginator import Paginator
import csv
from django.conf import settings


from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))

    with open(settings.BUS_STATION_CSV, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        content = list(reader)

        paginator = Paginator(content, 10)
        page = paginator.get_page(page_number)

        context = {
            'bus_stations': page,
            'page': page,
        }
        return render(request, 'stations/index.html', context)
