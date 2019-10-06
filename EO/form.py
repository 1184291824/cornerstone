from django import forms


class LoginForm(forms.Form):
    """登录"""
    user_id = forms.CharField(max_length=12, label='账号',)
    user_password = forms.CharField(widget=forms.PasswordInput, max_length=20, label='密码')


class RegisterForm(forms.Form):
    """注册"""
    user_id = forms.CharField(max_length=12, label='账号', )
    user_password = forms.CharField(widget=forms.PasswordInput, max_length=20, label='密码')
    user_password_check = forms.CharField(widget=forms.PasswordInput, max_length=20, label='确认密码')
    user_name = forms.CharField(max_length=20, label='姓名',)
