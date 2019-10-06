from django.urls import path
from EO.views import common, user
from django.views.generic import RedirectView

app_name = "BPlan"


urlpatterns = [
    path('test/', common.test, name='test'),
    path('', RedirectView.as_view(url='index')),  # 如果不输入详细网址，直接重定向到主页
    path('index/', common.index, name='index'),

    path('login/', user.login, name='login')

]
