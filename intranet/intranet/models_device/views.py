from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.list import ListView

from models_device.models import Device, ModelDevices
from cities.models import Cities, REGIONS
# Create your views here.


class DeviceView(ListView):
    template_name = "dev_list.html"
    paginate_by = 5


    def my_paginator(self, obj_list, num_list=5):
        try:
            page_num = self.request.GET['page']
        except KeyError:
            page_num = 1

        paginator = Paginator(obj_list, num_list)

        try:
            all_dev = paginator.page(page_num)
        except InvalidPage:
            all_dev = paginator.page(1)

        return all_dev


    def _city(self):
        try:
            reg = Cities.objects.filter(city=self.context["city"]).first()
        except Cities.DoesNotExist:
            raise Http404('Device not found!') 

        all_dev = Device.objects.filter(city=reg)
        self.context["devices"] = self.my_paginator(all_dev)

        return self.context


    def _region(self):
        reg_id = Cities.get_reg_id(self.context["region"])
        all_dev = []
        try:
            reg = Cities.objects.filter(region=reg_id)
        except Cities.DoesNotExist:
            raise Http404('Device not found!')         

        for _dev in reg:
            all_dev += list(Device.objects.filter(city=_dev))

        self.context["devices"] = self.my_paginator(all_dev)
        self.context["cities"] = reg

        return self.context


    def _all_dev(self):
        return Device.objects.all().order_by('city')    


    def get(self, request, *args, **kwargs):
        if "city" in self.kwargs:
            return self._city()

        elif "region" in self.kwargs:
            return self._region()

        else:
            self.all_dev_list = True
            regions = []
            for _reg in REGIONS:
                regions.append(_reg[1])
            self.kwargs["regions"] = regions


        return super(DeviceView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        self.context = super(DeviceView, self).get_context_data(**kwargs)
        self.context["regions"] = self.kwargs["regions"]
        
        return self.context


    def get_queryset(self):
        if self.all_dev_list:
            return self._all_dev()

