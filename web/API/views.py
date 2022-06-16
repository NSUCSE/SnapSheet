import pymongo
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
import json
from rest_framework.response import Response


@api_view(['POST', ])
@permission_classes([AllowAny])
def Insert_Course_Details(request):
    username = request.query_params['username']
    email = request.query_params['email']
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])
    Description = request.query_params['Description']
    SheetLink = request.query_params['SheetLink']
    Assessments = request.query_params.getlist('Assessments')

    print(Assessments)
    print(CourseCode)
    print(Section)

    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return JsonResponse({"msg": "DB Connection Failed!"}, safe=False)

    is_same_file_exists = {
        "Username": username,
        "Email": email,
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
    }
    val = collections.find_one(is_same_file_exists)


    if val is None:
        course_val = {
            "Username": username,
            "Email": email,
            "CourseCode": CourseCode,
            "SemesterCode": SemesterCode,
            "Section": Section,
            "Description": Description,
            "Assessments": Assessments,
            "SheetLink": SheetLink,
        }
        collections.insert_one(course_val)
        return JsonResponse({"msg": "Added Successfully!"}, safe=False)
    return JsonResponse({"msg": "Same course already exists!"}, safe=False)




@api_view(['POST', ])
@permission_classes([AllowAny])
def Add_Assessment(request):
    username = request.query_params['username']
    email = request.query_params['email']
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])
    Description = request.query_params['Description']
    SheetLink = request.query_params['SheetLink']
    Assessments = request.query_params['Assessments']
    print(SheetLink)

    print(username)
    print(CourseCode)

    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return JsonResponse({"msg": "DB Connection Failed!"}, safe=False)

    is_same_file_exists = {
        "Username": username,
        "Email": email,
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
    }
    val = collections.find_one(is_same_file_exists)
    print(val)
    list = val["Assessments"]
    list.append(Assessments)
    print(list)

    collections.replace_one(

        {
            "Username": username,
            "Email": email,
            "CourseCode": CourseCode,
            "SemesterCode": SemesterCode,
            "Section": Section,
        },
        {
            "Username": username,
            "Email": email,
            "CourseCode": CourseCode,
            "SemesterCode": SemesterCode,
            "Section": Section,
            "Descriptions": Description,
            "Assessments": list,
            "SheetLink": SheetLink,
        }

    )
    return JsonResponse({"msg": "Assessment Added Successfully!"}, safe=False)






@api_view(['GET', ])
@permission_classes([AllowAny])
def Get_Users_Courses(request):

    username = request.query_params['username']
    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return JsonResponse({"msg": "DB Connection Failed!"}, safe=False)

    res = []
    for records in collections.find({"Username": username}):
        dict = {}
        for x in records:
            if x != "_id":
                dict[x] = records[x]
        # print(dict)
        res.append(dict)

    print(res)
    return Response(res)








