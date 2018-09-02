from django.db import models

# Create your models here.

class ModelDevices(models.Model):
    type = models.CharField(max_length=30, verbose_name='Тип устройства.')
    model = models.CharField(max_length=30, help_text='Модель устройства.')
    ports = models.PositiveSmallIntegerField(help_text='Количество портов.')
    template = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тип и модель оборудования.'

    def __str__(self):
        _text = f"""
        Device: {type}
        Model: {model}
        Ports: {ports}
        Templat: {template}
        Comment: {comment}
        """
        return _text


class Device(models.Model):
    model = models.ForeignKey(ModelDevices, null=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(unique=True)
    up_connect_ip = models.GenericIPAddressField()
    comment = models.TextField(blank=True)
    update = models.DateTimeField(auto_now=True)

