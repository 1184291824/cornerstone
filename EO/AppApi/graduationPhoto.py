# coding=utf8
"""
创建者：马子轩
贡献者：
创建时间: 2020年05月29日
最后保存时间: 2020年05月29日
"""


from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import logout
from EO.form import GraduationLogin, GraduationInit
from EO.models import GraduationStudent
from django.views.decorators.csrf import csrf_exempt

import pandas as pd


def init_student(request):
    """初始化毕业生数据库"""
    # path = r'D:\project\cornerstone\static\xls\graduation.csv'
    if request.method == "POST":
        path = request.FILES['csv']
        table = pd.read_excel(path)
        graduation_student_list = list()
        for col in range(table.shape[0]):
            graduation_student_list.append(
                GraduationStudent(
                    student_id=table['学号'][col],
                    name=table['姓名'][col],
                    card_id=table['身份证'][col][-6:],
                    class_num=table['班级'][col],
                    gender=table['性别'][col],
                    admission_time=table['入学时间'][col],
                    dormitory=table['宿舍编号'][col],
                    address=table['生源地区'][col],
                    score=table['高考总分'][col],
                    graduation_school=table['毕业中学'][col],
                    ksh=table['考生号'][col],
                    byqx=table['毕业去向'][col],
                    byqxdw=table['单位'][col],
                    total_score=table['总分'][col],
                    get_credits=table['所得学分'][col],
                    average_score=table['平均学分绩'][col],
                    rank=table['排名'][col],
                    discipline=table['专业'][col],
                )
            )
        GraduationStudent.objects.bulk_create(graduation_student_list)
        return HttpResponse("success")
    else:
        form = GraduationInit()
        return render(request, "APP/graduationPhoto/initStudent.html", {
            'form': form,
        })


def test(request):
    return render(request, 'App/graduationPhoto.html')


def login(request):
    """登录系统"""
    login_status = request.session.get('graduation_login_status', 0)
    message = ''
    if request.method == "POST":  # 如果是POST则验证登录
        form = GraduationLogin(request.POST)
        student_id = request.POST['student_id']
        name = request.POST['name']
        card_id = request.POST['card_id']
        try:
            student = GraduationStudent.objects.get(student_id=student_id)
            if name == student.name and card_id == student.card_id:
                request.session['graduation_login_status'] = 1
                request.session['student_id'] = student.student_id
                request.session['name'] = student.name
                return redirect('APPApi:graduationPhoto_menu')
            else:
                message = '您输入的信息有误'
        except GraduationStudent.DoesNotExist:
            message = '您输入的用户不存在'
    else:
        if login_status != 0:
            return redirect('APPApi:graduationPhoto_menu')
        form = GraduationLogin()
    return render(request, 'App/graduationPhoto/login.html', {
        'form': form,
        'message': message,
        'title': '登录',
    })


def index(request):
    """返回主页"""
    if request.session.get('graduation_login_status', 0):
        student = GraduationStudent.objects.get(student_id=request.session.get('student_id'))
        student_photos = GraduationStudent.objects.filter(~Q(photo='')).order_by('pk').values_list('photo', flat=True)

        return render(request, 'App/graduationPhoto/index.html', {
            'student': student,
            'student_photos': list(student_photos),
        })
    else:
        return redirect('APPApi:graduationPhoto_login')


@csrf_exempt
def getbody(request):
    """人像抠图"""
    if request.session.get('graduation_login_status', 0):
        if request.method == "POST":
            import requests

            request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"  # API地址
            img = request.POST['image']  # 图片的base64编码

            params = {  # 请求参数
                "image": img,
                "type": "foreground"
            }
            access_token = '24.7e1152aa822f1fda2906f38ccbf3008c.2592000.1593790511.282335-20214655'  # 访问密码
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)  # 发起访问请求
            if response:
                # print(response.json())
                return JsonResponse(response.json())
            else:
                return HttpResponse(response)
    else:
        return redirect('APPApi:graduationPhoto_login')


@csrf_exempt
def get_photo(request):
    """获取提交的照片"""
    if request.session.get('graduation_login_status', 0):
        if request.method == "POST":
            photo = request.POST['img3']
            student = GraduationStudent.objects.get(student_id=request.session['student_id'])
            student.photo = photo
            student.save()
            return HttpResponse('success')
    else:
        return redirect('APPApi:graduationPhoto_login')


def student_logout(request):
    """退出登录（测试用）"""
    logout(request)
    return redirect('APPApi:graduationPhoto_login')


def menu(request):
    """菜单"""
    if request.session.get('graduation_login_status', 0):
        return render(request, "App/graduationPhoto/menu.html")
    else:
        return redirect("APPApi:graduationPhoto_login")


def mybill(request):
    """我的大学账单"""
    if request.session.get('graduation_login_status', 0):
        student = GraduationStudent.objects.get(student_id=request.session.get('student_id'))
        return render(request, 'App/graduationPhoto/mybill.html', {
            'student': student
        })
    else:
        return redirect("APPApi:graduationPhoto_login")

