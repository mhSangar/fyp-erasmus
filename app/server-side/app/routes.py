from flask import jsonify, request, Response
from app import app, db
from app.models import Student, Image
import numpy as np
import json
import cv2
import base64
import time

@app.route("/")
def index():
	return "FYP: Intelligent Assistant, by Mario Sanchez Garcia (17150868)"

@app.route("/recognise_me", methods=["POST"])
def recognise_student():
	img = store_image(request=request)
	

	time.sleep(3)

	return jsonify({"message": "image received"})

def store_image(request):
	# get image from request
	img_b64 = json.loads(request.data)["image"]

	# decode base64
	img_bytes = base64.b64decode(img_b64)
	# encode to uint8 to create a numpy array
	img_np_array = np.fromstring(img_bytes, np.uint8)
	# decode image
	img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

	# we add the image to the db to obtain the id, so every filename is different
	image = Image(img="")
	db.session.add(image)
	db.session.commit()

	# save image to a file
	filename = app.config["STUDENT_PHOTOS_FOLDER_PATH"] + "unknown-face-{0:0>3}.jpg".format(image.id)
	cv2.imwrite(filename, img)

	# update filename of the image
	image.img = filename
	db.session.commit()

	return image

#@app.route("/recognise_me/<int:student_id>", methods=["DELETE"])
#def delete_imgs_from_user(student_id):
	
