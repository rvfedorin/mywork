from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.list import ListView

from models_device.models import Device, ModelDevices
from cities.models import Cities
# Create your views here.


class DeviceView(ListView):
    template_name = "dev_list.html"
    paginate_by = 5


    def __init__(self, *args, **kwargs):
        super(DeviceView, self).__init__(*args, **kwargs)

        self.regions = Cities.all_regions


    def _city(self):
        try:
            reg = Cities.objects.filter(city=self.kwargs["city"]).first()
        except Cities.DoesNotExist:
            raise Http404('Device not found!') 

        return Device.objects.filter(city=reg)


    def _region(self):
        reg_id = Cities.get_reg_id(self.kwargs["region"])
        all_dev = []
        try:
            reg = Cities.objects.filter(region=reg_id)
        except Cities.DoesNotExist:
            raise Http404('Device not found!')         

        for _dev in reg:
            all_dev += list(Device.objects.filter(city=_dev))

        self.kwargs["cities"] = reg

        return all_dev


    def _all_dev(self):
        self.kwargs["regions"] = self.regions
        return Device.objects.all().order_by('city')    


    def get(self, request, *args, **kwargs):

        if "city" in self.kwargs:
            self._action_list = [self._city, "city", "region"]
        elif "region" in self.kwargs:
            self._action_list = [self._region, "cities", "region"]
        else:
            self._action_list = [self._all_dev, "regions"]
            
        return super(DeviceView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        self.context = super(DeviceView, self).get_context_data(**kwargs)

        for _key in self._action_list[1:]:
            self.context[_key] = self.kwargs[_key]

        return self.context


    def get_queryset(self):
        return self._action_list[0]()


