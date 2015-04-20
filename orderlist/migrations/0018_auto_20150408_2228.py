# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderlist', '0017_auto_20150408_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('product_group', models.CharField(default='O', max_length=50, choices=[('VG', 'Valve Guide'), ('VS', 'Valve Seat'), ('EV', 'Engine Valve'), ('EVO', 'Engine Valve Other'), ('NGP', '(Normalien)Guide Pin'), ('NLS', '(Normalien)Limit Switch'), ('NLS', '(Normalien)Other'), ('O', 'Other')])),
                ('own_product_no', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='product',
            field=models.TextField(max_length=50),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
