# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0011_invoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('product', models.TextField(max_length=50)),
                ('qty', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('delivery_line', models.ForeignKey(to='orderlist.DeliveryLine', null=True, blank=True)),
                ('invoice', models.ForeignKey(to='orderlist.Invoice')),
                ('order_line', models.ForeignKey(to='orderlist.OrderLine', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
