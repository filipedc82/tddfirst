# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0005_orderline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='order',
            field=models.ForeignKey(editable=False, to='orderlist.Order'),
            preserve_default=True,
        ),
    ]
