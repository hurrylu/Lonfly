# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from lonfly.models import Process, Products, Material, Produce, UserProfile

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'order_num', 'deliver_date')

class ProduceAdmin(admin.ModelAdmin):
    list_display = ('product', 'process', 'material', 'assigned_num', 'operator', 'produce_num', 'process_des', 'detect_log', 'inspect_log', 'inspect_date', 'inspector', 'description')

# Register your models here.
admin.site.register(Products, ProductsAdmin)
admin.site.register(Process)
admin.site.register(Material)
admin.site.register(UserProfile)
admin.site.register(Produce, ProduceAdmin)
