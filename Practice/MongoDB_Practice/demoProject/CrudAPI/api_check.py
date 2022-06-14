# http://127.0.0.1:8000/CrudAPI/course_get/?CourseCode=CSE299
import json
import requests

URL = "http://127.0.0.1:8000/CrudAPI/course_get/?CourseCode=299"
headers = {'content-Type' : 'application/json'}
r = requests.get(url=URL, headers=headers)
data = r.json()
print(data)