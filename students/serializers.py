from rest_framework import serializers

from students.models import Student, Group, Faculty, Specialty, University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'picture']

class AddUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'picture']

class FacultySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'university']

class SpecialtySerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'faculty']

class GroupSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'specialty']

class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'group', 'picture', 'user', 'username']

class AddStudentSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    class Meta:
        model = Student
        fields = ['id', 'name', 'group', 'picture', 'user']

class AddGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'specialty']

class AddSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'faculty']

class AddFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'university']

