from django.contrib.sites import requests
from django.shortcuts import render
import requests
from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        URL = "http://127.0.0.1:8000/API/Get_Users_Courses/?username=" + request.user.username
        headers = {'content-Type' : 'application/json'}
        r = requests.get(url=URL, headers=headers)
        data = r.json()
        print(data)
        params = {'Query': data, 'msg': 'here are your course directories!'}
        return render(request, 'dashboard.html', params)
    else:
        params = {'msg': 'Login to view your courses!'}
        return render(request, 'index.html', params)


def add_assessments(request):
    username = request.POST.get("user_name")
    email = request.POST.get("email")
    course_code = request.POST.get("course_code")
    semester_code = request.POST.get("semester_code")
    section = request.POST.get("section")
    description = request.POST.get("description")
    assessments = request.POST.get("assessment")
    sheet_link = request.POST.get("sheet_link")

    print(username)
    print(email)
    print(course_code)
    print(semester_code)
    print(assessments)
    print(sheet_link)
    print(description)
    print(section)

    URL = "http://127.0.0.1:8000/API/Add_Assessment/?username=" + username + "&email=" + email + "&CourseCode=" + course_code + "&SemesterCode=" + semester_code + "&Section=" + section + "&Description=" + description + "&Assessments=" + assessments + "&SheetLink=" + sheet_link
    headers = {'content-Type': 'application/json'}
    print(URL)
    r = requests.post(url=URL, headers=headers)
    data = r.json()
    print(data)
    params = {'Query': data}
    # return render(request, 'index.html', params)
    return redirect('/')


def delete_course(request):
    username = request.POST.get("user_name")
    email = request.POST.get("email")
    course_code = request.POST.get("course_code")
    semester_code = request.POST.get("semester_code")
    section = request.POST.get("section")
    section = str(section)    


    URL = "http://127.0.0.1:8000/API/delete_course/?username=" + username + "&email=" + email + "&CourseCode=" + course_code + "&SemesterCode=" + semester_code + "&Section=" + section
    headers = {'content-Type': 'application/json'}
    r = requests.post(url=URL, headers=headers)
    data = r.json()
    print(data)
    params = {'Query': data}
    # return render(request, 'index.html', params)
    return redirect('/')




