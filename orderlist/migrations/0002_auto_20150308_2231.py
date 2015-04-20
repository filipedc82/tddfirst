# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.TextField(verbose_name=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.TextField(verbose_name=50),
            preserve_default=True,
        ),
    ]
