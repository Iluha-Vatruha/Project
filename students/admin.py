from django.contrib import admin

from students.models import Group, Student, Specialty, University, Faculty

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group__id', 'group__name']



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "specialty__id", "specialty__name"]

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "faculty__id", "faculty__name"]

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "university__id", "university__name"]

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]