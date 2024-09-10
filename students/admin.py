from django.contrib import admin

from students.models import Group, Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
