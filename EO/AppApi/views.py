from django.shortcuts import HttpResponse
from EO.models import NoteGroup, Note, NoteRecode, User
import json
import markdown


def cors_response(result_list):
    """解决CORS的访问验证问题"""
    response = HttpResponse(json.dumps(result_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
    response["Access-Control-Allow-Origin"] = "http://127.0.0.1:8848"
    response['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


def get_note_group(request):
    """返回所有的笔记分组的名称和数量"""
    note_group_list = NoteGroup.objects.all().order_by('name')
    result_list = []
    for note_group_item in note_group_list:
        result = {
            'id': note_group_item.id,
            'name': note_group_item.name,
            'num': note_group_item.num,
            # 'user_name': user_name,
        }
        result_list.append(result)
    return cors_response(result_list)


def note_show(request):
    """获取笔记的列表"""
    group = NoteGroup.objects.get(id=request.GET.get('id', 1))
    note_list = Note.objects.filter(group=group).order_by('-time')
    result_list = []
    for note_item in note_list:
        result = {
            'id': note_item.id,
            'name': note_item.name,
            'user': note_item.user.user_name,
            'time': str(note_item.time),
        }
        result_list.append(result)
    return cors_response(result_list)
