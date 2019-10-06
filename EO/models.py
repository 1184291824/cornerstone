from django.db import models

# Create your models here.


class User(models.Model):
    """用户"""
    user_id = models.CharField(verbose_name='用户id', max_length=12)
    user_password = models.CharField(max_length=20, verbose_name='密码')
    user_name = models.CharField(max_length=12, default='保密', verbose_name='姓名')
    user_create_time = models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "User"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '用户'


class NoteGroup(models.Model):
    """笔记的组"""
    name = models.CharField(max_length=20, verbose_name='组名称')
    num = models.PositiveSmallIntegerField(verbose_name='组成员个数', default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "NoteGroup"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '笔记的组'


class Note(models.Model):
    """笔记"""
    name = models.CharField(max_length=30, verbose_name='笔记名')
    file = models.FileField(verbose_name='笔记的markdown文件', upload_to='notefile')
    group = models.ForeignKey(NoteGroup, verbose_name='笔记的组', related_name='NoteGroup', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='笔记创建人', related_name='NoteUser', on_delete=models.CASCADE)
    time = models.DateField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Note"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '笔记'


class NoteRecode(models.Model):
    """笔记修改记录"""
    '''选项'''
    NOTE_RECODE_CHOICE = (
        (0, '创建'),
        (1, '修改'),
    )
    note = models.ForeignKey(Note, related_name='note', verbose_name='笔记', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', verbose_name='修改人', on_delete=models.CASCADE)
    time = models.DateField(auto_now=True, verbose_name='修改时间')
    note_recode_category = models.PositiveSmallIntegerField(
        default=0,
        choices=NOTE_RECODE_CHOICE,
        verbose_name='操作类别'
    )

    # def __str__(self):
    #     return self.note.name

    class Meta:
        db_table = 'NoteRecode'
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '笔记修改记录'
