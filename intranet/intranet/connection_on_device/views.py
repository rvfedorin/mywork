from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

import re

from connection_on_device.models import ConnectionOnDevice
from models_device.models import Device
from connection_on_device.forms import AddConnectionForm

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
            try:
                up_dev = Device.objects.get(ip=dev.up_connect_ip)
                connection.connected = (f'UP to {dev.up_connect_port} port on {dev.model.type} {dev.up_connect_ip}', up_dev)
            except Device.DoesNotExist:
                connection.connected = f'UP to {dev.up_connect_port} port on {dev.model.type} {dev.up_connect_ip}'
        elif 'DOWN to ' in connection.connected:
            try:
                down_dev = Device.objects.get(ip=connection.connected[8:])
                connection.connected = (connection.connected, down_dev)
            except Device.DoesNotExist:
                connection.connected = connection.connected
 
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


class AddConnection(PermissionRequiredMixin, TemplateView):
    form = None
    template_name = "add_connection.html"
    permission_required = ('connection_on_device.add_connectionondevice', )

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
        id_dev = self.kwargs['id_dev']
        dev = Device.objects.get(pk=id_dev)
        self.form = AddConnectionForm(request.POST)

        if self.form.is_valid():
            connection = ConnectionOnDevice()
            connection.id_dev = dev
            connection.port = self.form.cleaned_data['port']
            connection.connected = self.form.cleaned_data['connected']
            connection.vlan = self.form.cleaned_data['vlan']
            connection.ip_client = self.form.cleaned_data['ip_client']
            connection.comment = self.form.cleaned_data['comment']
            connection.save()
            messages.add_message(request, messages.SUCCESS, "<b>Подключение добавлено.</b>")
            return redirect('connections_on_dev', id_dev=id_dev)
        else:
            return super(AddConnection, self).get(request, *args, **kwargs)


class DelConnection(PermissionRequiredMixin, TemplateView):
    form = None
    permission_required = ('connection_on_device.delete_connectionondevice', )


    def post(self, request, *args, **kwargs):
        id_dev = self.kwargs['id_dev']
        id_connection = request.POST['connection_to_delete']
        self._to_del = ConnectionOnDevice.objects.get(pk=id_connection)
        self._to_del.delete()
        messages.add_message(request, messages.SUCCESS, f"<b>Подключение удалено.<br>{self._to_del}</b>")
        # mail_message = f"""Удалено подключение:
        #     {self._to_del}
        #     """
        # send_mail(
        #     'Изменения в интранете.',
        #     mail_message,
        #     'vvvvvv@mail.ru',
        #     ['vvvvvv@mail.ru'],
        #     fail_silently=False,
        # )

        return redirect('connections_on_dev', id_dev)


class EditConnection(PermissionRequiredMixin, TemplateView):
    form = None
    template_name = 'edit_connection.html'
    permission_required = ('connection_on_device.change_connectionondevice', )

    def get(self, request, *args, **kwargs):
        self.id_con = self.kwargs['id_con']
        self.connection_instance = ConnectionOnDevice.objects.get(pk=self.id_con)
        self.form = AddConnectionForm(instance=self.connection_instance)
        self.connections, self.dev = on_device_get(request, self.kwargs['id_dev'])

        return super(EditConnection, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EditConnection, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        context['dev'] = self.dev
        context['connections'] = self.connections
        context['id_con'] = self.id_con
        context['color'] = COLORS[self.dev.model.type]

        return context

    def post(self, request, *args, **kwargs):
        self.form = AddConnectionForm(request.POST)
        if self.form.is_valid():
            old_connection = ConnectionOnDevice.objects.get(pk=self.kwargs['id_con'])
            connection = ConnectionOnDevice.objects.get(pk=self.kwargs['id_con'])

            connection.id_dev = Device.objects.get(pk=self.kwargs['id_dev'])
            connection.port = self.form.cleaned_data['port']
            connection.connected = self.form.cleaned_data['connected']
            connection.vlan = self.form.cleaned_data['vlan']
            connection.ip_client = self.form.cleaned_data['ip_client']
            connection.comment = self.form.cleaned_data['comment']
            connection.save()
            messages.add_message(request, messages.SUCCESS, "Изменения приняты.")

            mail_message = f"""Изменения приняты:
            устройство({'без изменений' if old_connection.id_dev == connection.id_dev else '--- изменено ---'}): {connection.id_dev.ip} 
            порт({'без изменений' if old_connection.port == connection.port else '--- изменено ---'}): {connection.port} 
            подключение({'без изменений' if old_connection.connected == connection.connected else '--- изменено ---'}): {connection.connected} 
            влан({'без изменений' if old_connection.vlan == connection.vlan else '--- изменено ---'}): {connection.vlan} 
            ip клиента({'без изменений' if old_connection.ip_client == connection.ip_client else '--- изменено ---'}): {connection.ip_client} 
            комментарий({'без изменений' if old_connection.comment == connection.comment else '--- изменено ---'}): {connection.comment} 
            """


            return redirect('connections_on_dev', self.kwargs['id_dev'])
        else:
            return super(EditConnection, self).get(request, *args, **kwargs)