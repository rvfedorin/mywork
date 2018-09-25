from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import InvalidPage
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin



from models_device.models import Device, ModelDevices
from cities.models import Cities
from connection_on_device.models import ConnectionOnDevice

# Create your views here.

class PathToCityMixin(ContextMixin):
    def __init__(self, *args, **kwargs):
        super(PathToCityMixin, self).__init__(*args, **kwargs)
        
        self.regions = Cities.all_regions()


    def _city(self):
        try:
            reg = Cities.objects.filter(city=self.kwargs["city"]).first()
        except Cities.DoesNotExist:
            raise Http404('Device not found!') 

        return Device.objects.filter(city=reg)


    def _region(self):
        reg_id = Cities.get_reg_id(self.kwargs["region"])
        all_dev = []

        for _dev in self.reg:
            all_dev += list(Device.objects.filter(city=_dev))

        return all_dev


    def _all_dev(self):
        return Device.objects.all().order_by('city')    


    def get(self, request, *args, **kwargs):
        current_user = request.user
        if "city" in self.kwargs:
            self._action_list = [self._city, "city", "region", "regions", "cities"]
            self.kwargs["regions"] = self.regions
            if Cities.get_reg_id(self.kwargs["region"]): # if there is such region
                reg_id = Cities.get_reg_id(self.kwargs["region"])
                try:
                    self.reg = Cities.objects.filter(region=reg_id)
                except Cities.DoesNotExist:
                    raise Http404('Device not found!') 
                self.kwargs["cities"] = self.reg
            try:
                Cities.objects.get(city=self.kwargs["city"])
            except Cities.DoesNotExist: # if there is no such city
                return redirect('device')
        elif "region" in self.kwargs:
            self._action_list = [self._region, "cities", "region", "regions"]
            if Cities.get_reg_id(self.kwargs["region"]): # if there is such region
                reg_id = Cities.get_reg_id(self.kwargs["region"])
                try:
                    self.reg = Cities.objects.filter(region=reg_id)
                except Cities.DoesNotExist:
                    raise Http404('Device not found!') 
                self.kwargs["cities"] = self.reg
                self.kwargs["regions"] = self.regions
            else:
                return redirect('device')
        else:
            self._action_list = [self._all_dev, "regions"]
            self.kwargs["regions"] = self.regions
            
        return super(PathToCityMixin, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        self.context = super(PathToCityMixin, self).get_context_data(**kwargs)

        for _key in self._action_list[1:]:
            self.context[_key] = self.kwargs[_key]
            # forming string view 'Region2 (Orel, Kursk, Voronezh)'
            #
            # if _key == "regions":
            #     cities = []
            #     for region in self.regions:
            #         _refion_with_sity_string = ""
            #         _citys_in_region = Cities.objects.filter(region=Cities.get_reg_id(region))
            #         _city_text = []
            #         for city_obj in _citys_in_region:
            #             _city_text.append(city_obj.city)
            #         _refion_with_sity_string += f" ( {', '.join(_city_text)} )"
            #         cities.append(_refion_with_sity_string)
            #     self.context["regions"] = zip(self.regions, cities)
                # end forming

        return self.context




class DeviceView(PathToCityMixin, ListView):
    template_name = "dev_list.html"
    paginate_by = 12

    def get_queryset(self):
        return self._action_list[0]()



class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['model', 'ip', 'incoming_port', 'up_connect_ip', 'up_connect_port', 'city', 'comment']
        error_messages = {'ip': {'unique': 'Устройство с таким IP уже существует.'}
        }



class DeviceDeleteForm(forms.Form):
    device_to_delete = forms.IntegerField()


class DeviceCreate(PathToCityMixin, TemplateView):
    form = None
    template_name = "device_add.html"


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.has_perm("models_device.add_device"):
                if "city" in self.kwargs:  # Если город определен, то выводим его в форме по умолчанию
                    self.form = DeviceForm(initial={'city': Cities.objects.filter(city=self.kwargs["city"]).first()})
                    print(self.kwargs["city"])
                else:
                    self.form = DeviceForm()

                return super(DeviceCreate, self).get(request, *args, **kwargs)
            else:
                return redirect("/login/?next=", request.path)
        else:
            return redirect("/login/?next=", request.path)    

    def get_context_data(self, **kwargs):
        context = super(DeviceCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.form = DeviceForm(request.POST)

        if self.form.is_valid():
            # Сохранение нового устройства
            self.form.save()

            # Добавление нового устройства на подключение к порту вышестоящего
            connect_on_dev = self.form.cleaned_data['up_connect_ip']
            if connect_on_dev != '255.255.255.255':
                form_connection_to_up = ConnectionOnDevice()
                form_connection_to_up.id_dev = Device.objects.get(ip=connect_on_dev)
                form_connection_to_up.port = self.form.cleaned_data['up_connect_port']
                form_connection_to_up.connected = f"DOWN to {self.form.cleaned_data['ip']}"
                form_connection_to_up.save()
                messages.add_message(request, messages.SUCCESS, 
                    f"На вышестоящем {connect_on_dev} добавлено: <b>DOWN to {self.form.cleaned_data['ip']} port {self.form.cleaned_data['up_connect_port']}</b>")
          


            # Добавление UP порта на новое устройство
            form_connection_to_me = ConnectionOnDevice()
            form_connection_to_me.id_dev = Device.objects.get(ip=self.form.cleaned_data['ip'])
            form_connection_to_me.port = self.form.cleaned_data['incoming_port']
            form_connection_to_me.connected = "UP"
            form_connection_to_me.save()
            messages.add_message(request, messages.SUCCESS, 
                    f"На новом {self.form.cleaned_data['ip']} добавлено: <b>UP to {self.form.cleaned_data['up_connect_ip']} port {self.form.cleaned_data['incoming_port']}</b>")

            return redirect('device')
        else:
            return super(DeviceCreate, self).get(request, *args, **kwargs)


class DeviceUpdate(PathToCityMixin, PermissionRequiredMixin, TemplateView):
    form = None
    template_name = 'device_edit.html'
    permission_required = ("models_device.change_device")

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
            # Сохранение нового устройства
            self.form.save()

            # Редактирование подключения нового устройства на порту вышестоящего connected
            connect_on_dev = self.form.cleaned_data['up_connect_ip']
            if connect_on_dev != '255.255.255.255':
                form_connection_to_up = ConnectionOnDevice.objects.get(connected=f"DOWN to {self.form.cleaned_data['ip']}")
                form_connection_to_up.id_dev = Device.objects.get(ip=connect_on_dev)
                form_connection_to_up.port = self.form.cleaned_data['up_connect_port']
                form_connection_to_up.connected = f"DOWN to {self.form.cleaned_data['ip']}"
                form_connection_to_up.save()
                messages.add_message(request, messages.SUCCESS, 
                    f"На вышестоящем {connect_on_dev} изменено: <b>DOWN to {self.form.cleaned_data['ip']} port {self.form.cleaned_data['up_connect_port']}</b>")

            # Редактирование UP порта на редактируемом устройстве
            form_connection_to_me = ConnectionOnDevice.objects.filter(id_dev=dev).get(connected="UP")
            form_connection_to_me.id_dev = Device.objects.get(ip=self.form.cleaned_data['ip'])
            form_connection_to_me.port = self.form.cleaned_data['incoming_port']
            form_connection_to_me.connected = "UP"
            form_connection_to_me.save()
            messages.add_message(request, messages.SUCCESS, 
                    f"На редактируемом {self.form.cleaned_data['ip']} изменено: <b>UP to {self.form.cleaned_data['up_connect_ip']} port {self.form.cleaned_data['incoming_port']}</b>")
          

            return redirect("device")
        else:
            return super(DeviceUpdate, self).get(request, *args, **kwargs)


class DeviceDelete(PermissionRequiredMixin, TemplateView):
    form = None
    permission_required = ("models_device.delete_device")

    def post(self, request, *args, **kwargs):
        form = DeviceDeleteForm(request.POST)
        if form.is_valid():
            device_to_delete = Device.objects.get(pk=form.cleaned_data["device_to_delete"])
            device_to_delete.delete()
        return redirect("device")
        # super(DeviceDelete, self).post(*args, **kwargs)