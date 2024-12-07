from .models import Teacher,Subjects,Course, Student

from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    years_of_experience = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'teacher_id',
            'name',
            'beginning_teaching',
            'teaching_subject_1',
            'teaching_subject_2',
            'teaching_subject_3',
            'years_of_experience',
        ]

    def get_years_of_experience(self, obj):
        return obj.years_of_experience

    def validate_teaching_subject(self, value):
        """Validate and normalize a single teaching subject."""
        # Normalize the input to title case
        normalized_value = value.title()
        if normalized_value not in Subjects.values:
            allowed_subjects = ', '.join(Subjects.values)
            raise serializers.ValidationError(
                f"Invalid subject '{value}'. Allowed subjects are: {allowed_subjects}."
            )
        return normalized_value

    def validate(self, data):
        """Validate and normalize multiple subject fields."""
        for field in ['teaching_subject_1', 'teaching_subject_2', 'teaching_subject_3']:
            if field in data:
                data[field] = self.validate_teaching_subject(data[field])
        return data





    
class StudentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Student
        fields = '__all__'
# course serializer


class StudentDetails(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name','interested_in')



class CourseSerializer(serializers.ModelSerializer):
 
    
    """
     the students fielfs is needed when when
     querying for the fields name and interested in teh student model
    """
    # students = StudentDetails(many=True)

    class Meta:
        model = Course
        fields = '__all__'
    
