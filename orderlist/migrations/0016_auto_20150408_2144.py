# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0015_auto_20150408_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_group',
            field=models.CharField(max_length=50, default='O', choices=[('VG', 'Valve Guide'), ('VS', 'Valve Seat'), ('EV', 'Engine Valve'), ('EVO', 'Engine Valve Other'), ('NGP', '(Normalien)Guide Pin'), ('NLS', '(Normalien)Limit Switch'), ('NLS', '(Normalien)Other'), ('O', 'Other')]),
            preserve_default=True,
        ),
    ]
