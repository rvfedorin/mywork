# Generated by Django 2.1 on 2018-09-03 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='city',
            field=models.ForeignKey(help_text='город подключения', on_delete=django.db.models.deletion.PROTECT, to='cities.Cities'),
        ),
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.GenericIPAddressField(help_text='IP устройства', unique=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='model',
            field=models.ForeignKey(help_text='модель устройства', null=True, on_delete=django.db.models.deletion.SET_NULL, to='models_device.ModelDevices'),
        ),
        migrations.AlterField(
            model_name='device',
            name='up_connect_ip',
            field=models.GenericIPAddressField(help_text='IP устройства от которого подключено'),
        ),
        migrations.AlterField(
            model_name='modeldevices',
            name='model',
            field=models.CharField(help_text='модель устройства', max_length=30),
        ),
        migrations.AlterField(
            model_name='modeldevices',
            name='ports',
            field=models.PositiveSmallIntegerField(help_text='количество портов'),
        ),
        migrations.AlterField(
            model_name='modeldevices',
            name='type',
            field=models.CharField(max_length=30, verbose_name='тип устройства'),
        ),
    ]
