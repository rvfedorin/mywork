from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage

from models_device.models import Device, ModelDevices
from cities.models import Cities, REGIONS
# Create your views here.


def my_paginator(request, obj_list, num_list=5):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1

    paginator = Paginator(obj_list, num_list)

    try:
        all_dev = paginator.page(page_num)
    except InvalidPage:
        all_dev = paginator.page(1)

    return all_dev


def index(request):
    regions = []
    for _reg in REGIONS:
        regions.append(_reg[1])

    all_dev = my_paginator(request, Device.objects.all().order_by('city'))

    return render(request, "dev_list.html", {
        "devices":all_dev, 
        "regions":regions, 
        })


def region(request, region):
    reg_id = Cities.get_reg_id(region)
    all_dev = []

    try:
        reg = Cities.objects.filter(region=reg_id)
    except Cities.DoesNotExist:
        raise Http404('Device not found!')         

    for _dev in reg:
        all_dev += list(Device.objects.filter(city=_dev))

    all_dev_page = my_paginator(request, all_dev)

    return render(request, "dev_list.html", {
        "devices":all_dev_page, 
        "cities":reg,
        "region":region,
        })


def city(request, region, city):

    try:
        reg = Cities.objects.filter(city=city).first()
    except Cities.DoesNotExist:
        raise Http404('Device not found!')  

    all_dev = Device.objects.filter(city=reg)

    all_dev_page = my_paginator(request, all_dev)

    return render(request, "dev_list.html", {
        "devices":all_dev_page, 
        "region":region,
        "city":city,
        })