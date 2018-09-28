from django import forms


from connection_on_device.models import ConnectionOnDevice


class AddConnectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['port'].widget.attrs.update({'class': 'form-control'})
        self.fields['connected'].widget.attrs.update({'class': 'form-control'})
        self.fields['vlan'].widget.attrs.update({'class': 'form-control'})
        self.fields['ip_client'].widget.attrs.update({'class': 'form-control'}, cols='20', rows='4')
        self.fields['comment'].widget.attrs.update({'class': 'form-control'}, cols='20', rows='1')


    class Meta:
        model = ConnectionOnDevice
        fields = ["port", "connected", "vlan", "ip_client", "comment"]