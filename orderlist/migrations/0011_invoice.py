# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0010_auto_20150331_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('invoice_no', models.TextField(max_length=50)),
                ('debitor', models.TextField(max_length=50)),
                ('invoice_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
