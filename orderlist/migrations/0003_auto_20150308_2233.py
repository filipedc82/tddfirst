# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0002_auto_20150308_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.TextField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.TextField(max_length=50),
            preserve_default=True,
        ),
    ]
