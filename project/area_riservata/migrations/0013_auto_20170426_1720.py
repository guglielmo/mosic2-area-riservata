# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-26 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area_riservata', '0012_allegato_id_allegato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allegato',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
