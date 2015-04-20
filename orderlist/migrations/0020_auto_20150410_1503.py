# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0019_auto_20150408_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('product_group', models.CharField(choices=[('VG', 'Valve Guide'), ('VS', 'Valve Seat'), ('EV', 'Engine Valve'), ('EVO', 'Engine Valve Other'), ('NGP', '(Normalien)Guide Pin'), ('NLS', '(Normalien)Limit Switch'), ('NLS', '(Normalien)Other'), ('O', 'Other')], default='O', max_length=50)),
                ('own_product_no', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
