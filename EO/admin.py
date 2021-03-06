from django.contrib import admin

# Register your models here.

from .models import *

admin.site.site_header = '助理手册系统后台'  # 网站登录页和H1
admin.site.site_title = '助理手册系统后台'   # 网站标题


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user_id',
        'user_password',
        'user_name',
        'user_create_time',
    ]
    search_fields = ['user_id', 'user_name']  # 搜索字段
    list_per_page = 20


@admin.register(NoteGroup)
class NoteGroupAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'num',
    ]

    search_fields = ['name']
    list_filter = ['name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'file',
        'group',
        'user',
        'time',
    ]

    search_fields = ['name']


@admin.register(NoteRecode)
class NoteRecodeAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'time',
        'note_recode_category',
        'note',
        'user',
    ]


@admin.register(BulletChat)
class BulletChatAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'contain',
        'verify',
    ]

    list_filter = ['verify']


@admin.register(GraduationStudent)
class GraduationStudentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'student_id',
        'name',
        'card_id',
        'class_num',
        'gender',
        'admission_time',
        'dormitory',
        'address',
        'score',
        'graduation_school',
        'ksh',
        'byqx',
        'byqxdw',
        'total_score',
        'get_credits',
        'average_score',
        'rank',
        'discipline',
    ]

    search_fields = ['name', 'student_id']
