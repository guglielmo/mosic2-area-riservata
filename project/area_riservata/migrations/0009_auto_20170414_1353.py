# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-14 11:53
from __future__ import unicode_literals

import area_riservata.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area_riservata', '0008_auto_20170412_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allegato',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=area_riservata.models.relURI_path),
        ),
    ]