# import pymongo
#
# client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
# mydb = client['SnapSheetDB']
# collections = mydb['CourseDetails']
#
#
#
# is_same_file_exists = {
#             "Email": 'omifarhan@gmail.com',
#         }
# val = collections.find_one(is_same_file_exists)
# print(val)

# url = "https://docs.google.com/spreadsheets/d/15f9haQilG4HkKdhIsusOggzT0IUwZWDG1dePTkeJcec/edit#gid=0"
# res = url.split("/")
#
# print(res[5])

def get_sheet_url(request, url):
    res = url.split("/")
    return res[5]

