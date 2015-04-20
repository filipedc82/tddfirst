# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0006_auto_20150310_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='order',
            field=models.ForeignKey(to='orderlist.Order'),
            preserve_default=True,
        ),
    ]
