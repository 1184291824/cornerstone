from django.shortcuts import HttpResponse
# from django.http import FileResponse
from EO.models import NoteGroup, Note, NoteRecode, User
import json
import markdown


def cors_response(result_list):
    """解决CORS的访问验证问题"""
    response = HttpResponse(json.dumps(result_list, ensure_ascii=False), content_type="application/json,charset=utf-8")
    # response["Access-Control-Allow-Origin"] = "http://127.0.0.1:8848"
    # response["Access-Control-Allow-Origin"] = "*"
    # response['Access-Control-Allow-Headers'] = 'x-requested-with'
    # response['Access-Control-Allow-Headers'] = "*"
    return response


def check_app(request):
    """检查APP的id是否为基石"""
    app_id = request.GET.get('app_id')
    if app_id == 'H533C5063':
        return True
    else:
        return False


def get_note_group(request):
    """返回所有的笔记分组的名称和数量"""
    if check_app(request):
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
    if check_app(request):
        group = NoteGroup.objects.get(id=request.GET.get('id', 1))
        note_list = Note.objects.filter(group=group).order_by('-time')
        # if note_list:
        #     return HttpResponse('EmptyGroup')
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


# def download(request):
#     """安装包下载"""
#     file = open('/static/App/H533C5063_huawei_1010133633.apk', 'rb')
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="基石.apk"'
#     return response


def update_get_version(request):
    """获取最新版本号"""
    if check_app(request):
        return HttpResponse(90)
