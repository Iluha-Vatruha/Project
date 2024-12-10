from django.db import models

class Student(models.Model):
    name = models.TextField("ФИО")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="students")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    @property
    def username(self):
        return self.user.username if self.user else '-'

class Group(models.Model):
    name = models.TextField("Название")
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
    
    def __str__(self) -> str:
        return self.name

class Specialty(models.Model):
    name = models.TextField("Название")
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
    def __str__(self) -> str:
        return self.name

class Faculty(models.Model):
    name = models.TextField("Название")
    university = models.ForeignKey("University", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"
    def __str__(self) -> str:
        return self.name

class University(models.Model):
    name = models.TextField("Название")
    picture = models.ImageField("Изображение", null=True, upload_to="universities")
    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"
    def __str__(self) -> str:
        return self.name
    
    