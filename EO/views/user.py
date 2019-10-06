from django.shortcuts import render, HttpResponse, redirect
from EO.models import *
from EO.form import LoginForm, RegisterForm
from django.contrib.auth import logout

# Create your views here.


def login(request):
    """登录"""
    login_status = request.session.get('login_status', 0)
    message = ''
    if request.method == "POST":  # 如果是POST则验证登录
        form = LoginForm(request.POST)
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                return redirect('EO:index')
            else:
                message = '您输入的密码有误'
        except User.DoesNotExist:
            message = '您输入的用户不存在'
    else:
        if login_status != 0:
            return redirect('EO:index')
        form = LoginForm()
    return render(request, 'PC/form.html', {
        'form': form,
        'message': message,
        'title': '登录',
    })


def login_logout(request):
    """退出登录"""
    logout(request)
    return redirect('EO:index')


def register(request):
    """注册"""
    login_status = request.session.get('login_status', 0)
    message = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        user_password_check = request.POST['user_password_check']
        user_name = request.POST['user_name']
        if User.objects.filter(user_id__exact=user_id):
            message = '您输入的账号已存在，请重新输入'
        elif user_password != user_password_check:
            message = '两次输入的密码不一致，请重新输入'
        else:
            user = User.objects.create(user_id=user_id, user_password=user_password, user_name=user_name)
            user.save()
            return render(request, 'PC/success.html', {
                'message': '注册成功,快去登录吧~',
                'title': '注册成功',
            })
    else:
        if login_status != 0:
            return redirect('EO:index')
        else:
            form = RegisterForm()
    return render(request, 'PC/form.html', {
        'title': '注册',
        'form': form,
        'message': message,
    })


def personal_information(request):
    """返回个人信息界面"""
    if request.session.get('login_status', 0):
        user = User.objects.get(user_id__exact=request.session['user_id'])
        recode_base = NoteRecode.objects.filter(user=user)  # 获取用户的操作记录
        recode_create_num = recode_base.filter(note_recode_category=0).count()  # 获取创建的个数
        recode_change_num = recode_base.filter(note_recode_category=1).count()  # 获取更改的个数
        return render(request, 'PC/user/PersonalInformation.html', {
            'user': user,
            'recode_create_num': recode_create_num,
            'recode_change_num': recode_change_num,
        })
    else:
        return redirect('EO:index')

