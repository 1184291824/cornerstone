from django.urls import path
# from EO.views import common, user, note
from EO.AppApi import views, Light
# from django.views.generic import RedirectView

app_name = "Api"

urlpatterns = [
    path('login/', views.login_check),
    path('register/', views.register),
    path('note/group/', views.get_note_group),
    path('note/show/', views.note_show),
    path('note/detail/', views.note_detail),
    # path('apk/', views.download),
    path('update/getVersion', views.update_get_version),
    path('520Light/', Light.stop, name='520'),
    # path('520Light/bullet', Light.bullet, name='520bullet'),

]
