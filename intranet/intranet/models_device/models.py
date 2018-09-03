from django.db import models

# My 
from cities.models import Cities

# Create your models here.

class ModelDevices(models.Model):
    type = models.CharField(max_length=30, verbose_name='Тип устройства.')
    model = models.CharField(max_length=30, help_text='Модель устройства.')
    ports = models.PositiveSmallIntegerField(help_text='Количество портов.')
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
    model = models.ForeignKey(ModelDevices, null=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(unique=True)
    up_connect_ip = models.GenericIPAddressField()
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        _text = f"{self.ip}({self.model.model}) connect from: {self.up_connect_ip};  {self.city}; Comment: {self.comment}; "
        return _text

    class Meta:
        verbose_name = 'Установленное борудование'
        verbose_name_plural = 'Установленное борудование'
