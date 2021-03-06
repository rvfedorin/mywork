# Generated by Django 2.1 on 2018-09-03 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('models_device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionOnDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.PositiveSmallIntegerField(help_text='Порт подключения.')),
                ('connected', models.CharField(help_text='Что подключено к порту.', max_length=30)),
                ('comment', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Дата добавления.')),
                ('update', models.DateTimeField(auto_now=True, help_text='Дата изменения.')),
                ('id_dev', models.ForeignKey(help_text='ID оборудования, к которому подключен клиент/устройство.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='models_device.Device')),
            ],
        ),
    ]
