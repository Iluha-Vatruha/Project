from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Max, Min
from rest_framework import serializers
from students.models import Student, Group, Specialty, Faculty, University
from students.serializers import StudentSerializer, GroupSerializer, SpecialtySerializer, FacultySerializer, UniversitySerializer, AddStudentSerializer, AddGroupSerializer, AddFacultySerializer, AddSpecialtySerializer, AddUniversitySerializer

class StudentsViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet
                    ):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
            return AddStudentSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()

        if (self.request.user.is_superuser):
            resQs = qs
        else:
            # фильтруем по текущему юзеру
            resQs = qs.filter(user=self.request.user)

        return resQs  
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        most_popular_group = serializers.CharField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        most_popular_group = Student.objects.values('group').annotate(group_count=Count('id')).order_by('-group_count').first()
        stats = Student.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        if most_popular_group:
            stats['most_popular_group'] = Group.objects.get(pk=most_popular_group['group'])
        else:
            stats['most_popular_group'] = None

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class GroupsViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet
                    ):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
          return AddGroupSerializer
        return super().get_serializer_class()
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        most_popular_specialty = serializers.CharField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        most_popular_specialty = Group.objects.values('specialty').annotate(specialty_count=Count('id')).order_by('-specialty_count').first()
        stats = Group.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        if most_popular_specialty:
            stats['most_popular_specialty'] = Specialty.objects.get(pk=most_popular_specialty['specialty'])
        else:
            stats['most_popular_specialty'] = None

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class SpecialtiesViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet
                    ):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
          return AddSpecialtySerializer
        return super().get_serializer_class()
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        most_popular_faculty = serializers.CharField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        most_popular_faculty = Specialty.objects.values('faculty').annotate(faculty_count=Count('id')).order_by('-faculty_count').first()
        stats = Specialty.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        if most_popular_faculty:
            stats['most_popular_faculty'] = Faculty.objects.get(pk=most_popular_faculty['faculty'])
        else:
            stats['most_popular_faculty'] = None

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)
    

class FacutiesViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet
                    ):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
          return AddFacultySerializer
        return super().get_serializer_class()
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        most_popular_university = serializers.CharField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        most_popular_university = Faculty.objects.values('university').annotate(university_count=Count('id')).order_by('-university_count').first()
        stats = Faculty.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        if most_popular_university:
            stats['most_popular_university'] = University.objects.get(pk=most_popular_university['university'])
        else:
            stats['most_popular_university'] = None

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class UniversitiesViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet
                    ):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    
    def get_serializer_class(self):
        if self.action in ('update', 'create'):
          return AddUniversitySerializer
        return super().get_serializer_class()
    
    class StatsSerializer(serializers.Serializer): #Renamed Serializer
        university_name = serializers.CharField()
        student_count = serializers.IntegerField()


    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        university_stats = University.objects.annotate(
            student_count=Count('faculty__specialty__group__student')
        ).values('name', 'student_count')

        serializer_data = []
        for university_data in university_stats:
            serializer_data.append({
                'university_name': university_data['name'],
                'student_count': university_data['student_count']
            })


        return Response(serializer_data)
    

class UserProfileViewset(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_url(self, request, *args, **kwargs):
        user = request.user
        data = {
            "is_authentificated": user.is_authenticated
        }
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser, 
                "name": user.username
            })
        return Response(data)