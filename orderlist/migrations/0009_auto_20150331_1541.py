# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0008_delivery_deliveryline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryline',
            name='order_line',
            field=models.ForeignKey(blank=True, to='orderlist.OrderLine'),
            preserve_default=True,
        ),
    ]
