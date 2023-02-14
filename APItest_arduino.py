import requests
import json
import time

#ser = serial.Serial('COM3', 9600)
url = "https://cog-ams-control.pxsuite.app/api/public/1a8e44c8-3213-4287-8c70-289c40e20493/presentations/trigger-event"

payload = json.dumps({
  "state": False,
  "triggerId": "2",
  "screenIds": [40]
})
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzM2MDMzNTUsImlzcyI6ImNvZy1hbXMiLCJleHAiOjE2ODM2MDMzNTV9.UIscZZyoQFbRhP7LqAB-yT8ccoC5QkepJl0lXNWyvgE',
  'Content-Type': 'application/json'
}

while True:
    #message = ser.readline()
    #print(message)

    if True:  
      response = requests.request("POST", url, headers = headers, data = payload)

      print(response.text)
      time.sleep(5)
