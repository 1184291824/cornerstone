from django.shortcuts import render, HttpResponse, redirect
from EO.models import NoteGroup, Note, NoteRecode, User
import json
from EO.form import NoteGroupForm, NoteForm

# Create your views here.


def create_group(request):
    """创建新的笔记分组"""
    if request.session.get('login_status', 0):
        message = ''
        if request.method == 'POST':
            form = NoteGroupForm(request.POST)
            name = request.POST['name']
            if NoteGroup.objects.filter(name=name):
                message = '您输入的组名称已经存在'
            else:
                new_group = NoteGroup.objects.create(name=name)
                new_group.save()
                return render(request, 'PC/success.html', {
                    'title': '创建成功',
                    'message': '您刚刚创建了一个笔记组：'+name+'，快去打开看看吧~'
                })
        else:
            form = NoteGroupForm()
        return render(request, 'PC/form.html', {
            'title': '创建笔记组',
            'message': message,
            'form': form,
        })
    else:
        return redirect('EO:index')


def get_note_group(request):
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
        if request.method == 'POST':
            # form = NoteForm(request.POST, request.FILES)
            group = NoteGroup.objects.get(id=request.POST['group'])
            user = User.objects.get(user_id=request.session['user_id'])
            note = Note.objects.create(
                name=request.POST['name'],
                file=request.FILES['file'],
                group=group,
                user=user,
            )
            # many to many 字段不能直接赋值，要使用set()进行赋值，且需要用filter过滤
            # note.group.set(NoteGroup.objects.filter(id=request.POST['group']))
            # note.user.set(User.objects.filter(user_id=request.session['user_id']))
            note.save()
            group.num += 1
            group.save()
            note_recode = NoteRecode.objects.create(
                note=note,
                user=user,
            )
            note_recode.save()
            return render(request, 'PC/success.html', {
                'message': '您刚刚成功创建了一篇助理笔记：'+request.POST['name']+'，快去看看吧~',
                'title': '创建成功',
            })
        else:
            form = NoteForm()
            return render(request, 'PC/form.html', {
                'title': '新建笔记',
                'form': form,
            })
    else:
        return redirect('EO:index')


def note_show(request):
    """获取笔记的列表"""
    if request.session.get('login_status', 0):
        group = NoteGroup.objects.get(id=request.GET.get('id', 1))
        note_list = Note.objects.filter(group=group).order_by('time')
        return render(request, 'PC/show.html', {
            'note_list': note_list,
            'title': group.name,
        })
    else:
        return redirect('EO:index')
