# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0014_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_group',
            field=models.CharField(default='O', max_length=50, choices=[('EVG', 'Valve Guide'), ('EVS', 'Valve Seat'), ('EV', 'Engine Valve'), ('EVO', 'Engine Valve Other'), ('NGP', '(Normalien)Guide Pin'), ('NLS', '(Normalien)Limit Switch'), ('NLS', '(Normalien)Other'), ('O', 'Other')]),
            preserve_default=True,
        ),
    ]
