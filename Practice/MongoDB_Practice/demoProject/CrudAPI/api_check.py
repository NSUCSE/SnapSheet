# http://127.0.0.1:8000/CrudAPI/course_get/?CourseCode=CSE299
import json

import pymongo
import requests
print(pymongo.version)

# URL = "http://127.0.0.1:8000/CrudAPI/course_get/?CourseCode=299"
# headers = {'content-Type' : 'application/json'}
# r = requests.get(url=URL, headers=headers)
# data = r.json()
# print(data)



client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client['DemoDatabase']
info = mydb.CourseDetails
list = ["quiz1", "quiz2"]

info.replace_one(

    {"CourseCode":"CSE299"},
    {
        "CourseCode": "CSE299.3",
        "SemesterCode": "SemesterCode",
        "Section": "Section",
        "Description": "Description",
        "Assesments": list,

    }

)