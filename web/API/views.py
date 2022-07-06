import pymongo
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
import json
from rest_framework.response import Response
from project_root.views import *
from sheets.add_assessment import add_assessment
from sheets.add_mark import add_mark

def get_sheet_id(url):
    res = url.split("/")
    return res[5]


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
        return JsonResponse({"msgs": "Added Successfully!"}, safe=False)
    return JsonResponse({"msgs": "Same course already exists!"}, safe=False)




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
    sheet_id = get_sheet_id(SheetLink)
    print(sheet_id)

    res = add_assessment(sheet_id, Assessments)

    if res != "":
        return JsonResponse({"msg": "Same Assessment already created!"}, safe=False)


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
    # print(list)

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
            "Description": Description,
            "Assessments": list,
            "SheetLink": SheetLink,
        }

    )

    return JsonResponse({"msg": "Assessment Added Successfully!"}, safe=False)




@api_view(['POST', ])
@permission_classes([AllowAny])
def delete_course(request):
    username = request.query_params['username']
    email = request.query_params['email']
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])

    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return JsonResponse({"msg": "DB Connection Failed!"}, safe=False)

    delete_document = {
        "Username": username,
        "Email": email,
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
    }

    collections.delete_one(delete_document)
    return JsonResponse({"msg": "Courses Deleted Successfully!"}, safe=False)




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




#api for verifying a user for android version login
@api_view()
@permission_classes([AllowAny])
def verify_user(request):
    id_token = request.query_params['id_token']

    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return Response({"msg": "DB Connection Failed!"}, safe=False)

    try:
        URL = 'https://oauth2.googleapis.com/tokeninfo?id_token=' + id_token
        headers = {'content-Type': 'application/json'}
        r = requests.get(url=URL, headers=headers)
        data = r.json()
        print(data)
        user_email = data['email']
        print(user_email)

        is_same_file_exists = {
            "Email": user_email,
        }
        val = collections.find_one(is_same_file_exists)
        print(val)

        if val is not None:
            user_name = val['Username']
            print(user_name)
            values = {'status': "OK", "username": user_name}
            return Response({'status' : 'OK', 'username' : user_name})
        return Response({'status':'Failed!'})

    except:
        return Response({'status': 'FAILED'})



@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def update_google_sheet(request):

    username = request.query_params['username']
    student_id = request.query_params['student_id']
    CourseCode = request.query_params['CourseCode']
    SemesterCode = request.query_params['SemesterCode']
    Section = int(request.query_params['Section'])
    assessment_name = request.query_params['Assessment']
    marks = request.query_params['Marks']

    print(username)
    print(CourseCode)
    print(SemesterCode)
    print(Section)
    print(assessment_name)

    try:
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['SnapSheetDB']
        collections = mydb['CourseDetails']
    except:
        return JsonResponse({"msg": "DB Connection Failed!"}, safe=False)

    is_the_file_exists = {
        "Username": username,
        "CourseCode": CourseCode,
        "SemesterCode": SemesterCode,
        "Section": Section,
    }
    val = collections.find_one(is_the_file_exists)
    print(val)
    if val is None:
        return Response({'msg':'No such course found!'})
    sheet_url = val["SheetLink"]
    print(sheet_url)
    if sheet_url is None:
        return Response({'msg':'No Url Found!'})
    sheet_id = get_sheet_id(sheet_url)
    print(sheet_id)
    res = add_mark(sheet_id, assessment_name, student_id, marks)
    if res == "Error: Assesment Doesn't Exists!":
        return Response({'msg': 'No Such Assessment Exist! Please Create an Assessment!'})
    elif res == "Error: Student Doesn't Exists!":
        return Response({'msg': 'No Such Student Exist! Please Enter the Student ID in the Sheet!'})
    elif res == "":
        return Response({'msg': 'Mark Updated Successfully!'})