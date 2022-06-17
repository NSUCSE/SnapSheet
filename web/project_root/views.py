from django.contrib.sites import requests
from django.shortcuts import render
import requests


def index(request):

    if request.user.is_authenticated:
        
        URL = "http://127.0.0.1:8000/API/Get_Users_Courses/?username=" + request.user.username
        headers = {'content-Type' : 'application/json'}
        r = requests.get(url=URL, headers=headers)
        data = r.json()
        print(data)
        params = {'Query': data, 'msg': 'here are your course directories!'}
        return render(request, 'index.html', params)

    else:
        params = {'msg': 'Login to view your courses!'}
      
        return render(request, 'index.html', params)