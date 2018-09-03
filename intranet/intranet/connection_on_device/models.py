from django.db import models
from models_device.models import Device

# Create your models here.

class ConnectionOnDevice(models.Model):
    id_dev = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL, 
        help_text='ID оборудования, к которому подключен клиент/устройство')
    port = models.PositiveSmallIntegerField(help_text='Порт подключения')
    connected = models.CharField(max_length=30, help_text='Что подключено к порту')
    comment = models.TextField(blank=True, help_text='Комментарий')
    date = models.DateTimeField(auto_now_add=True, help_text='Дата добавления')
    update = models.DateTimeField(auto_now=True, help_text='Дата изменения')

    def __str__(self):
        _text = f"{self.id_dev.city.city} --> {self.connected} on {self.id_dev.ip} port {self.port};  {self.comment}"
        return _text

    class Meta:
    	verbose_name = "Подключенное оборудование/клиенты"
    	verbose_name_plural = "Подключенное оборудование/клиенты"