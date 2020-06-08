from django.urls import path
# from EO.views import common, user, note
from EO.AppApi import views, Light, graduationPhoto
# from django.views.generic import RedirectView

app_name = "APPApi"

urlpatterns = [
    path('login/', views.login_check),
    path('register/', views.register),
    path('note/group/', views.get_note_group),
    path('note/show/', views.note_show),
    path('note/detail/', views.note_detail),
    # path('apk/', views.download),
    # path('update/getVersion', views.update_get_version),
    # path('520Light/', Light.stop, name='520'),
    # path('520Light/bullet', Light.bullet, name='520bullet'),
    path('graduationPhoto/', graduationPhoto.test, name='graduationPhoto_test'),
    path('graduationPhoto/index/', graduationPhoto.index, name='graduationPhoto_index'),
    path('graduationPhoto/mybill/', graduationPhoto.mybill, name='graduationPhoto_mybill'),
    path('graduationPhoto/login/', graduationPhoto.login, name='graduationPhoto_login'),
    path('graduationPhoto/logout/', graduationPhoto.student_logout, name='graduationPhoto_logout'),
    path('graduationPhoto/menu/', graduationPhoto.menu, name='graduationPhoto_menu'),
    path('graduationPhoto/getbody/', graduationPhoto.getbody, name='graduationPhoto_getbody'),
    path('graduationPhoto/get_photo/', graduationPhoto.get_photo, name='graduationPhoto_get_photo'),
    path('graduationPhoto/init_student/', graduationPhoto.init_student, name='graduationPhoto_init_student'),

]
