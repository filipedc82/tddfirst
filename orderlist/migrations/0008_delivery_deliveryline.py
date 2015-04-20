# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0007_auto_20150310_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('dlry_no', models.TextField(max_length=50)),
                ('recipient', models.TextField(max_length=50)),
                ('sender', models.TextField(max_length=50)),
                ('dispatch_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryLine',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('product', models.TextField(max_length=50)),
                ('qty', models.FloatField()),
                ('delivery', models.ForeignKey(to='orderlist.Delivery')),
                ('order_line', models.ForeignKey(to='orderlist.OrderLine')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
