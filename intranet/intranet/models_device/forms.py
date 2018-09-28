from django import forms

from models_device.models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['model', 'ip', 'incoming_port', 'up_connect_ip', 'up_connect_port', 'city', 'comment']
        error_messages = {'ip': {'unique': 'Устройство с таким IP уже существует.'}
        }


class DeviceDeleteForm(forms.Form):
    device_to_delete = forms.IntegerField() 