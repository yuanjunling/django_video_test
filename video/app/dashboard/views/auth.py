#coding:utf-8
from django.shortcuts import redirect,reverse
from django.views import View
from app.libs.base_render import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator
from app.utils.permission import dashboard_auth


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        #如果已经登录就直接跳转到首页
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        to = request.GET.get('to','')
        data={'error':'','to':to}
        return render_to_response(request, self.TEMPLATE,data=data)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to','')
        data={}
        exists = User.objects.filter(username=username).exists()
        data['error'] ='没有该用户'
        user = authenticate(username=username, password=password)
        if not exists:
            return render_to_response(request,self.TEMPLATE,data=data) 
        elif not user:
            data['error']='密码错误'
            return render_to_response(request,self.TEMPLATE,data=data)
        elif not user.is_superuser:
            data['error']='您无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)
        login(request,user)
        if to:
            return redirect(to)
        return redirect(reverse('dashboard_index'))

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login'))

class AdminManger(View):
    TEMPLATE = 'dashboard/auth/admin.html'
    @dashboard_auth
    def get(self,request):
        # users = User.objects.filter(is_superuser=True)
        users = User.objects.all().order_by('id')
        page = request.GET.get('page',1)
        p = Paginator(users,3)
        total_page = p.num_pages
        if int(page) <= 1:
            page=1
        current_page = p.get_page(int(page)).object_list
        data = {'users':current_page,'total':total_page,'page_num':int(page)}
        return render_to_response(request,self.TEMPLATE,data=data)

class UpdateAdminStatus(View):
    def get(self,request,user_id):
        status = request.GET.get('status',"on")
        _status = True if status == 'on' else False
        user = User.objects.filter(id=user_id)
        user.update(is_superuser=_status)
        return redirect(reverse("admin_manger"))