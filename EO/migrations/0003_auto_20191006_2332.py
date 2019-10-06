# Generated by Django 2.1.3 on 2019-10-06 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EO', '0002_auto_20191006_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NoteGroup', to='EO.NoteGroup', verbose_name='笔记的组'),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NoteUser', to='EO.User', verbose_name='笔记创建人'),
        ),
        migrations.AlterField(
            model_name='noterecode',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='EO.Note', verbose_name='笔记'),
        ),
        migrations.AlterField(
            model_name='noterecode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='EO.User', verbose_name='修改人'),
        ),
    ]
