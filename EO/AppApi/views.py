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


def login_check(request):
    """登录检测"""
    if check_app(request):
        user_id = request.GET.get('user_id', 0)
        try:
            user = User.objects.get(user_id=user_id)
            if request.GET.get('user_password', 0) == user.user_password:
                result = {
                    'code': 0,
                    'message': '登录成功',
                }
            else:
                result = {
                    'code': 1,
                    'message': '用户名或密码错误',
                }
        except User.DoesNotExist:
            result = {
                'code': 1,
                'message': '您输入的账号不存在'
            }
        return cors_response(result)
    else:
        return cors_response({'error': 'BadRequest'})


def register(request):
    """注册"""
    if check_app(request):
        user_id = request.GET.get('user_id')
        user_password = request.GET.get('user_password')
        user_name = request.GET.get('user_name')
        if user_id and user_password and user_name:
            if User.objects.filter(user_id__exact=user_id):
                result = {
                    'code': 1,
                    'message': '您输入的账号已存在，请重新输入'
                }
            else:
                user = User.objects.create(user_id=user_id, user_password=user_password, user_name=user_name)
                user.save()
                result = {
                    'code': 0,
                    'message': '注册成功',
                }
            return cors_response(result)
    return cors_response({'error': 'BadRequest'})


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
    else:
        return cors_response({'error': 'BadRequest'})


def note_show(request):
    """获取笔记的列表"""
    if check_app(request):
        group = NoteGroup.objects.get(id=request.GET.get('id', 1))
        if group.num == 0:
            return cors_response([{'result': 'EmptyGroup'}])
        note_list = Note.objects.filter(group=group).order_by('-time')
        # if len(note_list) == 0:
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
    else:
        return cors_response({'error': 'BadRequest'})


def note_detail(request):
    """获取笔记内容"""
    if check_app(request):
        note = Note.objects.get(id=request.GET.get('id', 1))
        text = note.file.open().read().decode()
        if text.startswith('\ufeff'):
            text = text[1::]
        #     print(text)
        # print(text.encode())
        html = markdown.markdown(text)
        note.file.close()
        result = {
            'name': note.name,
            'html': html,
            'user': note.user.user_name,
            'time': str(note.time),
        }
        return cors_response(result)
    else:
        return cors_response({'error': 'BadRequest'})


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
        return HttpResponse('1.3.2')
