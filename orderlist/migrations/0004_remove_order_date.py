# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0003_auto_20150308_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
    ]
