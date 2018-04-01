import requests
import json
import cv2
import base64

addr = "http://localhost:5000"
file = "client_imgs/001.jpeg"
student_test_ID = "17150868"
test_url = addr + "/recognise_me"

img = cv2.imread(file)
# encode as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# encode as text, so it can be serialized to json
img_as_text = base64.b64encode(img_encoded)

data = {"student_id": student_test_ID, "image": img_as_text}

# send req by POST with the img
response = requests.post(test_url, json=data)
# print the response
print(json.loads(response.text))
