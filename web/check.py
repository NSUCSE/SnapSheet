import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client['SnapSheetDB']
collections = mydb['CourseDetails']



is_same_file_exists = {
            "Email": 'omifarhan@gmail.com',
        }
val = collections.find_one(is_same_file_exists)
print(val)