import requests
import base64
import json

#apikeys: jgFVyVpDtd6flOYJ4jxU7OfCRU9ZyQBJ , 6yUoNC3AAIyLsaeT7eWbdR1DwYRWTFtG , xNe85ZKCeaW6PJlJcSfMFYadvwzPxFnn

def process(json_string):
    #json_string = """{"lang": "und", "all_text": "ID:\nMarks:\n2013 4 5 9 8 2\n17", "annotations": ["ID", ":", "Marks", ":", "2013", "4", "5", "9", "8", "2", "17"]}"""
    json_string = json_string.replace("\n", " ")

    data = json.loads(json_string.replace("\n", " "))

    print("UNPROCESSED:")
    print(data)


    data = data["all_text"].replace("\n", " ")
    data = data.replace(" ", "")



    #print(data)

    start = 0

    result = ""

    for c in data:
        if c >= '0' and c <= '9':
            result += c




    print("PROCESSED:")
    print(str("{"+result[:10]) + "," + str(result[10:])+"}")

url = "https://api.apilayer.com/image_to_text/upload"

f = open("handwriting13.jpg","rb")
file_content = f.read()


payload = file_content
headers= {
  "apikey": "xNe85ZKCeaW6PJlJcSfMFYadvwzPxFnn"
}

response = requests.request("POST", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text

process(response.text)

#process("""{"lang": "und", "all_text": "ID:\nMarks:\n2013 4 5 9 8 2\n17", "annotations": ["ID", ":", "Marks", ":", "2013", "4", "5", "9", "8", "2", "17"]}""")






