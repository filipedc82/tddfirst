# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0012_invoiceline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='dlry_no',
            new_name='delivery_no',
        ),
    ]
