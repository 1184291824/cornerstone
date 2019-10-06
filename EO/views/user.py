from django.shortcuts import render, HttpResponse, redirect
from EO.models import User


# Create your views here.


def login(request):
    """登录"""
    login_status = request.session.get('login_status', 0)
    if request.method == 'GET':  # 如果是get则返回登录界面
        if login_status == 0:
            return render(request, 'PC/user/login.html')
        else:
            return redirect('EO:index')
    elif request.method == 'POST':  # 如果是POST则验证登录
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try:
            user = User.objects.get(user_id__exact=user_id)
            if user_password == user.user_password:
                request.session['login_status'] = 1
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                return HttpResponse("successLogin")  # 返回登录成功
            else:
                return HttpResponse("passwordWrong")  # 返回密码错误
        except User.DoesNotExist:
            return HttpResponse("idDoesNotExist")  # 返回用户不存在
    else:
        return redirect('EO:index')

