# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-08 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area_riservata', '0002_auto_20170407_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allegato',
            name='punto_odg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allegati', to='area_riservata.PuntoODG'),
        ),
        migrations.AlterField(
            model_name='puntoodg',
            name='seduta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='punti_odg', to='area_riservata.Seduta'),
        ),
    ]
