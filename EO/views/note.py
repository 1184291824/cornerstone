from django.shortcuts import render, HttpResponse, redirect
from EO.models import NoteGroup, Note, NoteRecode, User
import json

# Create your views here.


def create_group(request):
    """创建新的笔记分组"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            return render(request, 'PC/note/noteGroupCreate.html')
        elif request.method == "POST":
            name = request.POST['name']
            if NoteGroup.objects.filter(name=name):
                return HttpResponse('nameExist')
            new_group = NoteGroup.objects.create(name=name)
            new_group.save()
            return HttpResponse('success')
    else:
        return redirect('EO:index')


def note_group(request):
    """返回所有的笔记分组的名称和数量"""
    note_group_list = NoteGroup.objects.all()
    result_list = []
    for note_group_item in note_group_list:
        result = {
            'id': note_group_item.id,
            'name': note_group_item.name,
            'num': note_group_item.num,
            # 'user_name': user_name,
        }
        result_list.append(result)
    return HttpResponse(json.dumps(result_list, ensure_ascii=False), content_type="application/json,charset=utf-8")


def create_note(request):
    """创建笔记"""
    if request.session.get('login_status', 0):
        if request.method == 'GET':
            return render(request, 'PC/note/noteGroupCreate.html')
        elif request.method == "POST":
            name = request.POST['name']
            if NoteGroup.objects.filter(name=name):
                return HttpResponse('nameExist')
            new_group = NoteGroup.objects.create(name=name)
            new_group.save()
            return HttpResponse('success')
    else:
        return redirect('EO:index')
