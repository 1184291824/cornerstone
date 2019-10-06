from django.shortcuts import render, HttpResponse, redirect
from EO.models import *
import json

# Create your views here.


def test(request):
    """测试"""
    file = Note.objects.get(id=1)
    text = file.file.open().read().decode()
    return HttpResponse(text)


def index(request):
    """返回主页"""
    return render(request, 'PC/index.html',{
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
