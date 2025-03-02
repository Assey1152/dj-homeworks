from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if data.get('students') is not None:
            count = len(data.get('students'))
            if count > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(f'Превышено максимальное количество студентов ({settings.MAX_STUDENTS_PER_COURSE})')
        return data
