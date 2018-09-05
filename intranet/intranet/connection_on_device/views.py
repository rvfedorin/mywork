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
    
    return render(request, "connection.html", {
        "connections":connections, 
        "dev":dev,
        })

def path_to(request, id_dev):

    COLORS = {"Switch":'Lime', "RWR":'Gold'}

    try:
        dev = Device.objects.get(pk=id_dev)
    except Device.DoesNotExist:
        raise Http404('Device not found!')

    path = f'<b><font color="{COLORS[dev.model.type]}">{dev.ip}</font></b>-{dev.incoming_port}port--{dev.up_connect_port}port'

    if_loop = 0
    while True:
        if_loop += 1
        try:
            dev = Device.objects.get(ip=dev.up_connect_ip)
        except Device.DoesNotExist:
            raise Http404('Device not found!')

        

        if str(dev.up_connect_ip) == '255.255.255.255':
            path += f'-<b><font color="{COLORS[dev.model.type]}">{dev.ip}</font></b>-{dev.incoming_port}port--<b>cisco</b>'
            return HttpResponse(path)
        else:
            path += f'-<b><font color="{COLORS[dev.model.type]}">{dev.ip}</font></b>-{dev.incoming_port}port--{dev.up_connect_port}port'

        if if_loop > 15:
            return HttpResponse('path not found')


