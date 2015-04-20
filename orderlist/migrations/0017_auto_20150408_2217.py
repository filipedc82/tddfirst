# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0016_auto_20150408_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='product',
            field=models.ForeignKey(to='orderlist.Product'),
            preserve_default=True,
        ),
    ]
