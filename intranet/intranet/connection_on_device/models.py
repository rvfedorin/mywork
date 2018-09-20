from django.db import models

# Create your models here.
from models_device.models import Device

class ConnectionOnDevice(models.Model):

    id_dev = models.ForeignKey(Device, on_delete=models.CASCADE, 
        help_text='ID оборудования, к которому подключен клиент/устройство')
    port = models.CharField(max_length=10, help_text='Порт подключения')
    connected = models.CharField(max_length=40, help_text='Что подключено к порту')
    vlan = models.CharField(max_length=5, default='Null', help_text='vlan клиента, если есть')
    ip_client = models.TextField(blank=True, verbose_name='IP клиента', help_text='IP/сети выделенные клиенту через ";"')
    comment = models.TextField(blank=True, help_text='Комментарий')
    date = models.DateTimeField(auto_now_add=True, help_text='Дата добавления')
    update = models.DateTimeField(auto_now=True, help_text='Дата изменения')


    def __str__(self):
        _text = f"{self.id_dev.city.city} --> {self.connected} on {self.id_dev.ip} port {self.port};  {self.comment}"
        return _text

    class Meta:
    	verbose_name = "Подключенное оборудование/клиенты"
    	verbose_name_plural = "Подключенное оборудование/клиенты"

