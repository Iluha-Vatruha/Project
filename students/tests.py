from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Group, Specialty, Faculty, University
# Create your tests here.

class StudentViewsetTestCase(TestCase):
    def setUP(self):
        self.client = APIClient()

    def test_get_list(self):
        grp = Group.objects.create(
            name="ИСТб-22-1"
        )
        student = Student.objects.create(
            name="Долгарев Дмитрий Сергеевич",
            group=grp,
        )
        
        r = self.client.get('/api/students/')
        data = r.json()
        print(data)

        assert student.name == data[0]['name']
        assert student.id == data[0]['id']
        assert student.group.id == data[0]['group']['id']
        assert len(data) == 1

class StudentCreateTestCase(TestCase):
    def test_create_student(self):
        grp = Group.objects.create(
            name="ИСТб-22-1"
        )

        r = self.client.post("/api/students/", {
            "name": "Студент",
            "group": grp.id
        })

        new_student_id = r.json()['id']

        students = Student.objects.all()
        assert len(students) == 1

        new_student = Student.objects.filter(id=new_student_id).first()
        assert new_student.name == 'Студент'
        assert new_student.group == grp

''' class GroupViewsetTestCase(TestCase):
    def setUP(self):
        self.client = APIClient()

    def test_get_list(self):
        spc = Specialty.objects.create(
            name="ИСТб",

        )
        grp = Group.objects.create(
            name="ИСТб-22-1",
            specialty=spc,
        )
        
        r = self.client.get('/api/students/')
        data = r.json()
        print(data)

        assert grp.name == data[0]['name']
        assert grp.id == data[0]['id']
        assert grp.specialty.id == data[0]['specialty']['id']
        assert len(data) == 1
'''
