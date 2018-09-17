from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import InvalidPage
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import redirect
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
    class Meta:
        model = Device
        fields = ['model', 'ip', 'incoming_port', 'up_connect_ip', 'up_connect_port', 'city', 'comment']


class DeviceDeleteForm(forms.Form):
    device_to_delete = forms.IntegerField()


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

    def post(self, request, *args, **kwargs):
        self.form = DeviceForm(request.POST)

        if self.form.is_valid():

            # Добавление нового устройства на подключение к порту вышестоящего
            connect_on_dev = self.form.cleaned_data['up_connect_ip']

            form_connection_to_up = ConnectionOnDevice()
            form_connection_to_up.id_dev = Device.objects.get(ip=connect_on_dev)
            form_connection_to_up.port = self.form.cleaned_data['up_connect_port']
            form_connection_to_up.connected = self.form.cleaned_data['ip']
            form_connection_to_up.save()
          
            # Сохранение нового устройства
            self.form.save()

            # Добавление UP порта на новое устройство
            form_connection_to_me = ConnectionOnDevice()
            form_connection_to_me.id_dev = Device.objects.get(ip=self.form.cleaned_data['ip'])
            form_connection_to_me.port = self.form.cleaned_data['incoming_port']
            form_connection_to_me.connected = "UP"
            form_connection_to_me.save()

            return redirect('device')
        else:
            return super(DeviceCreate, self).get(request, *args, **kwargs)


class DeviceUpdate(TemplateView):
    form = None
    template_name = 'device_edit.html'

    def get(self, request, *args, **kwargs):
        self.dev = Device.objects.get(pk = self.kwargs['dev_id'])
        self.form = DeviceForm(instance=self.dev)
        return super(DeviceUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DeviceUpdate, self).get_context_data(*args, **kwargs)
        context['device'] = self.dev
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        dev = Device.objects.get(pk = self.kwargs['dev_id'])
        self.form = DeviceForm(request.POST, instance=dev)
        if self.form.is_valid():

            # Редактирование нового устройства на подключение к порту вышестоящего connected
            connect_on_dev = self.form.cleaned_data['up_connect_ip']

            form_connection_to_up = ConnectionOnDevice.objects.get(connected=self.form.cleaned_data['ip'])
            form_connection_to_up.id_dev = Device.objects.get(ip=connect_on_dev)
            form_connection_to_up.port = self.form.cleaned_data['up_connect_port']
            form_connection_to_up.connected = self.form.cleaned_data['ip']
            form_connection_to_up.save()

            # Сохранение нового устройства
            self.form.save()

            # Редактирование UP порта на новом устройстве
            form_connection_to_me = ConnectionOnDevice.objects.get(id_dev=dev)
            form_connection_to_me.id_dev = Device.objects.get(ip=self.form.cleaned_data['ip'])
            form_connection_to_me.port = self.form.cleaned_data['incoming_port']
            form_connection_to_me.connected = "UP"
            form_connection_to_me.save()
          

            return redirect("device")
        else:
            return super(DeviceUpdate, self).get(request, *args, **kwargs)


class DeviceDelete(TemplateView):
    form = None

    def post(self, request, *args, **kwargs):
        form = DeviceDeleteForm(request.POST)
        if form.is_valid():
            device_to_delete = Device.objects.get(pk=form.cleaned_data["device_to_delete"])
            device_to_delete.delete()
        return redirect("device")
        # super(DeviceDelete, self).post(*args, **kwargs)