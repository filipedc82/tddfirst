# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0018_auto_20150408_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_group', models.CharField(default='O', max_length=50, choices=[('VG', 'Valve Guide'), ('VS', 'Valve Seat'), ('EV', 'Engine Valve'), ('EVO', 'Engine Valve Other'), ('NGP', '(Normalien)Guide Pin'), ('NLS', '(Normalien)Limit Switch'), ('NLS', '(Normalien)Other'), ('O', 'Other')])),
                ('own_product_no', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Produkt',
        ),
    ]
