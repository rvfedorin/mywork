from django.shortcuts import render
from django.http import HttpResponse

from models_device.models import Device, ModelDevices
# Create your views here.


def index(request):
	_result = ''
	all_device = Device.objects.all()

	for device in all_device:
		_result += f'{device}<br>'
	
	return HttpResponse(_result)