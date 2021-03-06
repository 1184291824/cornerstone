from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse
from django.utils.http import urlquote
from EO.models import NoteGroup, Note, NoteRecode, User
import json
import markdown
from EO.form import NoteGroupForm, NoteForm, NoteFormChange

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
        note_list = Note.objects.filter(group=group).order_by('-time')
        return render(request, 'PC/show.html', {
            'note_list': note_list,
            'title': group.name,
        })
    else:
        return redirect('EO:index')


def note_show_detail(request):
    """展示笔记的详细信息"""
    if request.session.get('login_status', 0):
        note = Note.objects.get(id=request.GET.get('id', 1))
        text = note.file.open().read().decode()
        if text.startswith('\ufeff'):
            text = text[1::]
        #     print(text)
        # print(text.encode())
        html = markdown.markdown(text)
        note.file.close()
        return render(request, 'PC/markdown.html', {
            'markdown_html': html,
            'note': note,
            'title': note.name,
        })
    else:
        return redirect('EO:index')


def note_show_record(request):
    """展示笔记的修正记录"""
    if request.session.get('login_status', 0):
        note = Note.objects.get(id=request.GET.get('id', 1))
        note_recode_list = NoteRecode.objects.filter(note=note)
        return render(request, 'PC/showRecord.html', {
            'title': '修正记录',
            'note_list': note_recode_list,
        })


def change_note(request):
    """修改笔记"""
    if request.session.get('login_status', 0):
        if request.method == 'POST':
            user = User.objects.get(user_id=request.session['user_id'])
            note = Note.objects.get(id=request.POST['id'])
            note.file.delete()
            note.file = request.FILES['file']
            note.save()
            note_recode = NoteRecode.objects.create(
                note=note,
                user=user,
                note_recode_category=1,
            )
            note_recode.save()
            return render(request, 'PC/success.html', {
                'message': '您刚刚成功修改了一篇助理笔记：'+request.POST['name']+'，快去看看吧~',
                'title': '创建成功',
            })
        else:
            form = NoteFormChange()
            form.fields['name'].widget.attrs.update({'value': request.GET['name']})
            form.fields['id'].widget.attrs.update({'value': request.GET['id']})
            return render(request, 'PC/form.html', {
                'title': '修改笔记',
                'form': form,
            })
    else:
        return redirect('EO:index')


def note_download(request):
    """下载笔记"""
    if request.session.get('login_status', 0):
        note = Note.objects.get(id=request.GET.get('id', 1))
        file = note.file
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(note.name)+'.md')
        return response
    else:
        return redirect('EO:index')
