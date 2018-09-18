from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django import forms

import re

from connection_on_device.models import ConnectionOnDevice
from models_device.models import Device

# Create your views here.

COLORS = {"Switch":'Lime', "RWR":'Yellow', "UBNT":'Gold'}


def index(request):
    all_dev = Device.objects.all()

    return render(request, "dev_list_con.html", {
        "devices":all_dev, 
        })


def on_device_get(request, id_dev):

    try:
        dev = Device.objects.get(pk=id_dev)
    except Device.DoesNotExist:
        raise Http404('Device not found!')

    all_connection = ConnectionOnDevice.objects.filter(id_dev=dev)

    connections = []

    for connection in all_connection:
        vlan = f'/{connection.vlan}vlan'

        if connection.connected == 'UP':
            connection.connected = f'UP to {dev.up_connect_port} port on {dev.model.type} {dev.up_connect_ip}'
 
        if connection.vlan != "Null":
            connection.vlan = vlan
        else:
            connection.vlan = ""

        connections.append(connection)
    connections = sorted(connections, key=lambda x: x.port)
    
    return connections, dev



def on_device(request, id_dev):
    connections, dev = on_device_get(request, id_dev)
    
    return render(request, "connection.html", {
        "connections":connections, 
        "dev":dev,
        "color":COLORS[dev.model.type],
        })


def path_to(request, id_dev):

    try:
        dev = Device.objects.get(pk=id_dev)
    except Device.DoesNotExist:
        raise Http404('Device not found!')

    path = [(dev, COLORS[dev.model.type])]
    to_dev = dev

    if dev.up_connect_ip == '255.255.255.255':
        return render(request, "path_to_device.html", {
                "path": path,
                "to_dev": to_dev,
                })

    if_loop = 0
    while True:
        if_loop += 1
        try:
            dev = Device.objects.get(ip=dev.up_connect_ip)
        except Device.DoesNotExist:
            raise Http404('Device not found!')
        

        if str(dev.up_connect_ip) == '255.255.255.255':
            path.append((dev, COLORS[dev.model.type]))
            return render(request, "path_to_device.html", {
                "path": path,
                "to_dev": to_dev,
                })
        else:
            path.append((dev, COLORS[dev.model.type]))

        if if_loop > 15:
            return HttpResponse('path not found')


def serch_connect(connect_on_port):
    # check for a downstream connection in the port, if it has - return object device
    ip_pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    _search = re.search(ip_pattern, connect_on_port)
    if _search is not None:
        result = Device.objects.get(ip=_search.group())
    else:
        result = False
    return result


def all_connection_port(dev, connections_dev):
    # get all connection on one device
    all_connection = ConnectionOnDevice.objects.filter(id_dev=dev)
    connections = []
    list_connection_lower_dev = []

    for connection in all_connection:
        _search = serch_connect(connection.connected)
        if _search:
            list_connection_lower_dev.append(_search)
        vlan = f'/{connection.vlan}vlan'

        if connection.connected == 'UP':
            connection.connected = f'UP to {dev.up_connect_port} port on {dev.model.type} {dev.up_connect_ip}'
 
        if connection.vlan != "Null":
            connection.vlan = vlan
        else:
            connection.vlan = ""
        connections.append(connection)
    connections_dev.append((dev, COLORS[dev.model.type], sorted(connections, key=lambda x: x.port)))

    for _dev in list_connection_lower_dev:
        all_connection_port(_dev, connections_dev)

    return connections_dev



def all_connection(request, id_dev):
    # get all connection on all devices from the needed device
    connections_dev = []
    try:
        dev = Device.objects.get(pk=id_dev)
    except Device.DoesNotExist:
        raise Http404('Device not found!')

    source_connect = dev
    connections = all_connection_port(dev, connections_dev) 
    
    
    return render(request, "all_connection_from.html", {
        "connections":connections, 
        "source":source_connect
        })


class AddConnectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['port'].widget.attrs.update({'class': 'form-control'})
        self.fields['connected'].widget.attrs.update({'class': 'form-control'})
        self.fields['vlan'].widget.attrs.update({'class': 'form-control'})
        self.fields['ip_client'].widget.attrs.update({'class': 'form-control'}, cols='20', rows='4')
        self.fields['comment'].widget.attrs.update({'class': 'form-control'}, cols='20', rows='2')


    class Meta:
        model = ConnectionOnDevice
        fields = ["port", "connected", "vlan", "ip_client", "comment"]



class AddConnection(TemplateView):
    form = None
    template_name = "add_connection.html"

    def get(self, request, *args, **kwargs):
        self.form = AddConnectionForm()
        self.connections, self.dev = on_device_get(request, self.kwargs['id_dev'])

        return super(AddConnection, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AddConnection, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        context['dev'] = self.dev
        context['connections'] = self.connections
        context['color'] = COLORS[self.dev.model.type]

        return context

    def post(self, request, *args, **kwargs):
        self.form = AddConnectionForm(request.POST)
        id_dev = self.kwargs['id_dev']

        if self.form.is_valid():
            connection = ConnectionOnDevice()
            connection.id_dev = Device.objects.get(pk=id_dev)
            connection.port = self.form.cleaned_data['port']
            connection.connected = self.form.cleaned_data['connected']
            connection.vlan = self.form.cleaned_data['vlan']
            connection.ip_client = self.form.cleaned_data['ip_client']
            connection.comment = self.form.cleaned_data['comment']
            connection.save()
            return redirect('connections_on_dev', id_dev=id_dev)
        else:
            return super(AddConnection, self).get(request, *args, **kwargs)


class DelConnection(TemplateView):
    form = None


    def post(self, request, *args, **kwargs):
        self.id_dev = self.kwargs['id_dev']
        id_connection = request.POST['connection_to_delete']
        self._to_del = ConnectionOnDevice.objects.get(pk=id_connection)
        self._to_del.delete()
        return redirect('connections_on_dev', self.id_dev)