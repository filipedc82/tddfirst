# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0004_remove_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('product', models.TextField(max_length=50)),
                ('qty', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('dlry_date', models.DateField()),
                ('order', models.ForeignKey(to='orderlist.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
