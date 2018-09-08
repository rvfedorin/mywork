from django.shortcuts import render
from django.http import HttpResponse, Http404

from models_device.models import Device, ModelDevices
from cities.models import Cities
# Create your views here.


def index(request):
    all_dev = Device.objects.all()

    return render(request, "dev_list.html", {
        "devices":all_dev, 
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

def city(request, city):
    all_dev = Device.objects.filter()

    return render(request, "dev_list.html", {
        "devices":all_dev, 
        })