from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import InvalidPage
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django import forms

from models_device.models import Device, ModelDevices
from cities.models import Cities
from connection_on_device.models import ConnectionOnDevice

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


class DeviceForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Device
        fields = ['model', 'ip', 'incoming_port', 'up_connect_ip', 'up_connect_port', 'city', 'comment']


class DeviceCreate(TemplateView):
    form = None
    template_name = "device_add.html"

    def get(self, request, *args, **kwargs):
        self.form = DeviceForm()
        return super(DeviceCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DeviceCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    # success_url = "device"

# class ConnectionOnDevice(models.Model):
#     id_dev = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL, 
#         help_text='ID оборудования, к которому подключен клиент/устройство')
#     port = models.PositiveSmallIntegerField(help_text='Порт подключения')
#     connected = models.CharField(max_length=30, help_text='Что подключено к порту')
#     vlan = models.CharField(max_length=5, default='Null', help_text='vlan клиента, если есть')
#     ip_client = models.TextField(blank=True, verbose_name='IP клиента', help_text='IP/сеть выделенные клиенту. Если несколько - через ";"')
#     comment = models.TextField(blank=True, help_text='Комментарий')
#     date = models.DateTimeField(auto_now_add=True, help_text='Дата добавления')
#     update = models.DateTimeField(auto_now=True, help_text='Дата изменения')