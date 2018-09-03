from django.db import models

# My 
from cities.models import Cities, REGIONS

# Create your models here.

class ModelDevices(models.Model):
    type = models.CharField(max_length=30, verbose_name='тип устройства')
    model = models.CharField(max_length=30, help_text='модель устройства')
    ports = models.PositiveSmallIntegerField(help_text='количество портов')
    template = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тип и модель оборудования'
        verbose_name_plural = 'Типы и модели оборудования'

    def __str__(self):
        _text = f"""
        Device: {self.type}; 
        Model: {self.model}; 
        Ports: {self.ports}; 
        Template: {self.template}; 
        Comment: {self.comment}; 
        """
        return _text


class Device(models.Model):
    model = models.ForeignKey(ModelDevices, null=True, on_delete=models.SET_NULL, help_text='модель устройства')
    ip = models.GenericIPAddressField(unique=True, help_text='IP устройства')
    up_connect_ip = models.GenericIPAddressField(help_text='IP устройства от которого подключено')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, help_text='город подключения')
    comment = models.TextField(blank=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        _text = f"{REGIONS[self.city.region-1][1]} {self.city.city} {self.ip} ({self.model.model}) connect from: {self.up_connect_ip}; Comment: {self.comment}; "
        return _text

    class Meta:
        verbose_name = 'Установленное оборудование'
        verbose_name_plural = 'Установленное оборудование'
