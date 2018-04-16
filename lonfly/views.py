# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from lonfly.models import Products, Process, Produce, Material, Worker
from lonfly.forms import ProductForm, ProcessForm, MaterialForm, ProduceForm, WorkerForm, UserForm, UserProfileForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import connection
from django.db.models import Count,Sum, Avg

def db_query(db_table):
    params = []
    date_format = "%Y-%m-%d %H:%i:%S"
    sql = 'select date_format(ifnull(update_time, create_time), %s) as result from information_schema.TABLES where table_schema=database() and table_name= %s '
    params.append(date_format)
    params.extend([db_table])
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        row = cursor.fetchone()
    return row

def encode_url(str):
    return str.replace('', '_')

def decode_url(str):
    return str.replace('_', '')

# Create your views here.
def index(request):
    request.session.set_test_cookie()
#    context = RequestContext(Request)
    product_list = Products.objects.order_by('product_id')
    table_update_time = db_query('lonfly_Products')[0]
    context_dict = {'products': product_list, 'table_update_time': table_update_time}

    for product in product_list:
        product.url = encode_url(product.product_name)

    return render(request, 'lonfly/index.html', context_dict)
#    return HttpResponse("<h1>Welcome to this site!"
#                        "<p><a href='/lonfly/about'>about</a></p></h1>")

def product_table(request):
    request.session.set_test_cookie()
    product_list = Products.objects.order_by('product_id')
    table_update_time = db_query('lonfly_Products')[0]
    context_dict = {'products': product_list, 'table_update_time': table_update_time}
    for product in product_list:
        product.url = encode_url(product.product_name)
    return render(request, 'lonfly/product_table.html', context_dict)

def page_product(request, product_id):
#    product_name = decode_url(product_name_url)
    context_dict = {'product_id': product_id}
    try:
        product = Products.objects.get(product_id__iexact=product_id)
        produce_list = Produce.objects.filter(product=product)
        table_update_time = db_query('lonfly_Produce')[0]
        context_dict['produce_list'] = produce_list
        context_dict['product'] = product
        context_dict['table_update_time'] = table_update_time
    except  Products.DoesNotExist:
        pass

    return render(request, "lonfly/product.html", context_dict)

def process_table(request):
    process_list = Process.objects.order_by('id')
    table_update_time = db_query('lonfly_Process')[0]
    context_dict = {'process_list': process_list, 'table_update_time': table_update_time}
    return render(request, 'lonfly/process_table.html', context_dict)

def material_table(request):
    material_list = Material.objects.order_by('id')
    table_update_time = db_query('lonfly_Material')[0]
    context_dict = {'material_list': material_list, 'table_update_time': table_update_time}
    return render(request, 'lonfly/material_table.html', context_dict)

def worker_table(request):
    worker_list = Worker.objects.order_by('worker_id')
    table_update_time = db_query('lonfly_Worker')[0]
    context_dict = {'worker_list': worker_list, 'table_update_time': table_update_time}
    return render(request, 'lonfly/worker_table.html', context_dict)

def about(request):
    context_dic = {}
    return render(request, "lonfly/about.html", context_dic)

def add_product(request):
    if request.method == 'POST':
        formset = ProductForm(request.POST)
        if formset.is_valid():
            formset.save()
            return index(request)
        else:
            print formset.errors
    else:
        formset = ProductForm()
    return render(request, "lonfly/add_product.html", {'formset': formset})

def add_process(request):
    if request.method == 'POST':
        formset = ProcessForm(request.POST)
        if formset.is_valid():
            formset.save()
            return material_table(request)
        else:
            print formset.errors
    else:
        formset = ProcessForm()
    return render(request, "lonfly/add_process.html", {'formset': formset})

def add_material(request):
    print request.method
    if request.method == 'POST':
        print request.method
        formset = MaterialForm(request.POST)
        print formset
        if formset.is_valid():
            formset.save()
            return material_table(request)
        else:
            print formset.errors
    else:
        formset = MaterialForm()
        print "MARK"
        print request.method
    return render(request, "lonfly/add_material.html", {'formset': formset})

def add_produce(request, product_id):
#    product_name = decode_url(product_name_url)
#    context_dict = {'product_name_url': product_name_url, 'product_name': product_name}
    context_dict = {'product_id': product_id}
    if request.method == 'POST':
        formset = ProduceForm(request.POST)
        if formset.is_valid():
            produce = formset.save(commit=False)
            try:
                product = Products.objects.get(product_id__iexact=product_id)
                produce.product = product
            except Products.DoesNotExist:
                return render(request, "lonfly/product.html", {})
            produce.save()
            return page_product(request, product_id)
        else:
            print formset.errors
    else:
        formset = ProduceForm()
    context_dict['formset'] = formset
    return render(request, "lonfly/add_produce.html", context_dict)

class ProductAdd(CreateView):
    model = Products
    fields = '__all__'

class ProductUpdate(UpdateView):
    model = Products
    fields = ['product_id', 'product_name', 'order_num', 'deliver_date', 'order_stats']

class ProductDelete(DeleteView):
    model = Products
    success_url = reverse_lazy('product_table')

class ProcessAdd(CreateView):
    model = Process
    fields = '__all__'

class ProcessUpdate(UpdateView):
    model = Process
    fields = ['name', 'code']

class ProcessDelete(DeleteView):
    model = Process
    success_url = reverse_lazy('process_table')

class MaterialAdd(CreateView):
    model = Material
    fields = '__all__'

class MaterialUpdate(UpdateView):
    model = Material
    fields = ['name', 'code', 'inventory', 'used']

class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('material_table')

class WorkerAdd(CreateView):
    model = Worker
    fields = '__all__'

class WorkerUpdate(UpdateView):
    model = Worker
    fields = ['worker_id', 'worker_name', 'is_operator', 'is_inspector', 'description']

class WorkerDelete(DeleteView):
    model = Worker
    success_url = reverse_lazy('worker_table')

class ProduceAdd(CreateView):
    model = Produce
    form_class = ProduceForm

class ProduceUpdate(UpdateView):
    model = Produce
    form_class = ProduceForm
#    fields = ['process', 'material', 'assigned_num', 'operator', 'produce_num', 'process_des', 'detect_log', 'inspect_log', 'inspect_date', 'inspector', 'description']

class ProduceDelete(DeleteView):
    model = Produce
    def get_success_url(self):
        return self.object.get_absolute_url()

def register(request):
    registered = False
    print request.method
    if request.method == 'POST':
        print request.POST
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        print user_form
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, "lonfly/register.html", context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/lonfly/')
            else:
                return HttpResponse('您的账号已被禁用！')
        else:
            print "登录信息有误：{0}, {1}" .format(username, password)
            return HttpResponse("无效的登录账户或密码！")
    else:
        return render(request, "lonfly/login.html", {})

def ChangePassword(request):
    context_dict = {}
    current_user = request.user
    if request.method == "POST":
        change_form = PasswordChangeForm(request.POST)
        print change_form
        if change_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            print password1, password2
            if password1 != password2:
                error_msg = "两次输入的密码不匹配！"
                context_dict['error_msg'] = error_msg
            else:
                user = User.objects.get(username=current_user)
                user.set_password(password1)
                user.save()
                success_msg = "密码已修改！"
                context_dict['success_msg'] = success_msg
                return HttpResponseRedirect('/lonfly/login/')
        else:
            print change_form.errors
    else:
        change_form = PasswordChangeForm()
    context_dict['change_form'] = change_form
    return render(request, "lonfly/change_password.html", context_dict)

@login_required
def restricted(request):
    return HttpResponse("账号受限，仅能登录此页面！")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/lonfly/')

@login_required(login_url='/lonfly/login/')
def report_by_worker(request):
#    search_key = request.GET.get(search_var, '')
    worker_list = Worker.objects.filter(is_operator='True').values_list('worker_name', flat=True).order_by('worker_id')
    context_dict = {'worker_list': worker_list}
#    search_var = request.GET.get('search_var')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    field_choice = request.GET.getlist('field_choice')
    if not field_choice or 'all' in field_choice:
        result = Worker.objects.values_list('worker_id', flat=True)
    else:
        result = Worker.objects.filter(worker_name__in=field_choice).values_list('worker_id', flat=True)
    print result
    if start_date and end_date and result:
        try:
            query_result = Produce.objects.filter(operator__in=result, inspect_date__gte=start_date, inspect_date__lte=end_date)
            query_sum = Produce.objects.filter(operator__in=result, inspect_date__gte=start_date, inspect_date__lte=end_date).values('operator__worker_name').annotate(product_count=Count('product', distinct=True),assigned_sum=Sum('assigned_num'), produce_num_sum=Sum('produce_num'), produce_num_avg=Avg('produce_num'))
        except Produce.DoesNotExist:
            query_result = []
            query_sum = []
        context_dict['query_result'] = query_result
        context_dict['query_sum'] = query_sum
    return render(request, "lonfly/report_by_worker.html", context_dict)

@login_required(login_url='/lonfly/login/')
def report_by_product(request):
#    search_key = request.GET.get(search_var, '')
    product_list = Products.objects.all().values('product_id', 'product_name').order_by('product_id')
    context_dict = {'product_list': product_list}
#    search_var = request.GET.get('search_var')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    field_choice = request.GET.getlist('field_choice')
    print field_choice
    if not field_choice or 'all' in field_choice:
        result = Products.objects.values_list('product_id', flat=True)
    else:
        result = Products.objects.filter(product_id__in=field_choice).values_list('product_id', flat=True)
    print result
    if start_date and end_date and result:
        try:
            query_result = Produce.objects.filter(product__in=result, inspect_date__gte=start_date, inspect_date__lte=end_date)
            print query_result
            query_sum = Produce.objects.filter(product__in=result, inspect_date__gte=start_date, inspect_date__lte=end_date).values('product__product_id', 'product__product_name', 'product__order_stats', 'operator__worker_name').annotate(assigned_sum=Sum('assigned_num'), produce_num_sum=Sum('produce_num'))
            print query_sum
        except Produce.DoesNotExist:
            query_result = []
            query_sum = []
        context_dict['query_result'] = query_result
        context_dict['query_sum'] = query_sum
    return render(request, "lonfly/report_by_product.html", context_dict)