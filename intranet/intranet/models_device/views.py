from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage

from models_device.models import Device, ModelDevices
from cities.models import Cities, REGIONS
# Create your views here.


def index(request):
    regions = []
    for _reg in REGIONS:
        regions.append(_reg[1])

    try:
    	page_num = request.GET['page']
    except KeyError:
    	page_num = 1

    paginator = Paginator(Device.objects.all().order_by('city'), 5)

    try:
    	all_dev = paginator.page(page_num)
    except InvalidPage:
    	all_dev = paginator.page(1)

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

    return render(request, "dev_list.html", {
        "devices":all_dev, 
        "cities":reg,
        "region":region,
        })

def city(request, region, city):

    try:
        reg = Cities.objects.filter(city=city).first()
    except Cities.DoesNotExist:
        raise Http404('Device not found!')  

    all_dev = Device.objects.filter(city=reg)

    return render(request, "dev_list.html", {
        "devices":all_dev, 
        "region":region,
        "city":city,
        })