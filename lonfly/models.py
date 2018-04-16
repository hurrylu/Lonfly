# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime


class Products(models.Model):
    STATS_CHOICES = [
        ('未开始', '未开始'),
        ('进行中', '进行中'),
        ('已完成', '已完成'),
    ]
    product_id = models.CharField("产品ID", max_length=8, primary_key=True, help_text=u"请输入产品标识：")
    product_name = models.CharField("产品名", max_length=128, unique=True, help_text=u"请输入产品名：")
    order_num = models.IntegerField("订单数量", default="0", help_text=u"请输入订单数量：")
    deliver_date = models.DateField("交货日期", max_length=8, default=datetime.datetime.now, help_text=u"请输入交货日期：")
    order_stats = models.CharField("订单状态", max_length=8, choices=STATS_CHOICES, default='未开始', help_text=u"请选择订单状态：")

    def get_absolute_url(self):
        return reverse('product_table')

    def __unicode__(self):
        return self.product_name


class Process(models.Model):
    name = models.CharField("工序名", max_length=128, help_text=u"请输入工序名：")
    code = models.CharField("工序代码", max_length=16, null=True, default="", help_text=u"请输入工序代码：")

    def get_absolute_url(self):
        return reverse('process_table')

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField("地址", max_length=255, blank=True)
    picture = models.ImageField(upload_to='profiel_images', blank=True)

    def __unicode__(self):
        return self.user.username


class Material(models.Model):
    name = models.CharField("材料名", max_length=128, unique=True, help_text=u"请输入材料名：")
    code = models.CharField("材料规格", max_length=128, null=True, help_text=u"请输入材料规格：")
    inventory = models.IntegerField("库存数量", null=True, default="0", help_text=u"请输入库存数量：")
    used = models.IntegerField("已用数量", null=True, default="0", help_text=u"请输入已用数量：")

    def get_absolute_url(self):
        return reverse('material_table')

    def __unicode__(self):
        return self.name

class Worker(models.Model):
    worker_id = models.IntegerField("工号", unique=True, primary_key=True, help_text=u"请输入员工工号：")
    worker_name = models.CharField("姓名", max_length=32, help_text=u"请输入员工姓名：")
    is_operator = models.BooleanField("作业员？", help_text=u"是否担当作业员角色？")
    is_inspector = models.BooleanField("巡检员？", help_text=u"是否担当巡检员角色？")
    description = models.TextField("描述", null=True, blank=True, help_text="请输入备注描述：")

    def get_absolute_url(self):
        return reverse('worker_table')

    def __unicode__(self):
        return self.worker_name

class Produce(models.Model):
    product = models.ForeignKey(Products)
    process = models.ForeignKey(Process, null=True, blank=True, help_text=u"请选择工序：")
    material = models.ForeignKey(Material, null=True, blank=True, help_text=u"请选择材料规格：")
    assigned_num = models.IntegerField("定额数量", null=True, default="0", help_text=u"请输入定额数量：")
#    operator = models.CharField("作业员", max_length=16, null=True, help_text=u"请输入作业人员：")
    operator = models.ForeignKey(Worker, null=True, blank=True, help_text="请选择作业员：")
    produce_num = models.IntegerField("生产数量", null=True, default="0", help_text=u"请输入生产数量：")
    process_des = models.TextField("作业要点指导", null=True, blank=True, help_text=u"请输入作业要点指导：")
    detect_log = models.TextField("首检记录", null=True, blank=True, help_text=u"请输入首检记录：")
    inspect_log = models.TextField("巡检记录", null=True, blank=True, help_text=u"请输入巡检记录：")
    inspect_date = models.DateField("日期", max_length=8, blank=True, default=datetime.datetime.now, help_text=u"请输入日期：")
    inspector = models.CharField("巡检员", max_length=16, null=True, blank=True, help_text=u"请输入巡检员：")
    description = models.TextField("备注", null=True, blank=True, help_text=u"请输入备注：")

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.product_id})

    def __unicode__(self):
        return self.product.product_name