from django.shortcuts import render
from django.http import HttpResponse, Http404

import re

from connection_on_device.models import ConnectionOnDevice
from models_device.models import Device

# Create your views here.

COLORS = {"Switch":'Lime', "RWR":'Yellow', "UBNT":'Gold'}


def index(request):
    _result = ''
    all_dev = Device.objects.all()

    return render(request, "dev_list.html", {
        "devices":all_dev, 
        })


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
    ip_pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    _search = re.search(ip_pattern, connect_on_port)
    if _search is not None:
        result = Device.objects.get(ip=_search.group())
    else:
        result = False
    return result



def all_connection_port(dev, connections_dev):
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