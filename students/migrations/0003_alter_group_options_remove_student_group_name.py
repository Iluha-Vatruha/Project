# Generated by Django 5.1 on 2024-09-10 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_group_alter_student_options_alter_student_group_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.RemoveField(
            model_name='student',
            name='group_name',
        ),
    ]
