from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import TemplateView

from models_device.models import Device, ModelDevices
from cities.models import Cities, REGIONS
# Create your views here.


class DeviceView(TemplateView):
    template_name = "dev_list.html"


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
        regions = []
        for _reg in REGIONS:
            regions.append(_reg[1])

        self.context["devices"] = self.my_paginator(Device.objects.all().order_by('city'))
        self.context["regions"] = regions

        return self.context        


    def get_context_data(self, **kwars):
        self.context = super(DeviceView, self).get_context_data(**kwars)

        if "city" in self.context:
            return self._city()

        elif "region" in self.context:
            return self._region()

        else:
            return self._all_dev()
