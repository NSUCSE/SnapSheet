from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CourseDetails

class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields=('CourseCode', 'SemesterCode', 'Section', 'Description')