from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from students.models import Student, Group, Specialty, Faculty, University

# Create your views here.
    


class ShowStudentsView(View):
    def get(request, *args, **kwargs):
        students = Student.objects.all()

        result = ""
        for s in students:
            result += s.name + "<br>"
        
        
        return HttpResponse(result)

class ShowGroupsView(View):
    def get(request, *args, **kwargs):
        groups = Group.objects.all()

        result = ""
        for s in groups:
            result += s.name + "<br>"
        
        
        return HttpResponse(result)

class ShowSpecialtiesView(View):
    def get(request, *args, **kwargs):
        specialty = Specialty.objects.all()

        result = ""
        for s in specialty:
            result += s.name + "<br>"
        
        
        return HttpResponse(result)
class ShowFacultiesView(View):
    def get(request, *args, **kwargs):
        falucties = Faculty.objects.all()

        result = ""
        for s in falucties:
            result += s.name + "<br>"
        
        
        return HttpResponse(result)
class ShowUniversitiesView(View):
    def get(request, *args, **kwargs):
        universities = University.objects.all()

        result = ""
        for s in universities:
            result += s.name + "<br>"
        
        
        return HttpResponse(result)
"""

class ShowStudentsView(TemplateViews):
    tamplate_name = "students/show_students.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['students'] = Student.object.all()

        return context
"""