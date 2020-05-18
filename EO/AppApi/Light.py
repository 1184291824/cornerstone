# coding=utf8
"""
创建者：马子轩
贡献者：
创建时间: 2020年05月16日
最后保存时间: 2020年05月16日
"""


from EO.models import BulletChat
from django.shortcuts import HttpResponse, render, redirect


def index(request):
    """直接返回页面"""
    bullet_group = BulletChat.objects.filter(verify=True)
    return render(request, "App/520.html", {
        'bullet': bullet_group
    })


def bullet(request):
    if request.method == "POST":
        name = request.POST['name']
        contain = request.POST['contain']
        BulletChat.objects.create(
            name=name,
            contain=contain,
        )
    return redirect('APPApi:520')
