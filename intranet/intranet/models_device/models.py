from django.db import models
from django.core.exceptions import ValidationError

# My 
from cities.models import Cities, REGIONS

# Create your models here.

def validate_up_connect_ip(ip):
    if ip != '255.255.255.255':
        try:
            id_dev = Device.objects.get(ip=ip)
        except Device.DoesNotExist:
            raise ValidationError("Указанного вышестоящего оборудования не существует.")


class ModelDevices(models.Model):
    type = models.CharField(max_length=30, verbose_name='Тип устройства')
    model = models.CharField(max_length=30, help_text='модель устройства', verbose_name='Модель')
    ports = models.PositiveSmallIntegerField(help_text='количество портов', verbose_name='Портов')
    template = models.CharField(max_length=50,help_text='имя файла с шаблоном', verbose_name='Шаблон')
    comment = models.TextField(blank=True, verbose_name='Комментарий', help_text='комментарий')

    class Meta:
        verbose_name = 'Тип и модель оборудования'
        verbose_name_plural = 'Типы и модели оборудования'
        ordering = ['model']

    def __str__(self):
        _text = f"{self.type} {self.model} {self.comment}"

        return _text


class Device(models.Model):
    model = models.ForeignKey(ModelDevices, null=True, on_delete=models.SET_NULL, help_text='модель устройства', verbose_name='Модель')
    ip = models.GenericIPAddressField(unique=True, help_text='IP нового устройства', verbose_name='IP устройства')
    incoming_port = models.CharField(max_length=10, help_text='приходящий порт', default=1, verbose_name='Приходящий порт')
    up_connect_ip = models.GenericIPAddressField(validators=[validate_up_connect_ip], help_text='IP устройства от которого подключено', verbose_name='IP вышестоящего')
    up_connect_port = models.CharField(max_length=10, help_text='порт подключения на вышестоящем устройстве', default=1, verbose_name='Порт вышестоящего')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, help_text='город подключения', verbose_name='Город')
    comment = models.TextField(blank=True, verbose_name='Комментарий', help_text='комментарий')
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        _text = f"{REGIONS[self.city.region-1][1]} {self.city.city} {self.ip} ({self.model.model}) connect from: {self.up_connect_ip}; Comment: {self.comment}; "
        return _text

    class Meta:
        verbose_name = 'Установленное оборудование'
        verbose_name_plural = 'Установленное оборудование'

