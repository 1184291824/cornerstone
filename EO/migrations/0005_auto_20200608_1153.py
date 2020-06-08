# Generated by Django 2.1.3 on 2020-06-08 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EO', '0004_bulletchat'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraduationStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=12, verbose_name='学号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('card_id', models.CharField(max_length=6, verbose_name='身份证号后6位')),
                ('photo', models.TextField(default='', verbose_name='图片的base64代码')),
                ('class_num', models.CharField(max_length=12, verbose_name='班级')),
                ('gender', models.CharField(max_length=1, verbose_name='性别')),
                ('admission_time', models.CharField(max_length=6, verbose_name='入学时间')),
                ('dormitory', models.CharField(max_length=20, verbose_name='宿舍')),
                ('address', models.CharField(max_length=50, verbose_name='生源地')),
                ('score', models.CharField(max_length=10, verbose_name='高考总分')),
                ('graduation_school', models.CharField(max_length=20, verbose_name='毕业中学')),
                ('ksh', models.CharField(max_length=14, verbose_name='考生号')),
                ('byqx', models.CharField(max_length=20, verbose_name='毕业去向')),
                ('byqxdw', models.CharField(max_length=100, verbose_name='毕业去向单位')),
                ('total_score', models.CharField(max_length=10, verbose_name='总分')),
                ('get_credits', models.CharField(max_length=10, verbose_name='所得学分')),
                ('average_score', models.CharField(max_length=10, verbose_name='平均学分绩')),
                ('rank', models.CharField(max_length=10, verbose_name='排名')),
                ('discipline', models.CharField(max_length=10, verbose_name='专业')),
            ],
            options={
                'verbose_name_plural': '毕业生账户',
                'db_table': 'GraduationStudent',
                'ordering': ['student_id'],
            },
        ),
        migrations.AlterField(
            model_name='bulletchat',
            name='verify',
            field=models.BooleanField(default=True, verbose_name='是否通过'),
        ),
    ]
