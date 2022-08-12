from django.shortcuts import render

# Create your views here.
from django.contrib.sites import requests
from django.shortcuts import render
import requests
from django.shortcuts import redirect


def index(request):
    return render(request, 'CreateCourse/addCourse.html')

def addCourse(request):
    
    username = request.POST.get("user_name")
    email = request.POST.get("email")
    course_code = request.POST.get("course_code")
    semester_code = request.POST.get("semester_code")
    section = request.POST.get("section")
    description = request.POST.get("description")
    assessments = []
    sheet_link = request.POST.get("sheet_link")

    print(username)
    print(email)
    print(course_code)
    print(semester_code)
    print(section)

    URL = "http://127.0.0.1:8000/API/course_details_insert/?username=" + username + "&email=" + email + "&CourseCode=" + course_code + "&SemesterCode=" + semester_code + "&Section=" + section + "&Description=" + description + "&SheetLink=" + sheet_link
    headers = {'content-Type': 'application/json'}
    r = requests.post(url=URL, headers=headers)
    data = r.json()
    print(data)
    print(data['msgs'])
    params = {'msgs': 'Same course already exists!'}
    if data['msgs'] == 'Same course already exists!':
        return render(request, 'CreateCourse/addCourse.html', params)
        # return redirect('index')
    else:
        params = {'msgs': 'Added Successfully!'}
        return render(request, 'CreateCourse/addCourse.html', params)






