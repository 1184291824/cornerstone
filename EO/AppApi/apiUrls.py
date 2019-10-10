from django.urls import path
# from EO.views import common, user, note
from EO.AppApi import views
# from django.views.generic import RedirectView

app_name = "Api"

urlpatterns = [
    path('note/group/', views.get_note_group),
    path('note/show/', views.note_show),
    path('apk/', views.download),

]
