from django.shortcuts import render

# Create your views here.
# this method redirects to home page
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
import json

from .models import CourseDetails
from .serializers import CourseDetailsSerializer


def index(request):
    # return render(request, "<p> Home Page </p")
    return HttpResponse("<p> Home Page of CrudAPI App </p")


# @csrf_exempt
# def CRUD_API_Insert(request):
#     if request.method == 'POST':
#         course_data = JSONParser().parse(request)
#         course_serializer = CourseDetailsSerializer(data=course_data)
#         if course_serializer.is_valid():
#             course_serializer.save()
#             return JsonResponse("Added Successfully!", safe=False)
#         return JsonResponse("Falied!!!!", safe=False)
#     elif request.method == 'GET':
#         course_data = JSONParser().parse(request)
#         show_courses_user = CourseDetails.objects.get(course_data['CourseCode'])
#         course_serializer = CourseDetailsSerializer(show_courses_user, many=True)
#         return JsonResponse(course_serializer.data, safe=False)


@api_view(['POST', ])
@permission_classes([AllowAny])
def CRUD_API_Insert(request):
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])
    Description = request.query_params['Description']

    print(CourseCode)
    print(Section)

    JSON_val = {
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
        "Description": Description
    }
    json_object = json.dumps(JSON_val)
    course_serializer = CourseDetailsSerializer(data=json_object)
    print(course_serializer)

    print(course_serializer.is_valid())
    if course_serializer.is_valid():
        course_serializer.save()
        return JsonResponse("Added Successfully!", safe=False)
    return JsonResponse("Falied!!!!", safe=False)

#  http://127.0.0.1:8000/CrudAPI/course_insert/?CourseCode=CourseCode&SemesterCode=SemesterCode&Section=Section&Description=Description
