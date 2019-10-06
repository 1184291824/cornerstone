from django.urls import path
from EO.views import common, user, note
from django.views.generic import RedirectView

app_name = "BPlan"


urlpatterns = [
    path('test/', common.test, name='test'),
    path('', RedirectView.as_view(url='index')),  # 如果不输入详细网址，直接重定向到主页
    path('index/', common.index, name='index'),
    path('index/whetherLogin/', common.whether_login, name='whether_login'),

    path('user/login/', user.login, name='login'),
    path('user/login/logout/', user.login_logout, name='logout'),
    path('user/register/', user.register, name='register'),
    path('user/personalInformation/', user.personal_information, name='personal_information'),


    path('note/group/', note.note_group, name='note_group'),
    path('note/group/create', note.create_group, name='create_group'),
    path('note/create', note.create_note, name='create_note'),

]
