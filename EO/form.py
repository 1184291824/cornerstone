from django import forms
from EO.models import NoteGroup


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


class NoteGroupForm(forms.Form):
    """笔记的组"""
    name = forms.CharField(max_length=20, label='组名称')


class NoteForm(forms.Form):
    """笔记"""
    name = forms.CharField(max_length=30, label='笔记名称')
    file = forms.FileField(label='笔记文件(md)')
    group = forms.ModelChoiceField(label='笔记组', queryset=NoteGroup.objects.all(), empty_label=None)


class NoteFormChange(forms.Form):
    """笔记修改"""
    name = forms.CharField(max_length=30, label='笔记名称', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    id = forms.IntegerField(widget=forms.HiddenInput())
    file = forms.FileField(label='笔记文件(md)')


class GraduationLogin(forms.Form):
    """毕业生登录"""
    student_id = forms.CharField(max_length=12, label='学号')
    name = forms.CharField(max_length=20, label='姓名')
    card_id = forms.CharField(max_length=6, label='身份证号后6位')


class GraduationInit(forms.Form):
    """毕业生初始化"""
    csv = forms.FileField(label='csv文件')
