# Generated by Django 2.1 on 2018-09-21 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_on_device', '0005_auto_20180917_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionondevice',
            name='connected',
            field=models.CharField(help_text='Что подключено к порту', max_length=40),
        ),
        migrations.AlterField(
            model_name='connectionondevice',
            name='ip_client',
            field=models.TextField(blank=True, help_text='IP/сети выделенные клиенту через ";"', verbose_name='IP клиента'),
        ),
    ]
