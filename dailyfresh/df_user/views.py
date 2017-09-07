#coding=utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect
from models import *
from hashlib import sha1

def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    #接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    #判断两次密码

    if upwd != upwd2:
        return redirect('/user/register/')

    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail

    user.save()

    #注册成功转到登录页面

    return redirect('/user/login/')


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember', 0)

    #根据用户名查询数据
    users = UserInfo.objects.filter(uname=uname)#查不到返回''用get查不到会抛出来异常，需要处理

    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')

            #记住用户
            if remember != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname','',max_age=-1)

            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red

        else:
            context = {'title': '用户登录', 'error_name':0,'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)

    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)



def info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    context = {'title':'用户中心',
               'user_email':user_email,
               'user_name':request.session['user_name']
    }

    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {'title':'用户中心'}
    return render(request, 'df_user/user_center_site.html', context)

def site(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.show = post.get('ushow')
        user.address = post.get('uaddress')
        user.postid = post.get('upostid')
        user.uphone = post.get('uphone')
        user.save()

    context = {'title':'用户中心', 'user':user}
    return render(request, 'df_user/user_center_site.html',context)