# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-08 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lonfly', '0002_products_order_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='order_stats',
            field=models.CharField(choices=[('plan', '\u672a\u5f00\u59cb'), ('working', '\u8fdb\u884c\u4e2d'), ('completed', '\u5df2\u5b8c\u6210')], default='\u672a\u5f00\u59cb', help_text='\u8bf7\u9009\u62e9\u8ba2\u5355\u72b6\u6001\uff1a', max_length=8, verbose_name='\u8ba2\u5355\u72b6\u6001'),
        ),
    ]