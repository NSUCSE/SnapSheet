from bson import json_util
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
from rest_framework.response import Response
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

import pymongo


@api_view(['POST', ])
@permission_classes([AllowAny])
def CRUD_API_Insert(request):
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])
    Description = request.query_params['Description']
    Assessments = request.query_params.getlist('Assessments')

    print(Assessments)
    print(CourseCode)
    print(Section)
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    mydb = client['DemoDatabase']
    info = mydb.CourseDetails

    JSON_val = {
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
        "Description": Description,
        "Assesments":Assessments,
    }

    info.insert_one(JSON_val)
    return JsonResponse("Added Successfully!", safe=False)

@api_view(['GET', ])
@permission_classes([AllowAny])
def CRUD_API_GET(request):
    CourseCode = request.query_params['CourseCode']
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    mydb = client['DemoDatabase']
    info = mydb.CourseDetails

    res = []
    for records in info.find({"CourseCode":CourseCode}):
        dict = {}
        for x in records:
            if x != "_id":
                dict[x] = records[x]
        # print(dict)
        res.append(dict)


    print(res)
    return Response(res)




#  http://127.0.0.1:8000/CrudAPI/course_insert/?CourseCode=CourseCode&SemesterCode=SemesterCode&Section=Section&Description=Description





































