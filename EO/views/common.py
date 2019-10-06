from django.shortcuts import render, HttpResponse, redirect
from EO.models import *

# Create your views here.


def test(request):
    """测试"""
    file = Note.objects.get(id=1)
    text = file.file.open().read().decode()
    return HttpResponse(text)


def index(request):
    """返回主页"""
    return render(request, 'PC/index.html')
