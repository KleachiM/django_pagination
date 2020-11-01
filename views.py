import csv
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from app.settings import BUS_STATION_CSV


# def index(request):
#     return redirect(reverse(bus_stations))
def index(request):
    param = urlencode({'page': 2})
    view = reverse(bus_stations)
    url = view + '?' + param
    # print(url)
    return redirect(url)

with open(BUS_STATION_CSV, encoding='cp1251') as f:
    from_csv = csv.DictReader(f)
    csv_data = []
    for row in from_csv:
        csv_data.append(row)

def bus_stations(request):
    # print(request.Get.get('page'))
    paginator = Paginator(csv_data, 10)
    current_page = request.GET.get('page')
    # current_page = 2
    next_page_url = None
    prev_page_url = None
    page = paginator.get_page(current_page)
    if page.has_previous():
        prev_page_num = page.previous_page_number()
        url = '?page=' + str(prev_page_num)
        prev_page_url = url
    if page.has_next():
        next_page_num = page.next_page_number()
        url = '?page=' + str(next_page_num)
        next_page_url = url
    return render(request, 'index.html', context={
        # 'bus_stations': [{'Name': 'название', 'Street': 'улица', 'District': 'район'},
        #                  {'Name': 'другое название', 'Street': 'другая улица', 'District': 'другой район'}],
        'bus_stations': page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

