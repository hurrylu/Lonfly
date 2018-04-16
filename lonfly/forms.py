# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm, ModelChoiceField
from lonfly.models import Products, Process, Material, UserProfile, Produce, Worker
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_id', 'order_num', 'deliver_date']

class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'code']

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'code', 'inventory', 'used']

class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("两次输入的密码不匹配")

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus': True}), strip=False)
    password2 = forms.CharField(widget=forms.PasswordInput, strip=False)

#    def clean(self):
#        cleaned_data = super(PasswordChangeForm, self).clean()
#        password1 = cleaned_data.get("password1")
#        password2 = cleaned_data.get("password2")
#        if password1 != password2:
#            raise forms.ValidationError("两次输入的密码不匹配")

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =['address', 'picture']

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.name

class WorkerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.worker_name

class ProduceForm(ModelForm):
#    process = forms.ModelChoiceField(queryset=Process.objects.all(), empty_label=None, to_field_name="process_name", help_text="请选择工序：")
#    material = forms.ModelChoiceField(queryset=Material.objects.all(), empty_label=None, to_field_name="material_name", help_text="请选择材料规格：")
    process = MyModelChoiceField(Process.objects.all(), help_text="请选择工序：")
    material = MyModelChoiceField(Material.objects.all(), help_text="请选择材料规格：")
    operator = WorkerChoiceField(Worker.objects.filter(is_operator='True'), help_text="请选择作业员：")
    inspector = WorkerChoiceField(Worker.objects.filter(is_inspector='True'), help_text="请选择巡检员：")
    class Meta:
        model = Produce
        fields = ['process', 'material', 'assigned_num', 'operator', 'produce_num', 'process_des', 'detect_log', 'inspect_log', 'inspect_date', 'inspector', 'description']
