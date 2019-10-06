from django.shortcuts import render, HttpResponse, redirect
from EO.models import *
import json

# Create your views here.


def test(request):
    """测试"""
    # file = Note.objects.get(id=3)
    # text = file.file.open().read().decode()
    # return HttpResponse(text)
    return render(request, 'PC/success.html',{
        'message': '恭喜你注册成功了我们的系统，我要回家睡觉奥二零ask的防护距离喀什地方',
        'title': '成功',
    })


def index(request):
    """返回主页"""
    return render(request, 'PC/index.html', {
        'title': '主页',
    })


def whether_login(request):
    """判断是否处于登录状态"""
    login_status = request.session.get('login_status', 0)
    user_id = request.session.get('user_id', 0)
    user_name = request.session.get('user_name', 0)
    result = {
        'login_status': login_status,
        'user_id': user_id,
        'user_name': user_name,
    }
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
