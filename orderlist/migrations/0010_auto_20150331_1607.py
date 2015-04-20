# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0009_auto_20150331_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryline',
            name='order_line',
            field=models.ForeignKey(blank=True, to='orderlist.OrderLine', null=True),
            preserve_default=True,
        ),
    ]
