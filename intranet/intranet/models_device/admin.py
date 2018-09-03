from django.contrib import admin

# Register your models here.
from models_device.models import ModelDevices, Device

admin.site.register(ModelDevices)
admin.site.register(Device)