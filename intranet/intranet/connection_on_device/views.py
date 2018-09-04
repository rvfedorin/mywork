from django.shortcuts import render
from django.http import HttpResponse, Http404

from connection_on_device.models import ConnectionOnDevice
from models_device.models import Device

# Create your views here.

def index(request):
    _result = ''
    all_dev = Device.objects.all()
    for dev in all_dev:
        id_dev = dev.pk
        _result += f'<a style="text-decoration:none;" href="/connection/{id_dev}/">{dev.city}&nbsp;&nbsp;&nbsp; {dev.ip} {dev.model.model}</a><br>'

    return HttpResponse(_result)


def on_device(request, id_dev):
    _result = ''
    try:
        dev = Device.objects.get(pk=id_dev)
    except Device.DoesNotExist:
        raise Http404('Device not found!')

    all_connection = ConnectionOnDevice.objects.filter(id_dev=dev)
    

    _result += f'connection on: {dev.ip} ({dev.model.type})<br>'
    for connection in all_connection:
        vlan = f'vlan:{connection.vlan}'
        if connection.connected == 'UP':
            connected = f'UP to {dev.up_connect_port} port on {dev.model.type} {dev.up_connect_ip}'
        else:
            connected = connection.connected
        _result += '&nbsp;'*25 + f'----> port {connection.port}: "{connected}" {vlan if connection.vlan != "Null" else ""} {connection.ip_client}<br>'

    return HttpResponse(_result)


